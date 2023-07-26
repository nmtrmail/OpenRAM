# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California, Santa Cruz
# All rights reserved.
#
from openram.base.pin_layout import pin_layout
from openram.base.vector import vector
from openram.tech import drc
from .graph_utils import snap


class graph_shape(pin_layout):
    """
    This class inherits the pin_layout class to change some of its behavior for
    the graph router.
    """

    def __init__(self, name, rect, layer_name_pp, core=None):

        pin_layout.__init__(self, name, rect, layer_name_pp)

        # Snap the shape to the grid here
        ll, ur = self.rect
        self.rect = [snap(ll), snap(ur)]
        # Core is the original shape from which this shape is inflated
        self.core = core


    def center(self):
        """ Override the default `center` behavior. """

        return snap(super().center())


    def height(self):
        """ Override the default `height` behavior. """

        return snap(super().height())


    def width(self):
        """ Override the default `width` behavior. """

        return snap(super().width())


    def get_core(self):
        """
        Return `self` if `self.core` is None. Otherwise, return `self.core`.
        """

        if self.core is None:
            return self
        return self.core


    def inflated_pin(self, spacing=None, multiple=0.5, extra_spacing=0):
        """ Override the default inflated_pin behavior. """

        ll, ur = self.inflate(spacing, multiple)
        extra = vector([extra_spacing] * 2)
        newll = ll - extra
        newur = ur + extra
        inflated_area = (newll, newur)
        return graph_shape(self.name, inflated_area, self.layer, self)


    def multiply(self, scale):
        """ Multiply the width and height with the scale value. """

        width = (self.width() * (scale - 1)) / 2
        height = (self.height() * (scale - 1)) / 2
        ll, ur = self.rect
        newll = vector(ll.x - width, ll.y - height)
        newur = vector(ur.x + width, ur.y + height)
        self.rect = [snap(newll), snap(newur)]


    def aligns(self, other):
        """ Return if the other shape aligns with this shape. """

        # Shapes must overlap to be able to align
        if not self.overlaps(other):
            return False
        ll, ur = self.rect
        oll, our = other.rect
        if ll.x == oll.x and ur.x == our.x:
            return True
        if ll.y == oll.y and ur.y == our.y:
            return True
        return False
