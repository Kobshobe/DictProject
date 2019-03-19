# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 06:26:04 2019

@author: Kobs
"""
#qtui_dict.py

from PyQt5 import QtWidgets,QtCore,QtGui,QtWebEngineWidgets
import sys
import qtawesome
import dict_sqlite as dsql
import re

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
        self.func = func
        self.slot(self.func)

        self.css = style = '''<style type="text/css">
        <!--************-->

        /* gum navigator */
        #nav {background:#fff;margin-bottom:10px;}
        #nav li{float:left;}
        .ui-navigator-list,
        .ui-navigator-list li {
            list-style: none;
        }
        .ui-navigator-list li {
            display: inline-block;
            white-space:nowrap;/*内容不换行*/
            border-bottom: 1px solid #fff;
            color: #000;
        }
        .ui-navigator-list {
            width: 100%;
            display: -webkit-box;
        }
        .ui-navigator-list li {
            height: 51px;
            line-height: 44px;
            font-size: 22px;
            text-align: center;
            -webkit-box-flex: 1;
            display: -webkit-box;
            -webkit-box-align: center;
            -webkit-box-pack: center;
        }
        .ui-navigator-list li a {
            padding-top: 6px;
            font-size: 22px;
            text-decoration: none;
            display: block;
            width: 100%;
            -webkit-box-sizing:border-box;
        }
        .ui-navigator-list li.ui-state-hover,
        .ui-navigator-list li.ui-state-active {
            border-bottom: 1px solid #FE940B;
        }
        .ui-scroller {
            padding: 0;
            margin: 0;
            float: left;
            display: inline-block;/*重要，靠他让宽度由子节点撑开*/
        }
        .ui-scroller .ui-navigator-list {
            display: table;
            table-layout: fixed;/*宽度可控*/
            white-space:nowrap;/*内容不换行*/
            width: auto;
        }
        .ui-scroller .ui-navigator-list:after {
            content: '';
            clear: both;
            display: inline-block;
            width: 0;
            height: 0;
            overflow: hidden;
        }
        .ui-scroller .ui-navigator-list li {
            display: inline-block;
            /*float: left;*/
        }
        /* gum slider */
        .ui-slider {
            width: 100%;
            overflow: hidden;
            position: relative;
            }
        .ui-slider-group {
            overflow: hidden;
            position: relative;
            white-space:nowrap;/*内容不换行*/
            -webkit-transform: translateZ(0);
        }
        .ui-slider-item {
            position: relative;
            float:left;
            overflow: hidden;
            -webkit-box-sizing:border-box;
        }
        .ui-slider-group .content{white-space: normal;}
        .ui-navigator-list li sup{font-size:15px;}
        /* css3 circle word */
        .circle-word{
            width: 20px;
            height: 20px;
            line-height:20px;
            background: #52B231;
            -moz-border-radius: 10px;
            -webkit-border-radius: 10px;
            border-radius: 10px;
            text-align:center;
            font-size:16px;
            color:#fff;
            padding-right:1px;
            display:inline-block;
        }
        /* fixed nav */
        #nav.nav-fixed{position:fixed;z-index: 9999;background: #fff;top:0;border-top:10px #F7F7F7 solid;border-bottom:10px #F7F7F7 solid;}
        #nav.nav-fixed .ui-navigator-list li{height: 50px;}

        /* framework */
        .footer{text-align:center;background: #F8F8F8;padding:10px 0 20px;}
        .wordhead,.labelbtn{position: relative;}
        .main{padding-bottom:0;padding:0;word-wrap: normal;}
        .scbadd,.arrowbtn{position: absolute;right:8px;top:4px;}
        .arrowbtn{right:10px;}
        .words{width: 88%;word-break: break-word;font-size:20px;color: #000;}
        .words sup{font-size:10px;}

        .labelbtn{padding:0 8px;font-size:16px;height: 25px;line-height:25px;margin-bottom:10px;}
        .labeltitle{position: relative;top:-1px; font-family: "Microsoft Yahei", STXihei, sans-serif; font-size: large; border-bottom: thick dotted #fff3f3; color: #c85179;}
        .label-content {font-family: "Microsoft Sans Serif", "Arial Unicode MS", Helvetica, sans-serif;}
        .wordhead{display:none;}
        #wordhead0{display: block;}

        .content{font-size:16px;line-height: 24px;padding:5px 0 0;}
        .label-content{border-top:1px solid #F1F1F1;padding:15px 8px;margin-top:-10px;margin-bottom:10px;font-size:16px;position: relative;white-space:normal;}
        .label-content-unfold{display: block;}
        .content dl{padding-bottom:0px;}
        .content dd{text-indent: 10px;}
        .cont-pos{margin-bottom: 8px;}
        .cont-list{padding-bottom:8px;}

        .word-desc{background: #fff;margin-bottom:10px;padding:15px 8px;font-size:16px;}
        .lab-cont-addscb img{position: absolute;right:4px;top: 12px;}
        .words-ce{width: 64px;height:64px;line-height:64px;text-align: center; position: relative;font-size:44px;}
        .words-ce img{position: absolute;left:0;top:0;z-index: 1;}
        .words-ce span{position: relative;z-index: 2;}

        .cont-exam-ex{line-height: 20px;}
        .cont-exam-trans{padding-top:2px;}

        .sound-words,.sound-data{display:none;}
        <!--****-->

        .content {font-family: Segoe UI, Lucida Grande, Lucida Sans, Roboto, Droid Sans Mono, Droid Sans, sans-serif;}
        .bullet {display: none;}
        .sense-dt-def-ex{font-family: Segoe UI, Lucida Grande, Lucida Sans, Roboto, Droid Sans Mono, Droid Sans, sans-serif;color: #0588e3; background-color: #f8fafb;}
        .sense-dt-def-trans{font-family: "Microsoft Yahei", STXihei, sans-serif;color: #0588e3; padding-bottom: 3px; background-color: #f8fafb;}
        .phrase-exam-trans{font-family: "Microsoft Yahei", STXihei, sans-serif; color: #0588e3;}
        .word-explain{line-height: 28px;}
        .word-pinyin{padding-bottom: 10px;font-size: 18px}
        .word-ex-index{color:#A2A2A2;}
        .words{font-size: 50px; font-weight: bold; color: #8852a5; font-style: normal; font-family: Microsoft Sans Serif, Arial Unicode MS, Helvetica, sans-serif;}
        .scbadd{top:16px;right:14px;}
        .cont-list{position: relative;}
        .cont-pos{position: absolute;left:0; text-align: right;display: inline-block;width:20px;}
        .cont-pos span{font-weight: bold;}
        .content{margin-bottom: 10px;}
        .content dl,.cont-pos-other,.word-explain dl{padding-left:25px;}
        .content dt span{font-size:10px;/*color: #1464aa;*/}
        .ui-navigator-list li a{font-size:18px;color:#9F9F9F;}
        .ui-navigator-list li.ui-state-hover,
        .ui-navigator-list li.ui-state-active{
            border-bottom: 1px solid #1464aa;
        }
        .ui-navigator-list li.ui-state-hover a,
        .ui-navigator-list li.ui-state-active a{
            color: #1464aa;
        }
        em{font-weight:bold;font-style:normal;}
        em1{font-size:20px;font-weight:bold;}
        em2{font-size:14px;font-weight:bold;}
        i{font-style:italic;}
        .cont-pos-other{padding-bottom: 10px;display: none;}
        .cont-pos-other-symbol,.cont-pos-other-ext{display:block;}
        .cont-pos_subsense {}

        .word-ex-index{position: absolute;left:0;}
        .word-ex{position: relative;}
        .word-ex-cont{padding-left:18px;}
        .word-ex-cont.word-ex-contx{padding-left:0;}

        .cont-img-src{padding-left:30px;width:240px; min-height: 168px; }
        .cont-img-title{text-align: center;padding-bottom:15px;}
        .cont-img-src img{width:240px;border:0;}

        .word-img{padding-left:18px;width:240px; min-height: 168px;}
        .word-img-pic img{width:240px;border:0;}
        .word-img-title{text-align: center;padding-bottom:15px;}

        .cont-tips{padding-bottom:20px;}
        .cont-tips-tag{background: #14A8C8;color:#fff;width:70px;text-align:center;margin-bottom:6px;}
        .cont-tips-title{color: #2D2D2D;padding-bottom:4px;}
        .cont-tips-content{color:#aaa;line-height: 26px;}

        .cont-phrase{padding-bottom:15px;}
        .cont-phrase-title{background: #FD7778;color:#fff;width:40px;text-align: center;margin-bottom:6px;}

        .word-derivative{padding-left:18px;}
        .word-derivative-tag{color:#666;font-size:12px;}

        .cont-list{padding-bottom:3px;}
        .cont-list dt{padding-bottom:0px;}
        .content dd{text-indent: 0;margin-left:20px;}
        .cont-exam-trans,.sense-dt-def-trans{ /*color:#A3A3A3;*/}
        .cont-ext{padding-bottom:10px;}

        .ui-navigator-list li a.nav-en{font-size:20px;}
        .lab-cont-addscb{display:none;}

        .cont-img-src{position: relative;}
        .cont-img-src img.cont-img-def{position: absolute;z-index: 1;}
        .cont-img-src img.cont-img-real{position: relative;z-index: 2;}

        .word-img{position: relative;}
        .word-img img.cont-img-def{position: absolute;z-index: 1;}
        .word-img img.cont-img-real{position: relative;z-index: 2;}

        .words-yinbiao{}
        .words-yinbiao img{position: relative;top:-3px;}
        .words-yinbiao span{color:gray;font-size:15px; font-family: "Lucida Sans Unicode", "Lucida Grande", sans-serif;}
        .words-yinbiao i,.word-ex i,.word-explain i{font-style:italic;font-family: Lucida Sans Unicode, Arial, sans-serif;}
        .cont-exam-ex i{font-style:italic;}
        .cont-exam-ex em{font-style:italic;}
        .cont-exam-ex nl{font-style:normal;font-weight:normal;}
        .cont-exam-ex nl em{font-style:normal;}
        .word-ext em{font-style:normal;}

        .cont-exam p{line-height: 20px;}
        .cont-exam{padding-bottom:4px;}
        .cont-exam-ex{padding-bottom:4px; color: #454545; font-weight: normal; font-family: Segoe UI, Lucida Grande, Lucida Sans, Roboto, Droid Sans Mono, Droid Sans, sans-serif; }
        .cont-exam p.cont-exam-ex{line-height: 20px;}

        .cont-ext,.cont-list-pos,.cont-list-ext,.cont-list-grammar{padding-bottom:3px; font-weight: bold; color: Deeppink; font-style: normal;}

        .cont-addition{line-height: 20px;margin-top: 8px;background: #F4F4F4;padding:5px;}
        .cont-addition em{font-style:normal;}
        .cont-addition i em{font-style: italic;}
        .cont-addition span{color:#fff;background: #ccc;margin-right:4px;padding:0 3px;}
        .main-addition{margin-top:0;}
        .spaceh20{font-size: 0;height:0;overflow:hidden;padding-top:20px;}
        .spaceh10{font-size: 0;height:0;overflow:hidden;padding-top:10px;}
        .marginleft18{margin-left:18px;}

        .label-derivative p{line-height: 20px;}
        .label-derivative .cont-exam{padding-bottom:6px; }
        .label-ext span{padding-bottom:4px;}

        .sense-pos,.phrase-pos{font-family: Microsoft Sans Serif, Optima, sans-serif; color: #0d3773;}
        .phrase-symbol{color: #D2D2D2;}

        .content dt div{line-height: 22px;padding-bottom:4px;}

        .word-origin em{font-style:normal;}
        .content .cont-exam em{font-weight:bold;}
        .label-ext em{font-weight: bold;}

        .phrase-exam dt div{line-height: normal;}
        .phrase-exam dt .phrase-exam-trans{padding-top:2px;line-height: 24px;}
        .phrase-exam .cont-list dt{padding-bottom:6px;}
        .word-origin{line-height: normal;}
        .word-origin i{font-style:oblique;}
        .cont-list-ext{line-height: normal;padding-bottom:5px;}
        .content dt .sense-dt-def-ex span{font-size: 16px;}

        .cont-exam p.cont-exam-trans{line-height: 24px;font-weight: normal; color: #301530; font-family: Microsoft Yahei, STXihei, sans-serif;}
        .content dt div.sense-dt-def-trans{line-height: 24px;}
        .special{}
        .content dt .sense-dt-def-ex .sub-def-ex{}
        .content dt .sense-dt-def-ex .sub-def-ex i{font-style:oblique;color:red}.
    </style>'''

    def getShowText(self):
        return self.css + self.info

    def initWord(self, data):
        self.id = data[0]
        self.word = data[1]
        self.symbol = data[2]
        self.info = data[3]
        self.grade = data[4]
        if self.symbol == None:
            self.symbol = ''
        self.label_text = '''<p style="color:#202020;font-size:45px;line-height:70%;">{}</p><p style="color:gray;">{}</p>'''.format(self.word, self.symbol)



    def slot(self,func):
        self.clicked.connect(lambda:self.func(self.label_text, self.getShowText()))

class DictPart(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # 连接数据库
        self.conn = dsql.getConn('dict_database.db')

        #词典主显区dict_widget
        self.dict_layout = MQVBoxLayout()

        #词典搜索区[search_widget]
        self.search_widget = QtWidgets.QWidget()
        self.search_widget.setContentsMargins(15, 0, 7, 0)
        self.search_layout = MQVBoxLayout()
        self.search_widget.setLayout(self.search_layout)

        #词典输入区[input_widget]
        self.searchbox_widget = QtWidgets.QWidget()
        self.searchbox_widget.setObjectName('input')
        self.searchbox_layout = QtWidgets.QHBoxLayout()
        self.searchbox_layout.setContentsMargins(10, 0, 20, 1)
        self.searchbox_widget.setLayout(self.searchbox_layout)

        self.search_input = QtWidgets.QLineEdit('')
        self.search_input.setMinimumHeight(90)
        self.search_input.setPlaceholderText('请输入你要查询的单词...')
        self.search_input.textChanged.connect(self.inputWord)
        #self.search_input.editingFinished.connect(self.finishEdit)
        self.search_button = QtWidgets.QPushButton('查   询')
        self.search_button.clicked.connect(self.finishEdit)
        self.search_button.setObjectName('search_button')
        self.search_button.setFixedSize(90, 40)
        self.hist_button = QtWidgets.QPushButton(qtawesome.icon('fa.history'), '')
        self.hist_button.setObjectName('search')
        self.del_button = QtWidgets.QPushButton(qtawesome.icon('fa.times-circle'), '')
        self.del_button.setObjectName('search')
        self.del_button.clicked.connect(self.clearWord)

        #布局添加 [searchbox_layout]
        self.searchbox_layout.addWidget(self.search_input)
        self.searchbox_layout.addWidget(self.del_button)
        self.searchbox_layout.addWidget(self.hist_button)
        self.searchbox_layout.addWidget(self.search_button)

        # 词条预览[words_widget]
        self.words_widget = QtWidgets.QWidget()
        self.words_layout = QtWidgets.QVBoxLayout()
        self.words_layout.setContentsMargins(0, 0, 0, 0)
        self.words_layout.setSpacing(0)
        self.words_widget.setLayout(self.words_layout)
        self.words_widget.setStyleSheet('''
                    QPushButton{background:#f4f5f8;text-align:left;height:45px;}QPushButton:hover{background:#eaebf1;}
                ''')
        for n in range(8):
            setattr(self,'b'+str(n),WordButton(self.getWordInfo))
        for n in range(8):
            exec("self.words_layout.addWidget(self.b{});self.b{}.hide()".format(n,n))

        #单词信息显示[wordinfo_widget]#####################################
        self.wordinfo_widget = QtWidgets.QWidget()
        self.wordinfo_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.wordinfo_layout = MQVBoxLayout()
        self.wordinfo_layout.setContentsMargins(20, 0, 0, 0)
        self.wordinfo_widget.setLayout(self.wordinfo_layout)

        #单词显示的词条
        self.wordhead_widget = QtWidgets.QWidget()
        self.wordhead_layout = MQHBoxLayout()
        self.wordhead_widget.setLayout(self.wordhead_layout)

        self.word_found = QtWidgets.QLabel()
        self.word_found.setContentsMargins(5,10,10,10)
        self.word_found.setWordWrap(True)
        self.word_coll = QtWidgets.QPushButton(qtawesome.icon('fa.star'),'')
        self.word_coll.hide()

        self.info_browser = QtWidgets.QLabel()
        self.info_browser.setStyleSheet('''border-top:2px solid #eaeaea''')
        self.info_browser.setWordWrap(True)
        self.info_browser.hide()

        #添加Scroll
        self.info_scroll = QtWidgets.QScrollArea()
        self.info_scroll.setWidget(self.wordinfo_widget)
        self.info_scroll.setWidgetResizable(True)

        ####添加布局 [wordhead_layout]词条
        self.wordhead_layout.addWidget(self.word_found)
        self.wordhead_layout.addWidget(self.word_coll)
        self.wordhead_layout.addStretch(1)


        ### 布局添加 [search_layout]
        self.search_layout.addWidget(self.searchbox_widget)
        self.search_layout.addWidget(self.words_widget)

        ### 布局添加 [word_info]
        self.wordinfo_layout.addWidget(self.wordhead_widget)
        self.wordinfo_layout.addWidget(self.info_browser)
        self.wordinfo_layout.addStretch(1)

        ## 布局添加 [dict_layout]
        self.dict_layout.addWidget(self.search_widget)
        self.dict_layout.addWidget(self.info_scroll)

        # 布局添加 [dict_widget]
        self.setLayout(self.dict_layout)
        self.setQss()

    #单词匹配时True则显示部件
    def isMatch(self,t=True):
        if t:
            self.word_coll.show()
            self.info_browser.show()
        else:
            self.word_coll.hide()
            self.info_browser.hide()

    def inputWord(self):               #词典输入时
        for n in range(8):             #隐藏词条
            exec("self.b{}.hide()".format(n))
        self.isMatch(False)
        text = self.search_input.text()
        self.word_found.setText(text)
        #判断输入，不为空检索数据库
        if text != '':
            sql = 'SELECT * FROM words WHERE word like "{}_%" limit 8'.format(text)
            words = dsql.fetchall(self.conn, sql)
            num = len(words)
            #数据库有结果则显示预览
            if num > 0:
                for n in range(num):
                    exec("self.b{}.initWord(words[n]);self.b{}.show();self.b{}.setText(self.b{}.word)".format(n,n,n,n))
                self.searchbox_widget.setStyleSheet('''QWidget#input{border-bottom:1px solid #eaebf1;}''')
                self.info_browser.setText(self.b0.getShowText())
                self.word_found.setText(self.b0.label_text)
                self.isMatch(True)
        else:
            self.searchbox_widget.setStyleSheet('''QWidget#input{border-bottom:none;}''')

    def finishEdit(self):
        if self.search_input.text().lower().strip() == self.b0.word.lower().strip():
            pass
        else:
            self.word_found.setText('未找到结果')
            self.isMatch(False)
        for n in range(8):             #隐藏词条，获取输入
            exec("self.b{}.hide()".format(n))

    def clearWord(self):
        self.search_input.clear()
        self.isMatch(False)
        self.searchbox_widget.setStyleSheet('''QWidget#input{border-bottom:none;}''')
        for n in range(8):
            exec("self.b{}.hide()".format(n))

    def getWordInfo(self,label_text, info):
        self.word_found.setText(label_text)
        self.info_browser.setText(info)
        for n in range(8):  # 隐藏词条
            exec("self.b{}.hide()".format(n))

    def setQss(self):
        self.search_widget.setStyleSheet('''
            QWidget#input{background:#f4f5f8;}
            QLineEdit{
                background:#f4f5f8;
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
        self.wordinfo_widget.setStyleSheet('''
            QWidget{background:;}
        ''')
        self.info_scroll.setStyleSheet('''
                    QScrollBar:vertical{background:white;width:12px;}
                    QScrollBar:horizontal{background:black;}
                    QScrollBar::handle:vertical{background:#f0f1f3;border-radius:6px;}
                ''')
        self.wordhead_widget.setStyleSheet('''
            *{border:0px solid black;}
        ''')

class World(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.SHOW_LEFT = True
        self.initUi()

        self.dict_part = DictPart()
        self.main_layout.addWidget(self.dict_part)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setQss()

    def initUi(self):
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
        self.main_layout.setContentsMargins(0,0,15,0)
        self.main_widget.setLayout(self.main_layout)

        #三级部件 底部状态栏
        self.status_button = QtWidgets.QPushButton('...')

        #布局添加 [一级容器][all_layout]
        self.all_layout.addWidget(self.left_widget)
        self.all_layout.addWidget(self.right_widget)

        #布局添加 [二级容器][right_layout]
        self.right_layout.addWidget(self.topbar_widget)
        self.right_layout.addWidget(self.main_widget)
        self.right_layout.addWidget(self.status_button)

        ##########################################################

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