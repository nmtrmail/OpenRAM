# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import debug
from tech import cell_properties as props
import bitcell_base


class dummy_bitcell_1port(bitcell_base.bitcell_base):
    """
    A single bit cell (6T, 8T, etc.)  This module implements the
    single memory cell used in the design. It is a hand-made cell, so
    the layout and netlist should be available in the technology
    library.
    """
    pin_names = [props.bitcell.cell_1port.pin.bl,
                 props.bitcell.cell_1port.pin.br,
                 props.bitcell.cell_1port.pin.wl,
                 props.bitcell.cell_1port.pin.vdd,
                 props.bitcell.cell_1port.pin.gnd]
    type_list = ["OUTPUT", "OUTPUT", "INPUT", "POWER", "GROUND"]

    def __init__(self, name):
        super().__init__(name)
        debug.info(2, "Create dummy bitcell")


