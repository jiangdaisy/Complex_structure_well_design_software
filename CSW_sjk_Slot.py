import re
import sys
from sklearn.ensemble import RandomForestClassifier
import random

from skimage import measure
import cv2
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSlot, Qt, QThread, pyqtSignal
import matplotlib as mpl
import matplotlib.dates as mdates
import matplotlib.style as mplStyle
from matplotlib import pyplot as plt
from scipy.interpolate import griddata

from CSw_sjk import Ui_MainWindow

from PyQt5.QtWidgets import (QApplication, QMainWindow,
                             QSplitter, QColorDialog, QLabel, QComboBox, QTreeWidgetItem, QProgressDialog,
                             QTableWidgetItem, QMessageBox)
from PyQt5.QtCore import pyqtSlot, QDir, QIODevice, QFile, QTextStream
from PyQt5.QtWidgets import QFileDialog
from myfigure import QmyFigure

import numpy as np
import CSw_dcfbx_Slot
import datetime
import pandas as pd

CJX = {}
BHD = {}
KXD = {}
STL = {}

DJDZSJ = {}
XSPMSJ = {}
SKSJ = {}
CSSJ = {}
CJDYSJ = {}
ZSJS = {}
XSQX = []
CYJS = {}
DS = []
CJDYZB = {}
jgjpj = []
jgjpj1 = []
jgjpj2 = []


class QmyMainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)  # 调用父类构造函数，创建窗体
        self.ui = Ui_MainWindow()  # 创建UI对象
        self.ui.setupUi(self)  # 构造UI界面

        self.stepx = 50
        self.stepy = 50
        self.qlqFloor = []  #潜力区所有需要筛选层的层名
        self.qlqBinary = {}
        self.qlqXb = {}
        self.qlqYb = {}
        self.qlqContours = {}
        self.qlqTable = {}
        self.qlqTableList = []
        self.mbj = []

        self.XMXYXHD = []
        self.XMXSTL = []
        self.XMXKXD = []
        self.XMXBHD = []

        # 展开节点
        self.ui.treeWidget.topLevelItem(0).setExpanded(True)
        self.ui.treeWidget.topLevelItem(1).setExpanded(True)
        # self.ui.treeWidget.setAlternatingRowColors(True)
        self.ui.treeWidget.clicked.connect(self.on_treeWidget_clicked)
        self.ui.treeWidget.topLevelItem(0).setIcon(0, QtGui.QIcon('images/122.bmp'))
        self.ui.treeWidget.topLevelItem(1).setIcon(0, QtGui.QIcon('images/122.bmp'))
        self.ui.treeWidget.topLevelItem(0).child(0).setIcon(0, QtGui.QIcon('images/122.bmp'))
        self.ui.treeWidget.topLevelItem(0).child(1).setIcon(0, QtGui.QIcon('images/122.bmp'))
        self.ui.treeWidget.topLevelItem(0).child(2).setIcon(0, QtGui.QIcon('images/122.bmp'))
        self.ui.treeWidget.topLevelItem(0).child(3).setIcon(0, QtGui.QIcon('images/122.bmp'))
        self.ui.treeWidget.topLevelItem(0).child(4).setIcon(0, QtGui.QIcon('images/122.bmp'))
        self.ui.treeWidget.topLevelItem(1).child(0).setIcon(0, QtGui.QIcon('images/122.bmp'))
        self.ui.treeWidget.topLevelItem(1).child(1).setIcon(0, QtGui.QIcon('images/122.bmp'))
        self.ui.treeWidget.topLevelItem(1).child(2).setIcon(0, QtGui.QIcon('images/122.bmp'))
        self.ui.treeWidget.topLevelItem(1).child(3).setIcon(0, QtGui.QIcon('images/122.bmp'))
        self.ui.treeWidget.topLevelItem(1).child(4).setIcon(0, QtGui.QIcon('images/122.bmp'))
        self.ui.treeWidget.topLevelItem(1).child(5).setIcon(0, QtGui.QIcon('images/122.bmp'))
        self.ui.treeWidget.topLevelItem(1).child(6).setIcon(0, QtGui.QIcon('images/122.bmp'))

        self.setWindowState(Qt.WindowMaximized)  # 窗口最大化显示
        # self.ui.tabWidget.setVisible(False)  # 隐藏
        self.ui.tabWidget.clear()  # 清除所有页面
        self.ui.tabWidget.setTabsClosable(True)  # Page有关闭按钮


        mplStyle.use("classic")  # 使用样式，必须在绘图之前调用,修改字体后才可显示汉字
        mpl.rcParams['font.sans-serif'] = ['KaiTi', 'SimHei']  # 显示汉字为 楷体， 汉字不支持 粗体，斜体等设置
        mpl.rcParams['font.size'] = 12
        ##  Windows自带的一些字体
        ##  黑体：SimHei 宋体：SimSun 新宋体：NSimSun 仿宋：FangSong  楷体：KaiTi
        mpl.rcParams['axes.unicode_minus'] = False  # 减号unicode编码

        self.__fig = None  # Figue对象
        self.__curAxes = None  # 当前操作的Axes，为了方便单独用变量
        # self.__createFigure()  # 创建Figure和FigureCanvas对象，初始化界面
        # self.__drawFig2X1()  # 绘图

        ##  ==============自定义功能函数========================

    # @pyqtSlot(int)
    # def on_tabWidget_currentChanged(self, index):  ##tabWidget当前页面变化
    #     print(self.ui.tabWidget.widget(index))


    @pyqtSlot(int)
    def on_tabWidget_tabCloseRequested(self, index):  ##分页关闭时关闭窗体
        print("tabclose")
        if (index < 0):
            return
        aForm = self.ui.tabWidget.widget(index)
        aForm.close()

    ##树组件响应画图
    @pyqtSlot()
    def on_treeWidget_clicked(self):
        try:
            itemParent = self.ui.treeWidget.currentItem().parent()
            item = self.ui.treeWidget.currentItem()

            if itemParent.text(0) == "沉积相":

                title = itemParent.text(0) + ":" + item.text(0)
                fig = QmyFigure(self)
                fig.setAttribute(Qt.WA_DeleteOnClose)
                curIndex = self.ui.tabWidget.addTab(fig, title)  # 添加到tabWidget
                self.ui.tabWidget.setCurrentIndex(curIndex)

                x = CJX[item.text(0)][0]  # float 型
                y = CJX[item.text(0)][1]
                v = CJX[item.text(0)][2]

                for i in range(len(v)):
                    if v[i] == -999:
                        v[i] = 0

                x = np.array(x)
                y = np.array(y)
                v = np.array(v)

                x = x.T
                y = y.T
                v = v.T

                xq = list(range(int(min(x)), int(max(x)), self.stepx))
                yq = list(range(int(min(y)), int(max(y)), self.stepy))

                xq = np.array(xq)
                yq = np.array(yq)

                xq, yq = np.meshgrid(xq, yq)

                vq1 = griddata((x, y), v, (xq, yq), method="linear")
                vq = griddata((x, y), v, (xq, yq), method="nearest")


                for i in range(vq1.shape[0]):
                    for j in range(vq1.shape[1]):
                        if (np.isnan(vq1[i][j]) == True):
                            vq[i][j] = vq1[i][j]


                ax1 = fig.fig.add_subplot(1, 1, 1, label=title)  # 子图1

                ax1.set_xlabel('X 轴')  # X轴标题
                ax1.set_ylabel('Y 轴')  # Y轴标题
                ax1.set_title(title)



                colors = ["white", "red", "orange","yellow", "green"]
                clrmap = mpl.colors.LinearSegmentedColormap.from_list("mycmap", colors)

                im = ax1.pcolormesh(xq, yq, vq, cmap=clrmap)

                fig.fig.colorbar(im)

                # ax1.plot(t, y1, 'r-o', label="sin", linewidth=2, markersize=5)  # 绘制一条曲线
                # ax1.plot(t, y2, 'b--', label="cos", linewidth=2)  # 绘制一条曲线
                # ax1.set_xlabel('X 轴')  # X轴标题
                # ax1.set_ylabel('Y 轴')  # Y轴标题
                # ax1.set_xlim([0, 10])  # X轴坐标范围
                # ax1.set_ylim([-1.5, 1.5])  # Y轴坐标范围
                # ax1.set_title("三角函数曲线")
                # ax1.legend()  # 自动创建图例
                fig.fig.canvas.draw()  ##刷新

                print(item.text(0))

            elif itemParent.text(0) == "孔隙度":

                title = itemParent.text(0) + ":" + item.text(0)
                fig = QmyFigure(self)
                fig.setAttribute(Qt.WA_DeleteOnClose)
                curIndex = self.ui.tabWidget.addTab(fig, title)  # 添加到tabWidget
                self.ui.tabWidget.setCurrentIndex(curIndex)

                x = KXD[item.text(0)][0]  # float 型
                y = KXD[item.text(0)][1]
                v = KXD[item.text(0)][2]

                for i in range(len(v)):
                    if v[i] == -999:
                        v[i] = 0

                x = np.array(x)
                y = np.array(y)
                v = np.array(v)

                x = x.T
                y = y.T
                v = v.T

                xq = list(range(int(min(x)), int(max(x)), self.stepx))
                yq = list(range(int(min(y)), int(max(y)), self.stepy))

                xq = np.array(xq)
                yq = np.array(yq)

                xq, yq = np.meshgrid(xq, yq)

                vq = griddata((x, y), v, (xq, yq), method="linear")

                # for i in range(vq.shape[0]):
                #     for j in range(vq.shape[1]):
                #         if np.isnan(vq[i][j]) == False:
                #             vq[i][j] = vq[i][j].astype(int)


                ax1 = fig.fig.add_subplot(1, 1, 1, label=title)  # 子图1
                ax1.set_xlabel('X 轴')  # X轴标题
                ax1.set_ylabel('Y 轴')  # Y轴标题
                ax1.set_title(title)

                im = ax1.pcolormesh(xq, yq, vq, )
                fig.fig.colorbar(im)

                fig.fig.canvas.draw()  #刷新
                print(item.text(0))


            elif itemParent.text(0) == "渗透率":

                title = itemParent.text(0) + ":" + item.text(0)
                fig = QmyFigure(self)
                fig.setAttribute(Qt.WA_DeleteOnClose)
                curIndex = self.ui.tabWidget.addTab(fig, title)  # 添加到tabWidget
                self.ui.tabWidget.setCurrentIndex(curIndex)

                x = STL[item.text(0)][0]  # float 型
                y = STL[item.text(0)][1]
                v = STL[item.text(0)][2]

                for i in range(len(v)):
                    if v[i] == -999:
                        v[i] = 0

                x = np.array(x)
                y = np.array(y)
                v = np.array(v)

                x = x.T
                y = y.T
                v = v.T

                xq = list(range(int(min(x)), int(max(x)), self.stepx))
                yq = list(range(int(min(y)), int(max(y)), self.stepy))

                xq = np.array(xq)
                yq = np.array(yq)

                xq, yq = np.meshgrid(xq, yq)

                vq = griddata((x, y), v, (xq, yq), method="linear")

                for i in range(vq.shape[0]):
                    for j in range(vq.shape[1]):
                        if np.isnan(vq[i][j]) == False:
                            vq[i][j] = vq[i][j].astype(int)

                ax1 = fig.fig.add_subplot(1, 1, 1, label=title)  # 子图1
                ax1.set_xlabel('X 轴')  # X轴标题
                ax1.set_ylabel('Y 轴')  # Y轴标题
                ax1.set_title(title)

                im = ax1.pcolormesh(xq, yq, vq, )
                fig.fig.colorbar(im)

                fig.fig.canvas.draw()  ##刷新
                print(item.text(0))


            elif itemParent.text(0) == "含油饱和度":

                title = itemParent.text(0) + ":" + item.text(0)
                fig = QmyFigure(self)
                fig.setAttribute(Qt.WA_DeleteOnClose)
                curIndex = self.ui.tabWidget.addTab(fig, title)  # 添加到tabWidget
                self.ui.tabWidget.setCurrentIndex(curIndex)

                x = BHD[item.text(0)][0]  # float 型
                y = BHD[item.text(0)][1]
                v = BHD[item.text(0)][2]

                for i in range(len(v)):
                    if v[i] == -999:
                        v[i] = 0

                x = np.array(x)
                y = np.array(y)
                v = np.array(v)

                x = x.T
                y = y.T
                v = v.T

                print(self.stepx)
                print(self.stepy)

                xq = list(range(int(min(x)), int(max(x)), self.stepx))
                yq = list(range(int(min(y)), int(max(y)), self.stepy))

                xq = np.array(xq)
                yq = np.array(yq)

                xq, yq = np.meshgrid(xq, yq)

                vq = griddata((x, y), v, (xq, yq), method="linear")

                # for i in range(vq.shape[0]):
                #     for j in range(vq.shape[1]):
                #         if np.isnan(vq[i][j]) == False:
                #             vq[i][j] = vq[i][j].astype(int)

                ax1 = fig.fig.add_subplot(1, 1, 1, label=title)  # 子图1
                ax1.set_xlabel('X 轴')  # X轴标题
                ax1.set_ylabel('Y 轴')  # Y轴标题
                ax1.set_title(title)

                im = ax1.pcolormesh(xq, yq, vq, )
                fig.fig.colorbar(im)

                fig.fig.canvas.draw()  ##刷新
                print(item.text(0))

            elif itemParent.text(0) == "沉积单元数据":

                title = itemParent.text(0) + ":" + item.text(0)
                fig1 = QmyFigure(self)
                fig1.setAttribute(Qt.WA_DeleteOnClose)
                curIndex = self.ui.tabWidget.addTab(fig1, title)  # 添加到tabWidget
                self.ui.tabWidget.setCurrentIndex(curIndex)

                floor = CJDYSJ[item.text(0)]  # float 型
                floor = np.array(floor)
                floor = floor.T
                floor = floor.tolist()
                wellNum = floor[2]
                x = []
                y = []



                bj1 = 1
                bj2 = 1
                yxhd = []
                yxhd1 = float(floor[13][0])
                kxd = []
                kxd1 = float(floor[14][0])
                stl = []
                stl1 = float(floor[15][0])

                for i in range(1,len(floor[0])-1):
                    print(i)
                    if floor[2][i] == floor[2][i-1]:

                        yxhd1 = yxhd1 + float(floor[13][i])
                        if float(floor[14][i]) == 0:
                            kxd1 = kxd1 + float(floor[14][i])
                        else:
                            bj1 = bj1 + 1
                            kxd1 = kxd1 + float(floor[14][i])

                        if float(floor[15][i]) == 0:
                            stl1 = stl1 + float(floor[15][i])
                        else:
                            bj2 = bj2 + 1
                            stl1 = stl1 + float(floor[15][i])
                    else:
                        for j in range(len(DJDZSJ)):
                            if floor[2][i-1] == list(DJDZSJ.keys())[j]:
                                if DJDZSJ[list(DJDZSJ.keys())[j]][2] == '0':
                                    y.append(DJDZSJ[list(DJDZSJ.keys())[j]][0])
                                    x.append(DJDZSJ[list(DJDZSJ.keys())[j]][1])
                                else:
                                    y.append(DJDZSJ[list(DJDZSJ.keys())[j]][2])
                                    x.append(DJDZSJ[list(DJDZSJ.keys())[j]][3])
                                yxhd.append(str(yxhd1))
                                kxd.append(str(kxd1/bj1))
                                stl.append(str(stl1/bj2))

                        bj1 = 1
                        bj2 = 1
                        yxhd1 = float(floor[13][i])
                        kxd1 = float(floor[14][i])
                        stl1 = float(floor[15][i])

                print(floor[13])
                print(yxhd)

                x = np.array(x)
                y = np.array(y)
                yxhd = np.array(yxhd)
                kxd = np.array(kxd)
                stl = np.array(stl)

                x = x.T
                y = y.T
                yxhd = yxhd.T
                kxd = kxd.T
                stl = stl.T

                print(int(min(x)))
                print(int(max(x)))
                print(int(min(y)))
                print(int(max(y)))

                xq = list(range(int(min(x)), int(max(x)), self.stepx))
                yq = list(range(int(min(y)), int(max(y)), self.stepy))

                xq = np.array(xq)
                yq = np.array(yq)

                xq, yq = np.meshgrid(xq, yq)

                yxhdq = griddata((x, y), yxhd, (xq, yq), method="linear")
                kxdq = griddata((x, y), kxd, (xq, yq), method="linear")
                stlq = griddata((x, y), stl, (xq, yq), method="linear")

                # # for i in range(vq.shape[0]):
                # #     for j in range(vq.shape[1]):
                # #         if np.isnan(vq[i][j]) == False:
                # #             vq[i][j] = vq[i][j].astype(int)

                ax1 = fig1.fig.add_subplot(1, 1, 1, label="sin-cos plot")  # 子图1
                ax1.set_xlabel('X 轴')  # X轴标题
                ax1.set_ylabel('Y 轴')  # Y轴标题
                ax1.set_title(title+"有效厚度展示")

                title = itemParent.text(0) + ":" + item.text(0)
                fig2 = QmyFigure(self)
                fig2.setAttribute(Qt.WA_DeleteOnClose)
                curIndex = self.ui.tabWidget.addTab(fig2, title)  # 添加到tabWidget
                self.ui.tabWidget.setCurrentIndex(curIndex)

                ax2 = fig2.fig.add_subplot(1, 1, 1, label="sin-cos plot")  # 子图2
                ax2.set_xlabel('X 轴')  # X轴标题
                ax2.set_ylabel('Y 轴')  # Y轴标题
                ax2.set_title(title+"孔隙度展示")

                title = itemParent.text(0) + ":" + item.text(0)
                fig3 = QmyFigure(self)
                fig3.setAttribute(Qt.WA_DeleteOnClose)
                curIndex = self.ui.tabWidget.addTab(fig3, title)  # 添加到tabWidget
                self.ui.tabWidget.setCurrentIndex(curIndex)

                ax3 = fig3.fig.add_subplot(1, 1, 1, label="sin-cos plot")  # 子图3
                ax3.set_xlabel('X 轴')  # X轴标题
                ax3.set_ylabel('Y 轴')  # Y轴标题
                ax3.set_title(title+"渗透率展示")

                im1 = ax1.pcolormesh(xq, yq, yxhdq)
                fig1.fig.colorbar(im1, ax=ax1)

                im2 = ax2.pcolormesh(xq, yq, kxdq)
                fig2.fig.colorbar(im2, ax=ax2)

                im3 = ax3.pcolormesh(xq, yq, stlq)
                fig3.fig.colorbar(im3, ax=ax3)

                fig1.fig.canvas.draw()  ##刷新

                fig2.fig.canvas.draw()  ##刷新

                fig3.fig.canvas.draw()  ##刷新
                print(item.text(0))

            elif itemParent.text(0) == "注水井史":

                self.zsjstitle = itemParent.text(0) + ":" + item.text(0)

                self.zsjswellnum = item.text(0)

                fig1 = QmyFigure(self)
                fig1.setAttribute(Qt.WA_DeleteOnClose)
                curIndex = self.ui.tabWidget.addTab(fig1, self.zsjstitle)  # 添加到tabWidget
                self.ui.tabWidget.setCurrentIndex(curIndex)

                data = [list(i) for i in zip(*ZSJS[self.zsjswellnum])]

                x = []
                for i in range(len(data[2])):
                    xT1 = datetime.datetime.strptime(data[2][i], "%Y%m").strftime("%Y-%m-%d")
                    xT = mdates.datestr2num(xT1)
                    x.append(xT)

                y = []
                for i in range(len(data[8])):
                    if data[8][i] != '':
                        y.append(float(data[8][i]))
                    else:
                        y.append(0)

                ax = fig1.fig.add_subplot(1, 1, 1, label="sin-cos plot")
                ax.set_xlabel('日期')  # X轴标题
                ax.set_ylabel('油压，MPa')  # Y轴标题
                ax.set_title(self.zsjswellnum + "油压")
                ax.plot(x, y)
                ax.xaxis_date()

                self.ui.comboBox_6.clear()
                self.ui.comboBox_6.addItem("绘制曲线")
                self.ui.comboBox_6.addItem("油压")
                self.ui.comboBox_6.addItem("日注水量")
                self.ui.comboBox_6.addItem("累注水量")


            elif itemParent.text(0) == "采油井史":

                self.cyjstitle = itemParent.text(0) + ":" + item.text(0)

                self.cyjswellnum = item.text(0)

                fig1 = QmyFigure(self)
                fig1.setAttribute(Qt.WA_DeleteOnClose)
                curIndex = self.ui.tabWidget.addTab(fig1, self.cyjstitle)  # 添加到tabWidget
                self.ui.tabWidget.setCurrentIndex(curIndex)

                data = [list(i) for i in zip(*CYJS[self.cyjswellnum])]

                x = []
                for i in range(len(data[2])):
                    xT1 = datetime.datetime.strptime(data[2][i], "%Y%m").strftime("%Y-%m-%d")
                    xT = mdates.datestr2num(xT1)
                    x.append(xT)

                y = []
                for i in range(len(data[13])):
                    if data[13][i] != '':
                        y.append(float(data[13][i]))
                    else:
                        y.append(0)


                ax = fig1.fig.add_subplot(1, 1, 1, label="sin-cos plot")
                ax.set_xlabel('日期')  # X轴标题
                ax.set_ylabel('流压，MPa')  # Y轴标题
                ax.set_title(self.cyjswellnum + "流压")
                ax.plot(x, y)
                ax.xaxis_date()

                self.ui.comboBox_6.clear()
                self.ui.comboBox_6.addItem("绘制曲线")
                self.ui.comboBox_6.addItem("流压")
                self.ui.comboBox_6.addItem("日产油量")
                self.ui.comboBox_6.addItem("日产水量")
                self.ui.comboBox_6.addItem("日产液量")
                self.ui.comboBox_6.addItem("含水")
                self.ui.comboBox_6.addItem("累产油量")
                self.ui.comboBox_6.addItem("累产水量")
                self.ui.comboBox_6.addItem("累产液量")

            elif itemParent.text(0) == "相渗曲线":

                if item.text(0) == "油水相渗":
                    self.xsqxtitle = item.text(0)

                    fig1 = QmyFigure(self)
                    fig1.setAttribute(Qt.WA_DeleteOnClose)
                    curIndex = self.ui.tabWidget.addTab(fig1, self.xsqxtitle)  # 添加到tabWidget
                    self.ui.tabWidget.setCurrentIndex(curIndex)

                    data = [list(i) for i in zip(*XSQX)]

                    x = []
                    y1 = []
                    y2 = []

                    for i in range(1,len(data[0])):
                        if data[0][i] != '':
                            x.append(float(data[0][i]))

                        if data[1][i] != '':
                            y1.append(float(data[1][i]))

                        if data[2][i] != '':
                            y2.append(float(data[2][i]))

                    print(x)
                    print(y1)
                    print(y2)

                    ax = fig1.fig.add_subplot(1, 1, 1, label="sin-cos plot")
                    ax.set_xlabel('含水饱和度')  # X轴标题
                    ax.set_ylabel('相对渗透率')  # Y轴标题
                    ax.plot(x, y1)
                    ax.plot(x, y2)

                elif item.text(0) == "油气相渗":
                    self.xsqxtitle = item.text(0)

                    fig1 = QmyFigure(self)
                    fig1.setAttribute(Qt.WA_DeleteOnClose)
                    curIndex = self.ui.tabWidget.addTab(fig1, self.xsqxtitle)  # 添加到tabWidget
                    self.ui.tabWidget.setCurrentIndex(curIndex)

                    data = [list(i) for i in zip(*XSQX)]
                    print(data)

                    x = []
                    y1 = []
                    y2 = []
                    for i in range(1,len(data[4])):
                        if data[4][i] != '':
                            x.append(float(data[4][i]))

                        if data[5][i] != '':
                            y1.append(float(data[5][i]))

                        if data[6][i] != '':
                            y2.append(float(data[6][i]))

                    print(x)
                    print(y1)
                    print(y2)

                    ax = fig1.fig.add_subplot(1, 1, 1, label="sin-cos plot")
                    ax.set_xlabel('含油饱和度')  # X轴标题
                    ax.set_ylabel('相对渗透率')  # Y轴标题
                    ax.plot(x, y1)
                    ax.plot(x, y2)

            elif itemParent.text(0) == "吸水剖面数据":
                title = itemParent.text(0) + ":" + item.text(0)
                fig = QmyFigure(self)
                fig.setAttribute(Qt.WA_DeleteOnClose)
                curIndex = self.ui.tabWidget.addTab(fig, title)  # 添加到tabWidget
                self.ui.tabWidget.setCurrentIndex(curIndex)

                data = XSPMSJ[item.text(0)]

                dates = data.keys()


                for i ,date in enumerate(dates):

                    oneDayXSPMSJ = [list(i) for i in zip(*data[date])]
                    if i == 0:
                        xsmin = float(min(oneDayXSPMSJ[9]))
                        xsmax = float(max(oneDayXSPMSJ[9]))
                        if float(min(oneDayXSPMSJ[10])) < xsmin:
                            xsmin = float(min(oneDayXSPMSJ[10]))
                        if float(max(oneDayXSPMSJ[10])) > xsmax:
                            xsmax = float(max(oneDayXSPMSJ[10]))
                    else:
                        if float(min(oneDayXSPMSJ[9])) < xsmin:
                            xsmin = float(min(oneDayXSPMSJ[9]))
                        if float(max(oneDayXSPMSJ[9])) > xsmax:
                            xsmax = float(max(oneDayXSPMSJ[9]))
                        if float(min(oneDayXSPMSJ[10])) < xsmin:
                            xsmin = float(min(oneDayXSPMSJ[10]))
                        if float(max(oneDayXSPMSJ[10])) > xsmax:
                            xsmax = float(max(oneDayXSPMSJ[10]))

                for i, date in enumerate(dates):

                    oneDayXSPMSJ = [list(i) for i in zip(*data[date])]

                    x = []
                    x1 = []
                    d = []
                    y = []
                    for j in range(len(oneDayXSPMSJ[9])):
                        x.append(float(oneDayXSPMSJ[9][j]))
                        x1.append(float(oneDayXSPMSJ[10][j]))
                        y.append(float(oneDayXSPMSJ[20][j]))
                        d.append(float(oneDayXSPMSJ[10][j]) - float(oneDayXSPMSJ[9][j]))
                    print(x)
                    print(y)
                    print(d)

                    ax1 = fig.fig.add_subplot(len(dates), 1, i + 1, label=date)  # 子图1
                    ax1.set_ylabel('吸水比例')  # Y轴标题
                    ax1.set_title(date)
                    ax1.bar(x, y, d, align='edge')
                    ax1.set_xlim(xsmin-3,xsmax+3)

                    if i != len(dates) - 1:
                        ax1.get_xaxis().set_visible(False)




                # data = [list(i) for i in zip(*XSPMSJ[item.text(0)])]



                # x = STL[item.text(0)][0]  # float 型
                # y = STL[item.text(0)][1]
                # v = STL[item.text(0)][2]
                #
                # for i in range(len(v)):
                #     if v[i] == -999:
                #         v[i] = 0
                #
                # x = np.array(x)
                # y = np.array(y)
                # v = np.array(v)
                #
                # x = x.T
                # y = y.T
                # v = v.T
                #
                # xq = list(range(int(min(x)), int(max(x)), self.stepx))
                # yq = list(range(int(min(y)), int(max(y)), self.stepy))
                #
                # xq = np.array(xq)
                # yq = np.array(yq)
                #
                # xq, yq = np.meshgrid(xq, yq)
                #
                # vq = griddata((x, y), v, (xq, yq), method="linear")
                #
                # for i in range(vq.shape[0]):
                #     for j in range(vq.shape[1]):
                #         if np.isnan(vq[i][j]) == False:
                #             vq[i][j] = vq[i][j].astype(int)



                # im = ax1.pcolormesh(xq, yq, vq, )
                # fig.fig.colorbar(im)

                # fig.fig.canvas.draw()  ##刷新
                # print(item.text(0))



        except AttributeError:
            print("AttributeError")

    @pyqtSlot(str)  #注水井史展示下拉列表变化时运行得函数
    def on_comboBox_6_activated(self, curText):


        if curText == "油压":

            fig1 = QmyFigure(self)
            fig1.setAttribute(Qt.WA_DeleteOnClose)
            curIndex = self.ui.tabWidget.addTab(fig1, self.zsjstitle)  # 添加到tabWidget
            self.ui.tabWidget.setCurrentIndex(curIndex)

            data = [list(i) for i in zip(*ZSJS[self.zsjswellnum])]

            x = []
            for i in range(len(data[2])):
                xT1 = datetime.datetime.strptime(data[2][i],"%Y%m").strftime("%Y-%m-%d")
                xT = mdates.datestr2num(xT1)
                x.append(xT)

            y = []
            for i in range(len(data[8])):
                if data[8][i] != '':
                    y.append(float(data[8][i]))
                else:
                    y.append(0)

            ax = fig1.fig.add_subplot(1, 1, 1, label="sin-cos plot")
            ax.set_xlabel('日期')  # X轴标题
            ax.set_ylabel('油压，MPa')  # Y轴标题
            ax.set_title(self.zsjswellnum + "油压")
            ax.plot(x, y)
            ax.xaxis_date()

        elif curText == "日注水量":

            fig1 = QmyFigure(self)
            fig1.setAttribute(Qt.WA_DeleteOnClose)
            curIndex = self.ui.tabWidget.addTab(fig1, self.zsjstitle)  # 添加到tabWidget
            self.ui.tabWidget.setCurrentIndex(curIndex)

            data = [list(i) for i in zip(*ZSJS[self.zsjswellnum])]

            x = []
            for i in range(len(data[2])):
                xT1 = datetime.datetime.strptime(data[2][i],"%Y%m").strftime("%Y-%m-%d")
                xT = mdates.datestr2num(xT1)
                x.append(xT)

            y = []
            for i in range(len(data[6])):
                if data[6][i] != '':
                    y.append(float(data[6][i]))
                else:
                    y.append(0)

            ax = fig1.fig.add_subplot(1, 1, 1, label="sin-cos plot")
            ax.set_xlabel('日期')  # X轴标题
            ax.set_ylabel('日注水量，m3/d')  # Y轴标题
            ax.set_title(self.zsjswellnum + "日注水量")
            ax.plot(x, y)
            ax.xaxis_date()

        elif curText == "累注水量":

            fig1 = QmyFigure(self)
            fig1.setAttribute(Qt.WA_DeleteOnClose)
            curIndex = self.ui.tabWidget.addTab(fig1, self.zsjstitle)  # 添加到tabWidget
            self.ui.tabWidget.setCurrentIndex(curIndex)

            data = [list(i) for i in zip(*ZSJS[self.zsjswellnum])]

            x = []
            for i in range(len(data[2])):
                xT1 = datetime.datetime.strptime(data[2][i], "%Y%m").strftime("%Y-%m-%d")
                xT = mdates.datestr2num(xT1)
                x.append(xT)

            y = []
            for i in range(len(data[14])):
                if data[14][i] != '':
                    y.append(float(data[14][i])*10000)
                else:
                    y.append(0)

            ax = fig1.fig.add_subplot(1, 1, 1, label="sin-cos plot")
            ax.set_xlabel('日期')  # X轴标题
            ax.set_ylabel('累注水量，m3/d')  # Y轴标题
            ax.set_title(self.zsjswellnum + "累注水量")
            ax.plot(x, y)
            ax.xaxis_date()

        elif curText == "流压":

            fig1 = QmyFigure(self)
            fig1.setAttribute(Qt.WA_DeleteOnClose)
            curIndex = self.ui.tabWidget.addTab(fig1, self.cyjstitle)  # 添加到tabWidget
            self.ui.tabWidget.setCurrentIndex(curIndex)

            data = [list(i) for i in zip(*CYJS[self.cyjswellnum])]

            x = []
            for i in range(len(data[2])):
                xT1 = datetime.datetime.strptime(data[2][i], "%Y%m").strftime("%Y-%m-%d")
                xT = mdates.datestr2num(xT1)
                x.append(xT)

            y = []
            for i in range(len(data[13])):
                if data[13][i] != '':
                    y.append(float(data[13][i]))
                else:
                    y.append(0)

            ax = fig1.fig.add_subplot(1, 1, 1, label="sin-cos plot")
            ax.set_xlabel('日期')  # X轴标题
            ax.set_ylabel('流压，MPa')  # Y轴标题
            ax.set_title(self.cyjswellnum + "流压")
            ax.plot(x, y)
            ax.xaxis_date()

        elif curText == "日产油量":

            fig1 = QmyFigure(self)
            fig1.setAttribute(Qt.WA_DeleteOnClose)
            curIndex = self.ui.tabWidget.addTab(fig1, self.cyjstitle)  # 添加到tabWidget
            self.ui.tabWidget.setCurrentIndex(curIndex)

            data = [list(i) for i in zip(*CYJS[self.cyjswellnum])]

            x = []
            for i in range(len(data[2])):
                xT1 = datetime.datetime.strptime(data[2][i], "%Y%m").strftime("%Y-%m-%d")
                xT = mdates.datestr2num(xT1)
                x.append(xT)

            y = []
            for i in range(len(data[17])):
                if data[17][i] != '':
                    y.append(float(data[17][i]))
                else:
                    y.append(0)

            ax = fig1.fig.add_subplot(1, 1, 1, label="sin-cos plot")
            ax.set_xlabel('日期')  # X轴标题
            ax.set_ylabel('日产油量，m3/d')  # Y轴标题
            ax.set_title(self.cyjswellnum + "日产油量")
            ax.plot(x, y)
            ax.xaxis_date()

        elif curText == "日产水量":

            fig1 = QmyFigure(self)
            fig1.setAttribute(Qt.WA_DeleteOnClose)
            curIndex = self.ui.tabWidget.addTab(fig1, self.cyjstitle)  # 添加到tabWidget
            self.ui.tabWidget.setCurrentIndex(curIndex)

            data = [list(i) for i in zip(*CYJS[self.cyjswellnum])]

            x = []
            for i in range(len(data[2])):
                xT1 = datetime.datetime.strptime(data[2][i], "%Y%m").strftime("%Y-%m-%d")
                xT = mdates.datestr2num(xT1)
                x.append(xT)

            y = []
            for i in range(len(data[18])):
                if data[18][i] != '':
                    y.append(float(data[18][i]))
                else:
                    y.append(0)

            ax = fig1.fig.add_subplot(1, 1, 1, label="sin-cos plot")
            ax.set_xlabel('日期')  # X轴标题
            ax.set_ylabel('日产水量，m3/d')  # Y轴标题
            ax.set_title(self.cyjswellnum + "日产水量")
            ax.plot(x, y)
            ax.xaxis_date()

        elif curText == "日产液量":

            fig1 = QmyFigure(self)
            fig1.setAttribute(Qt.WA_DeleteOnClose)
            curIndex = self.ui.tabWidget.addTab(fig1, self.cyjstitle)  # 添加到tabWidget
            self.ui.tabWidget.setCurrentIndex(curIndex)

            data = [list(i) for i in zip(*CYJS[self.cyjswellnum])]

            x = []
            for i in range(len(data[2])):
                xT1 = datetime.datetime.strptime(data[2][i], "%Y%m").strftime("%Y-%m-%d")
                xT = mdates.datestr2num(xT1)
                x.append(xT)

            y = []
            for i in range(len(data[17])):
                if data[17][i] != '' and data[18][i] != '':
                    y.append(float(data[17][i]) + float(data[18][i]))
                elif data[17][i] == '' and data[18][i] != '':
                    y.append(float(data[18][i]))
                elif data[17][i] != '' and data[18][i] == '':
                    y.append(float(data[17][i]))
                elif data[17][i] == '' and data[18][i] == '':
                    y.append(0)

            ax = fig1.fig.add_subplot(1, 1, 1, label="sin-cos plot")
            ax.set_xlabel('日期')  # X轴标题
            ax.set_ylabel('日产液量，m3/d')  # Y轴标题
            ax.set_title(self.cyjswellnum + "日产液量")
            ax.plot(x, y)
            ax.xaxis_date()

        elif curText == "含水":

            fig1 = QmyFigure(self)
            fig1.setAttribute(Qt.WA_DeleteOnClose)
            curIndex = self.ui.tabWidget.addTab(fig1, self.cyjstitle)  # 添加到tabWidget
            self.ui.tabWidget.setCurrentIndex(curIndex)

            data = [list(i) for i in zip(*CYJS[self.cyjswellnum])]

            x = []
            for i in range(len(data[2])):
                xT1 = datetime.datetime.strptime(data[2][i], "%Y%m").strftime("%Y-%m-%d")
                xT = mdates.datestr2num(xT1)
                x.append(xT)

            y = []
            for i in range(len(data[19])):
                if data[19][i] != '':
                    y.append(float(data[19][i]))
                else:
                    y.append(0)

            ax = fig1.fig.add_subplot(1, 1, 1, label="sin-cos plot")
            ax.set_xlabel('日期')  # X轴标题
            ax.set_ylabel('含水')  # Y轴标题
            ax.set_title(self.cyjswellnum + "含水")
            ax.plot(x, y)
            ax.xaxis_date()

        elif curText == "累产油量":

            fig1 = QmyFigure(self)
            fig1.setAttribute(Qt.WA_DeleteOnClose)
            curIndex = self.ui.tabWidget.addTab(fig1, self.cyjstitle)  # 添加到tabWidget
            self.ui.tabWidget.setCurrentIndex(curIndex)

            data = [list(i) for i in zip(*CYJS[self.cyjswellnum])]

            x = []
            for i in range(len(data[2])):
                xT1 = datetime.datetime.strptime(data[2][i], "%Y%m").strftime("%Y-%m-%d")
                xT = mdates.datestr2num(xT1)
                x.append(xT)

            y = []
            for i in range(len(data[26])):
                if data[26][i] != '':
                    y.append(float(data[26][i])*10000)
                else:
                    y.append(0)

            ax = fig1.fig.add_subplot(1, 1, 1, label="sin-cos plot")
            ax.set_xlabel('日期')  # X轴标题
            ax.set_ylabel('累产油量，m3/d')  # Y轴标题
            ax.set_title(self.cyjswellnum + "累产油量")
            ax.plot(x, y)
            ax.xaxis_date()

        elif curText == "累产水量":

            fig1 = QmyFigure(self)
            fig1.setAttribute(Qt.WA_DeleteOnClose)
            curIndex = self.ui.tabWidget.addTab(fig1, self.cyjstitle)  # 添加到tabWidget
            self.ui.tabWidget.setCurrentIndex(curIndex)

            data = [list(i) for i in zip(*CYJS[self.cyjswellnum])]

            x = []
            for i in range(len(data[2])):
                xT1 = datetime.datetime.strptime(data[2][i], "%Y%m").strftime("%Y-%m-%d")
                xT = mdates.datestr2num(xT1)
                x.append(xT)

            y = []
            for i in range(len(data[27])):
                if data[27][i] != '':
                    y.append(float(data[27][i])*10000)
                else:
                    y.append(0)

            ax = fig1.fig.add_subplot(1, 1, 1, label="sin-cos plot")
            ax.set_xlabel('日期')  # X轴标题
            ax.set_ylabel('累产水量，m3/d')  # Y轴标题
            ax.set_title(self.cyjswellnum + "累产水量")
            ax.plot(x, y)
            ax.xaxis_date()

        elif curText == "累产液量":

            fig1 = QmyFigure(self)
            fig1.setAttribute(Qt.WA_DeleteOnClose)
            curIndex = self.ui.tabWidget.addTab(fig1, self.cyjstitle)  # 添加到tabWidget
            self.ui.tabWidget.setCurrentIndex(curIndex)

            data = [list(i) for i in zip(*CYJS[self.cyjswellnum])]

            x = []
            for i in range(len(data[2])):
                xT1 = datetime.datetime.strptime(data[2][i], "%Y%m").strftime("%Y-%m-%d")
                xT = mdates.datestr2num(xT1)
                x.append(xT)

            y = []
            for i in range(len(data[26])):
                if data[26][i] != '' and data[27][i] != '':
                    y.append((float(data[26][i]) + float(data[27][i]))*10000)
                elif data[26][i] == '' and data[27][i] != '':
                    y.append(float(data[27][i])*10000)
                elif data[26][i] != '' and data[27][i] == '':
                    y.append(float(data[26][i])*10000)
                elif data[26][i] == '' and data[27][i] == '':
                    y.append(0)

            ax = fig1.fig.add_subplot(1, 1, 1, label="sin-cos plot")
            ax.set_xlabel('日期')  # X轴标题
            ax.set_ylabel('累产液量，m3/d')  # Y轴标题
            ax.set_title(self.cyjswellnum + "累产液量")
            ax.plot(x, y)
            ax.xaxis_date()


    ##导入沉积相数据
    @pyqtSlot()
    def on_actiongfd_triggered(self):

        print("test")
        curDir = QDir.currentPath()
        aDir = QFileDialog.getExistingDirectory(self, "选择一个目录",
                                                curDir, QFileDialog.ShowDirsOnly)
        dirObj = QDir(aDir)
        strList = dirObj.entryList(QDir.Files)

        labText = "正在导入文件..."  # 文本信息
        btnText = "取消"  # "取消"按钮的标题
        minV = 0
        maxV = len(strList)

        dlgProgress = QProgressDialog(labText, btnText, minV, maxV, self)
        dlgProgress.setWindowTitle("导入文件")
        dlgProgress.setWindowModality(Qt.WindowModal)  # 模态对话框
        dlgProgress.setAutoReset(True)  # value()达到最大值时自动调用reset()
        dlgProgress.setAutoClose(True)  # 调用reset()时隐藏窗口
        i = 1
        for str in strList:
            # self.progressBar.setValue(i)
            dlgProgress.setValue(i)
            dlgProgress.setLabelText("正在导入文件,第 %d 个" % i)

            floor = []
            x = []
            y = []
            phase = []  ##相
            fileName = re.findall(".*\.txt", str)
            if fileName != []:
                # print(fileName[0][0:-4])
                filePath = aDir + "/" + fileName[0]
                # print(filePath)
                fileDevice = QFile(filePath)
                fileDevice.open(QIODevice.ReadOnly | QIODevice.Text)
                try:
                    fileStream = QTextStream(fileDevice)
                    fileStream.setAutoDetectUnicode(True)  # 自动检测Unicode
                    fileStream.setCodec("GBK")  # 必须设置编码，否则不能正常显示汉字
                    while not fileStream.atEnd():
                        lineStr = fileStream.readLine()  # 返回QByteArray类型
                        # print(lineStr)

                        lineList = lineStr.split(" ")
                        x.append(float(lineList[0]))
                        y.append(float(lineList[1]))
                        phase.append(float(lineList[2]))



                except UnicodeDecodeError:
                    print(fileName[0] + "文件编码格式有误！")


                finally:
                    fileDevice.close()

                floor.append(x)  # 将读取出的数据按列表形式存储
                floor.append(y)  # 将读取出的数据按列表形式存储
                floor.append(phase)  # 将读取出的数据按列表形式存储
                f = np.array(floor)
                print(f.shape)
                CJX[fileName[0][0:-4]] = floor  # 用文件名作为键值将不同文件的数据存储在字典中
                item = QTreeWidgetItem()
                item.setText(0, fileName[0][0:-4])
                item.setIcon(0, QtGui.QIcon('images/29.ico'))
                self.ui.treeWidget.topLevelItem(0).child(2).addChild(item)
            i = i + 1

        self.ui.treeWidget.topLevelItem(0).child(2).setExpanded(True)

        # print(self.CJX["S21"])

    @pyqtSlot()
    def on_actionBHD_triggered(self):
        # print("test")
        curDir = QDir.currentPath()
        aDir = QFileDialog.getExistingDirectory(self, "选择一个目录",
                                                curDir, QFileDialog.ShowDirsOnly)
        dirObj = QDir(aDir)
        strList = dirObj.entryList(QDir.Files)
        # print(strList)
        labText = "正在导入文件..."  # 文本信息
        btnText = "取消"  # "取消"按钮的标题
        minV = 0
        maxV = len(strList)
        dlgProgress = QProgressDialog(labText, btnText, minV, maxV, self)
        dlgProgress.setWindowTitle("导入文件")
        dlgProgress.setWindowModality(Qt.WindowModal)  # 模态对话框
        dlgProgress.setAutoReset(True)  # value()达到最大值时自动调用reset()
        dlgProgress.setAutoClose(True)  # 调用reset()时隐藏窗口
        i = 1
        for str in strList:
            dlgProgress.setValue(i)
            dlgProgress.setLabelText("正在复制文件,第 %d 个" % i)
            floor = []
            x = []
            y = []
            phase = []  ##相
            fileName = re.findall(".*\.txt", str)
            if fileName != []:
                # print(fileName[0][0:-4])
                filePath = aDir + "/" + fileName[0]

                self.ui.comboBox.addItem(fileName[0][0:-4])

                self.qlqFloor.append(fileName[0][0:-4])

                # print(filePath)
                fileDevice = QFile(filePath)
                fileDevice.open(QIODevice.ReadOnly | QIODevice.Text)
                try:
                    fileStream = QTextStream(fileDevice)
                    fileStream.setAutoDetectUnicode(True)  # 自动检测Unicode
                    fileStream.setCodec("GBK")  # 必须设置编码，否则不能正常显示汉字
                    while not fileStream.atEnd():
                        lineStr = fileStream.readLine()  # 返回QByteArray类型

                        lineList = lineStr.split("\t")
                        x.append(float(lineList[0]))
                        y.append(float(lineList[1]))
                        phase.append(float(lineList[2]))



                except UnicodeDecodeError:
                    print(fileName[0] + "文件编码格式有误！")


                finally:
                    fileDevice.close()

                floor.append(x)  # 将读取出的数据按列表形式存储
                floor.append(y)  # 将读取出的数据按列表形式存储
                floor.append(phase)  # 将读取出的数据按列表形式存储
                f = np.array(floor)
                print(f.shape)
                BHD[fileName[0][0:-4]] = floor  # 用文件名作为键值将不同文件的数据存储在字典中
                item = QTreeWidgetItem()
                item.setText(0, fileName[0][0:-4])
                item.setIcon(0, QtGui.QIcon('images/29.ico'))
                self.ui.treeWidget.topLevelItem(0).child(4).addChild(item)
            i = i + 1

        self.ui.treeWidget.topLevelItem(0).child(4).setExpanded(True)
        # print(self.CJX["S21"])

    @pyqtSlot()
    def on_actionKXD_triggered(self):
        # print("test")
        curDir = QDir.currentPath()
        aDir = QFileDialog.getExistingDirectory(self, "选择一个目录",
                                                curDir, QFileDialog.ShowDirsOnly)
        dirObj = QDir(aDir)
        strList = dirObj.entryList(QDir.Files)
        # print(strList)
        labText = "正在导入文件..."  # 文本信息
        btnText = "取消"  # "取消"按钮的标题
        minV = 0
        maxV = len(strList)
        dlgProgress = QProgressDialog(labText, btnText, minV, maxV, self)
        dlgProgress.setWindowTitle("导入文件")
        dlgProgress.setWindowModality(Qt.WindowModal)  # 模态对话框
        dlgProgress.setAutoReset(True)  # value()达到最大值时自动调用reset()
        dlgProgress.setAutoClose(True)  # 调用reset()时隐藏窗口
        i = 1
        for str in strList:

            dlgProgress.setValue(i)
            dlgProgress.setLabelText("正在复制文件,第 %d 个" % i)

            floor = []
            x = []
            y = []
            phase = []  ##相
            fileName = re.findall(".*\.txt", str)
            if fileName != []:
                # print(fileName[0][0:-4])
                filePath = aDir + "/" + fileName[0]
                # print(filePath)
                fileDevice = QFile(filePath)
                fileDevice.open(QIODevice.ReadOnly | QIODevice.Text)
                try:
                    fileStream = QTextStream(fileDevice)
                    fileStream.setAutoDetectUnicode(True)  # 自动检测Unicode
                    fileStream.setCodec("GBK")  # 必须设置编码，否则不能正常显示汉字
                    while not fileStream.atEnd():
                        lineStr = fileStream.readLine()  # 返回QByteArray类型

                        lineList = lineStr.split("\t")
                        x.append(float(lineList[0]))
                        y.append(float(lineList[1]))
                        phase.append(float(lineList[2]))



                except UnicodeDecodeError:
                    print(fileName[0] + "文件编码格式有误！")


                finally:
                    fileDevice.close()

                floor.append(x)  # 将读取出的数据按列表形式存储
                floor.append(y)  # 将读取出的数据按列表形式存储
                floor.append(phase)  # 将读取出的数据按列表形式存储
                f = np.array(floor)
                print(f.shape)
                KXD[fileName[0][0:-4]] = floor  # 用文件名作为键值将不同文件的数据存储在字典中
                item = QTreeWidgetItem()
                item.setText(0, fileName[0][0:-4])
                item.setIcon(0, QtGui.QIcon('images/29.ico'))
                self.ui.treeWidget.topLevelItem(0).child(0).addChild(item)
            i = i + 1

        self.ui.treeWidget.topLevelItem(0).child(0).setExpanded(True)
        # print(self.CJX["S21"])

    @pyqtSlot()
    def on_actionSTL_triggered(self):
        # print("test")
        curDir = QDir.currentPath()
        aDir = QFileDialog.getExistingDirectory(self, "选择一个目录",
                                                curDir, QFileDialog.ShowDirsOnly)
        dirObj = QDir(aDir)
        strList = dirObj.entryList(QDir.Files)
        # print(strList)

        labText = "正在导入文件..."  # 文本信息
        btnText = "取消"  # "取消"按钮的标题
        minV = 0
        maxV = len(strList)
        dlgProgress = QProgressDialog(labText, btnText, minV, maxV, self)
        dlgProgress.setWindowTitle("导入文件")
        dlgProgress.setWindowModality(Qt.WindowModal)  # 模态对话框
        dlgProgress.setAutoReset(True)  # value()达到最大值时自动调用reset()
        dlgProgress.setAutoClose(True)  # 调用reset()时隐藏窗口
        i = 1

        for str in strList:

            dlgProgress.setValue(i)
            dlgProgress.setLabelText("正在复制文件,第 %d 个" % i)

            floor = []
            x = []
            y = []
            phase = []  ##相
            fileName = re.findall(".*\.txt", str)
            if fileName != []:

                # print(fileName[0][0:-4])
                filePath = aDir + "/" + fileName[0]
                # print(filePath)
                fileDevice = QFile(filePath)
                fileDevice.open(QIODevice.ReadOnly | QIODevice.Text)
                try:
                    fileStream = QTextStream(fileDevice)
                    fileStream.setAutoDetectUnicode(True)  # 自动检测Unicode
                    fileStream.setCodec("GBK")  # 必须设置编码，否则不能正常显示汉字
                    while not fileStream.atEnd():
                        lineStr = fileStream.readLine()  # 返回QByteArray类型

                        lineList = lineStr.split("\t")
                        x.append(float(lineList[0]))
                        y.append(float(lineList[1]))
                        phase.append(float(lineList[2]))



                except UnicodeDecodeError:
                    print(fileName[0] + "文件编码格式有误！")


                finally:
                    fileDevice.close()

                floor.append(x)  # 将读取出的数据按列表形式存储
                floor.append(y)  # 将读取出的数据按列表形式存储
                floor.append(phase)  # 将读取出的数据按列表形式存储
                f = np.array(floor)
                print(f.shape)
                STL[fileName[0][0:-4]] = floor  # 用文件名作为键值将不同文件的数据存储在字典中
                item = QTreeWidgetItem()
                item.setText(0, fileName[0][0:-4])
                item.setIcon(0, QtGui.QIcon('images/29.ico'))
                self.ui.treeWidget.topLevelItem(0).child(1).addChild(item)
            i = i + 1

        self.ui.treeWidget.topLevelItem(0).child(1).setExpanded(True)
        # print(self.CJX["S21"])

    # 导入单井地质数据
    @pyqtSlot()
    def on_actiondjdzsj_triggered(self):

        curPath = QDir.currentPath()  # 获取系统当前目录
        title = "打开一个文件"
        filt = "文本文件(*.txt);;所有文件(*.*)"
        fileName, flt = QFileDialog.getOpenFileName(self, title, curPath, filt)

        if fileName != "":
            fileDevice = QFile(fileName)
            fileDevice.open(QIODevice.ReadOnly | QIODevice.Text)
            try:
                fileStream = QTextStream(fileDevice)
                fileStream.setAutoDetectUnicode(True)  # 自动检测Unicode
                fileStream.setCodec("GBK")  # 必须设置编码，否则不能正常显示汉字
                i = 1
                while not fileStream.atEnd():

                    lineStr = fileStream.readLine()  # 返回QByteArray类型
                    lineList = lineStr.split("\t")

                    if lineList[0] != str(i):
                        continue

                    DJDZSJ[lineList[1]] = lineList[2:]
                    item = QTreeWidgetItem()
                    item.setText(0, lineList[1])

                    self.ui.treeWidget.topLevelItem(1).child(4).addChild(item)
                    i = i + 1



            except UnicodeDecodeError:
                print(fileName[0] + "文件编码格式有误！")

            finally:
                fileDevice.close()

            # print(self.DJDZSJ[-1])

            item = QTreeWidgetItem()
            item.setText(0, "单井地质数据")
            item.setIcon(0, QtGui.QIcon('images/29.ico'))
            # self.ui.treeWidget.topLevelItem(1).child(4).addChild(item)
        self.ui.treeWidget.topLevelItem(1).child(4).setExpanded(True)

    @pyqtSlot()
    def on_actionxspmsj_triggered(self):
        curPath = QDir.currentPath()  # 获取系统当前目录
        title = "打开一个文件"
        filt = "文本文件(*.txt);;所有文件(*.*)"
        fileName, flt = QFileDialog.getOpenFileName(self, title, curPath, filt)

        if fileName != "":
            fileDevice = QFile(fileName)
            fileDevice.open(QIODevice.ReadOnly | QIODevice.Text)
            try:
                fileStream = QTextStream(fileDevice)
                fileStream.setAutoDetectUnicode(True)  # 自动检测Unicode
                fileStream.setCodec("GBK")  # 必须设置编码，否则不能正常显示汉字

                i = 0
                while not fileStream.atEnd():
                    i = i + 1
                    lineStr = fileStream.readLine()  # 返回QByteArray类型
                    lineList = lineStr.split("\t")

                    if i == 1:
                        continue

                    if lineList[1] in XSPMSJ:
                        if lineList[2] in XSPMSJ[lineList[1]]:
                            XSPMSJ[lineList[1]][lineList[2]].append(lineList)
                        else:
                            XSPMSJ[lineList[1]][lineList[2]] = []
                            XSPMSJ[lineList[1]][lineList[2]].append(lineList)

                    else:
                        XSPMSJ[lineList[1]] = {}
                        XSPMSJ[lineList[1]][lineList[2]] = []
                        XSPMSJ[lineList[1]][lineList[2]].append(lineList)

                        item = QTreeWidgetItem()
                        item.setText(0, lineList[1])
                        item.setIcon(0, QtGui.QIcon('images/29.ico'))
                        self.ui.treeWidget.topLevelItem(1).child(3).addChild(item)

            except UnicodeDecodeError:
                print(fileName[0] + "文件编码格式有误！")

            finally:
                fileDevice.close()

            # print(self.XSPMSJ[-1])

            # item = QTreeWidgetItem()
            # item.setText(0, "射孔数据")
            # item.setIcon(0, QtGui.QIcon('images/29.ico'))
            # self.ui.treeWidget.topLevelItem(1).child(2).addChild(item)
        self.ui.treeWidget.topLevelItem(1).child(3).setExpanded(True)

    @pyqtSlot()
    def on_actionsksj_triggered(self):
        curPath = QDir.currentPath()  # 获取系统当前目录
        title = "打开一个文件"
        filt = "文本文件(*.txt);;所有文件(*.*)"
        fileName, flt = QFileDialog.getOpenFileName(self, title, curPath, filt)

        if fileName != "":
            fileDevice = QFile(fileName)
            fileDevice.open(QIODevice.ReadOnly | QIODevice.Text)
            try:
                fileStream = QTextStream(fileDevice)
                fileStream.setAutoDetectUnicode(True)  # 自动检测Unicode
                fileStream.setCodec("GBK")  # 必须设置编码，否则不能正常显示汉字

                i = 0
                while not fileStream.atEnd():
                    i = i + 1
                    lineStr = fileStream.readLine()  # 返回QByteArray类型
                    lineList = lineStr.split("\t")

                    if i == 1:
                        continue

                    if lineList[1] in SKSJ:
                        SKSJ[lineList[1]].append(lineList)
                    else:
                        SKSJ[lineList[1]] = []
                        SKSJ[lineList[1]].append(lineList)
                        item = QTreeWidgetItem()
                        item.setText(0, lineList[1])
                        item.setIcon(0, QtGui.QIcon('images/29.ico'))
                        self.ui.treeWidget.topLevelItem(1).child(2).addChild(item)

            except UnicodeDecodeError:
                print(fileName[0] + "文件编码格式有误！")

            finally:
                fileDevice.close()

        self.ui.treeWidget.topLevelItem(1).child(2).setExpanded(True)

    @pyqtSlot()
    def on_actioncssj_triggered(self):
        curPath = QDir.currentPath()  # 获取系统当前目录
        title = "打开一个文件"
        filt = "文本文件(*.txt);;所有文件(*.*)"
        fileName, flt = QFileDialog.getOpenFileName(self, title, curPath, filt)

        if fileName != "":
            fileDevice = QFile(fileName)
            fileDevice.open(QIODevice.ReadOnly | QIODevice.Text)
            try:
                fileStream = QTextStream(fileDevice)
                fileStream.setAutoDetectUnicode(True)  # 自动检测Unicode
                fileStream.setCodec("GBK")  # 必须设置编码，否则不能正常显示汉字

                i = 0
                while not fileStream.atEnd():
                    i = i + 1
                    lineStr = fileStream.readLine()  # 返回QByteArray类型
                    lineList = lineStr.split("\t")

                    if i == 1:
                        continue

                    if lineList[1] in CSSJ:
                        CSSJ[lineList[1]].append(lineList)
                    else:
                        CSSJ[lineList[1]] = []
                        CSSJ[lineList[1]].append(lineList)
                        item = QTreeWidgetItem()
                        item.setText(0, lineList[1])
                        item.setIcon(0, QtGui.QIcon('images/29.ico'))
                        self.ui.treeWidget.topLevelItem(1).child(5).addChild(item)

            except UnicodeDecodeError:
                print(fileName[0] + "文件编码格式有误！")

            finally:
                fileDevice.close()

        self.ui.treeWidget.topLevelItem(1).child(5).setExpanded(True)

    @pyqtSlot()
    def on_actioncjdysj_triggered(self):


        curPath = QDir.currentPath()  # 获取系统当前目录
        title = "打开一个文件"
        filt = "文本文件(*.txt);;所有文件(*.*)"
        fileName, flt = QFileDialog.getOpenFileName(self, title, curPath, filt)

        if fileName != "":
            fileDevice = QFile(fileName)
            fileDevice.open(QIODevice.ReadOnly | QIODevice.Text)
            try:
                fileStream = QTextStream(fileDevice)
                fileStream.setAutoDetectUnicode(True)  # 自动检测Unicode
                fileStream.setCodec("GBK")  # 必须设置编码，否则不能正常显示汉字
                i = 0
                while not fileStream.atEnd():
                    i = i + 1
                    lineStr = fileStream.readLine()  # 返回QByteArray类型
                    lineList = lineStr.split("\t")

                    if i == 1:
                        continue

                    floor1 = lineList[0]
                    CJDYZB[floor1] = []
                    CJDYZB[floor1].append(lineList)

                    floor = lineList[3] + "-" + lineList[4]
                    if floor in CJDYSJ:
                        CJDYSJ[floor].append(lineList)
                    else:
                        CJDYSJ[floor] = []
                        CJDYSJ[floor].append(lineList)
                        item = QTreeWidgetItem()
                        item.setText(0, floor)
                        item.setIcon(0, QtGui.QIcon('images/29.ico'))

                        self.ui.treeWidget.topLevelItem(1).child(1).addChild(item)

            except UnicodeDecodeError:
                print(fileName[0] + "文件编码格式有误！")

            finally:
                fileDevice.close()

            # item = QTreeWidgetItem()
            # item.setText(0, "沉积单元数据")
            # self.ui.treeWidget.topLevelItem(1).child(1).addChild(item)
        self.ui.treeWidget.topLevelItem(1).child(1).setExpanded(True)

    @pyqtSlot()
    def on_actionzsjs_triggered(self):

        curPath = QDir.currentPath()  # 获取系统当前目录
        title = "打开一个文件"
        filt = "文本文件(*.txt);;所有文件(*.*)"
        fileName, flt = QFileDialog.getOpenFileName(self, title, curPath, filt)



        if fileName != "":
            fileDevice = QFile(fileName)
            fileDevice.open(QIODevice.ReadOnly | QIODevice.Text)
            try:
                fileStream = QTextStream(fileDevice)
                fileStream.setAutoDetectUnicode(True)  # 自动检测Unicode
                fileStream.setCodec("GBK")  # 必须设置编码，否则不能正常显示汉字
                i = 0
                while not fileStream.atEnd():
                    i = i + 1
                    lineStr = fileStream.readLine()  # 返回QByteArray类型
                    lineList = lineStr.split("\t")

                    if i == 1:
                        continue

                    if lineList[1] in ZSJS:
                        ZSJS[lineList[1]].append(lineList)
                    else:
                        ZSJS[lineList[1]] = []
                        ZSJS[lineList[1]].append(lineList)
                        item = QTreeWidgetItem()
                        item.setText(0, lineList[1])
                        item.setIcon(0, QtGui.QIcon('images/29.ico'))
                        self.ui.treeWidget.topLevelItem(1).child(0).addChild(item)

            except UnicodeDecodeError:
                print(fileName[0] + "文件编码格式有误！")

            finally:
                fileDevice.close()

        self.ui.treeWidget.topLevelItem(1).child(0).setExpanded(True)

    @pyqtSlot()
    def on_actioncyjs_triggered(self):

        curPath = QDir.currentPath()  # 获取系统当前目录
        title = "打开一个文件"
        filt = "文本文件(*.txt);;所有文件(*.*)"
        fileName, flt = QFileDialog.getOpenFileName(self, title, curPath, filt)

        if fileName != "":
            fileDevice = QFile(fileName)
            fileDevice.open(QIODevice.ReadOnly | QIODevice.Text)
            try:
                fileStream = QTextStream(fileDevice)
                fileStream.setAutoDetectUnicode(True)  # 自动检测Unicode
                fileStream.setCodec("GBK")  # 必须设置编码，否则不能正常显示汉字
                i = 0
                while not fileStream.atEnd():
                    i = i + 1
                    lineStr = fileStream.readLine()  # 返回QByteArray类型
                    lineList = lineStr.split("\t")

                    if i == 1:
                        continue

                    if lineList[1] in CYJS:
                        CYJS[lineList[1]].append(lineList)
                    else:
                        CYJS[lineList[1]] = []
                        CYJS[lineList[1]].append(lineList)
                        item = QTreeWidgetItem()
                        item.setText(0, lineList[1])
                        item.setIcon(0, QtGui.QIcon('images/29.ico'))
                        self.ui.treeWidget.topLevelItem(1).child(6).addChild(item)

            except UnicodeDecodeError:
                print(fileName[0] + "文件编码格式有误！")

            finally:
                fileDevice.close()

        self.ui.treeWidget.topLevelItem(1).child(6).setExpanded(True)

    @pyqtSlot()
    def on_actionxsqx_triggered(self):

        curPath = QDir.currentPath()  # 获取系统当前目录
        title = "打开一个文件"
        filt = "文本文件(*.txt);;所有文件(*.*)"
        fileName, flt = QFileDialog.getOpenFileName(self, title, curPath, filt)

        if fileName != "":
            fileDevice = QFile(fileName)
            fileDevice.open(QIODevice.ReadOnly | QIODevice.Text)
            try:
                fileStream = QTextStream(fileDevice)
                fileStream.setAutoDetectUnicode(True)  # 自动检测Unicode
                fileStream.setCodec("GBK")  # 必须设置编码，否则不能正常显示汉字
                i = 0
                while not fileStream.atEnd():
                    i = i + 1
                    lineStr = fileStream.readLine()  # 返回QByteArray类型
                    lineList = lineStr.split("\t")
                    XSQX.append(lineList)


            except UnicodeDecodeError:
                print(fileName[0] + "文件编码格式有误！")

            finally:
                fileDevice.close()

            item = QTreeWidgetItem()
            item.setText(0, '油水相渗')
            item.setIcon(0, QtGui.QIcon('images/29.ico'))
            self.ui.treeWidget.topLevelItem(0).child(3).addChild(item)
            item = QTreeWidgetItem()
            item.setText(0, '油气相渗')
            item.setIcon(0, QtGui.QIcon('images/29.ico'))
            self.ui.treeWidget.topLevelItem(0).child(3).addChild(item)

        self.ui.treeWidget.topLevelItem(0).child(3).setExpanded(True)

    @pyqtSlot()
    def on_actionfsd_triggered(self):
        newWindow = CSw_dcfbx_Slot.QmyMainWindow(self)
        newWindow.show()

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        self.stepx = int(self.ui.lineEdit.text())
        self.stepy = int(self.ui.lineEdit_2.text())

        print(self.stepx)
        print(self.stepy)
        print("pushbotton2")

    @pyqtSlot()
    def on_pushButton_3_clicked(self):

        headerText = ["潜力区序号", "层号", "平面规模", "平均含油饱和度", "平均有效厚度", "平均渗透率","平均孔隙度","剩余油量","井数量","平均水淹程度"]
        self.ui.tableWidget.setColumnCount(len(headerText))
        self.ui.tableWidget.setHorizontalHeaderLabels(headerText)
        self.ui.tableWidget.clearContents()


        labText = "正在导入文件..."  # 文本信息
        btnText = "取消"  # "取消"按钮的标
        minV = 0
        maxV = len(self.qlqFloor)

        dlgProgress = QProgressDialog(labText, btnText, minV, maxV, self)
        dlgProgress.setWindowTitle("筛选数据")
        dlgProgress.setWindowModality(Qt.WindowModal)  # 模态对话框
        dlgProgress.setAutoReset(True)  # value()达到最大值时自动调用reset()
        dlgProgress.setAutoClose(True)  # 调用reset()时隐藏窗口

        pross = 1
        index = 0
        for qlqFloorName in self.qlqFloor:


            dlgProgress.setValue(pross)
            dlgProgress.setLabelText("正在筛选数据,第 %d 个" % pross)

            x = BHD[qlqFloorName][0]  # float 型
            y = BHD[qlqFloorName][1]
            v = BHD[qlqFloorName][2]

            for i in range(len(v)):
                if v[i] == -999:
                    v[i] = 0

            x = np.array(x)
            y = np.array(y)
            v = np.array(v)

            x = x.T
            y = y.T
            v = v.T

            xb = list(range(int(min(x)), int(max(x)), self.stepx))
            yb = list(range(int(min(y)), int(max(y)), self.stepy))

            xb = np.array(xb)
            yb = np.array(yb)

            xb, yb = np.meshgrid(xb, yb)

            bhdq = griddata((x, y), v, (xb, yb), method="linear")

            floor = CJDYSJ[qlqFloorName]  # float 型
            sycd = {}


            floor = np.array(floor)
            floor = floor.T
            floor = floor.tolist()
            # wellNum = floor[2]
            x = []
            y = []

            for i, sycdaction in enumerate(floor[16]):
                if sycdaction != "":
                    sycd[floor[2][i]] = sycdaction


            bj1 = 1
            bj2 = 1
            yxhd = []
            yxhd1 = float(floor[13][0])
            kxd = []
            kxd1 = float(floor[14][0])
            stl = []
            stl1 = float(floor[15][0])
            wellNum = []

            for i in range(1, len(floor[0]) - 1):
                if floor[2][i] == floor[2][i - 1]:

                    yxhd1 = yxhd1 + float(floor[13][i])
                    if float(floor[14][i]) == 0:
                        kxd1 = kxd1 + float(floor[14][i])
                    else:
                        bj1 = bj1 + 1
                        kxd1 = kxd1 + float(floor[14][i])

                    if float(floor[15][i]) == 0:
                        stl1 = stl1 + float(floor[15][i])
                    else:
                        bj2 = bj2 + 1
                        stl1 = stl1 + float(floor[15][i])
                else:
                    for j in range(len(DJDZSJ)):
                        if floor[2][i - 1] == list(DJDZSJ.keys())[j]:
                            if DJDZSJ[list(DJDZSJ.keys())[j]][2] == '0':
                                y.append(DJDZSJ[list(DJDZSJ.keys())[j]][0])
                                x.append(DJDZSJ[list(DJDZSJ.keys())[j]][1])
                            else:
                                y.append(DJDZSJ[list(DJDZSJ.keys())[j]][2])
                                x.append(DJDZSJ[list(DJDZSJ.keys())[j]][3])
                            wellNum.append(floor[2][i - 1])
                            yxhd.append(str(yxhd1))
                            kxd.append(str(kxd1 / bj1))
                            stl.append(str(stl1 / bj2))

                    bj1 = 1
                    bj2 = 1
                    yxhd1 = float(floor[13][i])
                    kxd1 = float(floor[14][i])
                    stl1 = float(floor[15][i])

            x = np.array(x)
            y = np.array(y)
            yxhd = np.array(yxhd)
            stl = np.array(stl)
            kxd = np.array(kxd)

            x = x.T
            y = y.T
            yxhd = yxhd.T
            stl = stl.T
            kxd = kxd.T

            yxhdq = griddata((x, y), yxhd, (xb, yb), method="linear")
            stlq = griddata((x, y), stl, (xb, yb), method="linear")
            kxdq = griddata((x, y), kxd, (xb, yb), method="linear")

            # print(yxhdq.shape)
            # print(stlq.shape)
            # print(bhdq.shape)


            qlq = yxhdq.copy()

            for i in range(bhdq.shape[0]):
                for j in range(bhdq.shape[1]):
                    if np.isnan(bhdq[i][j]) == False and np.isnan(stlq[i][j]) == False and np.isnan(
                            yxhdq[i][j]) == False:
                        if stlq[i][j] > 0.15 and bhdq[i][j] > 0.45 and yxhdq[i][j] > 2:
                            qlq[i][j] = 1
                        else:
                            qlq[i][j] = 0

            self.qlqBinary[qlqFloorName] = qlq
            self.qlqXb[qlqFloorName] = xb
            self.qlqYb[qlqFloorName] = yb


            contours = measure.find_contours(qlq, 0.4)


            for n, contour in enumerate(contours):
                for i in range(contour.shape[0]):
                    xcontour = round(contour[i][1])
                    ycontour = round(contour[i][0])

                    contour[i][1] = xcontour * self.stepx + xb[0][0]
                    contour[i][0] = ycontour * self.stepy + yb[0][0]

            areaX = int(self.ui.lineEdit_3.text())
            areaY = int(self.ui.lineEdit_4.text())

            self.qlqContours[qlqFloorName] = []

            for _, contour in enumerate(contours):
                qlqTableRow = {}

                contour = np.float32(contour)
                # 计算最小内接矩形
                rect = cv2.minAreaRect(contour)
                area = cv2.contourArea(contour)
                qlqTableRow["floor"] = qlqFloorName
                qlqTableRow["area"] = area

                # 提取矩形的关键信息
                center, size, angle = rect
                width, height = size
                if width > areaX and height > areaY:
                    index = index + 1
                    qlqTableRow["index"] = index

                    self.qlqContours[qlqFloorName].append(contour)
                    minx = min(contour[:,1])
                    miny = min(contour[:,0])
                    maxx = max(contour[:,1])
                    maxy = max(contour[:,0])
                    well = []

                    x = np.float32(x)
                    y = np.float32(y)

                    for i in range(len(wellNum)):
                        if minx < x[i] < maxx and miny < y[i] < maxy:
                            well.append(wellNum[i])

                    qlqTableRow["well"] = well

                    n = 0
                    sumStl = 0
                    sumYxhd = 0
                    sumBhd = 0
                    sumKxd = 0
                    for i in range(bhdq.shape[0]):
                        for j in range(bhdq.shape[1]):
                            if minx <= xb[i][j] <= maxx and miny <= yb[i][j] <= maxy and qlq[i][j] == 1:
                                n = n + 1
                                sumBhd = sumBhd + bhdq[i][j]
                                sumStl = sumStl + stlq[i][j]
                                sumYxhd = sumYxhd + yxhdq[i][j]
                                sumKxd = sumKxd + kxdq[i][j]

                    avStl = sumStl / n
                    avBhd = sumBhd / n
                    avYxhd = sumYxhd / n
                    avKxd = sumKxd / n
                    qlqTableRow["avStl"] = avStl
                    qlqTableRow["avBhd"] = avBhd
                    qlqTableRow["avYxhd"] = avYxhd
                    qlqTableRow["avKxd"] = avKxd
                    qlqTableRow["syyl"] = avKxd * avBhd * avYxhd * area
                    avsycd = ''
                    D = 0
                    Z = 0
                    G = 0
                    for i in well:
                        try:
                            if sycd[i] == 'D':
                                D = D + 1
                            if sycd[i] == 'Z':
                                Z = Z + 1
                            if sycd[i] == 'G':
                                G = G + 1
                        except KeyError:
                            print(KeyError)

                    if G > Z and G > D:
                        avsycd = "高"
                    if Z > G and Z > D:
                        avsycd = "中"
                    if D > G and D > Z:
                        avsycd = "低"

                    qlqTableRow["avsycd"] = avsycd
                    self.qlqTable[index] = qlqTableRow

            print("pushBotton")
            pross = pross + 1
        self.ui.tableWidget.setRowCount(index)
        self.ui.tableWidget.setAlternatingRowColors(True)

        self.ui.comboBox_2.addItem("请选择潜力区编号")
        for i in range(1,index):
            listrow = []

            # 潜力区编号
            listrow.append(self.qlqTable[i]["index"])
            self.ui.comboBox_2.addItem(str(self.qlqTable[i]["index"]))
            self.ui.comboBox_3.addItem(str(self.qlqTable[i]["index"]))
            item = QTableWidgetItem(str(self.qlqTable[i]["index"]))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled
                          | Qt.ItemIsUserCheckable)  # 不允许编辑文字
            self.ui.tableWidget.setItem(i-1, 0,item)


            # 层号
            listrow.append(self.qlqTable[i]["floor"])
            item = QTableWidgetItem(self.qlqTable[i]["floor"])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled
                          | Qt.ItemIsUserCheckable)  # 不允许编辑文字
            self.ui.tableWidget.setItem(i-1, 1,item)

            # 平面规模
            listrow.append(self.qlqTable[i]["area"])
            item = QTableWidgetItem(str(self.qlqTable[i]["area"]))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled
                          | Qt.ItemIsUserCheckable)  # 不允许编辑文字
            self.ui.tableWidget.setItem(i-1, 2,item)

            # 平均含油饱和度
            listrow.append(self.qlqTable[i]["avBhd"])
            item = QTableWidgetItem(str(self.qlqTable[i]["avBhd"]))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled
                          | Qt.ItemIsUserCheckable)  # 不允许编辑文字
            self.ui.tableWidget.setItem(i-1, 3,item)

            # 平均有效厚度
            listrow.append(self.qlqTable[i]["avYxhd"])
            item = QTableWidgetItem(str(self.qlqTable[i]["avYxhd"]))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled
                          | Qt.ItemIsUserCheckable)  # 不允许编辑文字
            self.ui.tableWidget.setItem(i-1, 4,item)

            # 平均渗透率
            listrow.append(self.qlqTable[i]["avStl"])
            item = QTableWidgetItem(str(self.qlqTable[i]["avStl"]))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled
                          | Qt.ItemIsUserCheckable)  # 不允许编辑文字
            self.ui.tableWidget.setItem(i-1, 5,item)

            # 平均孔隙度
            listrow.append(self.qlqTable[i]["avKxd"])
            item = QTableWidgetItem(str(self.qlqTable[i]["avKxd"]))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled
                          | Qt.ItemIsUserCheckable)  # 不允许编辑文字
            self.ui.tableWidget.setItem(i-1, 6,item)

            # 剩余油量
            listrow.append(self.qlqTable[i]["syyl"])
            item = QTableWidgetItem(str(self.qlqTable[i]["syyl"]))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled
                          | Qt.ItemIsUserCheckable)  # 不允许编辑文字
            self.ui.tableWidget.setItem(i-1, 7,item)

            # 井数量
            listrow.append(len(self.qlqTable[i]["well"]))
            item = QTableWidgetItem(str(len(self.qlqTable[i]["well"])))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled
                          | Qt.ItemIsUserCheckable)  # 不允许编辑文字
            self.ui.tableWidget.setItem(i-1, 8,item)

            # 平均水淹程度
            if self.qlqTable[i]["avsycd"] == "高":
                listrow.append(3)
            if self.qlqTable[i]["avsycd"] == "中":
                listrow.append(2)
            if self.qlqTable[i]["avsycd"] == "低":
                listrow.append(1)
            if self.qlqTable[i]["avsycd"] == '':
                listrow.append(3)

            item = QTableWidgetItem(str(self.qlqTable[i]["avsycd"]))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled
                          | Qt.ItemIsUserCheckable)  # 不允许编辑文字
            self.ui.tableWidget.setItem(i-1, 9,item)

            # a = random.randrange(0, 2, 1)
            # listrow.append(a)
            self.qlqTableList.append(listrow)
        print(self.qlqTableList)


    @pyqtSlot()
    def on_pushButton_clicked(self):

        comBoxText = self.ui.comboBox.currentText()

        title = comBoxText + "潜力区"
        fig1 = QmyFigure(self)
        fig1.setAttribute(Qt.WA_DeleteOnClose)
        curIndex = self.ui.tabWidget.addTab(fig1, title)  # 添加到tabWidget
        self.ui.tabWidget.setCurrentIndex(curIndex)



        ax1 = fig1.fig.add_subplot(1, 1, 1)  # 子图1
        ax1.set_xlabel('X 轴')  # X轴标题
        ax1.set_ylabel('Y 轴')  # Y轴标题
        ax1.set_title(title)

        im1 = ax1.pcolormesh(self.qlqXb[comBoxText], self.qlqYb[comBoxText], self.qlqBinary[comBoxText])
        fig1.fig.colorbar(im1, ax=ax1)



        for n, contour in enumerate(self.qlqContours[comBoxText]):

            ax1.plot(contour[:, 1], contour[:, 0], linewidth=2)

        print("pushBotton")

    @pyqtSlot(str)  #层间连通性判断得下拉列表变化时运行得函数
    def on_comboBox_2_activated(self, curText):

        comBoxin = self.ui.comboBox_2.currentIndex()
        if comBoxin > 0:
            comBoxzhi = int(self.ui.comboBox_2.currentText())

            # print(self.qlqTableList)
            # print(self.qlqTable[comBoxzhi]["well"])

            CJLTX = []#层间连通性
            CJLTXTJ = []#层间连通性统计

            blt = 0  # 不连通
            slt = 0  # 上连通
            xlt = 0  # 下连通
            jlt = 0  # 均连通

            if len(self.qlqTable[comBoxzhi]["well"]) == 0:
                print('潜力区内无注采井')
            else:
                for i in range(len(self.qlqTable[comBoxzhi]["well"])):
                    CJLTX1 = []
                    CJLTX1.append(self.qlqTable[comBoxzhi]["well"][i])
                    bj = 0
                    bj1 = 0
                    for j in range(1,len(CJDYZB)):
                        if self.qlqTable[comBoxzhi]["well"][i] == (CJDYZB[str(j)][0][2]):
                            ch = CJDYZB[str(j)][0][3] + "-" + CJDYZB[str(j)][0][4]#%合并层号
                            if ch == self.qlqTableList[comBoxzhi][1]:
                                bj = bj + 1
                                if bj == 1:
                                    for k in range(j-1,j-50,-1):
                                        if bj1 == 0:
                                            if CJDYZB[str(k)][0][9] != 0:
                                                bj1 = bj1 + 1
                                                CJLTX1.append(float(CJDYZB[str(k)][0][8]) + float(CJDYZB[str(k)][0][9]))
                                    CJLTX1.append(float(CJDYZB[str(j)][0][8]))
                                    CJLTX1.append(float(CJDYZB[str(j)][0][8]) + float(CJDYZB[str(j)][0][9]))
                                    if CJDYZB[str(j+1)][0][8] != 0:
                                        CJLTX1.append(float(CJDYZB[str(j+1)][0][8]))
                                elif CJDYZB[str(j)][0][8] == '0':
                                    if CJDYZB[str(j+1)][0][8] != 0:
                                        CJLTX1[4] = float(CJDYZB[str(j+1)][0][8])
                                elif CJDYZB[str(j)][0][8] != '0':
                                    CJLTX1[3] = float(CJDYZB[str(j)][0][8]) + float(CJDYZB[str(j)][0][9])
                                    if CJDYZB[str(j+1)][0][8] != 0:
                                        CJLTX1[4] = float(CJDYZB[str(j + 1)][0][8])

                    if CJLTX1[2] != []:
                        if CJLTX1[2] - CJLTX1[1] > 0.5:
                            if CJLTX1[4] - CJLTX1[3] > 0.5:
                                CJLTX1.append(0)
                                blt = blt + 1
                            else:
                                CJLTX1.append(2)
                                xlt = xlt + 1
                        else:
                            if CJLTX1[4] - CJLTX1[3] > 0.5:
                                CJLTX1.append(1)
                                slt = slt + 1
                            else:
                                CJLTX1.append(3)
                                jlt = jlt + 1
                    CJLTX.append(CJLTX1)
                #print(CJLTX1)#单井层间连通性统计数据
                CJLTXTJ.append('上下不连通')
                CJLTXTJ.append(blt)
                CJLTXTJ.append('上连通')
                CJLTXTJ.append(slt)
                CJLTXTJ.append('下连通')
                CJLTXTJ.append(xlt)
                CJLTXTJ.append('上下均连通')
                CJLTXTJ.append(jlt)

                print(CJLTX)#所选潜力区的所有井层间连通性表
                print(CJLTXTJ)#所选潜力区的所有井层间连通性统计表

                headerText = ["包含井号", "上层砂岩底深", "砂岩顶深", "砂岩底深", "下层砂岩顶深", "层间连通性"]
                self.ui.tableWidget_3.setColumnCount(len(headerText))
                self.ui.tableWidget_3.setHorizontalHeaderLabels(headerText)
                self.ui.tableWidget_3.clearContents()
                self.ui.tableWidget_3.setRowCount(len(CJLTX))
                self.ui.tableWidget_3.setAlternatingRowColors(True)


                for i in range(0,len(CJLTX)):
                    for j in range(0,len(CJLTX[0])):

                        item = QTableWidgetItem(str(CJLTX[i][j]))
                        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled
                                      | Qt.ItemIsUserCheckable)  # 不允许编辑文字
                        self.ui.tableWidget_3.setItem(i, j, item)


                headerText = ["连通情况", "潜力区井数量"]
                self.ui.tableWidget_2.setColumnCount(len(headerText))
                self.ui.tableWidget_2.setHorizontalHeaderLabels(headerText)
                self.ui.tableWidget_2.clearContents()
                self.ui.tableWidget_2.setRowCount(4)
                self.ui.tableWidget_2.setAlternatingRowColors(True)


                item = QTableWidgetItem(str(CJLTXTJ[0]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled
                              | Qt.ItemIsUserCheckable)  # 不允许编辑文字
                self.ui.tableWidget_2.setItem(0, 0, item)

                item = QTableWidgetItem(str(CJLTXTJ[1]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled
                              | Qt.ItemIsUserCheckable)  # 不允许编辑文字
                self.ui.tableWidget_2.setItem(0, 1, item)

                item = QTableWidgetItem(str(CJLTXTJ[2]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled
                              | Qt.ItemIsUserCheckable)  # 不允许编辑文字
                self.ui.tableWidget_2.setItem(1, 0, item)

                item = QTableWidgetItem(str(CJLTXTJ[3]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled
                              | Qt.ItemIsUserCheckable)  # 不允许编辑文字
                self.ui.tableWidget_2.setItem(1, 1, item)

                item = QTableWidgetItem(str(CJLTXTJ[4]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled
                              | Qt.ItemIsUserCheckable)  # 不允许编辑文字
                self.ui.tableWidget_2.setItem(2, 0, item)

                item = QTableWidgetItem(str(CJLTXTJ[5]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled
                              | Qt.ItemIsUserCheckable)  # 不允许编辑文字
                self.ui.tableWidget_2.setItem(2, 1, item)

                item = QTableWidgetItem(str(CJLTXTJ[6]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled
                              | Qt.ItemIsUserCheckable)  # 不允许编辑文字
                self.ui.tableWidget_2.setItem(3, 0, item)

                item = QTableWidgetItem(str(CJLTXTJ[7]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled
                              | Qt.ItemIsUserCheckable)  # 不允许编辑文字
                self.ui.tableWidget_2.setItem(3, 1, item)

    # 厚层识别按钮
    @pyqtSlot()
    def on_pushButton_11_clicked(self):

        HCSBB1 = [] #厚层识别表，删除无厚层的井号
        CJDYJH = [] #沉积单元井号
        pross = 1

        for i in range(1,len(CJDYZB)):
            if i == 1:
                CJDYJH.append(CJDYZB[str(i)][0][2])
            else:
                if CJDYJH[len(CJDYJH)-1] != CJDYZB[str(i)][0][2]:
                    CJDYJH.append(CJDYZB[str(i)][0][2])


        labText = "正在厚层识别..."  # 文本信息
        btnText = "取消"  # "取消"按钮的标
        minV = 0
        maxV = len(CJDYJH)

        dlgProgress = QProgressDialog(labText, btnText, minV, maxV, self)
        dlgProgress.setWindowTitle("厚层识别")
        dlgProgress.setWindowModality(Qt.WindowModal)  # 模态对话框
        dlgProgress.setAutoReset(True)  # value()达到最大值时自动调用reset()
        dlgProgress.setAutoClose(True)  # 调用reset()时隐藏窗口


        for i in range(len(CJDYJH)):

            dlgProgress.setValue(pross)
            dlgProgress.setLabelText("正在分析第 %d 口井" %pross)

            ch = []
            HCSBB = []
            HCSBB.append(CJDYJH[i])
            syhd = 0 #砂岩厚度，记录叠加厚层的砂岩厚度
            yxhd = 0 #有效厚度，记录叠加厚层的有效厚度
            bj = 0 #标记，用于标记单井是否有多段厚层
            bj1 = 0 #标记，用于删除0数值行

            for j in range(1,len(CJDYZB)):
                if CJDYJH[i] == CJDYZB[str(j)][0][2]:
                    a = float(CJDYZB[str(j)][0][8])#第一个砂岩顶深
                    if a != 0: # 第一个砂岩顶深不能为零
                        b = float(CJDYZB[str(j)][0][9]) #第一个砂岩层厚
                        d = float(CJDYZB[str(j)][0][13]) #第一个有效厚度

                        c = float(CJDYZB[str(j+1)][0][8]) #第二个砂岩顶深

                        for m in range(j+2, j+20):
                            if bj1 == 0:
                                if c == 0: #第二个砂岩顶深不能为零
                                    c = float(CJDYZB[str(m)][0][8])
                                else:
                                    bj1 = 1

                        if c == a + b: #判断条件，第二个砂岩顶深=第一个砂岩顶深+第一个砂岩层厚
                            ch.append(CJDYZB[str(j)][0][3] + "-" + CJDYZB[str(j)][0][4]) #合并层号，提取出第一个砂岩顶深所在的层号
                            syhd = syhd + b
                            yxhd = yxhd + d
                        else:
                            if syhd >= 5:
                                if bj == 0:
                                    ch.append(CJDYZB[str(j)][0][3] + "-" + CJDYZB[str(j)][0][4]) #合并层号，提取出第一个砂岩顶深所在的层号
                                    HCSBB.append(syhd)
                                    HCSBB.append(yxhd)
                                    for n in range(len(ch)):
                                        HCSBB.append(ch[n])
                                    bj = 1
                                    ch = []
                                    syhd = 0
                                    yxhd = 0
                                    print(HCSBB)
                                else:
                                    HCSBB1.append(HCSBB)
                                    HCSBB = []
                                    HCSBB.append(CJDYJH[i])
                                    ch.append(CJDYZB[str(j)][0][3] + "-" + CJDYZB[str(j)][0][4]) #合并层号，提取出第一个砂岩顶深所在的层号
                                    HCSBB.append(syhd)
                                    HCSBB.append(yxhd)
                                    for n in range(len(ch)):
                                        HCSBB.append(ch[n])
                                    bj = 1
                                    ch = []
                                    syhd = 0
                                    yxhd = 0
                            else:
                                ch = []
                                syhd = 0
                                yxhd = 0

            if len(HCSBB) != 1:
                HCSBB1.append(HCSBB)
                print(HCSBB1)

            pross = pross + 1

        print(HCSBB1)

        headerText = ["井号", "总砂岩厚度","总有效厚度","层位1","层位2","层位3","层位4","层位5","层位6"]
        self.ui.tableWidget_5.setColumnCount(len(headerText))
        self.ui.tableWidget_5.setHorizontalHeaderLabels(headerText)
        self.ui.tableWidget_5.clearContents()
        self.ui.tableWidget_5.setRowCount(len(HCSBB1))
        self.ui.tableWidget_5.setAlternatingRowColors(True)

        for i, row in  enumerate(HCSBB1):
            for j, a in enumerate(row):
                item = QTableWidgetItem(str(a))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled
                              | Qt.ItemIsUserCheckable)  # 不允许编辑文字
                self.ui.tableWidget_5.setItem(i, j, item)

    # 随机森林模型按钮
    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        Y = []
        for i, _ in enumerate(self.qlqTableList):
            Y.append(random.randrange(0, 2, 1))

        # 设置弱学习器数量为10
        self.model = RandomForestClassifier(n_estimators=10, random_state=123)
        X = [row[2:] for row in self.qlqTableList]
        self.model.fit(X, Y)

        dlgTitle = "提示"
        strInfo = "模型已经被正确导入."
        QMessageBox.information(self, dlgTitle, strInfo)

        # print(model.predict(X))

    @pyqtSlot()
    def on_pushButton_5_clicked(self):
        X = [row[2:] for row in self.qlqTableList]
        Y = self.model.predict(X)
        headerText = ["潜力区序号", "层号", "平面规模", "平均含油饱和度", "平均有效厚度", "平均渗透率","平均孔隙度","剩余油量","井数量","平均水淹程度","随机森林评价"]
        self.ui.tableWidget_4.setColumnCount(len(headerText))
        self.ui.tableWidget_4.setHorizontalHeaderLabels(headerText)
        self.ui.tableWidget_4.clearContents()
        self.ui.tableWidget_4.setRowCount(len(self.qlqTableList))
        self.ui.tableWidget_4.setAlternatingRowColors(True)

        for i, row in enumerate(self.qlqTableList):

            for j, a in enumerate(row):

                item = QTableWidgetItem(str(a))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled
                              | Qt.ItemIsUserCheckable)  # 不允许编辑文字
                self.ui.tableWidget_4.setItem(i, j, item)

            item = QTableWidgetItem(str(Y[i]))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled
                          | Qt.ItemIsUserCheckable)  # 不允许编辑文字
            self.ui.tableWidget_4.setItem(i, 10, item)

        print("评价完成")

    # @pyqtSlot()
    def on_checkBox_stateChanged(self,change):
        if self.ui.checkBox.isChecked():
            maxAvYxhd = max([row[4:5] for row in self.qlqTableList])
            minAvYxhd = min([row[4:5] for row in self.qlqTableList])
            self.ui.label_37.setText(str(round(minAvYxhd[0], 2)))
            self.ui.label_51.setText(str(round(maxAvYxhd[0], 2)))
            step = (maxAvYxhd[0] - minAvYxhd[0]) / 4
            # test = str(minAvYxhd[0] + step)
            self.ui.lineEdit_15.setText(str(round(minAvYxhd[0] + step, 2)))
            self.ui.lineEdit_14.setText(str(round(minAvYxhd[0] + 2 * step, 2)))
            self.ui.lineEdit_5.setText(str(round(minAvYxhd[0] + 3 * step, 2)))

    # @pyqtSlot()
    def on_checkBox_2_stateChanged(self,change):
        if self.ui.checkBox_2.isChecked():
            maxAvYxhd = max([row[7:8] for row in self.qlqTableList])
            minAvYxhd = min([row[7:8] for row in self.qlqTableList])
            self.ui.label_39.setText(str(round(minAvYxhd[0], 2)))
            self.ui.label_50.setText(str(round(maxAvYxhd[0], 2)))
            step = (maxAvYxhd[0] - minAvYxhd[0]) / 4
            # test = str(minAvYxhd[0] + step)
            self.ui.lineEdit_16.setText(str(round(minAvYxhd[0] + step, 2)))
            self.ui.lineEdit_13.setText(str(round(minAvYxhd[0] + 2 * step, 2)))
            self.ui.lineEdit_6.setText(str(round(minAvYxhd[0] + 3 * step, 2)))

    # @pyqtSlot()
    def on_checkBox_3_stateChanged(self,change):
        if self.ui.checkBox_3.isChecked():
            maxAvYxhd = max([row[2:3] for row in self.qlqTableList])
            minAvYxhd = min([row[2:3] for row in self.qlqTableList])
            self.ui.label_44.setText(str(round(minAvYxhd[0], 2)))
            self.ui.label_49.setText(str(round(maxAvYxhd[0], 2)))
            step = (maxAvYxhd[0] - minAvYxhd[0]) / 4
            # test = str(minAvYxhd[0] + step)
            self.ui.lineEdit_17.setText(str(round(minAvYxhd[0] + step, 2)))
            self.ui.lineEdit_12.setText(str(round(minAvYxhd[0] + 2 * step, 2)))
            self.ui.lineEdit_7.setText(str(round(minAvYxhd[0] + 3 * step, 2)))

    # @pyqtSlot()
    def on_checkBox_4_stateChanged(self,change):
        if self.ui.checkBox_4.isChecked():
            maxAvYxhd = max([row[9:10] for row in self.qlqTableList])
            minAvYxhd = min([row[9:10] for row in self.qlqTableList])
            self.ui.label_45.setText(str(round(minAvYxhd[0], 2)))
            self.ui.label_48.setText(str(round(maxAvYxhd[0], 2)))
            step = (maxAvYxhd[0] - minAvYxhd[0]) / 4
            # test = str(minAvYxhd[0] + step)
            self.ui.lineEdit_8.setText(str(round(minAvYxhd[0] + step, 2)))
            self.ui.lineEdit_11.setText(str(round(minAvYxhd[0] + 2 * step, 2)))
            self.ui.lineEdit_18.setText(str(round(minAvYxhd[0] + 3 * step, 2)))

    #@pyqtSlot()
    def on_checkBox_5_stateChanged(self,change):
        if self.ui.checkBox_5.isChecked():
            maxAvYxhd = max([row[4:5] for row in self.qlqTableList])
            minAvYxhd = min([row[4:5] for row in self.qlqTableList])
            self.ui.label_37.setText(str(round(minAvYxhd[0], 2)))
            self.ui.label_51.setText(str(round(maxAvYxhd[0], 2)))
            step = (maxAvYxhd[0] - minAvYxhd[0]) / 4
            # test = str(minAvYxhd[0] + step)
            self.ui.lineEdit_15.setText(str(round(minAvYxhd[0] + step, 2)))
            self.ui.lineEdit_14.setText(str(round(minAvYxhd[0] + 2 * step, 2)))
            self.ui.lineEdit_5.setText(str(round(minAvYxhd[0] + 3 * step, 2)))


    # 潜力区评价响应按钮
    @pyqtSlot()
    def on_pushButton_6_clicked(self):

        # 如果是需要分析的因素，则获得该因素的分级区间点
        # 因为区间点是可以手动修改的，所以需要重新读取一下界面数据

        if self.ui.checkBox.isChecked():
            print(float(self.ui.lineEdit_5.text()))
            hd1 = float(self.ui.lineEdit_5.text()) # 厚度
            hd2 = float(self.ui.lineEdit_14.text())
            hd3 = float(self.ui.lineEdit_15.text())


        if self.ui.checkBox_2.isChecked():
            print(float(self.ui.lineEdit_6.text()))
            yl1 = float(self.ui.lineEdit_6.text()) # 油量
            yl2 = float(self.ui.lineEdit_13.text())
            yl3 = float(self.ui.lineEdit_16.text())


        if self.ui.checkBox_3.isChecked():
            print(float(self.ui.lineEdit_7.text()))
            gm1 = float(self.ui.lineEdit_7.text()) # 规模
            gm2 = float(self.ui.lineEdit_12.text())
            gm3 = float(self.ui.lineEdit_17.text())


        if self.ui.checkBox_4.isChecked():
            print(float(self.ui.lineEdit_8.text()))
            sy1 = float(self.ui.lineEdit_8.text()) #水淹
            sy2 = float(self.ui.lineEdit_11.text())
            sy3 = float(self.ui.lineEdit_18.text())


        if self.ui.checkBox_5.isChecked():
            xs1 = float(self.ui.lineEdit_9.text()) # 吸水
            xs2 = float(self.ui.lineEdit_10.text())
            xs3 = float(self.ui.lineEdit_19.text())


        QLQPJB2 = []#潜力区评价表总表
        for m in range(len(self.qlqTableList)):
            QLQPJB = []  # 潜力区评价表
            QLQPJB1 = []

            if self.ui.checkBox.isChecked():
                if self.qlqTableList[m][4] > hd1:
                    QLQPJB.append(4)
                    QLQPJB1.append(QLQPJB)
                    QLQPJB = []
                elif self.qlqTableList[m][4] > hd2:
                    QLQPJB.append(3)
                    QLQPJB1.append(QLQPJB)
                    QLQPJB = []
                elif self.qlqTableList[m][4] > hd3:
                    QLQPJB.append(2)
                    QLQPJB1.append(QLQPJB)
                    QLQPJB = []
                else:
                    QLQPJB.append(1)
                    QLQPJB1.append(QLQPJB)
                    QLQPJB = []

            if self.ui.checkBox_2.isChecked():
                if self.qlqTableList[m][7] > yl1:
                    QLQPJB.append(4)
                    QLQPJB1.append(QLQPJB)
                    QLQPJB = []
                elif self.qlqTableList[m][7] > yl2:
                    QLQPJB.append(3)
                    QLQPJB1.append(QLQPJB)
                    QLQPJB = []
                elif self.qlqTableList[m][7] > yl3:
                    QLQPJB.append(2)
                    QLQPJB1.append(QLQPJB)
                    QLQPJB = []
                else:
                    QLQPJB.append(1)
                    QLQPJB1.append(QLQPJB)
                    QLQPJB = []

            if self.ui.checkBox_3.isChecked():
                if self.qlqTableList[m][2] > gm1:
                    QLQPJB.append(4)
                    QLQPJB1.append(QLQPJB)
                    QLQPJB = []
                elif self.qlqTableList[m][2] > gm2:
                    QLQPJB.append(4)
                    QLQPJB1.append(QLQPJB)
                    QLQPJB = []
                elif self.qlqTableList[m][2] > gm3:
                    QLQPJB.append(4)
                    QLQPJB1.append(QLQPJB)
                    QLQPJB = []
                else:
                    QLQPJB.append(1)
                    QLQPJB1.append(QLQPJB)
                    QLQPJB = []

            if self.ui.checkBox_4.isChecked():
                if self.qlqTableList[m][9] <= sy1:
                    QLQPJB.append(4)
                    QLQPJB1.append(QLQPJB)
                    QLQPJB = []
                elif self.qlqTableList[m][9] <= sy2:
                    QLQPJB.append(3)
                    QLQPJB1.append(QLQPJB)
                    QLQPJB = []
                elif self.qlqTableList[m][9] <= sy3:
                    QLQPJB.append(2)
                    QLQPJB1.append(QLQPJB)
                    QLQPJB = []
                else:
                    QLQPJB.append(1)
                    QLQPJB1.append(QLQPJB)
                QLQPJB = []

            if self.ui.checkBox_5.isChecked():
                n = 5
                if self.qlqTableList[m][9] > xs1:
                    QLQPJB.append(4)
                    QLQPJB1.append(QLQPJB)
                    QLQPJB = []
                elif self.qlqTableList[m][9] > xs2:
                    QLQPJB.append(4)
                    QLQPJB1.append(QLQPJB)
                    QLQPJB = []
                elif self.qlqTableList[m][9] > xs3:
                    QLQPJB.append(4)
                    QLQPJB1.append(QLQPJB)
                    QLQPJB = []
                else:
                    QLQPJB.append(4)
                    QLQPJB1.append(QLQPJB)
                    QLQPJB = []

            QLQPJB2.append(QLQPJB1)

            pjb = []
            for i in range(4):
                pjb.append(0) # 评价表

            for i in range(len(QLQPJB1)):
                for j in range(len(QLQPJB1[i])):
                    if QLQPJB1[i][j] == 4:
                        pjb[0] = pjb[0] + 1
                    elif QLQPJB1[i][j] == 3:
                        pjb[1] = pjb[1] + 1
                    elif QLQPJB1[i][j] == 2:
                        pjb[2] = pjb[2] + 1
                    elif QLQPJB1[i][j] == 1:
                        pjb[3] = pjb[3] + 1


            qz = []
            jg = 0
            for i in range(3):
                qz.append(1 / len(QLQPJB1))  # 权重
                jg = jg + qz[i] * float(pjb[i]) # 结果
            if len(self.qlqTableList[m]) ==11:
                self.qlqTableList[m][10] = 100*jg
            else:
                self.qlqTableList[m].append(100*jg)

        print(self.qlqTableList)

        headerText = ["潜力区序号", "层号", "平面规模", "平均含油饱和度", "平均有效厚度", "平均渗透率", "平均孔隙度",
                      "剩余油量", "井数量", "平均水淹程度","评分"]

        self.ui.tableWidget_6.setColumnCount(len(headerText))
        self.ui.tableWidget_6.setHorizontalHeaderLabels(headerText)
        self.ui.tableWidget_6.clearContents()
        self.ui.tableWidget_6.setRowCount(len(self.qlqTableList))
        self.ui.tableWidget_6.setAlternatingRowColors(True)


        for i in range(0,len(self.qlqTableList)):
            for j in range(0,len(self.qlqTableList[i])):

                item = QTableWidgetItem(str(self.qlqTableList[i][j]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled
                            | Qt.ItemIsUserCheckable)  # 不允许编辑文字
                self.ui.tableWidget_6.setItem(i, j, item)

    @pyqtSlot(str)  #小模型画图
    def on_comboBox_3_activated(self, curText):

        comBoxin = self.ui.comboBox_3.currentIndex()
        if comBoxin > 0:
            comBoxzhi = int(self.ui.comboBox_3.currentText())

            self.ui.comboBox_4.clear()
            self.ui.comboBox_5.clear()

            self.ui.comboBox_4.addItem("选择目标井井号")
            self.ui.comboBox_5.addItem("选择相关注水井")

            for i in range(len(self.qlqTable[comBoxzhi]["well"])):
                self.ui.comboBox_4.addItem(str(self.qlqTable[comBoxzhi]["well"][i]))
                self.ui.comboBox_5.addItem(str(self.qlqTable[comBoxzhi]["well"][i]))


            bj = 0 #用于标记所选的潜力区是该层内的第几个潜力区，便于后面选择左边矩阵
            for i in range(int(comBoxzhi)):
                if self.qlqTableList[i][1] == self.qlqTableList[comBoxzhi][1]:
                    bj = bj + 1


            xmax = max(list(self.qlqContours[self.qlqTableList[comBoxzhi][1]])[bj-1][:, 1])
            xmin = min(list(self.qlqContours[self.qlqTableList[comBoxzhi][1]])[bj-1][:, 1])
            ymax = max(list(self.qlqContours[self.qlqTableList[comBoxzhi][1]])[bj-1][:, 0])
            ymin = min(list(self.qlqContours[self.qlqTableList[comBoxzhi][1]])[bj-1][:, 0])

            print(xmax)
            print(xmin)
            print(ymax)
            print(ymin)

            x = BHD[self.qlqTableList[comBoxzhi][1]][0]  # float 型
            y = BHD[self.qlqTableList[comBoxzhi][1]][1]
            v = BHD[self.qlqTableList[comBoxzhi][1]][2]

            x = np.array(x)
            y = np.array(y)
            v = np.array(v)

            x = x.T
            y = y.T
            v = v.T

            xb = list(range(int(xmin), int(xmax), self.stepx))
            yb = list(range(int(ymin), int(ymax), self.stepy))

            xb = np.array(xb)
            yb = np.array(yb)

            xb, yb = np.meshgrid(xb, yb)

            self.XMXxb = xb
            self.XMXyb = yb

            bhdq = griddata((x, y), v, (xb, yb), method="linear")


            self.qlqBinary[comBoxzhi] = bhdq
            self.qlqXb[comBoxzhi] = xb
            self.qlqYb[comBoxzhi] = yb

            title ="潜力区" + str(comBoxzhi)
            self.fig1 = QmyFigure(self)
            self.fig1.setAttribute(Qt.WA_DeleteOnClose)
            curIndex = self.ui.tabWidget.addTab(self.fig1, title)  # 添加到tabWidget

            self.ui.tabWidget.setCurrentIndex(curIndex)
            self.ax1 = self.fig1.fig.add_subplot(1, 1, 1)  # 子图1
            self.ax1.set_xlabel('X 轴')  # X轴标题
            self.ax1.set_ylabel('Y 轴')  # Y轴标题
            self.ax1.set_title(title)

            im1 = self.ax1.pcolormesh(self.qlqXb[comBoxzhi], self.qlqYb[comBoxzhi], self.qlqBinary[comBoxzhi])
            self.fig1.fig.colorbar(im1, ax=self.ax1)

    @pyqtSlot(str)  # 选择目标井
    def on_comboBox_4_activated(self, curText):

        comBoxin = self.ui.comboBox_4.currentIndex()
        if comBoxin > 0:

            comBoxzhi = self.ui.comboBox_4.currentText() #所选的目标井

            jgjpj = []
            jgjpj2 = []
            #结构井评价，用于统计目标井周围的注水井的信息
            for i in range(len(DJDZSJ)):
                if comBoxzhi == list(DJDZSJ.keys())[i]:
                    if DJDZSJ[list(DJDZSJ.keys())[i]][2] == '0':
                        mbjy = float(DJDZSJ[list(DJDZSJ.keys())[i]][0]) #目标井y轴坐标
                        mbjx = float(DJDZSJ[list(DJDZSJ.keys())[i]][1]) #目标井x轴坐标
                    else:
                        mbjy = float(DJDZSJ[list(DJDZSJ.keys())[i]][2])
                        mbjx = float(DJDZSJ[list(DJDZSJ.keys())[i]][3])
            jgjpj.append("目标井")
            jgjpj.append(mbjx)
            jgjpj.append(mbjy)
            jgjpj2.append(jgjpj)
            jgjpj = []

            if self.mbj == ["填充"]:
                self.im2.remove()
                self.im2 = self.ax1.scatter(mbjx,mbjy,c='red',s=100) #画目标井
            else:
                self.im2 = self.ax1.scatter(mbjx, mbjy, c='red', s=100)  # 画目标井
            self.fig1.fig.canvas.draw()  ##刷新
            self.mbj = ["填充"]

    @pyqtSlot(str)  # 选择相关注水井
    def on_comboBox_5_activated(self, curText):

        comBoxin = self.ui.comboBox_5.currentIndex()
        if comBoxin > 0:
            comBoxzhi = self.ui.comboBox_5.currentText() #所选的注水井

            jgjpj = []
            for i in range(len(DJDZSJ)):
                if comBoxzhi == list(DJDZSJ.keys())[i]:
                    if DJDZSJ[list(DJDZSJ.keys())[i]][2] == '0':
                        mbjy1 = float(DJDZSJ[list(DJDZSJ.keys())[i]][0]) #目标井y轴坐标
                        mbjx1 = float(DJDZSJ[list(DJDZSJ.keys())[i]][1]) #目标井x轴坐标
                    else:
                        mbjy1 = float(DJDZSJ[list(DJDZSJ.keys())[i]][2])
                        mbjx1 = float(DJDZSJ[list(DJDZSJ.keys())[i]][3])
            jgjpj.append(comBoxzhi)#选择目标井周围的注水井
            jgjpj.append(mbjx1)
            jgjpj.append(mbjy1)
            jgjpj1.append(jgjpj)
            jgjpj = []

            im3 = self.ax1.scatter(mbjx1, mbjy1, c='blue', s=100) #画注水井
            print(jgjpj1)
            self.fig1.fig.canvas.draw()  ##刷新

    @pyqtSlot()#创建复杂结构井部署方案
    def on_pushButton_7_clicked(self):
        comBoxin = self.ui.comboBox_4.currentIndex()
        if comBoxin > 0:
            comBoxzhi = self.ui.comboBox_4.currentText() # 所选的目标井

            jgjpj = []
            # 结构井评价，用于统计目标井周围的注水井的信息
            for i in range(len(DJDZSJ)):
                if comBoxzhi == list(DJDZSJ.keys())[i]:
                    if DJDZSJ[list(DJDZSJ.keys())[i]][2] == '0':
                        mbjy = float(DJDZSJ[list(DJDZSJ.keys())[i]][0])  # 目标井y轴坐标
                        mbjx = float(DJDZSJ[list(DJDZSJ.keys())[i]][1])  # 目标井x轴坐标
                    else:
                        mbjy = float(DJDZSJ[list(DJDZSJ.keys())[i]][2])
                        mbjx = float(DJDZSJ[list(DJDZSJ.keys())[i]][3])

            im4 = self.ax1.plot([mbjx, mbjx], [mbjy, mbjy + 150],c='red')
            jgjpj.append("方案一")
            jgjpj.append(mbjx)
            jgjpj.append(mbjy + 150)
            jgjpj2.append(jgjpj)
            jgjpj = []
            im5 = self.ax1.plot([mbjx, mbjx + 106], [mbjy, mbjy + 106], c='red')
            jgjpj.append("方案二")
            jgjpj.append(mbjx + 106)
            jgjpj.append(mbjy + 106)
            jgjpj2.append(jgjpj)
            jgjpj = []
            im6 = self.ax1.plot([mbjx, mbjx + 150], [mbjy, mbjy], c='red')
            jgjpj.append("方案三")
            jgjpj.append(mbjx + 150)
            jgjpj.append(mbjy)
            jgjpj2.append(jgjpj)
            jgjpj = []
            im7 = self.ax1.plot([mbjx, mbjx + 106], [mbjy, mbjy - 106], c='red')
            jgjpj.append("方案四")
            jgjpj.append(mbjx + 106)
            jgjpj.append(mbjy - 106)
            jgjpj2.append(jgjpj)
            jgjpj = []
            im8 = self.ax1.plot([mbjx, mbjx], [mbjy, mbjy - 150], c='red')
            jgjpj.append("方案五")
            jgjpj.append(mbjx)
            jgjpj.append(mbjy - 150)
            jgjpj2.append(jgjpj)
            jgjpj = []
            im9 = self.ax1.plot([mbjx, mbjx - 106], [mbjy, mbjy - 106], c='red')
            jgjpj.append("方案六")
            jgjpj.append(mbjx - 106)
            jgjpj.append(mbjy - 106)
            jgjpj2.append(jgjpj)
            jgjpj = []
            im10 = self.ax1.plot([mbjx, mbjx - 150], [mbjy, mbjy], c='red')
            jgjpj.append("方案七")
            jgjpj.append(mbjx - 150)
            jgjpj.append(mbjy)
            jgjpj2.append(jgjpj)
            jgjpj = []
            im11 = self.ax1.plot([mbjx, mbjx - 106], [mbjy, mbjy + 106], c='red')
            jgjpj.append("方案八")
            jgjpj.append(mbjx - 106)
            jgjpj.append(mbjy + 106)
            jgjpj2.append(jgjpj)
            jgjpj = []

            print(jgjpj2)

            self.fig1.fig.canvas.draw()  ##刷新
    @pyqtSlot()#计算流动势/动量势
    def on_pushButton_8_clicked(self):

        for i in range(1,len(jgjpj2)): #侧钻井
            for j in range(len(jgjpj1)): #注水井
                Shi = 0
                d11 = 0
                d1 = round(((jgjpj1[j][2] - jgjpj2[0][2]) ** 2 + (jgjpj1[j][1] - jgjpj2[0][1]) ** 2) ** 0.5)
                d2 = round(((jgjpj1[j][2] - jgjpj2[i][2]) ** 2 + (jgjpj1[j][1] - jgjpj2[i][1]) ** 2) ** 0.5)

                for k in range(min(list([d1,d2])),max(list([d1,d2]))):
                    Shi = Shi + 3.14 * 0.3 * self.stepx / np.log(k * 100 / 10)
                    d11 = Shi * np.cos(np.arctan(((jgjpj2[0][1] + jgjpj2[i][1]) / 2 - jgjpj1[j][1]) / ((jgjpj2[0][2] + jgjpj2[i][2]) / 2 - jgjpj1[j][2])))

                    if jgjpj1[j][2] > (jgjpj2[0][2] + jgjpj2[i][2]) / 2:
                        d11 = d11 * -1

                jgjpj1[j].append(Shi)
                jgjpj1[j].append(d11)

            lShi = 0
            dShi = 0

            for j in range(len(jgjpj1)):
                for k in range(3,len(jgjpj1[j])):
                    lShi = lShi + jgjpj1[j][3]
                    dShi = dShi + jgjpj1[j][4]

            jgjpj2[i].append(lShi)
            jgjpj2[i].append(abs(dShi))

        jgjpj2[0].append("流量势")
        jgjpj2[0].append("动量势")

        print(jgjpj2)

        headerText = ["方案号", "X坐标", "Y坐标", "流量势", "能量势"]

        self.ui.tableWidget_7.setColumnCount(len(headerText))
        self.ui.tableWidget_7.setHorizontalHeaderLabels(headerText)
        self.ui.tableWidget_7.clearContents()
        self.ui.tableWidget_7.setRowCount(len(jgjpj2))
        self.ui.tableWidget_7.setAlternatingRowColors(True)

        for i in range(0, len(jgjpj2)):
            for j in range(0, len(jgjpj2[i])):
                item = QTableWidgetItem(str(jgjpj2[i][j]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled
                          | Qt.ItemIsUserCheckable)  # 不允许编辑文字
                self.ui.tableWidget_7.setItem(i, j, item)



    @pyqtSlot()#导出小模型
    def on_pushButton_9_clicked(self):

        labText = "正在导出小模型..."  # 文本信息
        btnText = "取消"  # "取消"按钮的标
        minV = 0
        maxV = len(self.qlqFloor)

        dlgProgress = QProgressDialog(labText, btnText, minV, maxV, self)
        dlgProgress.setWindowTitle("导出中")
        dlgProgress.setWindowModality(Qt.WindowModal)  # 模态对话框
        dlgProgress.setAutoReset(True)  # value()达到最大值时自动调用reset()
        dlgProgress.setAutoClose(True)  # 调用reset()时隐藏窗口

        pross = 0

        for qlqFloorName in self.qlqFloor:
            pross = pross + 1

            dlgProgress.setValue(pross)
            dlgProgress.setLabelText("正在计算数据,第 %d 个" % pross)

            x = BHD[qlqFloorName][0]  # float 型
            y = BHD[qlqFloorName][1]
            v = BHD[qlqFloorName][2]

            for i in range(len(v)):
                if v[i] == -999:
                    v[i] = 0

            x = np.array(x)
            y = np.array(y)
            v = np.array(v)

            x = x.T
            y = y.T
            v = v.T


            xb = self.XMXxb
            yb = self.XMXyb



            bhdq = griddata((x, y), v, (xb, yb), method="linear")
            self.XMXBHD.append(bhdq)



            floor = CJDYSJ[qlqFloorName]  # float 型
            sycd = {}

            floor = np.array(floor)
            floor = floor.T
            floor = floor.tolist()
            # wellNum = floor[2]
            x = []
            y = []

            for i, sycdaction in enumerate(floor[16]):
                if sycdaction != "":
                    sycd[floor[2][i]] = sycdaction

            bj1 = 1
            bj2 = 1
            yxhd = []
            yxhd1 = float(floor[13][0])
            kxd = []
            kxd1 = float(floor[14][0])
            stl = []
            stl1 = float(floor[15][0])
            wellNum = []

            for i in range(1, len(floor[0]) - 1):
                if floor[2][i] == floor[2][i - 1]:

                    yxhd1 = yxhd1 + float(floor[13][i])
                    if float(floor[14][i]) == 0:
                        kxd1 = kxd1 + float(floor[14][i])
                    else:
                        bj1 = bj1 + 1
                        kxd1 = kxd1 + float(floor[14][i])

                    if float(floor[15][i]) == 0:
                        stl1 = stl1 + float(floor[15][i])
                    else:
                        bj2 = bj2 + 1
                        stl1 = stl1 + float(floor[15][i])
                else:
                    for j in range(len(DJDZSJ)):
                        if floor[2][i - 1] == list(DJDZSJ.keys())[j]:
                            if DJDZSJ[list(DJDZSJ.keys())[j]][2] == '0':
                                y.append(DJDZSJ[list(DJDZSJ.keys())[j]][0])
                                x.append(DJDZSJ[list(DJDZSJ.keys())[j]][1])
                            else:
                                y.append(DJDZSJ[list(DJDZSJ.keys())[j]][2])
                                x.append(DJDZSJ[list(DJDZSJ.keys())[j]][3])
                            wellNum.append(floor[2][i - 1])
                            yxhd.append(str(yxhd1))
                            kxd.append(str(kxd1 / bj1))
                            stl.append(str(stl1 / bj2))

                    bj1 = 1
                    bj2 = 1
                    yxhd1 = float(floor[13][i])
                    kxd1 = float(floor[14][i])
                    stl1 = float(floor[15][i])

            x = np.array(x)
            y = np.array(y)
            yxhd = np.array(yxhd)
            stl = np.array(stl)
            kxd = np.array(kxd)

            x = x.T
            y = y.T
            yxhd = yxhd.T
            stl = stl.T
            kxd = kxd.T

            xb = self.XMXxb
            yb = self.XMXyb

            yxhdq = griddata((x, y), yxhd, (xb, yb), method="linear")
            stlq = griddata((x, y), stl, (xb, yb), method="linear")
            kxdq = griddata((x, y), kxd, (xb, yb), method="linear")

            self.XMXKXD.append(kxdq)
            self.XMXSTL.append(stlq)
            self.XMXYXHD.append(yxhdq)



        # #####################################################################################################

        curPath = QDir.currentPath()  # 获取系统当前目录
        title = "另存为一个文件"
        filt = "(*.txt);;所有文件(*.*)"
        fileName, flt = QFileDialog.getSaveFileName(self, title, curPath, filt)
        if (fileName == ""):
            return
        if self.__saveByStream(fileName):
            print(fileName)
        else:
            QMessageBox.critical(self, "错误", "保存文件失败")

    def __saveByStream(self, fileName):  ##用 QTextStream 保存文件
        fileDevice = QFile(fileName)
        if not fileDevice.open(QIODevice.WriteOnly | QIODevice.Text):
            return False
        try:
            fileStream = QTextStream(fileDevice)  # 用文本流读取文件
            fileStream.setAutoDetectUnicode(True)  # 自动检测Unicode
            fileStream.setCodec("utf-8")  # 必须设置编码,否则不能正常显示汉字

            fileStream << "RESULTS SIMULATOR STARS 201410\n" \
                          "INUNIT SI\n" \
                          "OUTUNIT SI \n" \
                          "OUTPRN GRID PRES TEMP SG SO SW VISO VISW \n" \
                          "OUTSRF GRID ADSORP CMPVISO CMPVISW FLUXRC PERMEFFI PERMEFFJ PERMEFFK PERMI PERMINTI PERMINTJ PERMINTK \n" \
                          "            PERMJ PERMK PRES SG SO MOLE SOLCONC STRMLN SW TEMP VISO VISW \n" \
                          "            VPOROS VPOROSGEO VPOROSTGEO W X Y \n" \
                          "REWIND 10\n" \
                          "OUTPRN ITER NEWTON\n" \
                          "WSRF WELL TIME \n" \
                          "WSRF GRID TNEXT\n" \
                          "WSRF SECTOR TIME\n" \
                          "OUTPRN WELL WELLCOMP\n" \
                          "WPRN GRID TNEXT\n" \
                          "RESULTS SUBMODEL_REFSS 428800\n" \
                          "RESULTS SUBMODEL_REFSS 5\n" \
                          "RESULTS SUBMODEL_REFSS 0\n" \
                          "RESULTS SUBMODEL_REFSS 0\n" \
                          "RESULTS SUBMODEL_REFSS 20\n" \
                          "RESULTS SUBMODEL_REFSS 428800\n" \
                          "RESULTS SUBMODEL_REFSS 0\n" \
                          "RESULTS SUBMODEL_REFSS 428800\n" \
                          "**  Distance units: m\n" \
                          "RESULTS XOFFSET           0.0000\n" \
                          "RESULTS YOFFSET           0.0000\n" \
                          "**  (DEGREES)\n" \
                          "RESULTS ROTATION           0.0000  **  (DEGREES)\n" \
                          "RESULTS AXES-DIRECTIONS 1.0 1.0 1.0\n" \
                          "RESULTS SUBMODEL_REFSS 686\n" \
                          "** ***************************************************************************\n" \
                          "** Definition of fundamental corner point grid\n" \
                          "** ***************************************************************************\n" \
                          "GRID VARI\t" # 使用流操作符写入
            fileStream << str(len(self.XMXxb[0])) + "\t"
            fileStream << str(len(self.XMXyb[0])) + "\t"
            fileStream << str(len(self.qlqFloor)) + "\t\n"
            fileStream << "KDIR DOWN\n" + str(len(self.XMXxb[0])) + "*" + str(self.stepx) + "\n"
            fileStream << "DJ JVAR \n" + str(len(self.XMXyb[0])) + "*" + str(self.stepy) + "\n"
            fileStream << "DK ALL\n"
            for f in self.XMXYXHD:
                for row in f:
                    for point in row:
                        if np.isnan(point) == True:
                            fileStream << "0" + "\t"
                        else:
                            fileStream << str(round(point, 2)) + "\t"
                    fileStream << "\n"

            fileStream << "NULL ALL\n"
            for f in self.XMXYXHD:
                for row in f:
                    for _ in row:
                            fileStream << "1" + "\t"
                    fileStream << "\n"

            fileStream << "POR ALL\n"
            for f in self.XMXKXD:
                for row in f:
                    for point in row:
                        if np.isnan(point) == True:
                            fileStream << "0" + "\t"
                        else:
                            fileStream << str(round(point, 2)) + "\t"
                    fileStream << "\n"

            fileStream << "PERMI ALL\n"
            for f in self.XMXSTL:
                for row in f:
                    for point in row:
                        if np.isnan(point) == True:
                            fileStream << "0" + "\t"
                        else:
                            fileStream << str(round(point, 2)) + "\t"
                    fileStream << "\n"

            fileStream << "PERMJ EQUALSI\n" \
                          "PERMK EQUALSI * 0.8\n" \
                          "END-GRID\n" \
                          "*ROCKTYPE 1\n" \
                          "*PRPOR 9376.6\n" \
                          "*CPOR 8.6E-06\n" \
                          "**  ==============  FLUID DEFINITIONS  ======================\n" \
                          "** Model and number of components\n" \
                          "MODEL 5 5 5 4\n" \
                          "COMPNAME 'WATER' 'Polymer' 'Alkaline' 'Surfact' 'OIL' \n" \
                          "CMM\n" \
                          "0.018 8 0.04 0.4 0.456\n" \
                          "PCRIT\n" \
                          "0 0 0 0 0 \n" \
                          "TCRIT\n" \
                          "0 0 0 0 0 \n" \
                          "PRSR 8000\n" \
                          "TEMR 50\n" \
                          "PSURF 101.325\n" \
                          "TSURF 25\n" \
                          "MASSDEN\n" \
                          "1000 0 0 0 866.5 \n" \
                          "CP\n" \
                          "3.75E-07 0 0 0 4.5E-06 \n" \
                          "AVISC\n" \
                          "1.2 50 1.2 1.2 7.09 \n" \
                          "BVISC\n" \
                          "0 0 0 0 0 \n" \
                          "VSMIXCOMP 'Polymer'\n" \
                          "VSMIXENDP 0 6.75E-06 \n" \
                          "VSMIXFUNC 0 0.2922029 0.3949899 0.4902958 0.5569731 0.6186517 0.6643415 0.7104549 0.7667288 0.8387194 0.8995727 \n" \
                          "**  ==============  ROCK-FLUID PROPERTIES  ======================\n" \
                          "*ROCKFLUID\n" \
                          "RPT 1 WATWET\n" \
                          "**        Sw       krw      krow      Pcow\n" \
                          "SWT\n" \
                          "        0.260              0              1      53.3\n" \
                          "        0.281           0.01   0.9321074965      36.3\n" \
                          "        0.320  0.02587519026   0.7963224894      28.3\n" \
                          "        0.359  0.04414003044   0.6506364922      22.8\n" \
                          "        0.389  0.05936073059   0.5417256011      20.0\n" \
                          "        0.418   0.0700152207   0.4526166902      17.5\n" \
                          "        0.447  0.08219178082   0.3776520509      14.8\n" \
                          "        0.477  0.09893455099   0.2927864215      12.0\n" \
                          "        0.505   0.1141552511   0.2206506365      10.3\n" \
                          "        0.535   0.1301272984   0.1640735502       9.3\n" \
                          "        0.564     0.14427157   0.1244695898       7.5\n" \
                          "        0.593   0.1555869873   0.1004243281       5.8\n" \
                          "        0.623   0.1739745403  0.08203677511       3.3\n" \
                          "        0.652   0.1937765205  0.06506364922       2.0\n" \
                          "        0.682   0.2121640736  0.04667609618       0.5\n" \
                          "         0.77   0.2531824611              0       0.2\n" \
                          "        1.000   0.3515981735              0       0.0\n" \
                          "**        Sl       krg      krog      Pcog\n" \
                          "SLT NOSWC\n" \
                          "            0         1         0         0\n" \
                          "         0.05    0.7905    0.0002         0\n" \
                          "       0.0805    0.5988    0.0064         0\n" \
                          "       0.0957    0.5162    0.0102         0\n" \
                          "       0.1262    0.3752    0.0184         0\n" \
                          "       0.1415    0.3159    0.0229         0\n" \
                          "        0.172    0.2176     0.034         0\n" \
                          "       0.1872    0.1777    0.0412         0\n" \
                          "       0.2177    0.1143    0.0613         0\n" \
                          "        0.233    0.0898    0.0755         0\n" \
                          "       0.2635    0.0531    0.1157         0\n" \
                          "       0.2635    0.0531    0.1157         0\n" \
                          "       0.2635    0.0531    0.1157         0\n" \
                          "       0.3702    0.0079    0.4913         0\n" \
                          "       0.4007    0.0042    0.7092         0\n" \
                          "       0.7589         0         1         0\n" \
                          "ADSCOMP 'Polymer' WATER\n" \
                          "*ADSPHBLK *W\n" \
                          "ADSTABLE\n" \
                          "**  Mole Fraction  Adsorbed moles per unit pore volume\n" \
                          "        0.00000000                              0.00000\n" \
                          "        0.00018000                              0.00030\n" \
                          "        0.00036000                              0.00040\n" \
                          "        0.00054000                              0.00041\n" \
                          "        0.00072000                              0.00043\n" \
                          "        0.00090000                              0.00045\n" \
                          "        0.00108000                              0.00047\n" \
                          "ADMAXT 4.450e-5\n" \
                          "ADRT 4.450e-5\n" \
                          "PORFT 0.9\n" \
                          "RRFT 2.5\n" \
                          "INITIAL\n" \
                          "VERTICAL DEPTH_AVE\n" \
                          "INITREGION 1\n" \
                          "REFPRES 7500\n" \
                          "REFDEPTH 750\n" \
                          "TEMP CON  50\n" \
                          "SW ALL\n"

            for f in self.XMXBHD:
                for row in f:
                    for point in row:
                        if np.isnan(point) == True:
                            fileStream << "0" + "\t"
                        else:
                            fileStream << str(round(1 - point, 2)) + "\t"
                    fileStream << "\n"


        finally:
            fileDevice.close()
        return True


if __name__ == "__main__":  # 用于当前窗体测试
    app = QApplication(sys.argv)  # 创建GUI应用程序
    form = QmyMainWindow()  # 创建窗体
    form.show()
    sys.exit(app.exec_())
