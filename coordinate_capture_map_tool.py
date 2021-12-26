# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CoordinateCaptureMapTool
                                 A QGIS plugin
 Python port of the deprecated Coordinate Capture core plugin
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2020-07-04
        git sha              : $Format:%H$
        copyright            : (C) 2020 by Stefanos Natsis
        email                : uclaros@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import pyqtSignal, Qt
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand
from qgis.core import QgsWkbTypes, QgsPointXY, QgsApplication


class CoordinateCaptureMapTool(QgsMapToolEmitPoint):
    mouseMoved = pyqtSignal(QgsPointXY)
    mouseClicked = pyqtSignal(QgsPointXY)

    def __init__(self, canvas):
        super(CoordinateCaptureMapTool, self).__init__(canvas)

        self.mapCanvas = canvas
        self.rubberBand = QgsRubberBand(self.mapCanvas, QgsWkbTypes.PolygonGeometry)
        self.rubberBand.setColor(Qt.red)
        self.rubberBand.setWidth(3)
        self.setCursor(QgsApplication.getThemeCursor(QgsApplication.Cursor.CrossHair))

    def canvasMoveEvent(self, e):
        originalPoint = QgsPointXY(self.mapCanvas.getCoordinateTransform().toMapCoordinates(e.x(), e.y()))
        self.mouseMoved.emit(originalPoint)

    def canvasPressEvent(self, e):
        if e.button() == Qt.LeftButton:
            originalPoint = QgsPointXY(self.mapCanvas.getCoordinateTransform().toMapCoordinates(e.x(), e.y()))
            self.mouseClicked.emit(originalPoint)

            point1 = QgsPointXY(self.mapCanvas.getCoordinateTransform().toMapCoordinates(e.x() - 1, e.y() - 1))
            point2 = QgsPointXY(self.mapCanvas.getCoordinateTransform().toMapCoordinates(e.x() + 1, e.y() - 1))
            point3 = QgsPointXY(self.mapCanvas.getCoordinateTransform().toMapCoordinates(e.x() + 1, e.y() + 1))
            point4 = QgsPointXY(self.mapCanvas.getCoordinateTransform().toMapCoordinates(e.x() - 1, e.y() + 1))

            self.rubberBand.reset(QgsWkbTypes.PolygonGeometry )

            self.rubberBand.addPoint(point1, False)
            self.rubberBand.addPoint(point2, False)
            self.rubberBand.addPoint(point3, False)
            self.rubberBand.addPoint(point4, True)
            self.rubberBand.show()

        elif e.button() == Qt.RightButton:
            self.deactivate()

    def deactivate(self):
        self.rubberBand.reset(QgsWkbTypes.LineGeometry)
        super(CoordinateCaptureMapTool, self).deactivate()
