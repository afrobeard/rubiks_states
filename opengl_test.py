import sys
import math, random

from PyQt5.QtCore import (QPoint, QPointF, QRect, QRectF, QSize, Qt, QTime,
        QTimer)
from PyQt5.QtGui import (QBrush, QColor, QFontMetrics, QImage, QPainter,
        QRadialGradient, QSurfaceFormat)
from PyQt5.QtWidgets import QApplication, QOpenGLWidget

import OpenGL.GL as gl


class GLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)

        midnight = QTime(0, 0, 0)
        random.seed(midnight.secsTo(QTime.currentTime()))

        self.object = 0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.image = QImage()
        self.lastPos = QPoint()

        self.Purple = QColor.fromCmykF(0.39, 0.39, 0.0, 0.0)

        self.animationTimer = QTimer()
        self.animationTimer.setSingleShot(False)
        self.animationTimer.timeout.connect(self.animate)
        self.animationTimer.start(25)

        self.setAutoFillBackground(False)
        self.setMinimumSize(400, 400)
        self.setWindowTitle("Overpainting a Scene")

    def setXRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle

    def setYRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle

    def setZRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle

    def initializeGL(self):
        # gl = self.context().versionFunctions()
        # gl.initializeOpenGLFunctions()

        self.object = self.makeObject()

    def mousePressEvent(self, event):
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & Qt.LeftButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setYRotation(self.yRot + 8 * dx)
        elif event.buttons() & Qt.RightButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setZRotation(self.zRot + 8 * dx)

        self.lastPos = event.pos()

    def paintEvent(self, event):
        self.makeCurrent()

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPushMatrix()

        self.setClearColor(self.Purple.darker())
        gl.glShadeModel(gl.GL_SMOOTH)
        gl.glEnable(gl.GL_DEPTH_TEST)
        #gl.glEnable(gl.GL_CULL_FACE)
        gl.glEnable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_LIGHT0)
        gl.glEnable(gl.GL_MULTISAMPLE)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION,
                (0.5, 5.0, 7.0, 1.0))

        self.setupViewport(self.width(), self.height())

        gl.glClear(
                gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()
        gl.glTranslated(0.0, 0.0, -10.0)
        gl.glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        gl.glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        gl.glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        gl.glCallList(self.object)

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPopMatrix()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.end()

    def resizeGL(self, width, height):
        self.setupViewport(width, height)


    def sizeHint(self):
        return QSize(400, 400)

    def makeObject(self):
        genList = gl.glGenLists(1)
        gl.glNewList(genList, gl.GL_COMPILE)

        self.setColor(QColor.fromCmykF(1.0, 0.0, 0.0, 0.0))
        gl.glBegin(gl.GL_QUADS)

        gl.glNormal3d(0.0, 1.0, 0.0);
        gl.glVertex3d(-0.5, 0.5, 0.5);
        gl.glVertex3d(0.5, 0.5, 0.5);
        gl.glVertex3d(0.5, 0.5, -0.5);
        gl.glVertex3d(-0.5, 0.5, -0.5);
        gl.glEnd()

        gl.glBegin(gl.GL_QUADS)
        gl.glNormal3d(0.0, 0.0, 1.0);
        gl.glVertex3d(0.5, -0.5, 0.5);
        gl.glVertex3d(0.5, 0.5, 0.5);
        gl.glVertex3d(-0.5, 0.5, 0.5);
        gl.glVertex3d(-0.5, -0.5, 0.5);
        gl.glEnd()

        gl.glBegin(gl.GL_QUADS)
        gl.glNormal3d(1.0, 0.0, 0.0);
        gl.glVertex3d(0.5, 0.5, -0.5);
        gl.glVertex3d(0.5, 0.5, 0.5);
        gl.glVertex3d(0.5, -0.5, 0.5);
        gl.glVertex3d(0.5, -0.5, -0.5);
        gl.glEnd()


        gl.glEndList()

        return genList


    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle

    def animate(self):
        self.update()

    def setupViewport(self, width, height):
        side = min(width, height)
        gl.glViewport((width - side) // 2, (height - side) // 2, side,
                side)

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(-0.5, +0.5, +0.5, -0.5, 4.0, 15.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def setClearColor(self, c):
        gl.glClearColor(c.redF(), c.greenF(), c.blueF(), c.alphaF())

    def setColor(self, c):
        gl.glColor4f(c.redF(), c.greenF(), c.blueF(), c.alphaF())


if __name__ == '__main__':

    app = QApplication(sys.argv)

    fmt = QSurfaceFormat()
    fmt.setSamples(4)
    QSurfaceFormat.setDefaultFormat(fmt)

    window = GLWidget()
    window.show()
    sys.exit(app.exec_())
