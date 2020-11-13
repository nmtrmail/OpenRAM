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


class bitcell_1port(bitcell_base.bitcell_base):
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
    storage_nets = ['Q', 'Q_bar']

    def __init__(self, name):
        super().__init__(name)
        debug.info(2, "Create bitcell")

        self.nets_match = self.do_nets_exist(self.storage_nets)

    def get_all_wl_names(self):
        """ Creates a list of all wordline pin names """
        row_pins = [props.bitcell.cell_1port.pin.wl]
        return row_pins

    def get_all_bitline_names(self):
        """ Creates a list of all bitline pin names (both bl and br) """
        pin = props.bitcell.cell_1port.pin
        column_pins = [pin.bl, pin.br]
        return column_pins

    def get_all_bl_names(self):
        """ Creates a list of all bl pins names """
        return [props.bitcell.cell_1port.pin.bl]

    def get_all_br_names(self):
        """ Creates a list of all br pins names """
        return [props.bitcell.cell_1port.pin.br]

    def get_bl_name(self, port=0):
        """Get bl name"""
        debug.check(port == 0, "One port for bitcell only.")
        return props.bitcell.cell_1port.pin.bl

    def get_br_name(self, port=0):
        """Get bl name"""
        debug.check(port == 0, "One port for bitcell only.")
        return props.bitcell.cell_1port.pin.br

    def get_wl_name(self, port=0):
        """Get wl name"""
        debug.check(port == 0, "One port for bitcell only.")
        return props.bitcell.cell_1port.pin.wl

    def build_graph(self, graph, inst_name, port_nets):
        """
        Adds edges based on inputs/outputs.
        Overrides base class function.
        """
        self.add_graph_edges(graph, port_nets)
