from __future__ import division
from __future__ import print_function

from myhdl import enum

def get_utilization(fn=None):    
    """ Parse the device resource utilization from the logs.
        
        The relevant part looks like this:
        
        Report Cell Usage: 
        +------+-------+------+
        |      |Cell   |Count |
        +------+-------+------+
        |1     |BUFG   |     1|
        |2     |CARRY4 |     7|
        |3     |LUT1   |    28|
        |4     |LUT3   |     1|
        |5     |LUT4   |     5|
        |6     |LUT5   |     3|
        |7     |FDRE   |    28|
        |8     |IBUF   |     1|
        |9     |OBUF   |     8|
        +------+-------+------+
    """
    
    log = open(fn, 'r')
    info = {}
    info['syn'] = {}
    
    found_start = False
    plus_count = 0
    for ln in log:
        if ln.find('Report Cell Usage:') != -1:
            # Start parsing
            found_start = True
            continue
        elif found_start:
            # Line with data found
            if ln.startswith('|'):
                splitted = ln.split('|')
                splitted = [elem.strip() for elem in splitted]
                if splitted[2] != 'Cell':
                    info['syn'][splitted[2]] = splitted[3]
            # Count lines without data to identify end of table
            elif ln.startswith('+'):
                plus_count = plus_count+1
                if plus_count >= 3:
                    found_start = False
    return info