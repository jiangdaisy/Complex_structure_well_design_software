# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CSw_sjk.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1709, 1206)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        self.treeWidget.setMaximumSize(QtCore.QSize(244, 16777215))
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
        self.horizontalLayout_2.addWidget(self.treeWidget)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.horizontalLayout_2.addWidget(self.tabWidget)
        self.toolBox = QtWidgets.QToolBox(self.centralwidget)
        self.toolBox.setObjectName("toolBox")
        self.page = QtWidgets.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 488, 1033))
        self.page.setObjectName("page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.page)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_6 = QtWidgets.QLabel(self.page)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(24)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.page)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.label_3 = QtWidgets.QLabel(self.page)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(24)
        self.label_3.setFont(font)
        self.label_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lineEdit = QtWidgets.QLineEdit(self.page)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(24)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_3.addWidget(self.lineEdit)
        self.label_4 = QtWidgets.QLabel(self.page)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.label_2 = QtWidgets.QLabel(self.page)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(24)
        self.label_2.setFont(font)
        self.label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.page)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(24)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_3.addWidget(self.lineEdit_2)
        self.label_5 = QtWidgets.QLabel(self.page)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(24)
        self.label_5.setFont(font)
        self.label_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.pushButton_2 = QtWidgets.QPushButton(self.page)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(16)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.toolBox.addItem(self.page, "")
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 488, 1033))
        self.page_2.setObjectName("page_2")
        self.gridLayout = QtWidgets.QGridLayout(self.page_2)
        self.gridLayout.setObjectName("gridLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.page_2)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 6, 0, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.page_2)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(16)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 3, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.page_2)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(16)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 5, 0, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.page_2)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(24)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 0, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_10 = QtWidgets.QLabel(self.page_2)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(24)
        self.label_10.setFont(font)
        self.label_10.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_5.addWidget(self.label_10)
        self.label_11 = QtWidgets.QLabel(self.page_2)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(24)
        self.label_11.setFont(font)
        self.label_11.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_5.addWidget(self.label_11)
        self.gridLayout.addLayout(self.horizontalLayout_5, 1, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.page_2)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(24)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 4, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.page_2)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(24)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout_4.addWidget(self.lineEdit_3)
        self.label_7 = QtWidgets.QLabel(self.page_2)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(24)
        self.label_7.setFont(font)
        self.label_7.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_4.addWidget(self.label_7)
        self.label_8 = QtWidgets.QLabel(self.page_2)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(24)
        self.label_8.setFont(font)
        self.label_8.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_4.addWidget(self.label_8)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.page_2)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(24)
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.horizontalLayout_4.addWidget(self.lineEdit_4)
        self.label_9 = QtWidgets.QLabel(self.page_2)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(24)
        self.label_9.setFont(font)
        self.label_9.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_4.addWidget(self.label_9)
        self.gridLayout.addLayout(self.horizontalLayout_4, 2, 0, 1, 1)
        self.toolBox.addItem(self.page_2, "")
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setGeometry(QtCore.QRect(0, 0, 488, 1033))
        self.page_3.setObjectName("page_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.page_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_13 = QtWidgets.QLabel(self.page_3)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(24)
        self.label_13.setFont(font)
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.verticalLayout_2.addWidget(self.label_13)
        self.comboBox_2 = QtWidgets.QComboBox(self.page_3)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(24)
        self.comboBox_2.setFont(font)
        self.comboBox_2.setObjectName("comboBox_2")
        self.verticalLayout_2.addWidget(self.comboBox_2)
        self.tableWidget_2 = QtWidgets.QTableWidget(self.page_3)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        self.verticalLayout_2.addWidget(self.tableWidget_2)
        self.tableWidget_3 = QtWidgets.QTableWidget(self.page_3)
        self.tableWidget_3.setObjectName("tableWidget_3")
        self.tableWidget_3.setColumnCount(0)
        self.tableWidget_3.setRowCount(0)
        self.verticalLayout_2.addWidget(self.tableWidget_3)
        self.verticalLayout_2.setStretch(2, 1)
        self.verticalLayout_2.setStretch(3, 2)
        self.toolBox.addItem(self.page_3, "")
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setGeometry(QtCore.QRect(0, 0, 488, 1033))
        self.page_4.setObjectName("page_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.page_4)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.page_4)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(16)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout_3.addWidget(self.pushButton_4)
        self.pushButton_5 = QtWidgets.QPushButton(self.page_4)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(16)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")
        self.verticalLayout_3.addWidget(self.pushButton_5)
        self.tableWidget_4 = QtWidgets.QTableWidget(self.page_4)
        self.tableWidget_4.setObjectName("tableWidget_4")
        self.tableWidget_4.setColumnCount(0)
        self.tableWidget_4.setRowCount(0)
        self.verticalLayout_3.addWidget(self.tableWidget_4)
        self.toolBox.addItem(self.page_4, "")
        self.page_5 = QtWidgets.QWidget()
        self.page_5.setObjectName("page_5")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.page_5)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_14 = QtWidgets.QLabel(self.page_5)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(24)
        self.label_14.setFont(font)
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.verticalLayout_7.addWidget(self.label_14)
        self.pushButton_11 = QtWidgets.QPushButton(self.page_5)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(16)
        self.pushButton_11.setFont(font)
        self.pushButton_11.setObjectName("pushButton_11")
        self.verticalLayout_7.addWidget(self.pushButton_11)
        self.tableWidget_5 = QtWidgets.QTableWidget(self.page_5)
        self.tableWidget_5.setObjectName("tableWidget_5")
        self.tableWidget_5.setColumnCount(0)
        self.tableWidget_5.setRowCount(0)
        self.verticalLayout_7.addWidget(self.tableWidget_5)
        self.toolBox.addItem(self.page_5, "")
        self.horizontalLayout_2.addWidget(self.toolBox)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 4)
        self.horizontalLayout_2.setStretch(2, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1709, 23))
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
        self.actionBHD = QtWidgets.QAction(MainWindow)
        self.actionBHD.setObjectName("actionBHD")
        self.actionKXD = QtWidgets.QAction(MainWindow)
        self.actionKXD.setObjectName("actionKXD")
        self.actionSTL = QtWidgets.QAction(MainWindow)
        self.actionSTL.setObjectName("actionSTL")
        self.actiondataset = QtWidgets.QAction(MainWindow)
        self.actiondataset.setObjectName("actiondataset")
        self.actiondjdzsj = QtWidgets.QAction(MainWindow)
        self.actiondjdzsj.setObjectName("actiondjdzsj")
        self.actionxspmsj = QtWidgets.QAction(MainWindow)
        self.actionxspmsj.setObjectName("actionxspmsj")
        self.actionsksj = QtWidgets.QAction(MainWindow)
        self.actionsksj.setObjectName("actionsksj")
        self.actioncssj = QtWidgets.QAction(MainWindow)
        self.actioncssj.setObjectName("actioncssj")
        self.actioncjdysj = QtWidgets.QAction(MainWindow)
        self.actioncjdysj.setObjectName("actioncjdysj")
        self.actionzsjs = QtWidgets.QAction(MainWindow)
        self.actionzsjs.setObjectName("actionzsjs")
        self.actionxsqx = QtWidgets.QAction(MainWindow)
        self.actionxsqx.setObjectName("actionxsqx")
        self.actioncyjs = QtWidgets.QAction(MainWindow)
        self.actioncyjs.setObjectName("actioncyjs")
        self.actionds = QtWidgets.QAction(MainWindow)
        self.actionds.setObjectName("actionds")
        self.menu_2.addAction(self.actionbao)
        self.menu_2.addAction(self.actionlingc)
        self.menu_7.addAction(self.actiongfd)
        self.menu_7.addAction(self.actionBHD)
        self.menu_7.addAction(self.actionKXD)
        self.menu_7.addAction(self.actionSTL)
        self.menu_7.addAction(self.actiondjdzsj)
        self.menu_7.addAction(self.actionxspmsj)
        self.menu_7.addAction(self.actionsksj)
        self.menu_7.addAction(self.actioncssj)
        self.menu_7.addAction(self.actioncjdysj)
        self.menu_7.addAction(self.actionzsjs)
        self.menu_7.addAction(self.actionxsqx)
        self.menu_7.addAction(self.actioncyjs)
        self.menu_7.addAction(self.actionds)
        self.menu.addAction(self.actionfd)
        self.menu.addAction(self.actionxi)
        self.menu.addAction(self.menu_7.menuAction())
        self.menu.addAction(self.menu_2.menuAction())
        self.menu.addAction(self.actiondataset)
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
        self.toolBox.setCurrentIndex(4)
        self.toolBox.layout().setSpacing(10)
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
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))
        self.label_6.setText(_translate("MainWindow", "查看精度"))
        self.label.setText(_translate("MainWindow", "X"))
        self.label_3.setText(_translate("MainWindow", "Y"))
        self.lineEdit.setText(_translate("MainWindow", "50"))
        self.label_4.setText(_translate("MainWindow", "m"))
        self.label_2.setText(_translate("MainWindow", "X"))
        self.lineEdit_2.setText(_translate("MainWindow", "50"))
        self.label_5.setText(_translate("MainWindow", "m"))
        self.pushButton_2.setText(_translate("MainWindow", "确定"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), _translate("MainWindow", "查看数据"))
        self.pushButton_3.setText(_translate("MainWindow", "开始筛选"))
        self.pushButton.setText(_translate("MainWindow", "潜力区查看"))
        self.label_12.setText(_translate("MainWindow", "筛选精度"))
        self.label_10.setText(_translate("MainWindow", "X"))
        self.label_11.setText(_translate("MainWindow", "Y"))
        self.label_7.setText(_translate("MainWindow", "m"))
        self.label_8.setText(_translate("MainWindow", "X"))
        self.label_9.setText(_translate("MainWindow", "m"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), _translate("MainWindow", "潜力区筛选"))
        self.label_13.setText(_translate("MainWindow", "层间连通性判断"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_3), _translate("MainWindow", "层间连通性"))
        self.pushButton_4.setText(_translate("MainWindow", "导入模型"))
        self.pushButton_5.setText(_translate("MainWindow", "随机森林评价"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_4), _translate("MainWindow", "随机森林模型"))
        self.label_14.setText(_translate("MainWindow", "厚度识别"))
        self.pushButton_11.setText(_translate("MainWindow", "开始识别"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_5), _translate("MainWindow", "厚度识别"))
        self.menu.setTitle(_translate("MainWindow", "数据库"))
        self.menu_2.setTitle(_translate("MainWindow", "保存数据库"))
        self.menu_7.setTitle(_translate("MainWindow", "导入单项数据"))
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
        self.actionBHD.setText(_translate("MainWindow", "含油饱和度"))
        self.actionKXD.setText(_translate("MainWindow", "孔隙度"))
        self.actionSTL.setText(_translate("MainWindow", "渗透率"))
        self.actiondataset.setText(_translate("MainWindow", "导入数据库"))
        self.actiondjdzsj.setText(_translate("MainWindow", "单井地质数据"))
        self.actionxspmsj.setText(_translate("MainWindow", "吸水剖面数据"))
        self.actionsksj.setText(_translate("MainWindow", "射孔数据"))
        self.actioncssj.setText(_translate("MainWindow", "措施数据"))
        self.actioncjdysj.setText(_translate("MainWindow", "沉积单元数据"))
        self.actionzsjs.setText(_translate("MainWindow", "注水井史"))
        self.actionxsqx.setText(_translate("MainWindow", "相渗曲线"))
        self.actioncyjs.setText(_translate("MainWindow", "采油井史"))
        self.actionds.setText(_translate("MainWindow", "顶深"))
