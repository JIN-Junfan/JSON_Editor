from PyQt5.QtCore import Qt,QEvent 
from json_editor_UI_ui import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QSplitter, QVBoxLayout, QWidget, QAction, QFileDialog, QMessageBox,QTreeWidgetItem, QLineEdit,QToolBar, QPlainTextEdit
from PyQt5.QtGui import QIcon, QPixmap, QKeyEvent
from PyQt5.QtCore import QByteArray

import json
import sys
from exe_resource import Icon

class CustomPlainTextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent

    def keyPressEvent(self, event):
        # 如果是Ctrl+回车，则换行
        if event.key() == Qt.Key_Return and event.modifiers() & Qt.ControlModifier:
            self.insertPlainText('\n')
        # 如果键盘输入回车或者小键盘回车，则退出编辑
        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.parent_window.finish_edit()
        elif event.key() == Qt.Key_Escape:
            self.parent_window.cancel_edit()
        else:
            super().keyPressEvent(event)
    
    def focusOutEvent(self, event):
        # 在失去焦点时退出编辑
        self.parent_window.finish_edit()
        super().focusOutEvent(event)

class Json_Edit(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.Win = Ui_MainWindow()
        self.Win.setupUi(self)
        self.menubar_init()
        self.toolbar_init()
        self.Win.treeWidget.clear()
        self.Win.treeWidget.setHeaderLabels(['键名 Key','值 Value'])
        self.Win.treeWidget.setColumnWidth(0, 300)
        self.Win.treeWidget.doubleClicked.connect(self.get_selected_content)
        self.Win.treeWidget.itemDoubleClicked.connect(self.edit_item)
        self.win_icon = self.icon_setup(Icon.JSON)
        # self.currentEditingItem = None
        # self.currentEditingColumn = -1
    
    def toolbar_init(self):
        self.basic_toolbar = QToolBar("Toolbar", self) 
        self.addToolBar(self.basic_toolbar)
        self.new_toolbar_action = QAction(self.icon_setup(Icon.NEW_FILE), '新建',self)
        self.basic_toolbar.addAction(self.new_toolbar_action)
        self.open_toolbar_action = QAction(self.icon_setup(Icon.OPEN), '打开',self)
        self.open_toolbar_action.triggered.connect(self.open_file_func)
        self.basic_toolbar.addAction(self.open_toolbar_action)
        self.save_toolbar_action = QAction(self.icon_setup(Icon.SAVE), '保存',self)
        self.basic_toolbar.addAction(self.save_toolbar_action)
        self.saveas_toolbar_action = QAction(self.icon_setup(Icon.SAVEAS), '另存为',self)
        self.basic_toolbar.addAction(self.saveas_toolbar_action)
        self.saveas_toolbar_action = QAction(self.icon_setup(Icon.UNDO), '撤销',self)
        self.basic_toolbar.addAction(self.saveas_toolbar_action)
        self.saveas_toolbar_action = QAction(self.icon_setup(Icon.RECOVER), '恢复',self)
        self.basic_toolbar.addAction(self.saveas_toolbar_action)
    
    def icon_setup(self, icon_code):
        pixmap = QPixmap()
        pixmap.loadFromData(QByteArray(icon_code.encode()))
        return QIcon(pixmap)
    
    def menubar_init(self):
        self.menubar = self.menuBar()
        # 文件栏
        self.file_menu = self.menubar.addMenu('文件')
        self.new_menubar_action = QAction('新建', self)
        self.file_menu.addAction(self.new_menubar_action)
        self.open_menubar_action = QAction('打开', self)
        self.file_menu.addAction(self.open_menubar_action)
        self.open_menubar_action.triggered.connect(self.open_file_func)
        self.save_menubar_action = QAction('保存', self)
        self.file_menu.addAction(self.save_menubar_action)
        self.saveas_menubar_action = QAction('另存为', self)
        self.file_menu.addAction(self.saveas_menubar_action)
        self.option_menubar_action = QAction('选项', self)
        self.file_menu.addAction(self.option_menubar_action)
        self.exit_menubar_action = QAction('退出', self)
        self.file_menu.addAction(self.exit_menubar_action)
        self.exit_menubar_action.triggered.connect(self.close)
        
        
        
        
        
        # 编辑栏
        self.edit_menu = self.menubar.addMenu('编辑')
        
        # 查找栏
        self.search_menu = self.menubar.addMenu('查看')
        self.all_expand_action = QAction('全部展开', self.search_menu)
        self.search_menu.addAction(self.all_expand_action)
        self.all_expand_action.triggered.connect(lambda: self.Win.treeWidget.expandAll())
        self.all_collapse_action = QAction('全部折叠', self)
        self.search_menu.addAction(self.all_collapse_action)
        self.all_collapse_action.triggered.connect(lambda: self.Win.treeWidget.collapseAll())
        self.word_wrap_action = QAction('自动换行', self)
        self.word_wrap_action.setCheckable(True)
        self.search_menu.addAction(self.word_wrap_action)
        self.word_wrap_action.triggered.connect(self.word_wrap_func)
        
        # 帮助栏
        self.help_menu = self.menubar.addMenu('帮助')
    
    # 打开文件
    def open_file_func(self):
        # 打开浏览文件的对话框
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, '请选择Json文件', '', 'json 文件 (*.json)', options=options)
        # 如果已经选择了文件，排除未选择而关闭对话框的情况
        if file_path:
            # 清空上一个文件的显示
            self.Win.treeWidget.clear()
            self.Win.le_Dir.clear()
            # 读取json文件
            with open(file_path, 'r', encoding='utf-8') as file:
                self.json_data = json.load(file)
            # 建立json数据树
            self.populate_tree(self.json_data, self.Win.treeWidget)
    
    # 构建树结构
    # json支持的数据类型：对象/字典，数组/列表，字符串，数字，布尔值，空值Null
    def populate_tree(self, data, parent):
        try:
            # 判断为字典类型
            if isinstance(data, dict):
                # 遍历字典
                for key, value in data.items():
                    item_parent = QTreeWidgetItem(parent)
                    item_parent.setText(0, str(key))
                    # 如果值为 dict 或者 list ，则调用自身，直到子项没有 dict 或者 list
                    if isinstance(value, (dict, list)):
                        self.populate_tree(value, item_parent)
                    else:
                        item_parent.setText(1, str(value))
            # 判断为列表类型
            elif isinstance(data, list):
                # 遍历列表
                for i, item in enumerate(data):
                    item_parent = QTreeWidgetItem(parent)
                    # 为列表添加伪键名 <list>数字， 如 <list>1
                    item_parent.setText(0, '<list>'+str(i))
                    # 如果值为 dict 或者 list ，则调用自身，直到子项没有 dict 或者 list
                    if isinstance(item, (dict, list)):
                        self.populate_tree(item, item_parent)
                    else:
                        item_parent.setText(1, str(item))
        except Exception as e:
            QMessageBox.information(None, 'Infomation', str(e))
            return
    
    # 自动换行 有bug
    def word_wrap_func(self):
        if self.word_wrap_action.isChecked():
            self.Win.treeWidget.setWordWrap(True)
        else:
            self.Win.treeWidget.setWordWrap(False)
    
    # 获取项目双击内容
    def get_selected_content(self):
        selected_item = self.Win.treeWidget.currentItem()
        self.get_select_dir_func(selected_item)
    
    # 获取双击的项目在json的路径
    def get_select_dir_func(self, selected_item):
        # 获取当前选择项目的父项
        parent = selected_item.parent()
        parent_path = []
        # 当存在父项，则在parent_path的0位插入父项的键名，然后继续查找父项，直至父项为None
        while parent:
                parent_path.insert(0, parent.text(0))
                parent = parent.parent()
        # 在路径后面添加当前的键名，并用/连接parent_path的各值
        parent_path.append(selected_item.text(0))
        path = '/'.join(parent_path)
        # 在le_Dir中显示数据路径
        self.Win.le_Dir.setText(path)
        # 在lb_TreeDataType显示当前数据的类型
        self.Win.lb_TreeDataType.setText(self.get_select_type_func(parent_path))
    
    def get_select_type_func(self, key_list):
        try:
            # key_list数据如：['widgets','pb_Enviroment']，0位为根目录
            data = self.json_data[key_list[0]]
            # 从1位开始，寻找子项，直至无子项
            for key in key_list[1:]:
                # 如果是列表，则分离<list>与数字，获取数字，查找值
                if isinstance(data, list):
                    index = int(key.split('>')[1])
                    data = data[index]
                # 如果是字典，直接通过key查找值
                elif isinstance(data, dict):
                    data = data[key]
            # 此处必须返回字符串，因为调用时，setText必须接收字符串
            return str(type(data))
        except Exception as e:
            QMessageBox.information(None, 'Infomation', str(e))
    
    def edit_item(self, item: QTreeWidgetItem, column: int):
        # 如果点击的是值(列1)，同时没有子项，则进行编辑
        if column == 1 and item.childCount() == 0:
            # 获取原文本内容
            self.original_text = item.text(1)
            # 获取原项显示高度
            original_item_height = self.Win.treeWidget.visualItemRect(item).height()
            # 实例化编辑器，并初始化
            editor = CustomPlainTextEdit(self)
            editor.setStyleSheet("font: 10pt;")
            editor.setPlainText(self.original_text)
            # 如果原高度不足100px,则扩大至100px，若大于100px，则保持原高度
            if original_item_height < 100: editor.setMaximumHeight(100)
            else: editor.setMaximumHeight(original_item_height)
            # 记录当前的项目和列
            self.currentEditingItem = item
            self.currentEditingColumn = column
            # 将原项替换为编辑器
            self.Win.treeWidget.setItemWidget(item, column, editor)
    
    # 取消编辑
    def cancel_edit(self):
        self.Win.treeWidget.removeItemWidget(self.currentEditingItem, self.currentEditingColumn)
        self.currentEditingItem.setText(self.currentEditingColumn, self.original_text)
    # 结束编辑
    def finish_edit(self):
        # 找到编辑器实例
        editor = self.Win.treeWidget.itemWidget(self.currentEditingItem, self.currentEditingColumn)
        # 获取编辑器中的文字内容
        edited_text = editor.toPlainText()
        # 移除编辑器
        self.Win.treeWidget.removeItemWidget(self.currentEditingItem, self.currentEditingColumn)
        # 将文本添加回原项中
        self.currentEditingItem.setText(self.currentEditingColumn, edited_text)