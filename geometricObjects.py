# -*- coding: utf-8 -*-
#! python

import numpy as np
import warnings

"""Geometric Objects

These are the base object classes for manipulating planar graphs that contain
geographic data. These objects are meant for setting up a double connected edge
list or a half-edge data structure for containing geographic data.
"""

class GeoPointDatum(object):
    """GeoPointDatum is a geographical point with data attached to it.

    Attributes
    ----------
    h : ndarray of floats
        The geographical point's horizontal (surface) space coordinates. An
        ndarray with `float` type.
    v : float
        The geographical point's vertical (altitude) space coordinate.
    data : dict
    """

    def __init__(self, h=[0.0,0.0], v=0.0):
        """Initiate a GeoPointDatum object.

        Parameters
        ----------
        h : ndarray or list of float
            The point's horizontal coordinates or the point's projection onto
            the surface.
        v : float
            The point's vertical coordinate. Altitude is positive, depth is
            negative.

        Examples
        --------
        >>> point0 = GeoPointDatum(np.array([5.01, 3.01]), -1.0)
        >>> point1 = GeoPointDatum()
        """
        super(GeoPointDatum, self).__init__()
        self.h = np.array(h, dtype = float)
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

        Examples
        --------
        >>> point0 = GeoPointDatum()
        >>> point0.addDatum('color','purple')
        >>> point0.data
        {'color': 'purple'}
        >>> point0.addDatum('temperature', 390.25)
        >>> point0.data
        {'color': 'purple', 'temperature': 390.25}
        """
        self.data[key] = value

    @property
    def position(self):
        """ndarray: The GeoPointDatum position on the surface.

        Examples
        --------
        >>> point0 = GeoPointDatum(np.array([5.01, 3.01]), -1.0)
        >>> point0.position
        array([ 5.01,  3.01])
        >>> point0.position = [6,12]
        >>> point0.position
        array([  6.,  12.])
        """
        return self.h

    @position.setter
    def position(self, newPos):
        """Move the datum to a new position on the surface.

        Parameters
        ----------
        newPos : ndarray
            The geographical point's new horizontal (surface) space
            coordinates. An ndarray or list with `float` type.
        """
        self.h = np.array(newPos,dtype=float)

    @property
    def altitude(self):
        """float: The GeoPointDatum altitude above or below the surface.

        Examples
        --------
        >>> point0 = GeoPointDatum(np.array([5.01, 3.01]), -1.0)
        >>> point0.altitude
        -1.0
        >>> point0.altitude = -2.25
        >>> point0.altitude
        -2.25
        """
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
        A 2-tuple of GeoPointData. Reference to the endpoints of the line
        segment.
    halfedges : tuple of GeoPointDatum
        A 2-tuple of special GeoPointDatum. Positions match one of the GeoLine
        endpoints, data is the facing GeoShape, the next half-edge, the previous
        half-edge, the parent GeoLine, and the twin half-edge.
    data : dict
    """

    def __init__(self, p0, p1):
        """Initiate a GeoLine object that connects two endpoints. The degenerate
        case where the two endpoints are the same is allowed.

        Parameters
        ----------
        p0 : GeoPointDatum
            Endpoint of the line segment.
        p1 : GeoPointDatum
            Other endpoint of the line segment.

        Examples
        --------
        >>> line0 = GeoLine(GeoPointDatum([1.3, 1.4]), GeoPointDatum([-1.3, 1.4]))
        """
        self.endPoints = p0, p1
        tp0 = GeoPointDatum(p0.h, p0.v)
        tp1 = GeoPointDatum(p1.h, p1.v)
        tp0.addDatum('shape', None)
        tp0.addDatum('next', tp1)
        tp0.addDatum('previous', tp1)
        tp0.addDatum('twin', tp1)
        tp0.addDatum('parent', self)
        tp1.addDatum('shape', None)
        tp1.addDatum('next', tp0)
        tp1.addDatum('previous', tp0)
        tp1.addDatum('twin', tp0)
        tp1.addDatum('parent', self)
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

        Examples
        --------
        >>> p = [GeoPointDatum([1.3, 1.4]), GeoPointDatum([-1.3, 1.4])]
        >>> line0 = GeoLine(p[0], p[1])
        >>> line0.addDatum('color','firebrick')
        >>> line0.data
        {'color': 'firebrick'}
        """
        self.data[key] = value

    def joinLines(self, line0):
        """Join two line segments into a curve. The two line segments should
        have at least one of their endpoints in common. The degenerate cases
        where both lines are the same and where both lines have the two same
        endpoints is allowed.

        Parameters
        ----------
        line0 : GeoLine
            The line to be joined to this GeoLine to create a curve.

        Examples
        --------
        >>> points = [GeoPointDatum([1.3, 1.4]),
        ...     GeoPointDatum([0.0, 1.6]),
        ...     GeoPointDatum([-1.3, 1.4])]
        >>> lines = [GeoLine(points[0], points[1]), GeoLine(points[1], points[2])]
        >>> lines[0].joinLines(lines[1])
        """
        # find out which endpoint the two lines share in common
        connection = {0 : None, 1 : None}
        connectionCount = 0
        if self.endPoints[0] in line0.endPoints:
            connectionCount = connectionCount + 1
            if self.endPoints[0] is line0.endPoints[0]:
                connection[0] = 0
            elif self.endPoints[0] is line0.endPoints[1]:
                connection[0] = 1
        if self.endPoints[1] in line0.endPoints:
            connectionCount = connectionCount + 1
            if self.endPoints[1] is line0.endPoints[0]:
                connection[1] = 0
            elif self.endPoints[1] is line0.endPoints[1]:
                connection[1] = 1

        if connectionCount == 0:
            warnings.warn("joinLines() did not join the line segments. Zero common endpoints.")

        for k,v in connection.items():
            if v is not None:
                outEdge = self.halfedges[k]
                inEdge = self.halfedges[k].data['previous']
                newOut = line0.halfedges[v]
                newIn = line0.halfedges[v].data['twin']
                outEdge.data['previous'] = newIn
                newIn.data['next'] = outEdge
                newIn.data['shape'] = outEdge.data['shape']
                inEdge.data['next'] = newOut
                newOut.data['previous'] = inEdge
                newOut.data['shape'] = inEdge.data['shape']

class GeoShape(object):
    """GeoShape is a representation of a planar shape. The shape and the plane
    itself is represented in a half-edge data structure, so the shape references
    only one of its bounding half-edges per boundary. The rest of the bounding
    half-edges and the bounding vertices can be reached via next and previous
    half-edge references. Outer boundaries should be defined counter-clockwise
    to the positive normal to the plane for consistency's sake. May also include
    an attached data dictionary.

    Attributes
    ----------
    boundaryRefs : list of GeoPoints
        A list of half-edges, one for every inner and outer boundary of the
        GeoShape
    data : dict
    """

    def __init__(self, halfedge):
        try:
            halfedge.data['shape'] = self
        except (AttributeError, KeyError) as e:
            message = "GeoShape not initialized with a proper half-edge object."
            raise TypeError(message)

        temp = halfedge.data['next']
        while temp is not halfedge:
            temp.data['shape'] = self
            temp = temp.data['next']

if __name__ == "__main__":
    import doctest
    doctest.testmod()
