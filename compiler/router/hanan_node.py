# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California, Santa Cruz
# All rights reserved.
#
from openram.base.vector import vector
from openram.base.vector3d import vector3d
from openram.tech import drc


class hanan_node:
    """ This class represents a node on the Hanan graph. """

    # This is used to assign unique ids to nodes
    next_id = 0

    def __init__(self, center):

        self.id = hanan_node.next_id
        hanan_node.next_id += 1
        if isinstance(center, vector3d):
            self.center = center
        else:
            self.center = vector3d(center)
        self.neighbors = []


    def add_neighbor(self, other):
        """ Connect two nodes. """

        if other not in self.neighbors:
            self.neighbors.append(other)
            other.neighbors.append(self)


    def remove_neighbor(self, other):
        """ Disconnect two nodes. """

        if other in self.neighbors:
            self.neighbors.remove(other)
            other.neighbors.remove(self)


    def remove_all_neighbors(self):
        """ Disconnect all current neighbors. """

        for neighbor in self.neighbors:
            self.neighbors.remove(neighbor)
            neighbor.neighbors.remove(self)


    def get_direction(self, b):
        """ Return the direction of path from a to b. """

        horiz = self.center.x == b.center.x
        vert = self.center.y == b.center.y
        return (horiz, vert)


    def get_edge_cost(self, other, prev_node=None):
        """ Get the cost of going from this node to the other node. """

        if other in self.neighbors:
            is_vertical = self.center.x == other.center.x
            layer_dist = self.center.distance(other.center)
            # Edge is on non-preferred direction
            if is_vertical != bool(self.center.z):
                layer_dist *= 2
                # Wire bends towards non-preferred direction
                # NOTE: Adding a fixed cost prevents multiple dog-legs in
                # non-preferred direction
                if prev_node and self.get_direction(prev_node) != self.get_direction(other):
                    layer_dist += drc["grid"]
            via_dist = abs(self.center.z - other.center.z) * 2
            return layer_dist + via_dist
        return float("inf")
