# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from bs4 import BeautifulSoup
import requests
import webbrowser

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # PyQt5 UI ------------------------------------
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 850)
        font = QtGui.QFont()
        font.setFamily("나눔스퀘어")
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.post_listview = QtWidgets.QListView(self.centralwidget)
        self.post_listview.setGeometry(QtCore.QRect(30, 150, 600, 650))
        font = QtGui.QFont()
        font.setFamily("나눔스퀘어")
        font.setPointSize(10)
        self.post_listview.setFont(font)
        self.post_listview.setLineWidth(1)
        self.post_listview.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.post_listview.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.post_listview.setUniformItemSizes(False)
        self.post_listview.setObjectName("post_listview")
        self.news_list_label = QtWidgets.QLabel(self.centralwidget)
        self.news_list_label.setGeometry(QtCore.QRect(30, 110, 179, 30))
        self.post_listview.setSpacing(5)
        font = QtGui.QFont()
        font.setFamily("나눔스퀘어")
        font.setPointSize(16)
        self.news_list_label.setFont(font)
        self.news_list_label.setObjectName("news_list_label")
        self.webpage_label = QtWidgets.QLabel(self.centralwidget)
        self.webpage_label.setGeometry(QtCore.QRect(30, 10, 200, 30))
        font = QtGui.QFont()
        font.setFamily("나눔스퀘어")
        font.setPointSize(16)
        self.webpage_label.setFont(font)
        self.webpage_label.setObjectName("webpage_label")
        self.page_spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.page_spinBox.setGeometry(QtCore.QRect(650, 760, 131, 41))
        font = QtGui.QFont()
        font.setFamily("나눔스퀘어")
        font.setPointSize(16)
        self.page_spinBox.setFont(font)
        self.page_spinBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.page_spinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.page_spinBox.setObjectName("page_spinBox")
        self.page_index_label = QtWidgets.QLabel(self.centralwidget)
        self.page_index_label.setGeometry(QtCore.QRect(650, 730, 101, 22))
        font = QtGui.QFont()
        font.setFamily("나눔스퀘어")
        font.setPointSize(12)
        self.page_index_label.setFont(font)
        self.page_index_label.setObjectName("page_index_label")
        self.webpage_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.webpage_comboBox.setGeometry(QtCore.QRect(30, 50, 601, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.webpage_comboBox.setFont(font)
        self.webpage_comboBox.setObjectName("webpage_comboBox")
        self.go_to_website_button = QtWidgets.QPushButton(self.centralwidget)
        self.go_to_website_button.setGeometry(QtCore.QRect(650, 150, 131, 61))
        font = QtGui.QFont()
        font.setFamily("나눔스퀘어")
        font.setPointSize(12)
        self.go_to_website_button.setFont(font)
        self.go_to_website_button.setObjectName("go_to_website_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Execute code ------------------------------------
        # Set events
        self.go_to_website_button.clicked.connect(self.clicked_go_to_website_button)
        self.page_spinBox.valueChanged.connect(self.changed_page_spinBox)
        self.post_listview.doubleClicked.connect(self.clicked_go_to_website_button)
        self.webpage_comboBox.currentTextChanged.connect(self.changed_webpage_comboBox)

        # Add item to combobox
        self.webpage_comboBox.addItem('[Clien] 새로운소식')
        self.webpage_comboBox.addItem('[Clien] 강좌/사용기')
        self.webpage_comboBox.addItem('[Underkg] News')

        # Load list to show
        post_list = self.load_post_list()

        # Set listview
        model = QtGui.QStandardItemModel()
        for node in post_list:
            model.appendRow(QtGui.QStandardItem(node[0]))
        self.post_listview.setModel(model)
        self.post_listview.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MySearch"))
        self.news_list_label.setText(_translate("MainWindow", "Your News List"))
        self.webpage_label.setText(_translate("MainWindow", "Select Webpage"))
        self.page_index_label.setText(_translate("MainWindow", "Page Index"))
        self.go_to_website_button.setText(_translate("MainWindow", "Go To\nWebsite"))

    def clicked_go_to_website_button(self):
        # Check if selected
        is_selected = bool(len(self.post_listview.selectedIndexes()))

        # Execute if it's selected
        if is_selected != False:
            # Get selected website index
            selected_index = self.post_listview.selectedIndexes()[0].row()

            # Load list to show
            post_list = self.load_post_list()

            # Open web browser
            url = post_list[selected_index][1]
            webbrowser.open(url)

    def changed_webpage_comboBox(self):
        self.page_spinBox.setValue(0)        
        post_list = self.load_post_list()

        # Reload listview
        model = QtGui.QStandardItemModel()
        for node in post_list:
            model.appendRow(QtGui.QStandardItem(node[0]))
        self.post_listview.setModel(model)

    def changed_page_spinBox(self):
        # Get that page post list
        post_list = self.load_post_list()

        # Reload listview
        model = QtGui.QStandardItemModel()
        for node in post_list:
            model.appendRow(QtGui.QStandardItem(node[0]))
        self.post_listview.setModel(model)

    def load_post_list(self):
        # Get combobox_current_index
        combobox_current_index = self.webpage_comboBox.currentIndex()

        # Make get_list according to combobox's current index
        get_list = []
        page_num = self.page_spinBox.value()

        if combobox_current_index == 0:
            get_list = self.get_clien_news_list(page_num)
        elif combobox_current_index == 1:
            get_list = self.get_clien_review_list(page_num)
        elif combobox_current_index == 2:
            get_list = self.get_underkg_news_list(page_num)

        return get_list

    def get_clien_news_list(self, index):
        # Get data from clien news
        html = requests.get('https://www.clien.net/service/board/news?&od=T31&po=' + str(index))
        soup = BeautifulSoup(html.text, 'html.parser')
        data = soup.find('div', {'class': 'list_content'})
        title_data = data.findAll('span', {'class': 'subject_fixed'})
        url_data = data.findAll('a', {'class': 'list_subject'})

        # Make post_list
        title_list = []
        url_list = []

        for title_line in title_data:
            title_list.append(title_line.text)

        for url_line in url_data:
            url_list.append("https://www.clien.net" + url_line.get('href'))

        post_list = []
        post_list_len = len(title_list)

        for i in range(0, post_list_len):
            post_list.append([title_list[i], url_list[i]])

        return post_list

    def get_clien_review_list(self, index):
        # Get data from clien review
        html = requests.get('https://www.clien.net/service/group/allreview?&od=T31&po=' + str(index))
        soup = BeautifulSoup(html.text, 'html.parser')
        data = soup.find('div', {'class': 'list_content'})
        title_data = data.findAll('span', {'class': 'subject_fixed'})
        url_data = data.findAll('a', {'class': 'list_subject'})

        # Make post_list
        title_list = []
        url_list = []

        for title_line in title_data:
            title_list.append(title_line.text)

        for url_line in url_data:
            url_list.append("https://www.clien.net" + url_line.get('href'))

        post_list = []
        post_list_len = len(title_list)

        for i in range(0, post_list_len):
            post_list.append([title_list[i], url_list[i]])

        return post_list

    def get_underkg_news_list(self, index):
        # Get data from underkg news
        html = requests.get('http://underkg.co.kr/index.php?mid=news&page=' + str(index + 1))
        soup = BeautifulSoup(html.text, 'html.parser')
        data = soup.find('div', {'class': 'article'})
        data = data.findAll('h1', {'class', 'title'})

        # Make post_list

        title_list = []
        url_list = []

        for line in data:
            title_list.append(line.find('a').text.strip('\n'))
            url_list.append(line.find('a').get('href'))

        post_list = []
        post_list_len = len(title_list)

        for i in range(0, post_list_len):
            post_list.append([title_list[i], url_list[i]])

        return post_list

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

