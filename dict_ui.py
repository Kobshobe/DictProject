# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 06:26:04 2019

@author: Kobs
"""
#qtui_dict.py

from PyQt5 import QtWidgets,QtCore,QtGui,sip
import sys
import qtawesome
import dict_sqlite as dsql

class MQVBoxLayout(QtWidgets.QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

class MQHBoxLayout(QtWidgets.QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)

class WordButton(QtWidgets.QPushButton):
    def __init__(self,func):
        super().__init__()
        self.word = ''
        self.symbol = ''
        self.info = ''
        self.func = func
        self.slot(self.func)

    def slot(self,func):
        self.clicked.connect(lambda:self.func(self.word))

class DictPart(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # 连接数据库
        self.conn = dsql.getConn('dict_database.db')
        # 四级容器[1-2:2-3:2-4] 词典主显区dict_widget
        self.dict_layout = MQVBoxLayout()

        # 五级容器[1-2:2-3:2-4-5:1] 词典搜索区[search_widget]
        self.search_widget = QtWidgets.QWidget()
        self.search_widget.setContentsMargins(15, 0, 20, 0)
        self.search_layout = MQVBoxLayout()
        self.search_widget.setLayout(self.search_layout)

        # 六级容器[1-2:2-3:2-4-5:1-6:1] 词典输入区[input_widget]
        self.searchbox_widget = QtWidgets.QWidget()
        self.setMinimumHeight(200)
        self.searchbox_widget.setObjectName('input')
        self.searchbox_layout = QtWidgets.QHBoxLayout()
        self.searchbox_layout.setContentsMargins(10, 0, 20, 1)
        self.searchbox_widget.setLayout(self.searchbox_layout)

        self.search_input = QtWidgets.QLineEdit('')
        self.search_input.setPlaceholderText('请输入你要查询的单词...')
        self.search_input.textEdited.connect(self.inputWord)
        # self.search_input.editingFinished.connect(self.finishEdit)
        self.search_button = QtWidgets.QPushButton('查   询')
        self.search_button.clicked.connect(self.finishEdit)
        self.search_button.setObjectName('search_button')
        self.search_button.setFixedSize(90, 40)
        self.hist_button = QtWidgets.QPushButton(qtawesome.icon('fa.history'), '')
        self.hist_button.setObjectName('search')
        self.del_button = QtWidgets.QPushButton(qtawesome.icon('fa.times-circle'), '')
        self.del_button.setObjectName('search')
        self.del_button.clicked.connect(self.clearWord)

        # 布局添加 [六级容器][searchbox_layout]
        self.searchbox_layout.addWidget(self.search_input)
        self.searchbox_layout.addWidget(self.del_button)
        self.searchbox_layout.addWidget(self.hist_button)
        self.searchbox_layout.addWidget(self.search_button)

        # 六级器[1-2:2-3:2-4-5:2-6:2] 词条预览[words_widget]
        self.words_widget = QtWidgets.QWidget()
        self.words_layout = QtWidgets.QVBoxLayout()
        self.words_layout.setContentsMargins(0, 0, 0, 0)
        self.words_layout.setSpacing(0)
        self.words_widget.setLayout(self.words_layout)
        self.words_widget.setStyleSheet('''
                    QPushButton{background:#f4f5f8;text-align:left;height:45px;}QPushButton:hover{background:#eaebf1;}
                ''')
        for n in range(8):
            setattr(self,'b'+str(n),WordButton(self.test))
        for n in range(8):
            exec("self.words_layout.addWidget(self.b{});self.b{}.hide()".format(n,n))

        # 五级布局[1-2:2-3:2-4-5:2] 单词信息显示[wordinfo_widget]
        self.wordinfo_widget = QtWidgets.QWidget()
        self.wordinfo_layout = QtWidgets.QVBoxLayout()
        self.wordinfo_widget.setLayout(self.wordinfo_layout)
        self.wordinfo_roll = QtWidgets.QScrollArea()
        self.wordinfo_roll.setStyleSheet('''
                    QScrollBar:vertical{background:white;width:12px;}
                    QScrollBar::handle:vertical{background:#f0f1f3;border-radius:6px;}
                ''')
        self.wordinfo_roll.setWidget(self.wordinfo_widget)
        self.wordinfo_widget.setMinimumSize(120, 600)

        # 布局添加 [五级布局][search_layout]
        self.search_layout.addWidget(self.searchbox_widget)
        self.search_layout.addWidget(self.words_widget)

        # 布局添加 [四级布局][dict_layout]
        self.dict_layout.addWidget(self.search_widget)
        self.dict_layout.addWidget(self.wordinfo_roll)

        # 布局添加 [三级布局添加][dict_widget]
        self.setLayout(self.dict_layout)
        self.setQss()

    #词典输入时
    def inputWord(self):
        #隐藏词条，获取输入
        for n in range(8):
            exec("self.b{}.hide()".format(n))
        text = self.search_input.text()
        #判断输入，不为空检索数据库
        if text != '':
            sql = 'SELECT * FROM words_info WHERE ID like "{}_%" limit 8'.format(text)
            words = dsql.fetchall(self.conn, sql)
            num = len(words)
            #数据库有结果则显示预览
            if num > 0:
                for n in range(num):
                    exec("self.b{}.show();self.b{}.word=words[n][1];self.b{}.setText(self.b{}.word)".format(n,n,n,n))
                self.searchbox_widget.setStyleSheet('''QWidget#input{border-bottom:1px solid #eaebf1;}''')
        else:
            self.searchbox_widget.setStyleSheet('''QWidget#input{border-bottom:none;}''')

    def finishEdit(self):
        for n in range(8):
            exec("self.b{}.hide()".format(n))

    def clearWord(self):
        self.search_input.clear()
        self.searchbox_widget.setStyleSheet('''QWidget#input{border-bottom:none;}''')
        for n in range(8):
            exec("self.b{}.hide()".format(n))
    def test(self,q):
        print('ok '+q)

    def setQss(self):
        self.search_widget.setStyleSheet('''
            QWidget#input{background:#f4f5f8;}
            QLineEdit{
                background:#f4f5f8;
                height:90px;
                font-size:30px;
            }
            QPushButton#search_button{
                border:none;
                color:white;
                background:#d2a9ca;
                border-radius:7px;
            }
            QPushButton#search{
                height:30px;
                background:none;
            }
        ''')

class World(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.SHOW_LEFT = True

        #窗口属性设置
        self.setGeometry(450,60,1200,820)
        self.setMinimumSize(1200,820)

        #一级容器[1] 主容器[all_widget] 水平布局
        self.all_widget = QtWidgets.QWidget()
        self.all_layout = MQHBoxLayout()
        self.all_widget.setLayout(self.all_layout)
        self.setCentralWidget(self.all_widget)

        #二级容器[1-2:1] 左容器[left_widget] 垂直布局
        self.left_widget = QtWidgets.QWidget()
        self.left_layout = MQVBoxLayout()
        self.left_layout.setAlignment(QtCore.Qt.AlignTop)
        self.left_widget.setLayout(self.left_layout)
        # self.left_layout.setContentsMargins(0,0,0,0)
        self.left_logo = QtWidgets.QPushButton()
        self.left_logo.setMinimumSize(200,200)
        self.left_logo.setIcon(QtGui.QIcon('logo.png'))
        self.left_logo.setIconSize(QtCore.QSize(80,90))
        self.left_layout.addWidget(self.left_logo)

        bot = {'词  典':[],'背单词':[],'阅  读':[],'设  置':[]}
        for k,_ in bot.items():
            self.left_botton = QtWidgets.QPushButton(k)
            self.left_layout.addWidget(self.left_botton)
            self.left_botton.setMinimumHeight(70)

        #二级容器[1-2:2] 右容器[right-widget] 垂直布局
        self.right_widget = QtWidgets.QWidget()
        self.right_layout = MQVBoxLayout()
        self.right_layout.setSpacing(0)
        self.right_widget.setLayout(self.right_layout)
        self.all_layout.addWidget(self.right_widget)
        
        #三级容器[1-2:2-3:1] 顶部栏 [topbar_widget] 水平布局
        self.topbar_widget = QtWidgets.QWidget()
        self.topbar_widget.setObjectName('topbar')
        self.topbar_layout = QtWidgets.QHBoxLayout()
        self.topbar_widget.setLayout(self.topbar_layout)
        self.right_fold = QtWidgets.QPushButton(qtawesome.icon('fa.angle-left'), '')
        self.right_fold.clicked.connect(self.foldLeft)
        self.right_fold.setFixedSize(30, 30)
        self.right_user = QtWidgets.QPushButton(qtawesome.icon('fa.user'), '')
        self.right_user.setFixedSize(30, 30)
        self.right_close = QtWidgets.QPushButton(qtawesome.icon('fa.times'),'')
        self.right_close.setFixedSize(30,30)
        self.right_close.clicked.connect(QtWidgets.qApp.quit)
        self.right_max = QtWidgets.QPushButton(qtawesome.icon('fa.square'),'')
        self.right_max.setFixedSize(30,30)
        self.right_max.clicked.connect(self.showMaximized)
        self.right_min = QtWidgets.QPushButton(qtawesome.icon('fa.minus',weight=0.2),'')
        self.right_min.clicked.connect(self.showMinimized)
        self.right_min.setFixedSize(30,30)

        self.topbar_layout.addWidget(self.right_fold)
        self.topbar_layout.addStretch(1)
        self.topbar_layout.addWidget(self.right_user)
        self.topbar_layout.addWidget(self.right_min)
        self.topbar_layout.addWidget(self.right_max)
        self.topbar_layout.addWidget(self.right_close)
        self.topbar_layout.setAlignment(QtCore.Qt.AlignRight)

        #三级容器 [1-2:2-3:2] 主显区 [main_widget] 水平布局
        self.main_widget = QtWidgets.QWidget()
        self.main_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.main_layout = MQVBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        #布局添加 [一级容器][all_layout]
        self.all_layout.addWidget(self.left_widget)
        self.all_layout.addWidget(self.right_widget)

        #布局添加 [二级容器][right_layout]
        self.right_layout.addWidget(self.topbar_widget)
        self.right_layout.addWidget(self.main_widget)

        ##########################################################

        self.dict_part = DictPart()
        self.main_layout.addWidget(self.dict_part)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setQss()

    def setQss(self):
        self.all_widget.setStyleSheet('''
                    QWidget{background:white;border:0px solid black;font-family:Microsoft YaHei;}
            ''')
        self.left_widget.setStyleSheet('''
            QWidget{background:#f4f5f8}
        ''')

    def foldLeft(self):
        if self.SHOW_LEFT == True:
            self.left_widget.hide()
            self.right_fold.setIcon(qtawesome.icon('fa.angle-right'))
        else:
            self.left_widget.show()
            self.right_fold.setIcon(qtawesome.icon('fa.angle-left'))
        self.SHOW_LEFT = ~self.SHOW_LEFT

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            #self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

def main():
    app = QtWidgets.QApplication(sys.argv)
    dictpart = World()
    dictpart.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()