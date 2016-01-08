

from myhdl import Signal, intbv, always_seq, always_comb, concat


def io_stub(clock, reset, sdi, sdo, port_inputs, port_outputs, valid):
    """ Port emulators, serial to parallel input / output

    This module is a port emulator, a single input and single output
    will be serialized into larger parallel data words (bus).

    This module is a simple module used for synthesis testing for 
    particular FPGA devices.  This module allows a bunch of inputs 
    to be tied to a couple IO (pins).  Typically this is not used
    in a functionally working implementation but a circuit valid
    and timing valid implementation to determine a rough number
    of resources required for a design.

    Ports
    -----
    clock:
    reset:
    sdi: serial-data in, this should be assigned to a pin on
        the device
    sdo: serial-data out, this should be assigned to a pin on
        the device
    port_inputs: number of inputs desired, list of same type Signals,
        output of this module
    port_outputs: number of outputs desired, list of same type Signals,
        input to this module
    valid: load new inputs, outputs valid

    Parameters
    ----------
    None

    Limitations
    -----------
    Each member in the `pin` and `pout` lists need to be
    the same type.

    Return
    ------
    myhdl generators

    This module is myhdl convertible
    """
    
    # verify pin and pout are lists
    pin, pout = port_inputs, port_outputs
    assert isinstance(pin, list)
    assert isinstance(pout, list)

    nin = len(pin)      # number of inputs (outputs of this module)
    nout = len(pout)    # number of outputs (inputs to this module)
    nbx = len(pin[0])   # bit lengths of the inputs
    nby = len(pout[0])  # bit lengths of the outputs

    signed = True if pin[0].min < 0 else False

    # make the input and output registers same length
    xl, yl = nin*nbx, nout*nby
    nbits = max(xl, yl)
    irei = Signal(bool(0))
    oreo = Signal(bool(0))
    ireg = [Signal(intbv(0)[nbx:]) for _ in range(nin)]
    oreg = [Signal(intbv(0)[nby:]) for _ in range(nin)]

    scnt = Signal(intbv(0, min=0, max=nbits+1))
    imax = scnt.max-1

    @always_seq(clock.posedge, reset=reset)
    def beh_shifts():
        irei.next = sdi
        oreo.next = oreg[nout-1][nby-1]
        sdo.next = oreo

        # build the large shift register out of the logical
        # list of signals (array)
        for ii in range(nin):
            if ii == 0:
                ireg[ii].next = concat(ireg[ii][nbx-1:0], irei)
            else:
                ireg[ii].next = concat(ireg[ii][nbx-1:0], ireg[ii-1][nbx-1])

        if scnt == imax:
            valid.next = True
            scnt.next = 0
            for oo in range(nout):
                oreg[oo].next = pout[oo]
        else:
            valid.next = False
            scnt.next = scnt + 1
            for oo in range(nout):
                if oo == 0:
                    oreg[oo].next = oreg[oo] << 1
                else:
                    oreg[oo].next = concat(oreg[oo][nby-1:0], oreg[oo-1][nby-1])

    @always_comb
    def beh_assign():
        for ii in range(nin):
            pin[ii].next = ireg[ii]

    return beh_shifts, beh_assign

