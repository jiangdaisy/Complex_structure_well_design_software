import re
import sys

from PyQt5.QtCore import pyqtSlot, Qt
import matplotlib as mpl
import matplotlib.style as mplStyle
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from scipy.interpolate import griddata
from CSw_sjk import Ui_MainWindow

from PyQt5.QtWidgets import (QApplication, QMainWindow,
                             QSplitter, QColorDialog, QLabel, QComboBox, QTreeWidgetItem)
from PyQt5.QtCore import pyqtSlot, QDir, QIODevice, QFile, QTextStream
from PyQt5.QtWidgets import QFileDialog
import numpy as np


class QmyMainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)  # 调用父类构造函数，创建窗体
        self.ui = Ui_MainWindow()  # 创建UI对象
        self.ui.setupUi(self)  # 构造UI界面

        # 展开节点
        self.ui.treeWidget.topLevelItem(0).setExpanded(True)
        self.ui.treeWidget.topLevelItem(1).setExpanded(True)
        self.ui.treeWidget.setAlternatingRowColors(True)
        self.ui.treeWidget.clicked.connect(self.on_treeWidget_clicked)

        self.CJX = {}

        mplStyle.use("classic")  # 使用样式，必须在绘图之前调用,修改字体后才可显示汉字
        mpl.rcParams['font.sans-serif'] = ['KaiTi', 'SimHei']  # 显示汉字为 楷体， 汉字不支持 粗体，斜体等设置
        mpl.rcParams['font.size'] = 12
        ##  Windows自带的一些字体
        ##  黑体：SimHei 宋体：SimSun 新宋体：NSimSun 仿宋：FangSong  楷体：KaiTi
        mpl.rcParams['axes.unicode_minus'] = False  # 减号unicode编码

        self.__fig = None  # Figue对象
        self.__curAxes = None  # 当前操作的Axes，为了方便单独用变量
        self.__createFigure()  # 创建Figure和FigureCanvas对象，初始化界面
        # self.__drawFig2X1()  # 绘图

        ##  ==============自定义功能函数========================

    def __createFigure(self):
        ##      self.__fig=mpl.figure.Figure(figsize=(8, 5),constrained_layout=True, tight_layout=None)  #单位英寸
        ##      self.__fig=mpl.figure.Figure(figsize=(8, 5))  #单位英寸
        self.__fig = Figure()
        figCanvas = FigureCanvas(self.__fig)  # 创建FigureCanvas对象，必须传递一个Figure对象
        self.__fig.suptitle("suptitle:matplotlib in Qt GUI", fontsize=16, fontweight='bold')  # 总的图标题

        splitter = QSplitter(self)
        splitter.setOrientation(Qt.Horizontal)
        splitter.addWidget(self.ui.treeWidget)  # 左侧控制面板
        splitter.addWidget(figCanvas)  # 右侧FigureCanvas对象
        self.setCentralWidget(splitter)

    ##树组件响应画图
    @pyqtSlot()
    def on_treeWidget_clicked(self):
        itemParent = self.ui.treeWidget.currentItem().parent()
        item = self.ui.treeWidget.currentItem()

        if itemParent.text(0) == "沉积相":
            x = self.CJX[item.text(0)][0]  # float 型
            y = self.CJX[item.text(0)][1]
            v = self.CJX[item.text(0)][2]

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
        print(vq)
        vq = vq.astype(int)
        print(vq)

        f = np.array(vq)
        print(f.shape)

        ax1 = self.__fig.add_subplot(2, 1, 1, label="sin-cos plot")  # 子图1
        ax2 = self.__fig.add_subplot(2, 1, 2, label="sin-cos plot")

        ax1.pcolormesh(xq, yq, vq)
        ax2.scatter(x, y, v)
        # ax1.plot(t, y1, 'r-o', label="sin", linewidth=2, markersize=5)  # 绘制一条曲线
        # ax1.plot(t, y2, 'b--', label="cos", linewidth=2)  # 绘制一条曲线
        # ax1.set_xlabel('X 轴')  # X轴标题
        # ax1.set_ylabel('Y 轴')  # Y轴标题
        # ax1.set_xlim([0, 10])  # X轴坐标范围
        # ax1.set_ylim([-1.5, 1.5])  # Y轴坐标范围
        # ax1.set_title("三角函数曲线")
        ax1.legend()  # 自动创建图例
        self.__fig.canvas.draw()  ##刷新
        print(item.text(0))

    ##导入沉积相数据
    @pyqtSlot()
    def on_actiongfd_triggered(self):
        # print("test")
        curDir = QDir.currentPath()
        aDir = QFileDialog.getExistingDirectory(self, "选择一个目录",
                                                curDir, QFileDialog.ShowDirsOnly)
        dirObj = QDir(aDir)
        strList = dirObj.entryList(QDir.Files)
        # print(strList)
        for str in strList:
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
                    fileStream.setCodec("utf-8")  # 必须设置编码，否则不能正常显示汉字
                    while not fileStream.atEnd():
                        lineStr = fileStream.readLine()  # 返回QByteArray类型

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
                self.CJX[fileName[0][0:-4]] = floor  # 用文件名作为键值将不同文件的数据存储在字典中
                item = QTreeWidgetItem()
                item.setText(0, fileName[0][0:-4])
                self.ui.treeWidget.topLevelItem(0).child(2).addChild(item)

        self.ui.treeWidget.topLevelItem(0).child(2).setExpanded(True)
        # print(self.CJX["S21"])


if __name__ == "__main__":  # 用于当前窗体测试
    app = QApplication(sys.argv)  # 创建GUI应用程序
    form = QmyMainWindow()  # 创建窗体
    form.show()
    sys.exit(app.exec_())
