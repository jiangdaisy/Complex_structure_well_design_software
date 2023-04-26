# coding=UTF-8
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from figure import Ui_MainWindow
from matplotlib.backends.backend_qt5agg import (FigureCanvas,
                                                NavigationToolbar2QT as NavigationToolbar)
from matplotlib import colorbar
from matplotlib.figure import Figure
import re
import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSlot, Qt, QThread, pyqtSignal
import matplotlib as mpl
import matplotlib.style as mplStyle

from scipy.interpolate import griddata


from PyQt5.QtWidgets import (QApplication, QMainWindow,
                             QSplitter, QColorDialog, QLabel, QComboBox, QTreeWidgetItem, QProgressDialog)
from PyQt5.QtCore import pyqtSlot, QDir, QIODevice, QFile, QTextStream
from PyQt5.QtWidgets import QFileDialog

import numpy as np
import CSw_dcfbx_Slot


class QmyFigure(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.createFigure()  # 创建Figure和FigureCanvas对象，初始化界面



    def createFigure(self):
        ##      self.__fig=mpl.figure.Figure(figsize=(8, 5),constrained_layout=True, tight_layout=None)  #单位英寸
        ##      self.__fig=mpl.figure.Figure(figsize=(8, 5))  #单位英寸
        self.fig = Figure()
        # self.fig.tight_layout()
        figCanvas = FigureCanvas(self.fig)  # 创建FigureCanvas对象，必须传递一个Figure对象

        # self.__fig.suptitle("数据展示区", fontsize=16, fontweight='bold')  # 总的图标题

        naviToolbar = NavigationToolbar(figCanvas, self)  # 创建NavigationToolbar工具栏

        # actList = naviToolbar.actions()  # 关联的Action列表
        # count = len(actList)  # Action的个数
        # lastAction = actList[count - 1]  # 最后一个Action

        # self.progressLable = QLabel("当前子图")
        # self.progressLable.setVisible(False)
        # naviToolbar.insertWidget(lastAction, self.progressLable)
        #
        # self.progressBar = QtWidgets.QProgressBar()
        # self.progressBar.setVisible(False)
        # naviToolbar.insertWidget(lastAction, self.progressBar)

        self.addToolBar(naviToolbar)
        splitter = QSplitter(self)
        splitter.setOrientation(Qt.Horizontal)
        splitter.addWidget(figCanvas)  # 右侧FigureCanvas对象
        self.setCentralWidget(splitter)


import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = QmyFigure()
    form.show()
    sys.exit(app.exec_())
