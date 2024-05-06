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
import os
import pathlib
import sys


def classFactory(iface):  # pylint: disable=invalid-name
    """Load RousettusMain class from file RousettusMain.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    os.environ["ROUSETTUS_ROOT"] = str(pathlib.Path(__file__).parent.absolute())
    sys.path.append(os.environ.get("ROUSETTUS_ROOT"))
    try:
        from .rousettus import RousettusMain
    except Exception as e:
        sys.path.remove(os.environ.get("ROUSETTUS_ROOT"))
        os.environ.pop("ROUSETTUS_ROOT")
        raise e
    return RousettusMain(iface)
