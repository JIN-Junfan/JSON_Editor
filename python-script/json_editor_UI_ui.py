from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 722)
        MainWindow.setStyleSheet("QLineEdit[objectName = \'le_Dir\'], QLabel{\n"
"    font: 16pt;\n"
"}\n"
"QPushButton{\n"
"    min-width:40px;\n"
"    max-width:40px;\n"
"    margin: 0px;\n"
"}\n"
"QFrame{\n"
"    padding: 0;\n"
"}\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(900, 700))
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_PathInfo = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_PathInfo.sizePolicy().hasHeightForWidth())
        self.frame_PathInfo.setSizePolicy(sizePolicy)
        self.frame_PathInfo.setMinimumSize(QtCore.QSize(0, 30))
        self.frame_PathInfo.setMaximumSize(QtCore.QSize(16777215, 30))
        self.frame_PathInfo.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_PathInfo.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_PathInfo.setLineWidth(0)
        self.frame_PathInfo.setObjectName("frame_PathInfo")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_PathInfo)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.le_Dir = QtWidgets.QLineEdit(self.frame_PathInfo)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_Dir.sizePolicy().hasHeightForWidth())
        self.le_Dir.setSizePolicy(sizePolicy)
        self.le_Dir.setObjectName("le_Dir")
        self.horizontalLayout_4.addWidget(self.le_Dir)
        self.verticalLayout.addWidget(self.frame_PathInfo)
        self.frame_main = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.frame_main.sizePolicy().hasHeightForWidth())
        self.frame_main.setSizePolicy(sizePolicy)
        self.frame_main.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_main.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_main.setObjectName("frame_main")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_main)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(self.frame_main)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lb_TreeDataType = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_TreeDataType.sizePolicy().hasHeightForWidth())
        self.lb_TreeDataType.setSizePolicy(sizePolicy)
        self.lb_TreeDataType.setMinimumSize(QtCore.QSize(0, 20))
        self.lb_TreeDataType.setMaximumSize(QtCore.QSize(16777215, 20))
        self.lb_TreeDataType.setText("")
        self.lb_TreeDataType.setObjectName("lb_TreeDataType")
        self.verticalLayout_2.addWidget(self.lb_TreeDataType)
        self.treeWidget = QtWidgets.QTreeWidget(self.frame)
        self.treeWidget.setObjectName("treeWidget")
        self.verticalLayout_2.addWidget(self.treeWidget)
        self.horizontalLayout.addWidget(self.frame)
        self.verticalLayout.addWidget(self.frame_main)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
