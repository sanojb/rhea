
from pprint import pprint

import rhea.build as build
from rhea.build.boards import get_board
from blink import blinky


def run_red_pitaya():
    # get a board to implement the design on
    brd = get_board('red_pitaya')
    flow = build.flow.Vivado(brd=brd, top=blinky)
    flow.run()
    info = flow.get_utilization()
    pprint(info)
    

if __name__ == '__main__':
    run_red_pitaya()