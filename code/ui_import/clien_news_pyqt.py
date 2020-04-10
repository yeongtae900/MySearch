from bs4 import BeautifulSoup
import requests
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import webbrowser

form_class = uic.loadUiType("viewer.ui")[0]

class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        # Fix main window size
        self.setFixedSize(800, 850)
        self.post_listview.setSpacing(5)

        # Set events
        self.go_to_website_button.clicked.connect(self.clicked_go_to_website_button)
        self.page_spinBox.valueChanged.connect(self.changed_page_spinBox)
        self.post_listview.doubleClicked.connect(self.clicked_go_to_website_button)
        self.webpage_comboBox.currentTextChanged.connect(self.changed_webpage_comboBox)

        # Add combobox item
        self.webpage_comboBox.addItem('[Clien] 새로운소식')
        self.webpage_comboBox.addItem('[Clien] 강좌/사용기')
        self.webpage_comboBox.addItem('[Underkg] News')

        # Load list to show
        post_list = self.load_post_list()

        # Set listview
        model = QStandardItemModel()
        for node in post_list:
            model.appendRow(QStandardItem(node[0]))
        self.post_listview.setModel(model)
        self.post_listview.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Finish init and start loop
        self.show()

    def clicked_go_to_website_button(self):
        # Check if selected
        is_selected = bool(len(self.post_listview.selectedIndexes()))

        # Execute if it's selected
        if is_selected != False:
            # Get selected website index
            selected_index = self.post_listview.selectedIndexes()[0].row()
            print(selected_index)

            # Load list to show
            post_list = self.load_post_list()

            # Open web browser
            url = post_list[selected_index][1]
            webbrowser.open(url)

    def changed_webpage_comboBox(self):
        post_list = self.load_post_list()

        # Reload listview
        model = QStandardItemModel()
        for node in post_list:
            model.appendRow(QStandardItem(node[0]))
        self.post_listview.setModel(model)

    def changed_page_spinBox(self):
        # Get that page post list
        post_list = self.load_post_list()

        # Reload listview
        model = QStandardItemModel()
        for node in post_list:
            model.appendRow(QStandardItem(node[0]))
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

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()


