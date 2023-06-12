import re
import sys
from sklearn.ensemble import RandomForestClassifier
import random

from skimage import measure
import cv2
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSlot, Qt, QThread, pyqtSignal
import matplotlib as mpl
import matplotlib.style as mplStyle

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

CJX = {}
BHD = {}
KXD = {}
STL = {}

DJDZSJ = {}
XSPMSJ = []
SKSJ = []
CSSJ = []
CJDYSJ = {}
ZSJS = []
XSQX = []
CYJS = []
DS = []
CJDYZB = {}



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

                im = ax1.pcolormesh(xq, yq, vq, )
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

        except AttributeError:
            print("AttributeError")

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
                while not fileStream.atEnd():
                    lineStr = fileStream.readLine()  # 返回QByteArray类型

                    lineList = lineStr.split("\t")

                    XSPMSJ.append(lineList)

            except UnicodeDecodeError:
                print(fileName[0] + "文件编码格式有误！")

            finally:
                fileDevice.close()

            # print(self.XSPMSJ[-1])

            item = QTreeWidgetItem()
            item.setText(0, "吸水剖面数据")
            item.setIcon(0, QtGui.QIcon('images/29.ico'))
            self.ui.treeWidget.topLevelItem(1).child(3).addChild(item)
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
                while not fileStream.atEnd():
                    lineStr = fileStream.readLine()  # 返回QByteArray类型

                    lineList = lineStr.split("\t")
                    XSPMSJ.append(lineList)

            except UnicodeDecodeError:
                print(fileName[0] + "文件编码格式有误！")

            finally:
                fileDevice.close()

            # print(self.XSPMSJ[-1])

            item = QTreeWidgetItem()
            item.setText(0, "射孔数据")
            item.setIcon(0, QtGui.QIcon('images/29.ico'))
            self.ui.treeWidget.topLevelItem(1).child(2).addChild(item)
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
                while not fileStream.atEnd():
                    lineStr = fileStream.readLine()  # 返回QByteArray类型

                    lineList = lineStr.split("\t")
                    CSSJ.append(lineList)

            except UnicodeDecodeError:
                print(fileName[0] + "文件编码格式有误！")

            finally:
                fileDevice.close()

            # print(self.XSPMSJ[-1])

            item = QTreeWidgetItem()
            item.setText(0, "措施数据")
            item.setIcon(0, QtGui.QIcon('images/29.ico'))
            self.ui.treeWidget.topLevelItem(1).child(5).addChild(item)
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
                while not fileStream.atEnd():
                    lineStr = fileStream.readLine()  # 返回QByteArray类型

                    lineList = lineStr.split("\t")
                    ZSJS.append(lineList)

            except UnicodeDecodeError:
                print(fileName[0] + "文件编码格式有误！")

            finally:
                fileDevice.close()

            # print(self.XSPMSJ[-1])

            item = QTreeWidgetItem()
            item.setText(0, "注水井史")
            item.setIcon(0, QtGui.QIcon('images/29.ico'))
            self.ui.treeWidget.topLevelItem(1).child(0).addChild(item)
        self.ui.treeWidget.topLevelItem(1).child(0).setExpanded(True)

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


        for i in range(1,index):
            listrow = []

            # 潜力区编号
            listrow.append(self.qlqTable[i]["index"])
            self.ui.comboBox_2.addItem(str(self.qlqTable[i]["index"]))
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
            item = QTableWidgetItem(str(self.qlqTable[i]["avsycd"]))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled
                          | Qt.ItemIsUserCheckable)  # 不允许编辑文字
            self.ui.tableWidget.setItem(i-1, 9,item)

            # a = random.randrange(0, 2, 1)
            # listrow.append(a)
            self.qlqTableList.append(listrow)








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

    @pyqtSlot(str)  #层间联通性判断得下拉列表变化时运行得函数
    def on_comboBox_2_activated(self, curText):

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

        for i, row in  enumerate(self.qlqTableList):

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







if __name__ == "__main__":  # 用于当前窗体测试
    app = QApplication(sys.argv)  # 创建GUI应用程序
    form = QmyMainWindow()  # 创建窗体
    form.show()
    sys.exit(app.exec_())
