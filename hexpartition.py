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
        The geograhical point's vertical (altitude) space coordinate.
    data
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
