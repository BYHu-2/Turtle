import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import qtawesome
import matplotlib.pyplot as plt
import csv
import numpy as np
import datetime
import os

class Stack:
    def __init__(self):
        self.items=[]

    def isEmpty(self):
        return self.items==[]

    def push(self,item):
        self.items.append(item)

    def peek(self):
        return self.items[len(self.items)-1]

    def pop(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

class MainUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.advice=[]
        self.stack=Stack()
        self.isLeftPressDown = False
        self.dragPosition = 0
        self.Numbers = self.enum(UP=0, DOWN=1, LEFT=2, RIGHT=3, LEFTTOP=4, LEFTBOTTOM=5, RIGHTBOTTOM=6, RIGHTTOP=7,NONE=8)
        self.dir = self.Numbers.NONE
        self.setMouseTracking(True)

    def enum(self, **enums):
        return type('Enum', (), enums)

    def mouseReleaseEvent(self, event):
        if (event.button() == Qt.LeftButton):
            self.isLeftPressDown = False
            if (self.dir != self.Numbers.NONE):
                self.releaseMouse()

    def mousePressEvent(self, event):
        if (event.button() == Qt.LeftButton):
            self.isLeftPressDown = True
            if (self.dir != self.Numbers.NONE):
                self.mouseGrabber()
            else:
                self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        gloPoint = event.globalPos()
        rect = self.rect()
        tl = self.mapToGlobal(rect.topLeft())
        rb = self.mapToGlobal(rect.bottomRight())

        if (not self.isLeftPressDown):
            self.region(gloPoint)
        else:
            if (self.dir != self.Numbers.NONE):
                rmove = QRect(tl, rb)
                if (self.dir == self.Numbers.LEFT):
                    if (rb.x() - gloPoint.x() <= self.minimumWidth()):
                        rmove.setX(tl.x())
                    else:
                        rmove.setX(gloPoint.x())
                elif (self.dir == self.Numbers.RIGHT):
                    rmove.setWidth(gloPoint.x() - tl.x())
                elif (self.dir == self.Numbers.UP):
                    if (rb.y() - gloPoint.y() <= self.minimumHeight()):
                        rmove.setY(tl.y())
                    else:
                        rmove.setY(gloPoint.y())
                elif (self.dir == self.Numbers.DOWN):
                    rmove.setHeight(gloPoint.y() - tl.y())
                elif (self.dir == self.Numbers.LEFTTOP):
                    if (rb.x() - gloPoint.x() <= self.minimumWidth()):
                        rmove.setX(tl.x())
                    else:
                        rmove.setX(gloPoint.x())
                    if (rb.y() - gloPoint.y() <= self.minimumHeight()):
                        rmove.setY(tl.y())
                    else:
                        rmove.setY(gloPoint.y())
                elif (self.dir == self.Numbers.RIGHTTOP):
                    rmove.setWidth(gloPoint.x() - tl.x())
                    rmove.setY(gloPoint.y())
                elif (self.dir == self.Numbers.LEFTBOTTOM):
                    rmove.setX(gloPoint.x())
                    rmove.setHeight(gloPoint.y() - tl.y())
                elif (self.dir == self.Numbers.RIGHTBOTTOM):
                    rmove.setWidth(gloPoint.x() - tl.x())
                    rmove.setHeight(gloPoint.y() - tl.y())
                else:
                    pass
                self.setGeometry(rmove)
            else:
                self.move(event.globalPos() - self.dragPosition)
                event.accept()


    def initUI(self):
        self.setFixedSize(1200,900)
        self.main_widget = QWidget()
        self.main_layout = QGridLayout()
        self.main_widget.setLayout(self.main_layout)

        self.left_widget = QWidget()
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QGridLayout()
        self.left_widget.setLayout(self.left_layout)

        self.right_widget = QWidget()
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QGridLayout()
        self.right_widget.setLayout(self.right_layout)

        self.main_layout.addWidget(self.left_widget,0,0,16,2)
        self.main_layout.addWidget(self.right_widget,0,2,16,9)
        self.setCentralWidget(self.main_widget)

        self.left_label_1 = QPushButton("参数设置")
        self.left_label_1.setObjectName('left_label')
        self.left_label_1.setEnabled(False)
        self.left_label_2 = QPushButton("图像显示")
        self.left_label_2.setObjectName('left_label')
        self.left_label_2.setEnabled(False)
        self.left_label_3 = QPushButton("帮助")
        self.left_label_3.setObjectName('left_label')
        self.left_label_3.setEnabled(False)

        self.left_button_1 = QPushButton(qtawesome.icon('fa.rmb', color='white'), "设置期初资金")
        self.left_button_1.setObjectName('left_button')
        self.left_button_1.clicked.connect(self.buttonDialog1)
        self.left_button_2 = QPushButton(qtawesome.icon('fa.hourglass-start', color='white'), "设置交易开始时间")
        self.left_button_2.setObjectName('left_button')
        self.left_button_2.clicked.connect(self.buttonDialog2)
        self.left_button_3 = QPushButton(qtawesome.icon('fa.hourglass-end', color='white'), "设置交易结束时间")
        self.left_button_3.setObjectName('left_button')
        self.left_button_3.clicked.connect(self.buttonDialog3)
        self.left_button_4 = QPushButton(qtawesome.icon('fa.line-chart', color='white'), "修改唐奇安通道")
        self.left_button_4.setObjectName('left_button')
        self.left_button_4.clicked.connect(self.buttonDialog4)
        self.left_button_5 = QPushButton(qtawesome.icon('fa.check-circle-o', color='white'), "修改ATR")
        self.left_button_5.setObjectName('left_button')
        self.left_button_5.clicked.connect(self.buttonDialog5)
        self.left_button_6 = QPushButton(qtawesome.icon('fa.pie-chart', color='white'), "修改手续费")
        self.left_button_6.setObjectName('left_button')
        self.left_button_6.clicked.connect(self.buttonDialog6)
        self.left_button_7 = QPushButton(qtawesome.icon('fa.sort-amount-asc', color='white'), "修改投资系数")
        self.left_button_7.setObjectName('left_button')
        self.left_button_7.clicked.connect(self.buttonDialog7)
        self.left_checkbox_1 = QCheckBox('策略收益')
        self.left_checkbox_1.setChecked(True)
        self.left_checkbox_2 = QCheckBox('沪深300')
        self.left_checkbox_2.setChecked(True)
        self.left_checkbox_3 = QCheckBox('仓位图')
        self.left_checkbox_3.setChecked(True)
        self.left_button_8 = QPushButton(qtawesome.icon('fa.question', color='white'), "专业名词含义查询")
        self.left_button_8.setObjectName('left_button')
        self.left_button_8.clicked.connect(self.buttonDialog8)
        self.left_button_9 = QPushButton(qtawesome.icon('fa.comment', color='white'), "反馈建议")
        self.left_button_9.setObjectName('left_button')
        self.left_button_9.clicked.connect(self.buttonDialog9)
        self.left_button_10 = QPushButton(qtawesome.icon('fa.envelope', color='white'), "联系我们")
        self.left_button_10.setObjectName('left_button')
        self.left_button_10.clicked.connect(self.buttonDialog10)

        self.left_layout.addWidget(self.left_label_1, 0, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_1, 1, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_2, 2, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_3, 3, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_4, 4, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_5, 5, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_6, 6, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_7, 7, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_2, 8, 0, 1, 3)
        self.left_layout.addWidget(self.left_checkbox_1, 9, 0, 1, 3)
        self.left_layout.addWidget(self.left_checkbox_2, 10, 0, 1, 3)
        self.left_layout.addWidget(self.left_checkbox_3, 11, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_3, 12, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_8, 13, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_9, 14, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_10, 15, 0, 1, 3)

        self.left_checkbox_1.setStyleSheet("QCheckBox{color:rgb(255,250,250)}")
        self.left_checkbox_2.setStyleSheet("QCheckBox{color:rgb(255,250,250)}")
        self.left_checkbox_3.setStyleSheet("QCheckBox{color:rgb(255,250,250)}")

        self.left_widget.setStyleSheet('''
            QCheckBox{font-family: "Helvetica Neue", Helvetica, KaiTi, sans-serif;
                      font-size:16px}
            QPushButton{border:none;
                        color:white;
                        text-align: left;
                        font-family: "Helvetica Neue", Helvetica, KaiTi, sans-serif;
                        font-size:16px}
            QPushButton#left_label{
                border:none;
                border-bottom:1px solid white;
                font-size:20px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, KaiTi, sans-serif;
            }
            QPushButton#left_button:hover{border-left:4px solid blue;font-weight:700;}
            QWidget#left_widget{
                background:gray;
                border-top:1px solid white;
                border-bottom:1px solid white;
                border-left:1px solid white;
                border-top-left-radius:10px;
                border-bottom-left-radius:10px;
            }
        ''')

        self.right_label_0 =QLabel('')
        self.right_label_1 = QLabel('期初资金')
        self.right_label_1.setAlignment(Qt.AlignCenter)
        self.right_label_1.setFont(QFont('KaiTi',12))
        self.right_label_2 = QLabel('总资产')
        self.right_label_2.setAlignment(Qt.AlignCenter)
        self.right_label_2.setFont(QFont('KaiTi', 12))
        self.right_label_3 = QLabel('累计盈亏')
        self.right_label_3.setAlignment(Qt.AlignCenter)
        self.right_label_3.setFont(QFont('KaiTi', 12))
        self.right_label_4 = QLabel('可交易天数')
        self.right_label_4.setAlignment(Qt.AlignCenter)
        self.right_label_4.setFont(QFont('KaiTi', 12))
        self.right_label_5 = QLabel('基准收益率')
        self.right_label_5.setAlignment(Qt.AlignCenter)
        self.right_label_5.setFont(QFont('KaiTi', 12))
        self.right_label_6 = QLabel('年化收益率')
        self.right_label_6.setAlignment(Qt.AlignCenter)
        self.right_label_6.setFont(QFont('KaiTi', 12))
        self.right_label_7 = QLabel('开始时间')
        self.right_label_7.setAlignment(Qt.AlignCenter)
        self.right_label_7.setFont(QFont('KaiTi', 12))
        self.right_label_8 = QLabel('结束时间')
        self.right_label_8.setAlignment(Qt.AlignCenter)
        self.right_label_8.setFont(QFont('KaiTi', 12))
        self.right_label_9 = QLabel('胜率')
        self.right_label_9.setAlignment(Qt.AlignCenter)
        self.right_label_9.setFont(QFont('KaiTi', 12))

        self.right_layout.addWidget(self.right_label_0, 0, 3, 1, 3)
        self.right_layout.addWidget(self.right_label_1, 1, 3, 1, 1)
        self.right_layout.addWidget(self.right_label_2, 1, 4, 1, 1)
        self.right_layout.addWidget(self.right_label_3, 1, 5, 1, 1)
        self.right_layout.addWidget(self.right_label_4, 1, 6, 1, 1)
        self.right_layout.addWidget(self.right_label_5, 1, 7, 1, 1)
        self.right_layout.addWidget(self.right_label_6, 1, 8, 1, 1)
        self.right_layout.addWidget(self.right_label_7, 1, 9, 1, 1)
        self.right_layout.addWidget(self.right_label_8, 1, 10, 1, 1)
        self.right_layout.addWidget(self.right_label_9, 1, 11, 1, 1)

        self.right_lineEdit_1 = QLineEdit()
        self.right_lineEdit_1.setReadOnly(True)
        self.right_lineEdit_1.setText('')

        self.right_lineEdit_2 = QLineEdit()
        self.right_lineEdit_2.setReadOnly(True)
        self.right_lineEdit_2.setText('')

        self.right_lineEdit_3 = QLineEdit()
        self.right_lineEdit_3.setReadOnly(True)
        self.right_lineEdit_3.setText('')

        self.right_lineEdit_4 = QLineEdit()
        self.right_lineEdit_4.setReadOnly(True)
        self.right_lineEdit_4.setText('')

        self.right_lineEdit_5 = QLineEdit()
        self.right_lineEdit_5.setReadOnly(True)
        self.right_lineEdit_5.setText('')

        self.right_lineEdit_6 = QLineEdit()
        self.right_lineEdit_6.setReadOnly(True)
        self.right_lineEdit_6.setText('')

        self.right_lineEdit_7 = QLineEdit()
        self.right_lineEdit_7.setReadOnly(True)
        self.right_lineEdit_7.setText('')

        self.right_lineEdit_8 = QLineEdit()
        self.right_lineEdit_8.setReadOnly(True)
        self.right_lineEdit_8.setText('')

        self.right_lineEdit_9 = QLineEdit()
        self.right_lineEdit_9.setReadOnly(True)
        self.right_lineEdit_9.setText('')

        self.right_layout.addWidget(self.right_lineEdit_1, 2, 3, 1, 1)
        self.right_layout.addWidget(self.right_lineEdit_2, 2, 4, 1, 1)
        self.right_layout.addWidget(self.right_lineEdit_3, 2, 5, 1, 1)
        self.right_layout.addWidget(self.right_lineEdit_4, 2, 6, 1, 1)
        self.right_layout.addWidget(self.right_lineEdit_5, 2, 7, 1, 1)
        self.right_layout.addWidget(self.right_lineEdit_6, 2, 8, 1, 1)
        self.right_layout.addWidget(self.right_lineEdit_7, 2, 9, 1, 1)
        self.right_layout.addWidget(self.right_lineEdit_8, 2, 10, 1, 1)
        self.right_layout.addWidget(self.right_lineEdit_9, 2, 11, 1, 1)

        self.right_figure_1 = QLabel()
        self.figure_1 = QPixmap("猫咪老师4.png")
        self.right_figure_1.setPixmap(self.figure_1)
        self.right_figure_1.setScaledContents(True)
        self.right_figure_2 = QLabel()
        self.figure_2 = QPixmap("喵.png")
        self.right_figure_2.setPixmap(self.figure_2)
        self.right_figure_2.setScaledContents(True)

        self.right_layout.addWidget(self.right_figure_1, 3, 3, 7, 9)
        self.right_layout.addWidget(self.right_figure_2, 10, 3, 5, 9)

        self.right_button_1 = QPushButton(qtawesome.icon('fa.repeat', color='blue'), "测试/重测")
        self.right_button_1.clicked.connect(self.start)
        self.right_button_1.clicked.connect(self.tryOrRepeat1)
        self.right_button_1.clicked.connect(self.tryOrRepeat2)
        self.right_button_2 = QPushButton(qtawesome.icon('fa.floppy-o', color='gray'), "删除当前结果")
        self.right_button_2.clicked.connect(self.figuredelete)
        self.right_button_3 = QPushButton(qtawesome.icon('fa.times', color='red'), "退出")
        self.right_button_3.clicked.connect(self.quitApplicaton)

        self.right_layout.addWidget(self.right_button_1, 16, 3, 1, 3)
        self.right_layout.addWidget(self.right_button_2, 16, 6, 1, 3)
        self.right_layout.addWidget(self.right_button_3, 16, 9, 1, 3)

        self.right_widget.setStyleSheet('''
            QWidget#right_widget{
                color:#232C51;
                background:white;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
            QLabel{
                border:None;
                font-weight:700;
                font-size=25px;
                font-family: "Helvetica Neue", Helvetica, KaiTi, sans-serif;
            }
            QLineEdit{
                    font:bold;
                    border:1px solid gray;
                    width:300px;
                    padding:2px 4px;
                    background-color:rgb(255,250,250);
                    selection-color:white;
            }
            QPushButton{font-family: "Helvetica Neue", Helvetica, KaiTi, sans-serif;
                        font-size:16px}
        ''')

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.main_layout.setSpacing(0)

    def buttonDialog1(self):
        self.dialog1 = QDialog()
        self.dialog1.setWindowIcon(QIcon("猫咪老师1.jpg"))
        self.dialog1.resize(250,100)
        self.dialog1.setWindowTitle('设置期初资金')
        formLayout = QFormLayout()
        label = QLabel('请输入您的期初资金(整数万元）')
        self.edit1 = QLineEdit()
        self.edit1.setValidator(QIntValidator())
        self.edit1.setAlignment(Qt.AlignRight)
        self.edit1.setFont(QFont('Arial', 10))
        button_ok = QPushButton('OK')
        button_ok.clicked.connect(self.okk1)
        button_cancel = QPushButton('Cancel')
        button_cancel.clicked.connect(self.cancel1)
        formLayout.addRow(label)
        formLayout.addRow(self.edit1)
        formLayout.addRow(button_ok, button_cancel)
        self.dialog1.setLayout(formLayout)

        self.dialog1.setStyleSheet('''
                    QPushButton{color:black;text-align: center;}
                    QLabel{font-family: "Helvetica Neue", Helvetica, KaiTi, sans-serif;font-size:16px}
                    QDialog{background:lightgray;
                            border-top:1px solid royalblue;
                            border-bottom:1px solid royalblue;
                            border-left:1px solid royalblue;
                            border-right:1px solid royalblue;
                            border-top-left-radius:10px;
                            border-bottom-left-radius:10px;
                            border-top-right-radius:10px;
                            border-bottom-right-radius:10px;
                            }
                    ''')

        self.dialog1.setWindowModality(Qt.ApplicationModal)
        self.dialog1.exec_()

    def okk1(self):
        if self.edit1.text() != '':
            global initial_cash
            global cash
            initial_cash=eval(self.edit1.text())*10000
            self.dialog1.close()

    def cancel1(self):
        self.edit1.setText('')

    def buttonDialog2(self):
        self.dialog2 = QDialog()
        self.dialog2.setWindowIcon(QIcon("猫咪老师1.jpg"))
        self.dialog2.resize(280,100)
        self.dialog2.setWindowTitle('设置交易开始时间')
        formLayout = QFormLayout()
        label1 = QLabel('请输入您的交易开始时间')
        label2 = QLabel('时间格式示例：2011-03-01')
        label3 = QLabel('时间范围为2011-03-01至2021-04-01')
        self.edit2 = QLineEdit()
        self.edit2.setAlignment(Qt.AlignRight)
        self.edit2.setFont(QFont('Arial', 10))
        button_ok = QPushButton('OK')
        button_ok.clicked.connect(self.okk2)
        button_cancel = QPushButton('Cancel')
        button_cancel.clicked.connect(self.cancel2)
        formLayout.addRow(label1)
        formLayout.addRow(label2)
        formLayout.addRow(label3)
        formLayout.addRow(self.edit2)
        formLayout.addRow(button_ok, button_cancel)
        self.dialog2.setLayout(formLayout)

        self.dialog2.setStyleSheet('''
                    QPushButton{color:black;text-align: center;}
                    QLabel{font-family: "Helvetica Neue", Helvetica, KaiTi, sans-serif;font-size:16px}
                    QDialog{background:lightgray;
                            border-top:1px solid royalblue;
                            border-bottom:1px solid royalblue;
                            border-left:1px solid royalblue;
                            border-right:1px solid royalblue;
                            border-top-left-radius:10px;
                            border-bottom-left-radius:10px;
                            border-top-right-radius:10px;
                            border-bottom-right-radius:10px;
                            }
                    ''')

        self.dialog2.setWindowModality(Qt.ApplicationModal)
        self.dialog2.exec_()

    def okk2(self):
        if self.edit2.text()!='':
            global start_time
            start_time=self.edit2.text()
            start_time = nearestdate(start_time, 1)

            self.dialog2.close()

    def cancel2(self):
        self.edit2.setText('')

    def buttonDialog3(self):
        self.dialog3 = QDialog()
        self.dialog3.setWindowIcon(QIcon("猫咪老师1.jpg"))
        self.dialog3.resize(280,100)
        self.dialog3.setWindowTitle('设置交易结束时间')
        formLayout = QFormLayout()
        label1 = QLabel('请输入您的交易结束时间')
        label2 = QLabel('时间格式示例：2021-04-01')
        label3 = QLabel('时间范围为2011-03-01至2021-04-01')
        self.edit3 = QLineEdit()
        self.edit3.setAlignment(Qt.AlignRight)
        self.edit3.setFont(QFont('Arial', 10))
        button_ok = QPushButton('OK')
        button_ok.clicked.connect(self.okk3)
        button_cancel = QPushButton('Cancel')
        button_cancel.clicked.connect(self.cancel3)
        formLayout.addRow(label1)
        formLayout.addRow(label2)
        formLayout.addRow(label3)
        formLayout.addRow(self.edit3)
        formLayout.addRow(button_ok, button_cancel)
        self.dialog3.setLayout(formLayout)

        self.dialog3.setStyleSheet('''
                    QPushButton{color:black;text-align: center;}
                    QLabel{font-family: "Helvetica Neue", Helvetica, KaiTi, sans-serif;font-size:16px}
                    QDialog{background:lightgray;
                            border-top:1px solid royalblue;
                            border-bottom:1px solid royalblue;
                            border-left:1px solid royalblue;
                            border-right:1px solid royalblue;
                            border-top-left-radius:10px;
                            border-bottom-left-radius:10px;
                            border-top-right-radius:10px;
                            border-bottom-right-radius:10px;
                            }
                    ''')

        self.dialog3.setWindowModality(Qt.ApplicationModal)
        self.dialog3.exec_()

    def okk3(self):
        if self.edit3.text()!='':
            global end_time
            end_time=self.edit3.text()
            end_time = nearestdate(end_time, -1)

            self.dialog3.close()

    def cancel3(self):
        self.edit3.setText('')

    def buttonDialog4(self):
        self.dialog4 = QDialog()
        self.dialog4.setWindowIcon(QIcon("猫咪老师1.jpg"))
        self.dialog4.resize(280,100)
        self.dialog4.setWindowTitle('修改唐奇安通道')
        formLayout = QFormLayout()
        label = QLabel('唐奇安通道修改为(5~50)：')
        self.edit4 = QLineEdit('20')
        self.edit4.setReadOnly(True)
        self.edit4.setAlignment(Qt.AlignRight)
        self.edit4.setFont(QFont('Arial', 10))
        self.slider1 = QSlider(Qt.Horizontal)
        self.slider1.setMinimum(5)
        self.slider1.setMaximum(50)
        self.slider1.setSingleStep(1)
        self.slider1.setValue(20)
        self.slider1.setTickPosition(QSlider.TicksBelow)
        self.slider1.setTickInterval(1)
        self.slider1.valueChanged.connect(self.valueChange1)
        button_ok = QPushButton('OK')
        button_ok.clicked.connect(self.okk4)
        button_cancel = QPushButton('Cancel')
        button_cancel.clicked.connect(self.cancel4)
        formLayout.addRow(label)
        formLayout.addRow(self.edit4)
        formLayout.addRow(self.slider1)
        formLayout.addRow(button_ok, button_cancel)
        self.dialog4.setLayout(formLayout)

        self.dialog4.setStyleSheet('''
                    QPushButton{color:black;text-align: center;}
                    QLabel{font-family: "Helvetica Neue", Helvetica, KaiTi, sans-serif;font-size:16px}
                    QDialog{background:lightgray;
                            border-top:1px solid royalblue;
                            border-bottom:1px solid royalblue;
                            border-left:1px solid royalblue;
                            border-right:1px solid royalblue;
                            border-top-left-radius:10px;
                            border-bottom-left-radius:10px;
                            border-top-right-radius:10px;
                            border-bottom-right-radius:10px;
                            }
                    ''')

        self.dialog4.setWindowModality(Qt.ApplicationModal)
        self.dialog4.exec_()

    def okk4(self):
        global Dontime
        Dontime=int(self.edit4.text())

        self.dialog4.close()

    def cancel4(self):
        self.slider1.setValue(20)

    def valueChange1(self):
        self.edit4.setText('%d'%self.slider1.value())

    def buttonDialog5(self):
        self.dialog5 = QDialog()
        self.dialog5.setWindowIcon(QIcon("猫咪老师1.jpg"))
        self.dialog5.resize(250,100)
        self.dialog5.setWindowTitle('修改ATR')
        formLayout = QFormLayout()
        label = QLabel('ATR修改为(5~50)：')
        self.edit5 = QLineEdit('20')
        self.edit5.setReadOnly(True)
        self.edit5.setAlignment(Qt.AlignRight)
        self.edit5.setFont(QFont('Arial', 10))
        self.slider2 = QSlider(Qt.Horizontal)
        self.slider2.setMinimum(5)
        self.slider2.setMaximum(50)
        self.slider2.setSingleStep(1)
        self.slider2.setValue(20)
        self.slider2.setTickPosition(QSlider.TicksBelow)
        self.slider2.setTickInterval(1)
        self.slider2.valueChanged.connect(self.valueChange2)
        button_ok = QPushButton('OK')
        button_ok.clicked.connect(self.okk5)
        button_cancel = QPushButton('Cancel')
        button_cancel.clicked.connect(self.cancel5)
        formLayout.addRow(label)
        formLayout.addRow(self.edit5)
        formLayout.addRow(self.slider2)
        formLayout.addRow(button_ok, button_cancel)
        self.dialog5.setLayout(formLayout)

        self.dialog5.setStyleSheet('''
                    QPushButton{color:black;text-align: center;}
                    QLabel{font-family: "Helvetica Neue", Helvetica, KaiTi, sans-serif;font-size:16px}
                    QDialog{background:lightgray;
                            border-top:1px solid royalblue;
                            border-bottom:1px solid royalblue;
                            border-left:1px solid royalblue;
                            border-right:1px solid royalblue;
                            border-top-left-radius:10px;
                            border-bottom-left-radius:10px;
                            border-top-right-radius:10px;
                            border-bottom-right-radius:10px;
                            }
                    ''')

        self.dialog5.setWindowModality(Qt.ApplicationModal)
        self.dialog5.exec_()

    def okk5(self):
        global atrtime
        atrtime=int(self.edit5.text())

        self.dialog5.close()

    def cancel5(self):
        self.slider2.setValue(20)

    def valueChange2(self):
        self.edit5.setText('%d'%self.slider2.value())

    def buttonDialog6(self):
        self.dialog6 = QDialog()
        self.dialog6.setWindowIcon(QIcon("猫咪老师1.jpg"))
        self.dialog6.resize(280,100)
        self.dialog6.setWindowTitle('修改手续费')
        formLayout = QFormLayout()
        label = QLabel('修改手续费为（单位：万分之一）：')
        self.edit6 = QLineEdit('1')
        self.edit6.setValidator(QIntValidator())
        self.edit6.setAlignment(Qt.AlignRight)
        self.edit6.setFont(QFont('Arial', 10))
        button_ok = QPushButton('OK')
        button_ok.clicked.connect(self.okk6)
        button_cancel = QPushButton('Cancel')
        button_cancel.clicked.connect(self.cancel6)
        formLayout.addRow(label)
        formLayout.addRow(self.edit6)
        formLayout.addRow(button_ok, button_cancel)
        self.dialog6.setLayout(formLayout)

        self.dialog6.setStyleSheet('''
                    QPushButton{color:black;text-align: center;}
                    QLabel{font-family: "Helvetica Neue", Helvetica, KaiTi, sans-serif;font-size:16px}
                    QDialog{background:lightgray;
                            border-top:1px solid royalblue;
                            border-bottom:1px solid royalblue;
                            border-left:1px solid royalblue;
                            border-right:1px solid royalblue;
                            border-top-left-radius:10px;
                            border-bottom-left-radius:10px;
                            border-top-right-radius:10px;
                            border-bottom-right-radius:10px;
                            }
                    ''')

        self.dialog6.setWindowModality(Qt.ApplicationModal)
        self.dialog6.exec_()

    def okk6(self):
        if self.edit6.text() != '':
            global backtest_commission_ratio
            backtest_commission_ratio=eval(self.edit6.text())/10000
            self.dialog6.close()

    def cancel6(self):
        self.edit6.setText('1')

    def buttonDialog7(self):
        self.dialog7 = QDialog()
        self.dialog7.setWindowIcon(QIcon("猫咪老师1.jpg"))
        self.dialog7.resize(280,100)
        self.dialog7.setWindowTitle('修改投资系数')
        formLayout = QFormLayout()
        label = QLabel('修改投资系数为（单位：百分之一）：')
        self.edit7 = QLineEdit('1')
        self.edit7.setAlignment(Qt.AlignRight)
        self.edit7.setFont(QFont('Arial', 10))
        button_ok = QPushButton('OK')
        button_ok.clicked.connect(self.okk7)
        button_cancel = QPushButton('Cancel')
        button_cancel.clicked.connect(self.cancel7)
        formLayout.addRow(label)
        formLayout.addRow(self.edit7)
        formLayout.addRow(button_ok, button_cancel)
        self.dialog7.setLayout(formLayout)

        self.dialog7.setStyleSheet('''
                    QPushButton{color:black;text-align: center;}
                    QLabel{font-family: "Helvetica Neue", Helvetica, KaiTi, sans-serif;font-size:16px}
                    QDialog{background:lightgray;
                            border-top:1px solid royalblue;
                            border-bottom:1px solid royalblue;
                            border-left:1px solid royalblue;
                            border-right:1px solid royalblue;
                            border-top-left-radius:10px;
                            border-bottom-left-radius:10px;
                            border-top-right-radius:10px;
                            border-bottom-right-radius:10px;
                            }
                    ''')

        self.dialog7.setWindowModality(Qt.ApplicationModal)
        self.dialog7.exec_()

    def okk7(self):
        if self.edit7.text() != '':
            global unit_rate
            unit_rate=eval(self.edit7.text())/100

            self.dialog7.close()

    def cancel7(self):
        self.edit7.setText('1')

    def buttonDialog8(self):
        self.dialog8 = QDialog()
        self.dialog8.setWindowIcon(QIcon("猫咪老师1.jpg"))
        self.dialog8.resize(280,100)
        self.dialog8.setWindowTitle('专业名词含义查询')
        layout=QVBoxLayout()
        self.label = QLabel('请选择专业名词：')
        self.cb = QComboBox()
        self.cb.addItems(['唐奇安通道', 'ATR', '投资系数', '基准收益率','年化收益率'])
        self.cb.currentIndexChanged.connect(self.selectionChange)
        layout.addWidget(self.label)
        layout.addWidget(self.cb)
        self.dialog8.setLayout(layout)

        self.dialog8.setStyleSheet('''
                    QLabel{font-family: "Helvetica Neue", Helvetica, KaiTi, sans-serif;font-size:16px}
                    QComboBox{font-family: "Helvetica Neue", Helvetica, KaiTi, sans-serif;font-size:16px}
                    QDialog{background:lightgray;
                            border-top:1px solid royalblue;
                            border-bottom:1px solid royalblue;
                            border-left:1px solid royalblue;
                            border-right:1px solid royalblue;
                            border-top-left-radius:10px;
                            border-bottom-left-radius:10px;
                            border-top-right-radius:10px;
                            border-bottom-right-radius:10px;
                            }
                    ''')

        self.dialog8.setWindowModality(Qt.ApplicationModal)
        self.dialog8.exec_()

    def selectionChange(self,i):
        dict0={'唐奇安通道':"唐奇安通道主要是一个突破型趋势跟踪指标，可以提供两种不同的突破信号", 'ATR':"ATR是日内指数最大波动的平均振幅，由当日最高、最低价和上一交易日的收盘价决定", '投资系数':"每一次开仓交易合约数unit的确定是将总资产的投资系数除以价值波动量得到", '基准收益率':"默认沪深300指数收益",'年化收益率':"年化收益率是指投资期限为一年的收益率"}
        self.label.setText('%s'%dict0[self.cb.currentText()])

    def buttonDialog9(self):
        self.dialog9 = QDialog()
        self.dialog9.setWindowIcon(QIcon("猫咪老师1.jpg"))
        self.dialog9.resize(250,100)
        self.dialog9.setWindowTitle('反馈建议')
        formlayout=QFormLayout()
        label = QLabel('您的反馈与建议是：')
        self.edit9 = QTextEdit('')
        self.edit9.setAlignment(Qt.AlignLeft)
        self.edit9.setFont(QFont('KaiTi', 10))
        button_ok = QPushButton('OK')
        button_ok.clicked.connect(self.okk9)
        button_cancel = QPushButton('Cancel')
        button_cancel.clicked.connect(self.cancel9)
        formlayout.addRow(label)
        formlayout.addRow(self.edit9)
        formlayout.addRow(button_ok,button_cancel)
        self.dialog9.setLayout(formlayout)

        self.dialog9.setStyleSheet('''
                    QPushButton{color:black;text-align: center;}
                    QLabel{font-family: "Helvetica Neue", Helvetica, KaiTi, sans-serif;font-size:16px}
                    QDialog{background:lightgray;
                            border-top:1px solid royalblue;
                            border-bottom:1px solid royalblue;
                            border-left:1px solid royalblue;
                            border-right:1px solid royalblue;
                            border-top-left-radius:10px;
                            border-bottom-left-radius:10px;
                            border-top-right-radius:10px;
                            border-bottom-right-radius:10px;
                            }
                    ''')

        self.dialog9.setWindowModality(Qt.ApplicationModal)
        self.dialog9.exec_()

    def okk9(self):
        QMessageBox.about(self,'感谢','感谢您的反馈与建议！基于您的反馈与建议，我们会努力做得更好！')
        self.dialog9.close()

    def cancel9(self):
        self.edit9.setText('')

    def buttonDialog10(self):
        self.dialog10 = QDialog()
        self.dialog10.setWindowIcon(QIcon("猫咪老师1.jpg"))
        self.dialog10.resize(250,150)
        self.dialog10.setWindowTitle('联系我们')
        layout=QVBoxLayout()
        label1 = QLabel('欢迎您来信联系我们！')
        label2 = QLabel('我们的邮箱是：')
        label5 = QLabel('hl1127591548@stu.pku.edu.cn')
        label6 = QLabel('byhu2018@pku.edu.cn')
        label7 = QLabel('stevenhu@stu.pku.edu.cn')

        label3 = QLabel('')
        label3.setOpenExternalLinks(True)
        label3.setText("<A href='https://mail.163.com/'>网易邮箱</a>")
        label3.setAlignment(Qt.AlignCenter)
        label3.setToolTip('点击进入网易邮箱主页')

        label4 = QLabel('')
        label4.setOpenExternalLinks(True)
        label4.setText("<A href='https://mail.qq.com/'>QQ邮箱</a>")
        label4.setAlignment(Qt.AlignCenter)
        label4.setToolTip('点击进入QQ邮箱主页')

        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.addWidget(label5)
        layout.addWidget(label6)
        layout.addWidget(label7)
        layout.addWidget(label3)
        layout.addWidget(label4)

        self.dialog10.setLayout(layout)

        self.dialog10.setStyleSheet('''
                    QLabel{font-family: "Helvetica Neue", Helvetica, KaiTi, sans-serif;font-size:16px}
                    QDialog{background:lightgray;
                            border-top:1px solid royalblue;
                            border-bottom:1px solid royalblue;
                            border-left:1px solid royalblue;
                            border-right:1px solid royalblue;
                            border-top-left-radius:10px;
                            border-bottom-left-radius:10px;
                            border-top-right-radius:10px;
                            border-bottom-right-radius:10px;
                            }
                    ''')

        self.dialog10.setWindowModality(Qt.ApplicationModal)
        self.dialog10.exec_()

    def tryOrRepeat1(self):
        if self.left_checkbox_1.isChecked() or self.left_checkbox_2.isChecked():
            plt.figure()
            plt.title('Asset-Time')
            if self.left_checkbox_1.isChecked():
                plt.plot(xs, l_asset, linestyle='-', color='firebrick', linewidth=1.5, label='Asset')
            if self.left_checkbox_2.isChecked():
                plt.plot(xs, l_index, linestyle='-', color='royalblue', linewidth=1, label='Index')
            plt.plot(xs, l_initial, linestyle='--', color='black', label='Initial')
            plt.xlabel('Time')
            plt.ylabel('Asset')
            plt.gcf().autofmt_xdate()
            plt.legend()
            plt.rcParams['figure.figsize'] = (9.0, 4.0) 
            theTime1=datetime.datetime.now()
            figure_1_name='figure_1'+str(theTime1)+'.png'
            figure_1_name = ''.join(figure_1_name.split(':'))
            self.stack.push(figure_1_name)
            plt.savefig(figure_1_name,dpi=300,bbox_inches='tight')
            plt.close()
            self.figure_1=QPixmap(figure_1_name)
            self.right_figure_1.setPixmap(self.figure_1)
        else:
            self.figure_1 = QPixmap("猫咪老师4.png")
            self.right_figure_1.setPixmap(self.figure_1)
        

    def tryOrRepeat2(self):
        if self.left_checkbox_3.isChecked():
            plt.figure()
            plt.title('Long/Short-Time')
            long_tem = []
            short_tem = []
            initial_bar = []
            for i in range(len(position_long)-1):
                long_tem.append(position_long[i][1])
                short_tem.append(-position_short[i][1])
                initial_bar.append(0)
            plt.bar(xs, long_tem,linestyle='-', color='firebrick', linewidth=1, label='long')
            plt.bar(xs, short_tem,linestyle='-', color='royalblue', linewidth=1, label='short')
            plt.plot(xs, initial_bar, linestyle='--', color='black', label='Initial')
            plt.xlabel('Time')
            plt.ylabel('')
            plt.gcf().autofmt_xdate()
            plt.legend()
            plt.rcParams['figure.figsize'] = (9.0, 4.0) 
            theTime2 = datetime.datetime.now()
            figure_2_name = 'figure_2' + str(theTime2) + '.png'
            figure_2_name = ''.join(figure_2_name.split(':'))
            self.stack.push(figure_2_name)
            plt.savefig(figure_2_name, dpi=300, bbox_inches='tight')
            plt.close()
            self.figure_2 = QPixmap(figure_2_name)
            self.right_figure_2.setPixmap(self.figure_2)
        else:
            self.figure_2 = QPixmap("喵.png")
            self.right_figure_2.setPixmap(self.figure_2)

    def quitApplicaton(self):
        app = MainUI.instance()
        app.quit()

    def figuredelete(self):
        figure_1_delete=self.stack.pop()
        figure_2_delete = self.stack.pop()
        os.remove(figure_1_delete)
        os.remove(figure_2_delete)
        self.right_button_2.setEnabled(False)

    def start(self):
        global time
        global date
        global winningRate
        global baseline
        global annualized_rate
        global xs
        global l_initial
        global position_long
        global position_short
        global l_time
        global l_asset
        global l_index


        self.right_button_2.setEnabled(True)

        position_long = []
        position_short = []
        for n in range(finddatepos(start_time), finddatepos(end_time) + 1):
            position_long.append([result[n][0], 0])
            position_short.append([result[n][0], 0])
            cash.append([result[n][0], 0])

        cash[0][1] = initial_cash
        start_date_position = finddatepos(start_time)
        end_date_position = finddatepos(end_time)
        for d in range(start_date_position + 1, end_date_position + 1):
            on_bar(result[d][0], atrtime)
            in_bar(result[d][0], atrtime)

        l_time = []
        l_asset = []
        l_index = []
        time = 0
        for d in range(start_date_position + 1, end_date_position + 1):
            time += 1
            l_time.append(result[d][0])
            l_asset.append(current_asset(result[d][0]))
            l_index.append(result[d][4] * initial_cash / result[start_date_position + 1][4])
            if position_short[time][1] != position_short[time - 1][1] or position_long[time][1] != \
                    position_long[time - 1][1]:
                date += 1
                if current_asset(result[d][0]) >= current_asset(result[d - 1][0]):
                    winningRate += 1
        winningRate /= date
        baseline = (l_index[-1] / l_index[0]) - 1
        d1 = datetime.datetime(int(start_time.split('-')[0]), int(start_time.split('-')[1]),
                               int(start_time.split('-')[2]))
        d2 = datetime.datetime(int(end_time.split('-')[0]), int(end_time.split('-')[1]), int(end_time.split('-')[2]))
        interval = d2 - d1
        annualized_rate = ((current_asset(end_time) / current_asset(start_time)) - 1) * 365 / interval.days
        xs =[]
        xs = [datetime.datetime.strptime(d, '%Y-%m-%d').date() for d in l_time]
        l_initial = []
        l_initial = [initial_cash] * (end_date_position - start_date_position)

        self.right_lineEdit_1.setText('%d' % int(initial_cash))
        self.right_lineEdit_2.setText('%d' % int(current_asset(end_time)))
        self.right_lineEdit_3.setText('%d' % int(current_asset(end_time)-initial_cash))
        self.right_lineEdit_4.setText('%d' % date)
        baseline0 = baseline * 100
        self.right_lineEdit_5.setText('%.2f' % baseline0 + '%')
        annualized_rate0 = annualized_rate * 100
        self.right_lineEdit_6.setText('%.2f' % annualized_rate0 + '%')
        self.right_lineEdit_7.setText('%s' % start_time)
        self.right_lineEdit_8.setText('%s' % end_time)
        winningRate0 = winningRate * 100
        self.right_lineEdit_9.setText('%.2f' % winningRate0 + '%')

def main():
    app = QApplication(sys.argv)
    gui = MainUI()
    gui.show()
    sys.exit(app.exec_())

def finddatepos(date):
    i = 0
    while result[i][0] != date:
        i += 1
    return i


def calAtr(result, start_time, end_time, tr_list): # Calculate atr
    counter = 0
    atr_list = []
    for i in range(1, len(result)-1):
        if result[i][0] == start_time:
            counter = 1
        if counter == 1:
            tr = max(float(result[i][2])-float(result[i][3]), float(result[i][2])-float(result[i-1][4]), float(result[i-1][4])-float(result[i][3]))
            tr_list.append([result[i][0], tr])
            atr_list.append(tr)
        if result[i][0] == end_time:
            counter = 0
    atr = int(np.floor(np.mean(atr_list)))
    atr_half = int(np.floor(0.5 * atr))
    return [atr, atr_half]

def calDon(result, time, atr_half, Dontime = 30): # Calculate Donchian tunnel
    for i in range(Dontime, len(result)-1):
        high_list = []
        low_list = []
        if result[i][0] == time:
            for j in range(i-Dontime, i):
                high_list.append(result[j][2])
                low_list.append(result[j][3])
            don_open = np.max(high_list)
            don_close = np.min(low_list)
    short_add_point = don_close - atr_half
    short_stop_loss = don_close + atr_half
    long_add_point = don_open + atr_half
    long_stop_loss = don_open - atr_half
    return [long_add_point, long_stop_loss, short_add_point, short_stop_loss]



def on_bar(date, atrtime = 10):
    i = 0
    while result[i][0] != date:
        i += 1
    yesterday = result[i-1][0]
    startatrday = result[i-atrtime][0]

    open = result[i][1]
    atr = calAtr(result, startatrday, yesterday, tr_list)[0]
    atr_half = calAtr(result, startatrday, yesterday, tr_list)[1]
    Donlst = calDon(result, date, atr_half)
    long_add_point = Donlst[0]
    long_stop_loss = Donlst[1]
    short_add_point = Donlst[2]
    short_stop_loss = Donlst[3]

    date_pos = 0
    while cash[date_pos][0] != date:
        date_pos += 1

    position_long[date_pos][1] = position_long[date_pos - 1][1]
    position_short[date_pos][1] = position_short[date_pos - 1][1]
    cash[date_pos][1] = cash[date_pos - 1][1]

    if position_long[date_pos][1] == 0 and position_short[date_pos][1] == 0:

        if open > long_add_point - atr_half:
            # 如果向上突破唐奇安通道，则开多
            if cash[date_pos][1] >= (1 + backtest_commission_ratio) * open * unit(current_asset(yesterday),yesterday):
                position_long[date_pos][1] = unit(current_asset(yesterday),yesterday)
                print(date, '开多仓%.1f'%(unit(current_asset(yesterday),yesterday)))
                cash[date_pos][1] -= (1 + backtest_commission_ratio) * open * unit(current_asset(yesterday),yesterday)
            else:
                position_long[date_pos][1] = cash[date_pos][1] / (1 + backtest_commission_ratio) / open
                print(date, '开多仓%.1f'%(cash[date_pos][1] / (1 + backtest_commission_ratio) / open))
                cash[date_pos][1] = 0

        if open < short_add_point + atr_half:
            # 如果向下突破唐奇安通道，则开空
            position_short[date_pos][1] = unit(current_asset(yesterday),yesterday)
            print(date, '开空仓%.1f'%(unit(current_asset(yesterday),yesterday)))
            cash[date_pos][1] += (1 - backtest_commission_ratio) * open * unit(current_asset(yesterday),yesterday)

    if position_long[date_pos][1] != 0:
        if open > long_add_point:
            # 当突破1/2atr时加仓
            if cash[date_pos][1] >= (1 + backtest_commission_ratio) * open * unit(current_asset(yesterday), yesterday):
                position_long[date_pos][1] += unit(current_asset(yesterday),yesterday)
                print(date, '继续加仓%.1f'%(unit(current_asset(yesterday),yesterday)))
                cash[date_pos][1] -= (1 + backtest_commission_ratio) * open * unit(current_asset(yesterday), yesterday)
            else:
                position_long[date_pos][1] += cash[date_pos][1] / (1 + backtest_commission_ratio) / open
                print(date, '继续加仓%.1f' % (cash[date_pos][1] / (1 + backtest_commission_ratio) / open))
                cash[date_pos][1] = 0

        if open < long_stop_loss:
            # 持多仓，止损位计算
            if position_long[date_pos][1] - unit(current_asset(yesterday),yesterday) >= 0:
                print(date, '平多仓%.1f'%(unit(current_asset(yesterday),yesterday)))
                cash[date_pos][1] += (1 - backtest_commission_ratio) * open * unit(current_asset(yesterday),
                                                                                       yesterday)
            else:
                print(date, '平多仓%.1f' % (position_long[date_pos][1]))
                cash[date_pos][1] += (1 - backtest_commission_ratio) * position_long[date_pos][1] * open

            position_long[date_pos][1] = max(position_long[date_pos][1] - unit(current_asset(yesterday),yesterday), 0)
            '''print(date, '平多仓%.1f'%(position_long[date_pos][1]))
            cash[date_pos][1] += (1 - backtest_commission_ratio) * open * position_long[date_pos][1]
            position_long[date_pos][1] = 0'''

    if position_short[date_pos][1] != 0:
        if open < short_add_point:
            # 当突破1/2atr时加仓
            position_short[date_pos][1] += unit(current_asset(yesterday),yesterday)
            print(date, '继续加仓%.1f'%(unit(current_asset(yesterday),yesterday)))
            cash[date_pos][1] += (1 - backtest_commission_ratio) * open * unit(current_asset(yesterday), yesterday)

        if open > short_stop_loss:
            # 持空仓，止损位计算
            m = min(position_short[date_pos][1] * open, open * unit(current_asset(yesterday),yesterday), cash[date_pos][1] / (1 + backtest_commission_ratio))
            print(date, '平空仓%.1f'%(m / open))
            cash[date_pos][1] -= (1 + backtest_commission_ratio) * m
            position_short[date_pos][1] = position_short[date_pos][1] - m / open
            '''m = position_short[date_pos][1] * open
            print(date, '平空仓%.1f'%(m / open))
            cash[date_pos][1] -= (1 + backtest_commission_ratio) * m
            position_short[date_pos][1] = position_short[date_pos][1] - m / open'''

def in_bar(date, atrtime = 10):
    i = 0
    while result[i][0] != date:
        i += 1
    yesterday = result[i-1][0]
    startatrday = result[i-atrtime][0]

    close = result[i][4]
    atr = calAtr(result, startatrday, yesterday, tr_list)[0]
    atr_half = calAtr(result, startatrday, yesterday, tr_list)[1]
    Donlst = calDon(result, date, atr_half)
    long_add_point = Donlst[0]
    long_stop_loss = Donlst[1]
    short_add_point = Donlst[2]
    short_stop_loss = Donlst[3]

    date_pos = 0
    while cash[date_pos][0] != date:
        date_pos += 1



    if position_long[date_pos][1] == 0 and position_short[date_pos][1] == 0:

        if close > long_add_point - atr_half:
            # 如果向上突破唐奇安通道，则开多
            if cash[date_pos][1] >= (1 + backtest_commission_ratio) * close * unit(current_asset(yesterday),yesterday):
                position_long[date_pos][1] = unit(current_asset(yesterday),yesterday)
                print(date, '开多仓%.1f'%(unit(current_asset(yesterday),yesterday)))
                cash[date_pos][1] -= (1 + backtest_commission_ratio) * close * unit(current_asset(yesterday),yesterday)
            else:
                position_long[date_pos][1] = cash[date_pos][1] / (1 + backtest_commission_ratio) / close
                print(date, '开多仓%.1f'%(cash[date_pos][1] / (1 + backtest_commission_ratio) / close))
                cash[date_pos][1] = 0

        if close < short_add_point + atr_half:
            # 如果向下突破唐奇安通道，则开空
            position_short[date_pos][1] = unit(current_asset(yesterday),yesterday)
            print(date, '开空仓%.1f'%(unit(current_asset(yesterday),yesterday)))
            cash[date_pos][1] += (1 - backtest_commission_ratio) * close * unit(current_asset(yesterday),yesterday)

    if position_long[date_pos][1] != 0:
        if close > long_add_point:
            # 当突破1/2atr时加仓
            if cash[date_pos][1] >= (1 + backtest_commission_ratio) * close * unit(current_asset(yesterday), yesterday):
                position_long[date_pos][1] += unit(current_asset(yesterday),yesterday)
                print(date, '继续加仓%.1f'%(unit(current_asset(yesterday),yesterday)))
                cash[date_pos][1] -= (1 + backtest_commission_ratio) * close * unit(current_asset(yesterday), yesterday)
            else:
                position_long[date_pos][1] += cash[date_pos][1] / (1 + backtest_commission_ratio) / close
                print(date, '继续加仓%.1f' % (cash[date_pos][1] / (1 + backtest_commission_ratio) / close))
                cash[date_pos][1] = 0

        if close < long_stop_loss:
            # 持多仓，止损位计算
            if position_long[date_pos][1] - unit(current_asset(yesterday),yesterday) >= 0:
                print(date, '平多仓%.1f'%(unit(current_asset(yesterday),yesterday)))
                cash[date_pos][1] += (1 - backtest_commission_ratio) * close * unit(current_asset(yesterday),
                                                                                       yesterday)
            else:
                print(date, '平多仓%.1f' % (position_long[date_pos][1]))
                cash[date_pos][1] += (1 - backtest_commission_ratio) * position_long[date_pos][1] * close

            position_long[date_pos][1] = max(position_long[date_pos][1] - unit(current_asset(yesterday),yesterday), 0)
            '''print(date, '平多仓%.1f'%(position_long[date_pos][1]))
            cash[date_pos][1] += (1 - backtest_commission_ratio) * close * position_long[date_pos][1]
            position_long[date_pos][1] = 0'''


    if position_short[date_pos][1] != 0:
        if close < short_add_point:
            # 当突破1/2atr时加仓
            position_short[date_pos][1] += unit(current_asset(yesterday),yesterday)
            print(date, '继续加仓%.1f'%(unit(current_asset(yesterday),yesterday)))
            cash[date_pos][1] += (1 - backtest_commission_ratio) * close * unit(current_asset(yesterday), yesterday)

        if close > short_stop_loss:
            # 持空仓，止损位计算
            m = min(position_short[date_pos][1] * close, close * unit(current_asset(yesterday),yesterday), cash[date_pos][1] / (1 + backtest_commission_ratio))
            print(date, '平空仓%.1f'%(m / close))
            cash[date_pos][1] -= (1 + backtest_commission_ratio) * m
            position_short[date_pos][1] = position_short[date_pos][1] - m / close
            '''m = position_short[date_pos][1] * close
            print(date, '平空仓%.1f'%(m / close))
            cash[date_pos][1] -= (1 + backtest_commission_ratio) * m
            position_short[date_pos][1] = position_short[date_pos][1] - m / close'''



def unit(total_asset, date, atrtime = 10):
    i = 0
    while result[i][0] != date:
        i += 1
    end_time = result[i + atrtime - 1][0]
    DV = calAtr(result, date, end_time, tr_list)[0]
    return total_asset * unit_rate / DV

def current_asset(date):
    date_pos = 0
    while cash[date_pos][0] != date:
        date_pos += 1
    return cash[date_pos][1] + (position_long[date_pos][1] - position_short[date_pos][1]) * result[finddatepos(date)][4]

def nearestdate(date, counter = 1):
    dateset = set()
    for k in range(len(result)):
        dateset.add(result[k][0])
    while date not in dateset:
        dt = datetime.datetime.strptime(date, '%Y-%m-%d')
        if counter == 1:
            date = (dt + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
            if date[8] == '0':
                date = date[:8] + date[9:]
            if date[5] == '0':
                date = date[:5] + date[6:]
        elif counter == -1:
            date = (dt - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
            if date[8] == '0':
                date = date[:8] + date[9:]
            if date[5] == '0':
                date = date[:5] + date[6:]
    return date
    


if __name__ == '__main__':
    csvFile = open("data.csv", "r")
    reader = csv.reader(csvFile)

    result = []
    for item in reader:
        # Ignore first line
        if reader.line_num == 1:
            continue
        result.append(
            [item[0], float(item[1]), float(item[2]), float(item[3]), float(item[4])])  # date, open, high, low, close
    csvFile.close()

    initial_cash = 0
    backtest_commission_ratio = 0.0001
    start_time = '2021-03-01'
    end_time = '2021-04-27'
    tr_list = []
    cash = []
    position_short = []
    position_long = []
    atrtime = 20
    Dontime = 30
    unit_rate = 0.01
    winningRate = 0
    date = 0
    time = 0
    baseline = 0
    annualized_rate = 0
    l_time = []
    l_asset = []
    l_index = []
    xs=[]
    l_initial = []

    main()