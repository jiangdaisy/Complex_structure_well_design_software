# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CSw_qlqyz.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1549, 769)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(50, 170, 321, 481))
        self.tableView.setObjectName("tableView")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(60, 80, 101, 41))
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(240, 80, 101, 41))
        self.textEdit_2.setObjectName("textEdit_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(70, 20, 301, 41))
        font = QtGui.QFont()
        font.setFamily("Adobe 黑体 Std R")
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(170, 90, 54, 21))
        font = QtGui.QFont()
        font.setFamily("Adobe 黑体 Std R")
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(360, 90, 54, 21))
        font = QtGui.QFont()
        font.setFamily("Adobe 黑体 Std R")
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(60, 670, 241, 21))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(60, 702, 231, 31))
        self.pushButton.setObjectName("pushButton")
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(460, 30, 241, 21))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(460, 80, 231, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.tableView_2 = QtWidgets.QTableView(self.centralwidget)
        self.tableView_2.setGeometry(QtCore.QRect(460, 120, 321, 131))
        self.tableView_2.setObjectName("tableView_2")
        self.tableView_3 = QtWidgets.QTableView(self.centralwidget)
        self.tableView_3.setGeometry(QtCore.QRect(460, 260, 321, 391))
        self.tableView_3.setObjectName("tableView_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(480, 660, 81, 41))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(600, 660, 81, 41))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(480, 700, 81, 41))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(600, 700, 81, 41))
        self.label_7.setObjectName("label_7")
        self.comboBox_3 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_3.setGeometry(QtCore.QRect(830, 30, 241, 21))
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(880, 672, 191, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1549, 23))
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
        self.menu_2.addAction(self.actionbao)
        self.menu_2.addAction(self.actionlingc)
        self.menu_7.addAction(self.actiongfd)
        self.menu_7.addAction(self.actionBHD)
        self.menu_7.addAction(self.actionKXD)
        self.menu_7.addAction(self.actionSTL)
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
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "富集区最小规模（网格大小50m）"))
        self.label_2.setText(_translate("MainWindow", "m     x"))
        self.label_3.setText(_translate("MainWindow", "m"))
        self.comboBox.setItemText(0, _translate("MainWindow", "删除潜力区"))
        self.pushButton.setText(_translate("MainWindow", "复原潜力区"))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "1"))
        self.pushButton_2.setText(_translate("MainWindow", "层间连通性判断"))
        self.label_4.setText(_translate("MainWindow", "0-上下不连通"))
        self.label_5.setText(_translate("MainWindow", "1-上连通"))
        self.label_6.setText(_translate("MainWindow", "2-下连通"))
        self.label_7.setText(_translate("MainWindow", "3-上下均连通"))
        self.comboBox_3.setItemText(0, _translate("MainWindow", "请选择场图类型"))
        self.pushButton_3.setText(_translate("MainWindow", "断层有效性判断"))
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
import sys
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())