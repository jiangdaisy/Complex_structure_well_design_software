# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CSw_sjk.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import re
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtChart import QChartView



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(982, 636)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        self.treeWidget.setGeometry(QtCore.QRect(0, 30, 256, 541))
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "数据目录")
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        self.graphicsView = QChartView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(280, 30, 611, 541))
        self.graphicsView.setObjectName("graphicsView")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 982, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menu)
        self.menu_2.setObjectName("menu_2")
        self.menu_7 = QtWidgets.QMenu(self.menu)
        self.menu_7.setObjectName("menu_7")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        self.menu_4 = QtWidgets.QMenu(self.menubar)
        self.menu_4.setObjectName("menu_4")
        self.menu_6 = QtWidgets.QMenu(self.menu_4)
        self.menu_6.setObjectName("menu_6")
        self.menu_5 = QtWidgets.QMenu(self.menubar)
        self.menu_5.setObjectName("menu_5")
        MainWindow.setMenuBar(self.menubar)
        self.actionfd = QtWidgets.QAction(MainWindow)
        self.actionfd.setObjectName("actionfd")
        self.actionxi = QtWidgets.QAction(MainWindow)
        self.actionxi.setObjectName("actionxi")
        self.actionbao = QtWidgets.QAction(MainWindow)
        self.actionbao.setObjectName("actionbao")
        self.actionlingc = QtWidgets.QAction(MainWindow)
        self.actionlingc.setObjectName("actionlingc")
        self.actionfsd = QtWidgets.QAction(MainWindow)
        self.actionfsd.setObjectName("actionfsd")
        self.actionfds = QtWidgets.QAction(MainWindow)
        self.actionfds.setObjectName("actionfds")
        self.actionfda = QtWidgets.QAction(MainWindow)
        self.actionfda.setObjectName("actionfda")
        self.actionfdsa = QtWidgets.QAction(MainWindow)
        self.actionfdsa.setObjectName("actionfdsa")
        self.actionfda_2 = QtWidgets.QAction(MainWindow)
        self.actionfda_2.setObjectName("actionfda_2")
        self.actionfdf = QtWidgets.QAction(MainWindow)
        self.actionfdf.setObjectName("actionfdf")
        self.actionfdf_2 = QtWidgets.QAction(MainWindow)
        self.actionfdf_2.setObjectName("actionfdf_2")
        self.actionfds_2 = QtWidgets.QAction(MainWindow)
        self.actionfds_2.setObjectName("actionfds_2")
        self.actionfdf_4 = QtWidgets.QAction(MainWindow)
        self.actionfdf_4.setObjectName("actionfdf_4")
        self.actionfdf_5 = QtWidgets.QAction(MainWindow)
        self.actionfdf_5.setObjectName("actionfdf_5")
        self.actionfdf_6 = QtWidgets.QAction(MainWindow)
        self.actionfdf_6.setObjectName("actionfdf_6")
        self.actiongfd = QtWidgets.QAction(MainWindow)
        self.actiongfd.setObjectName("actiongfd")
        self.menu_2.addAction(self.actionbao)
        self.menu_2.addAction(self.actionlingc)
        self.menu_7.addAction(self.actiongfd)
        self.menu.addAction(self.actionfd)
        self.menu.addAction(self.actionxi)
        self.menu.addAction(self.menu_7.menuAction())
        self.menu.addAction(self.menu_2.menuAction())
        self.menu_3.addAction(self.actionfsd)
        self.menu_3.addAction(self.actionfds)
        self.menu_3.addAction(self.actionfda)
        self.menu_3.addAction(self.actionfdsa)
        self.menu_3.addAction(self.actionfda_2)
        self.menu_6.addAction(self.actionfds_2)
        self.menu_6.addAction(self.actionfdf_4)
        self.menu_4.addAction(self.actionfdf_2)
        self.menu_4.addAction(self.actionfdf)
        self.menu_4.addAction(self.menu_6.menuAction())
        self.menu_5.addAction(self.actionfdf_5)
        self.menu_5.addAction(self.actionfdf_6)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())
        self.menubar.addAction(self.menu_5.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, _translate("MainWindow", "模型数据"))
        self.treeWidget.topLevelItem(0).child(0).setText(0, _translate("MainWindow", "孔隙度"))
        self.treeWidget.topLevelItem(0).child(1).setText(0, _translate("MainWindow", "渗透率"))
        self.treeWidget.topLevelItem(0).child(2).setText(0, _translate("MainWindow", "沉积相"))
        self.treeWidget.topLevelItem(0).child(3).setText(0, _translate("MainWindow", "相渗曲线"))
        self.treeWidget.topLevelItem(0).child(4).setText(0, _translate("MainWindow", "含油饱和度"))
        self.treeWidget.topLevelItem(1).setText(0, _translate("MainWindow", "注采井数据"))
        self.treeWidget.topLevelItem(1).child(0).setText(0, _translate("MainWindow", "油水井史"))
        self.treeWidget.topLevelItem(1).child(1).setText(0, _translate("MainWindow", "沉积单元数据"))
        self.treeWidget.topLevelItem(1).child(2).setText(0, _translate("MainWindow", "射孔数据"))
        self.treeWidget.topLevelItem(1).child(3).setText(0, _translate("MainWindow", "吸水剖面数据"))
        self.treeWidget.topLevelItem(1).child(4).setText(0, _translate("MainWindow", "单井地质数据"))
        self.treeWidget.topLevelItem(1).child(5).setText(0, _translate("MainWindow", "措施数据"))
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.menu.setTitle(_translate("MainWindow", "数据库"))
        self.menu_2.setTitle(_translate("MainWindow", "保存数据库"))
        self.menu_7.setTitle(_translate("MainWindow", "导入数据库"))
        self.menu_3.setTitle(_translate("MainWindow", "属性插值计算"))
        self.menu_4.setTitle(_translate("MainWindow", "潜力区筛选与评价"))
        self.menu_6.setTitle(_translate("MainWindow", "潜力区评价"))
        self.menu_5.setTitle(_translate("MainWindow", "复杂结构井设计"))
        self.actionfd.setText(_translate("MainWindow", "查看数据库"))
        self.actionxi.setText(_translate("MainWindow", "新建数据库"))
        self.actionbao.setText(_translate("MainWindow", "保存"))
        self.actionlingc.setText(_translate("MainWindow", "另存为"))
        self.actionfsd.setText(_translate("MainWindow", "计算所有参数"))
        self.actionfds.setText(_translate("MainWindow", "孔隙度计算"))
        self.actionfda.setText(_translate("MainWindow", "渗透率计算"))
        self.actionfdsa.setText(_translate("MainWindow", "有效厚度计算"))
        self.actionfda_2.setText(_translate("MainWindow", "砂岩厚度计算"))
        self.actionfdf.setText(_translate("MainWindow", "潜力区验证"))
        self.actionfdf_2.setText(_translate("MainWindow", "潜力区筛选"))
        self.actionfds_2.setText(_translate("MainWindow", "模糊综合评价法"))
        self.actionfdf_4.setText(_translate("MainWindow", "随机森林评价法"))
        self.actionfdf_5.setText(_translate("MainWindow", "设计方案优选"))
        self.actionfdf_6.setText(_translate("MainWindow", "导出为CMG模型"))
        self.actiongfd.setText(_translate("MainWindow", "沉积相"))
        # self.treeWidget.clicked.connect(self.on_treeWidget_clicked)
        # print('init')





