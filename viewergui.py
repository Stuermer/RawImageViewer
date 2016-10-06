# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'viewer.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.setWindowModality(QtCore.Qt.NonModal)
        Form.resize(826, 567)
        self.gridLayout_2 = QtGui.QGridLayout(Form)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.iv_2dspec_zoom = ImageView(Form)
        self.iv_2dspec_zoom.setMaximumSize(QtCore.QSize(350, 350))
        self.iv_2dspec_zoom.setObjectName(_fromUtf8("iv_2dspec_zoom"))
        self.gridLayout.addWidget(self.iv_2dspec_zoom, 1, 0, 1, 1)
        self.plotwidget_3 = PlotWidget(Form)
        self.plotwidget_3.setMaximumSize(QtCore.QSize(100, 350))
        self.plotwidget_3.setObjectName(_fromUtf8("plotwidget_3"))
        self.gridLayout.addWidget(self.plotwidget_3, 1, 1, 1, 1)
        self.dial = QtGui.QDial(Form)
        self.dial.setMinimum(10)
        self.dial.setMaximum(150)
        self.dial.setSingleStep(2)
        self.dial.setProperty("value", 50)
        self.dial.setOrientation(QtCore.Qt.Horizontal)
        self.dial.setWrapping(False)
        self.dial.setNotchesVisible(False)
        self.dial.setObjectName(_fromUtf8("dial"))
        self.gridLayout.addWidget(self.dial, 3, 1, 1, 1)
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 2, 1, 1, 1)
        self.plotwidget_2 = PlotWidget(Form)
        self.plotwidget_2.setMaximumSize(QtCore.QSize(350, 100))
        self.plotwidget_2.setObjectName(_fromUtf8("plotwidget_2"))
        self.gridLayout.addWidget(self.plotwidget_2, 2, 0, 2, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 2, 1, 1, 1)
        self.listWidget = QtGui.QListWidget(Form)
        self.listWidget.setMaximumSize(QtCore.QSize(450, 16777215))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.gridLayout_2.addWidget(self.listWidget, 0, 1, 1, 1)
        self.iv_2dspec = ImageView(Form)
        self.iv_2dspec.setObjectName(_fromUtf8("iv_2dspec"))
        self.gridLayout_2.addWidget(self.iv_2dspec, 0, 0, 3, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.gridLayout_2.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        self.checkBox = QtGui.QCheckBox(Form)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.gridLayout_2.addWidget(self.checkBox, 1, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Image viewer", None))
        self.label_4.setText(_translate("Form", "box size:", None))
        self.label.setText(_translate("Form", "X", None))
        self.label_3.setText(_translate("Form", "Y", None))
        self.label_2.setText(_translate("Form", "value", None))
        self.checkBox.setText(_translate("Form", "rotate?", None))

from pyqtgraph import ImageView, PlotWidget
