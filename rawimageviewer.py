from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import sys
from astropy.io import fits
from viewergui import Ui_Form
from scipy import ndimage
from scipy.interpolate import splrep, splev, sproot
import glob

def FWHM_spline(x, y):
    """
    Determine full-with-half-maximum of a peaked set of points, x and y.

    Assumes that there is only one peak present in the datasset.  The function
    uses a spline interpolation of order k=3.
    """
    ymin = np.min(y)
    half_max = np.amax(y-ymin)/2.0
    s = splrep(x, y - ymin - half_max)
    roots = sproot(s)

    x2 = np.linspace(min(x), max(x), 1000)
    tck = splrep(x, y)
    y2 = splev(x2, tck)

    if len(roots) > 2:
        print("The dataset appears to have multiple peaks, and thus the FWHM can't be determined.")
        return 0, 0, 0
    elif len(roots) < 2:
        print("No proper peaks were found in the data set; likely the dataset is flat (e.g. all zeros).")
        return 0, 0, 0
    else:
        return abs(roots[1] - roots[0]), roots[0], splev(roots[0], tck), roots[1], splev(roots[1], tck)


class RawViewer(QtGui.QDialog):
    def __init__(self):
        super(RawViewer, self).__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.rawdata = None
        self.proxy = None

        self.zoombox = pg.QtGui.QGraphicsRectItem()
        self.zoombox.setPen(pg.mkPen((200, 0, 0, 150)))
        self.ui.iv_2dspec.addItem(self.zoombox)

        self.update_zoom = True
        self.zoom_region = None

        # setup plot style
        self.ui.iv_2dspec_zoom.ui.roiBtn.hide()
        self.ui.iv_2dspec_zoom.ui.menuBtn.hide()
        self.ui.iv_2dspec_zoom.ui.histogram.hide()

        self.ui.iv_2dspec.ui.roiBtn.hide()
        self.ui.iv_2dspec.ui.menuBtn.hide()

        self.ui.listWidget.itemClicked.connect(self.listwidget_click)

        self.roi = pg.ROI([25, 50], [25, 50])
        self.roi.addScaleHandle([0.5, 1], [0.5, 0.5])
        self.roi.addScaleHandle([0, 0.5], [0.5, 0.5])
        self.ui.iv_2dspec_zoom.addItem(self.roi)
        self.roi.sigRegionChanged.connect(self.update_1d_zoom)
        self.data1d_y = None
        self.data1d_x = None

        self.zoomx_1d_menu = self.ui.plotwidget_2.getPlotItem().getMenu()
        self.zoomx_1d_menu.addAction("test")

        self.ui.plotwidget_2.scene().sigMouseClicked.connect(self.MouseClick1d)
        self.ui.plotwidget_3.scene().sigMouseClicked.connect(self.MouseClick1d)

        self.proxy = pg.SignalProxy(self.ui.iv_2dspec.scene.sigMouseMoved, rateLimit=60, slot=self.MouseOver2d)

        self.ui.iv_2dspec.scene.sigMouseClicked.connect(self.MouseClick2d)

        self.directory = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.populate_image_list(directory=self.directory)

    def populate_image_list(self, directory):
        for filename in glob.iglob(directory + '/*.fit'):
            self.ui.listWidget.addItem(filename)
        for filename in glob.iglob(directory + '/*.fits'):
            self.ui.listWidget.addItem(filename)

    def listwidget_click(self, item):
        self.load_image(item.text(), self.ui.checkBox.isChecked())

    def load_image(self, filepath, orientation):
        self.rawdata = fits.getdata(str(filepath))
        if orientation == 0:
            self.rawdata = ndimage.rotate(self.rawdata, -90)

        self.ui.iv_2dspec.setImage(self.rawdata.T)

    def update_1d_zoom(self):
        xmin, xmax, ymin, ymax = self.zoom_region
        selected = self.roi.getArrayRegion(self.rawdata[ymin:ymax, xmin:xmax].T, self.ui.iv_2dspec_zoom.getImageItem())
        self.data1d_x = selected.mean(axis=1)
        self.ui.plotwidget_2.plot(self.data1d_x, clear=True)
        self.data1d_y = selected.mean(axis=0)
        curve = self.ui.plotwidget_3.plot(self.data1d_y, clear=True)
        curve.rotate(-90)

    def MouseOver2d(self, event):
        position = event[0]
        test = self.ui.iv_2dspec.getImageItem().mapFromScene(position)
        x = test.x()
        y = test.y()

        if self.update_zoom:
            if (0 < x < self.rawdata.shape[1]) and (0 < y < self.rawdata.shape[0]):
                xmin = int(max(x - self.ui.dial.value(), 0))
                xmax = int(min(self.rawdata.shape[1], x + self.ui.dial.value()))

                ymin = int(max(0, y - self.ui.dial.value()))
                ymax = int(min(self.rawdata.shape[0], y + self.ui.dial.value()))

                self.zoom_region = [xmin, xmax, ymin, ymax]
                self.ui.iv_2dspec_zoom.setImage(self.rawdata[ymin:ymax, xmin:xmax].T)
                self.ui.label.setText("X: %d" % x)
                self.ui.label_3.setText("Y: %d" % y)
                self.ui.label_2.setText("Value: %d" % self.rawdata[int(y), int(x)])

                self.zoombox.setRect(x - self.ui.dial.value(), y - self.ui.dial.value(), 2. * self.ui.dial.value(),
                                     2. * self.ui.dial.value())

    def MouseClick1d(self):
        fwhm = FWHM_spline(np.arange(len(self.data1d_x)), self.data1d_x)
        if not fwhm[0] == 0:
            self.ui.plotwidget_2.plot([fwhm[1], fwhm[3]], [fwhm[2], fwhm[4]])
            text = pg.TextItem("%.4f" % fwhm[0])
            self.ui.plotwidget_2.addItem(text)
            text.setPos(fwhm[1], fwhm[2])

        fwhm = FWHM_spline(np.arange(len(self.data1d_y)), self.data1d_y)
        if not fwhm[0] == 0:
            curve = self.ui.plotwidget_3.plot([fwhm[1], fwhm[3]], [fwhm[2], fwhm[4]])
            curve.rotate(-90)
            text = pg.TextItem("%.4f" % fwhm[0])
            self.ui.plotwidget_3.addItem(text)
            text.setPos(fwhm[2], -fwhm[1])
            text.rotate(90)

    def MouseClick2d(self, event):
        if event.button() == 1:
            self.update_zoom = not (self.update_zoom)
            self.update_1d_zoom()


def main():
    app = QtGui.QApplication(sys.argv)
    w = RawViewer()
    w.showMaximized()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()