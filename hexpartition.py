# -*- coding: utf-8 -*-
#! python

import numpy as np

"""Hexagonal partitioner

This module enable a triangle drawn over geographical data to be partioned into
smaller hexagons and fractions of hexagons.
"""

class GeoPointDatum(object):
    """GeoPointDatum is a geographical point with data attached to it.

    Attributes
    ----------
    h : ndarray
        The geographical point's horizontal (surface) space coordinates. A 2D
        array with `float` type.
    v : float
        The geographical point's vertical (altitude) space coordinate.
    data : dict
    """

    def __init__(self, h0=0.0, h1=0.0, v=0.0):
        """Initiate a GeoPointDatum object.

        Parameters
        ----------
        h0 : float
            The point's first horizontal coordinate.
        h1 : float
            The point's second horizontal coordinate.
        v : float
            The point's vertical coordinate.
        """
        super(GeoPointDatum, self).__init__()
        self.h = np.array([h0, h1], dtype = float)
        self.v = v

        #: dict: A dictionary of the data associated with this point in space
        self.data = {}

    def addDatum(self, key, value):
        """Add a key:value pair to the GeoPointDatum data dictionary.

        Parameters
        ----------
        key
            A dictionary key for referencing the datum later on. Usually a name
            or a short descriptor.
        value
            The datum that the key references. it could be an int, float, string
            or any other kind of object.
        """
        self.data[key] = value

    @property
    def position(self):
        """ndarray: The GeoPointDatum position on the surface."""
        return self.h

    @position.setter
    def position(self, newPos):
        """Move the datum to a new position on the surface.

        Parameters
        ----------
        newPos : ndarray
            The geographical point's new horizontal (surface) space
            coordinates. A 2D array with `float` type.
        """
        self.h = newPos

    @property
    def altitude(self):
        """float: The GeoPointDatum altitude above or below the surface."""
        return self.v

    @altitude.setter
    def altitude(self, newAlt):
        """Move the datum to a new altitude.

        Parameters
        ----------
        newAlt : float
            The geograhical point's new altitude above or below the surface.
        """
        self.v = newAlt

class GeoLine(object):
    """GeoLine is an object that represents a line segment. A data dictionary
    may be attached.

    Attributes
    ----------
    endPoints : tuple of GeoPointDatum
        A 2-tuple of GeoPointData.
    halfedges : tuple of GeoPointDatum
        A 2-tuple of special GeoPointDatum. Positions match one of the GeoLine
        endpoints, data is the facing GeoShape, the next half-edge, the parent
        GeoLine, and the twin half-edge
    data : dict
    """

    def __init__(self, p0, p1):
        """Initiate a GeoLine object

        Parameters
        ----------
        p0 : GeoPointDatum
            Endpoint of the line segment.
        p1 : GeoPointDatum
            Other endpoint of the line segment.
        """
        self.endPoints = p0, p1
        tp0 = GeoPointDatum(p0.h[0], p0.h[1], p0.v)
        tp1 = GeoPointDatum(p1.h[0], p1.h[1], p1.v)
        tp0.addDatum('shape':None)
        tp0.addDatum('next':tp1)
        tp0.addDatum('twin':tp1)
        tp0.addDatum('parent':self)
        tp1.addDatum('shape':None)
        tp1.addDatum('next':tp0)
        tp1.addDatum('twin':tp0)
        tp1.addDatum('parent':self)
        self.halfedges = tp0, tp1

        #: dict: A dictionary of the data associated with this line
        self.data = {}

    def addDatum(self, key, value):
        """Add a key:value pair to the GeoLine data dictionary.

        Parameters
        ----------
        key
            A dictionary key for referencing the datum later on. Usually a name
            or a short descriptor.
        value
            The datum that the key references. it could be an int, float, string
            or any other kind of object.
        """
        self.data[key] = value
