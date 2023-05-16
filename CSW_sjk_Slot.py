import re
import sys

from skimage import measure

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSlot, Qt, QThread, pyqtSignal
import matplotlib as mpl
import matplotlib.style as mplStyle

from scipy.interpolate import griddata

from CSw_sjk import Ui_MainWindow

from PyQt5.QtWidgets import (QApplication, QMainWindow,
                             QSplitter, QColorDialog, QLabel, QComboBox, QTreeWidgetItem, QProgressDialog)
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


class QmyMainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)  # 调用父类构造函数，创建窗体
        self.ui = Ui_MainWindow()  # 创建UI对象
        self.ui.setupUi(self)  # 构造UI界面

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

                xq = list(range(int(min(x)), int(max(x)), 50))
                yq = list(range(int(min(y)), int(max(y)), 50))

                xq = np.array(xq)
                yq = np.array(yq)

                xq, yq = np.meshgrid(xq, yq)

                vq = griddata((x, y), v, (xq, yq), method="linear")
                # print(vq.shape)
                # print(vq.shape[0])
                # print(vq.shape[1])
                # print(vq)
                for i in range(vq.shape[0]):
                    for j in range(vq.shape[1]):
                        if (np.isnan(vq[i][j]) == False):
                            # print(str(i)+" "+str(j))
                            # print(type(vq[i][j]))
                            # print(vq[i][j])
                            vq[i][j] = vq[i][j].astype(int)
                # print(vq)
                # print("1111111111")

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

                xq = list(range(int(min(x)), int(max(x)), 50))
                yq = list(range(int(min(y)), int(max(y)), 50))

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

                xq = list(range(int(min(x)), int(max(x)), 50))
                yq = list(range(int(min(y)), int(max(y)), 50))

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

                xq = list(range(int(min(x)), int(max(x)), 50))
                yq = list(range(int(min(y)), int(max(y)), 50))

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
                yxhd = floor[13]
                kxd = floor[14]
                stl = floor[15]

                for i in wellNum:
                    x.append(DJDZSJ[i][0])
                    y.append(DJDZSJ[i][1])

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

                xq = list(range(int(min(x)), int(max(x)), 50))
                yq = list(range(int(min(y)), int(max(y)), 50))

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

                im1 = ax1.pcolormesh(xq, yq, kxdq)
                fig1.fig.colorbar(im1, ax=ax1)

                im2 = ax2.pcolormesh(xq, yq, yxhdq)
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

                    floor = lineList[3] + lineList[4]
                    if floor in CJDYSJ:
                        CJDYSJ[floor].append(lineList)
                    else:
                        CJDYSJ[floor] = []
                        CJDYSJ[floor].append(lineList)
                        item = QTreeWidgetItem()
                        item.setText(0, floor)
                        item.setIcon(0, QtGui.QIcon('images/29.ico'))
                        self.ui.comboBox.addItem(floor)
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
    def on_pushButton_clicked(self):

        comBoxText = self.ui.comboBox.currentText()

        title = "潜力区筛选"
        fig1 = QmyFigure(self)
        fig1.setAttribute(Qt.WA_DeleteOnClose)
        curIndex = self.ui.tabWidget.addTab(fig1, title)  # 添加到tabWidget
        self.ui.tabWidget.setCurrentIndex(curIndex)

        floor = CJDYSJ[comBoxText]  # float 型
        floor = np.array(floor)
        floor = floor.T
        floor = floor.tolist()
        wellNum = floor[2]
        x = []
        y = []
        yxhd = floor[13]
        stl = floor[15]

        for i in wellNum:
            x.append(DJDZSJ[i][0])
            y.append(DJDZSJ[i][1])

        x = np.array(x)
        y = np.array(y)
        yxhd = np.array(yxhd)
        stl = np.array(stl)

        x = x.T
        y = y.T
        yxhd = yxhd.T
        stl = stl.T

        xq = list(range(int(min(x)), int(max(x)), 50))
        yq = list(range(int(min(y)), int(max(y)), 50))

        xq = np.array(xq)
        yq = np.array(yq)

        xq, yq = np.meshgrid(xq, yq)

        yxhdq = griddata((x, y), yxhd, (xq, yq), method="linear")
        stlq = griddata((x, y), stl, (xq, yq), method="linear")

        x = BHD[comBoxText][0]  # float 型
        y = BHD[comBoxText][1]
        v = BHD[comBoxText][2]

        for i in range(len(v)):
            if v[i] == -999:
                v[i] = 0

        x = np.array(x)
        y = np.array(y)
        v = np.array(v)

        x = x.T
        y = y.T
        v = v.T

        xb = list(range(int(min(x)), int(max(x)), 50))
        yb = list(range(int(min(y)), int(max(y)), 50))

        xb = np.array(xb)
        yb = np.array(yb)

        xb, yb = np.meshgrid(xb, yb)

        vq = griddata((x, y), v, (xb, yb), method="linear")

        print(yxhdq.shape)
        print(stlq.shape)
        print(vq.shape)




        # qlq = yxhdq
        #
        # for point,pointyxhdq,pointkxdq,pointstlq in qlq,yxhdq,kxdq,stlq:
        #     if np.isnan(point) == False:
        #         if pointkxdq > 2 and pointstlq > 200 :
        #             point = 1
        #         else:
        #             point = 0
        #
        #
        #
        # # # for i in range(vq.shape[0]):
        # # #     for j in range(vq.shape[1]):
        # # #         if np.isnan(vq[i][j]) == False:
        # # #             vq[i][j] = vq[i][j].astype(int)
        #
        # ax1 = fig1.fig.add_subplot(1, 1, 1, label="sin-cos plot")  # 子图1
        # ax1.set_xlabel('X 轴')  # X轴标题
        # ax1.set_ylabel('Y 轴')  # Y轴标题
        # ax1.set_title(title + "有效厚度展示")
        #
        # title = ""
        # fig2 = QmyFigure(self)
        # fig2.setAttribute(Qt.WA_DeleteOnClose)
        # curIndex = self.ui.tabWidget.addTab(fig2, title)  # 添加到tabWidget
        # self.ui.tabWidget.setCurrentIndex(curIndex)
        #
        # ax2 = fig2.fig.add_subplot(1, 1, 1, label="sin-cos plot")  # 子图2
        # ax2.set_xlabel('X 轴')  # X轴标题
        # ax2.set_ylabel('Y 轴')  # Y轴标题
        # ax2.set_title(title + "孔隙度展示")
        #
        # title = ""
        # fig3 = QmyFigure(self)
        # fig3.setAttribute(Qt.WA_DeleteOnClose)
        # curIndex = self.ui.tabWidget.addTab(fig3, title)  # 添加到tabWidget
        # self.ui.tabWidget.setCurrentIndex(curIndex)
        #
        # ax3 = fig3.fig.add_subplot(1, 1, 1, label="sin-cos plot")  # 子图3
        # ax3.set_xlabel('X 轴')  # X轴标题
        # ax3.set_ylabel('Y 轴')  # Y轴标题
        # ax3.set_title(title + "渗透率展示")
        #
        # im1 = ax1.pcolormesh(xq, yq, kxdq)
        # fig1.fig.colorbar(im1, ax=ax1)
        #
        # im2 = ax2.pcolormesh(xq, yq, yxhdq)
        # fig2.fig.colorbar(im2, ax=ax2)
        #
        # im3 = ax3.pcolormesh(xq, yq, stlq)
        # fig3.fig.colorbar(im3, ax=ax3)
        #
        # fig1.fig.canvas.draw()  ##刷新
        #
        # fig2.fig.canvas.draw()  ##刷新
        #
        # fig3.fig.canvas.draw()  ##刷新


        print("pushBotton")

if __name__ == "__main__":  # 用于当前窗体测试
    app = QApplication(sys.argv)  # 创建GUI应用程序
    form = QmyMainWindow()  # 创建窗体
    form.show()
    sys.exit(app.exec_())
