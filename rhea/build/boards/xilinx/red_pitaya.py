##
# Board definition for Red Pitaya
#
# Constraints are extracted from
# https://github.com/RedPitaya/RedPitaya/blob/master/fpga/sdc/red_pitaya.xdc
##


from rhea.build import FPGA
from rhea.build.toolflow import Vivado


class RedPitaya(FPGA):
    vendor = 'xilinx'
    family = 'zynq'
    device = 'XC7Z010'
    package = 'CLG400'
    speed = -1
    _name = 'red_pitaya'
    
    default_clocks = {
        'clock': dict(frequency=125e6, pins=('L16',),
                      iostandard='LVCMOS33'),
    }

    # default_resets = {
    #     'reset': dict(active=0, async=True, pins=('G14',),
    #                   iostandard='LVCMOS25'),  #  drive=4
    # }
    
    default_ports = {
		### ADC
		# ADC data
        'adc_dat_i_[1]': dict(pins=('Y17', 'W16', 'Y16', 'W15', 'W14', 'Y14', 'W13', 'V12', 'V13', 'T14', 'T15', 'V15', 'T16', 'V16'),
                    iostandard='LVCMOS18', iob='TRUE'),
		'adc_dat_i_[2]': dict(pins=('R18', 'P16', 'P18', 'N17', 'R19', 'T20', 'T19', 'U20', 'V20', 'W20', 'W19', 'Y19', 'W18', 'Y18'),
                    iostandard='LVCMOS18', iob='TRUE'),
					
		# ADC clock
		'adc_clk_i': dict(pins=('U18', 'U19'),						# Input
                    iostandard='DIFF_HSTL_I_18'),
		'adc_clk_o': dict(pins=('N20', 'P20'),						# Output
                    iostandard='LVCMOS18', slew='FAST', drive='8'),
		'adc_cdcs_o': dict(pins=('V18'),							# Stabilizer
                    iostandard='LVCMOS18', slew='FAST', drive='8'),
					
		### DAC
		# DAC data
        'dac_dat_o': dict(pins=('M19', 'M20', 'L19', 'L20', 'K16', 'J19', 'J20', 'H20', 'G19', 'G20', 'F19', 'F20', 'D20', 'D19'),
                    iostandard='LVCMOS33', slew='SLOW', drive='4'),
					
		# DAC control
		'dac_wrt_o': dict(pins=('M17'),
                    iostandard='LVCMOS33', slew='FAST', drive='8'),
		'dac_sel_o': dict(pins=('N16'),
                    iostandard='LVCMOS33', slew='FAST', drive='8'),
		'dac_clk_o': dict(pins=('M18'),
                    iostandard='LVCMOS33', slew='FAST', drive='8'),
		'dac_rst_o': dict(pins=('N15'),
                    iostandard='LVCMOS33', slew='FAST', drive='8'),
					
		### PWM DAC
		'dac_pwm_o': dict(pins=('T10', 'T11', 'P15', 'U13'),
                    iostandard='LVCMOS18', slew='FAST', drive='12', iob='TRUE'),
					
		### XADC (AD8, AD0, AD1, AD9, V_0)
		'vinp_i': dict(pins=('B19', 'C20', 'E17', 'E18', 'K9'),
                    iostandard='LVCMOS33'),
		'vinn_i': dict(pins=('A20', 'B20', 'D18', 'E19', 'L10'),
                    iostandard='LVCMOS33'),
					
		### Expansion connector
		'exp_p_io': dict(pins=('G17', 'H16', 'J18', 'K17', 'L14', 'L16', 'K16', 'M14'),
                    iostandard='LVCMOS33', slew='FAST', drive='8'),
		'exp_n_io': dict(pins=('G18', 'H17', 'H18', 'K18', 'L15', 'L17', 'J16', 'M15'),
                    iostandard='LVCMOS33', slew='FAST', drive='8'),
					
		### SATA connector
		'daisy_p_o': dict(pins=('T12', 'U14'),
                    iostandard='LVCMOS18'),
		'daisy_n_o': dict(pins=('U12', 'U15'),
                    iostandard='LVCMOS18'),
		'daisy_p_i': dict(pins=('P14', 'N18'),
                    iostandard='LVCMOS18'),
		'daisy_n_i': dict(pins=('R14', 'P19'),
                    iostandard='LVCMOS18'),
					
		## LED
		'led': dict(pins=('F16', 'F17', 'G15', 'H15', 'K14', 'G14', 'J15', 'J14'),
                    iostandard='LVCMOS33', slew='SLOW', drive='4'),
					
					
		
    }

    def get_flow(self, top=None):
        return Vivado(brd=self, top=top)
