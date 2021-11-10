# -*- coding: utf-8 -*-
"""
/***************************************************************************
 RousettusMain
                                 A QGIS plugin
 process geophysical data, collected with SibGis UAV platform

                             -------------------
        begin                : 2021-11-04
        copyright            : (C) 2021 by Vladimir Morozov
        email                : raulett@gmail.com
        git sha              : $Format:%H$

"""


def classFactory(iface):  # pylint: disable=invalid-name
    """Load RousettusMain class from file RousettusMain.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    from .rousettus import RousettusMain
    return RousettusMain(iface)
