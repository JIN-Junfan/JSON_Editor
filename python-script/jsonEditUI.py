from PyQt5.QtWidgets import QAction, QFileDialog, QMessageBox, QTreeWidgetItem, QToolBar, QMenu
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QByteArray
import json
import os

from exe_resource import Icon
from json_editor_UI_ui import *
from cunstom_widget import *


class Json_Edit(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.Win = Ui_MainWindow()
        self.Win.setupUi(self)
        self.parameter_init()
        self.menubar_init()
        self.toolbar_init()
        self.connection_init()
        self.UI_retranslate()
    
    # UI界面设置
    def UI_retranslate(self):
        self.Win.treeWidget.clear()
        self.Win.treeWidget.setHeaderLabels(['键名 Key','值 Value'])
        self.Win.treeWidget.setColumnWidth(0, 300)
        self.win_icon = self.icon_setup(Icon.JSON)
        self.Win.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.Win.treeWidget.customContextMenuRequested.connect(self.context_menu_init)
        self.Win.treeWidget.setEnabled(False)
        self.Win.le_Dir.setFocusPolicy(Qt.ClickFocus)
    
    # 参数初始化
    def parameter_init(self):
        self.save_change = {}
        self.change_record = {}
        self.undo_record = {}
        self.save_data = None
        self.unicode_flag = False
        self.format_flag = True
        self.format_parameter = 4
        self.json_name = None
    
    # 信号连接
    def connection_init(self):
        self.Win.treeWidget.clicked.connect(self.get_selected_content)
        self.Win.treeWidget.itemDoubleClicked.connect(self.edit_item)
    
    # 设置图标
    def icon_setup(self, icon_code):
        pixmap = QPixmap()
        pixmap.loadFromData(QByteArray(icon_code.encode()))
        return QIcon(pixmap)
    
    # 菜单栏初始化
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
        self.save_menubar_action.triggered.connect(lambda: self.save_func(self.current_file_path))
        self.file_menu.addAction(self.save_menubar_action)
        self.saveas_menubar_action = QAction('另存为', self)
        self.saveas_menubar_action.triggered.connect(self.save_as_func)
        self.file_menu.addAction(self.saveas_menubar_action)
        self.option_menubar_action = QAction('选项', self)
        self.file_menu.addAction(self.option_menubar_action)
        self.exit_menubar_action = QAction('退出', self)
        self.file_menu.addAction(self.exit_menubar_action)
        self.exit_menubar_action.triggered.connect(self.close)
        
        # 编辑栏
        self.edit_menu = self.menubar.addMenu('编辑')
        self.unicode_menubar_action = QAction('使用Unicode编码', self)
        self.unicode_menubar_action.setCheckable(True)
        self.unicode_menubar_action.setChecked(self.unicode_flag)
        self.unicode_menubar_action.triggered.connect(self.unicode_update)
        self.edit_menu.addAction(self.unicode_menubar_action)
        self.format_menubar_action = QAction('格式化输出json文件', self)
        self.format_menubar_action.setCheckable(True)
        self.format_menubar_action.setChecked(self.format_flag)
        self.format_menubar_action.triggered.connect(self.format_update)
        self.edit_menu.addAction(self.format_menubar_action)
        
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
    
    # 工具条初始化
    def toolbar_init(self):
        self.basic_toolbar = QToolBar("Toolbar", self) 
        self.addToolBar(self.basic_toolbar)
        self.new_toolbar_action = QAction(self.icon_setup(Icon.NEW_FILE), '新建',self)
        self.basic_toolbar.addAction(self.new_toolbar_action)
        self.open_toolbar_action = QAction(self.icon_setup(Icon.OPEN), '打开',self)
        self.open_toolbar_action.triggered.connect(self.open_file_func)
        self.basic_toolbar.addAction(self.open_toolbar_action)
        self.save_toolbar_action = QAction(self.icon_setup(Icon.SAVE), '保存',self)
        self.save_toolbar_action.triggered.connect(lambda: self.save_func(self.current_file_path))
        self.basic_toolbar.addAction(self.save_toolbar_action)
        self.saveas_toolbar_action = QAction(self.icon_setup(Icon.SAVEAS), '另存为',self)
        self.saveas_toolbar_action.triggered.connect(self.save_as_func)
        self.basic_toolbar.addAction(self.saveas_toolbar_action)
        self.undo_toolbar_action = QAction(self.icon_setup(Icon.UNDO), '撤销',self)
        self.basic_toolbar.addAction(self.undo_toolbar_action)
        self.recover_toolbar_action = QAction(self.icon_setup(Icon.RECOVER), '恢复',self)
        self.basic_toolbar.addAction(self.recover_toolbar_action)
        self.search_toolbar_action = QAction(self.icon_setup(Icon.SEARCH), '查找',self)
        self.basic_toolbar.addAction(self.search_toolbar_action)
        self.unicode_toolbar_action = QAction(self.icon_setup(Icon.UNICODE), '使用Unicode编码',self)
        self.unicode_toolbar_action.setCheckable(True)
        self.unicode_toolbar_action.setChecked(self.unicode_flag)
        self.unicode_toolbar_action.triggered.connect(self.unicode_update)
        self.basic_toolbar.addAction(self.unicode_toolbar_action)
        self.format_toolbar_action = QAction(self.icon_setup(Icon.FORMAT), '格式化输出json文件',self)
        self.format_toolbar_action.setCheckable(True)
        self.format_toolbar_action.setChecked(self.format_flag)
        self.format_toolbar_action.triggered.connect(self.format_update)
        self.basic_toolbar.addAction(self.format_toolbar_action)
        self.undo_recover_update()
    
    # 撤销恢复更新
    def undo_recover_update(self):
        if not self.change_record:
            self.undo_toolbar_action.setEnabled(False)
        else: self.undo_toolbar_action.setEnabled(True)
        if not self.undo_record:
            self.recover_toolbar_action.setEnabled(False)
        else: self.recover_toolbar_action.setEnabled(True)
    
    # 右键菜单
    def context_menu_init(self, pos):
        item = self.sender().itemAt(pos)
        index = self.Win.treeWidget.indexFromItem(item)
        if item:
            column = self.sender().currentColumn()
            if column == 0:
                # 创建 Key 的右键菜单
                key_menu = QMenu(self)
                expand_action = QAction('展开', self)
                expand_action.setEnabled(not item.isExpanded())
                expand_action.triggered.connect(lambda: self.Win.treeWidget.expand(index))
                key_menu.addAction(expand_action)
                collapse_action = QAction('折叠', self)
                collapse_action.setEnabled(item.isExpanded())
                collapse_action.triggered.connect(lambda: self.Win.treeWidget.collapse(index))
                key_menu.addAction(collapse_action)
                key_menu.addAction(self.all_expand_action)
                key_menu.addAction(self.all_collapse_action)
                plugin_before_menu = QMenu('插入(向前)', self)
                key_menu.addMenu(plugin_before_menu)
                new_item_action = QAction('项目', self)
                new_dict_action = QAction('对象/字典', self)
                new_list_action = QAction('数组/列表', self)
                plugin_before_menu.addAction(new_item_action)
                plugin_before_menu.addAction(new_dict_action)
                plugin_before_menu.addAction(new_list_action)
                plugin_after_menu =  QMenu('新建(向后)', self)
                key_menu.addMenu(plugin_after_menu)
                plugin_after_menu.addAction(new_item_action)
                plugin_after_menu.addAction(new_dict_action)
                plugin_after_menu.addAction(new_list_action)
                cut_action = QAction('剪切', self)
                key_menu.addAction(cut_action)
                copy_action = QAction('复制', self)
                key_menu.addAction(copy_action)
                paste_action = QAction('粘贴', self)
                key_menu.addAction(paste_action)
                delete_action = QAction('删除', self)
                key_menu.addAction(delete_action)
                rename_action = QAction('重命名', self)
                key_menu.addAction(rename_action)
                key_menu.exec_(self.sender().mapToGlobal(pos))
            elif column == 1:
                # 创建 Value 的右键菜单
                value_menu = QMenu(self)
                change_type_menu = QMenu('改变数据类型', value_menu)
                change_type_menu.setEnabled(False if item.childCount()>0 else True)
                value_menu.addMenu(change_type_menu)
                
                int_action = QAction('int整数型', self)
                int_action.setEnabled(self.test_convert(int, item.text(1)))
                int_action.triggered.connect(lambda: self.data_type_change(item, 1))
                change_type_menu.addAction(int_action)
                
                float_action = QAction('float浮点型', self)
                float_action.setEnabled(self.test_convert(float, item.text(1)))
                float_action.triggered.connect(lambda: self.data_type_change(item, 0.1))
                change_type_menu.addAction(float_action)
                
                bool_action = QAction('bool布尔值型', self)
                bool_action.setEnabled(self.test_convert('bool', item.text(1)))
                bool_action.triggered.connect(lambda: self.data_type_change(item, True))
                change_type_menu.addAction(bool_action)
                
                str_action = QAction('str字符型', self)
                str_action.setEnabled(self.test_convert(str, item.text(1)))
                str_action.triggered.connect(lambda: self.data_type_change(item, 'str'))
                change_type_menu.addAction(str_action)
                
                null_action = QAction('null空值', self)
                null_action.setEnabled(self.test_convert('None', item.text(1)))
                null_action.triggered.connect(lambda: self.data_type_change(item, None))
                change_type_menu.addAction(null_action)
                
                
                value_menu.exec_(self.sender().mapToGlobal(pos))
    
    # 更新Unicode设置
    def unicode_update(self):
        self.unicode_flag = not self.unicode_flag
        self.unicode_menubar_action.setChecked(self.unicode_flag)
        self.unicode_toolbar_action.setChecked(self.unicode_flag)
    
    def format_update(self):
        self.format_flag = not self.format_flag
        self.format_menubar_action.setChecked(self.format_flag)
        self.format_toolbar_action.setChecked(self.format_flag)
        self.format_parameter = 4 if self.format_flag else None

    # 打开json文件
    def open_file_func(self):
        # 打开浏览文件的对话框
        options = QFileDialog.Options()
        self.current_file_path, _ = QFileDialog.getOpenFileName(self, '请选择Json文件', '', 'json 文件 (*.json)', options=options)
        self.read_file_func(self.current_file_path)
    
    # 读取json文件
    def read_file_func(self, json_file):
        # 如果已经选择了文件，排除未选择而关闭对话框的情况
        if json_file:
            self.json_name = os.path.basename(json_file)
            # 读取json文件
            with open(json_file, 'r', encoding='utf-8') as file:
                self.json_data = json.load(file)
            self.update_tree()
            self.setWindowTitle('Json编辑器\t\t'+self.json_name)
    
    # 更新树显示
    def update_tree(self):
        expanded_state = {}
        self.record_expanded_state(self.Win.treeWidget.invisibleRootItem(),expanded_state)
        # 清空上一个文件的显示
        self.Win.treeWidget.clear()
        self.Win.le_Dir.clear()
        # 建立json数据树
        self.populate_tree(self.json_data, self.Win.treeWidget)
        self.apply_expanded_state(self.Win.treeWidget.invisibleRootItem(), expanded_state)
        if self.current_file_path:
            self.Win.treeWidget.setEnabled(True)
    
    def record_expanded_state(self, item, expanded_state):
        # 递归记录项的展开状态
        for i in range(item.childCount()):
            child_item = item.child(i)
            expanded_state[child_item.text(0)] = item.isExpanded()
            self.record_expanded_state(child_item, expanded_state)
    
    def apply_expanded_state(self, item, expanded_state):
        # 递归应用保存的展开状态
        for i in range(item.childCount()):
            child_item = item.child(i)
            if child_item.text(0) in expanded_state:
                item.setExpanded(expanded_state[child_item.text(0)])
            self.apply_expanded_state(child_item, expanded_state)
    
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
        return path
    
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
        
        data_path = self.Win.le_Dir.text()
        data_type = self.Win.lb_TreeDataType.text()
        if edited_text != self.original_text:
            self.save_change[data_path] = [None, data_type, edited_text]
    
    def save_func(self, file_path):
        for key, value in self.save_change.items():
            path_list = key.split('/')
            parent = self.json_data
            for path_part in path_list[0:-1]:
                if path_part.startswith('<list>'):
                    path_part = int(path_part.split('>')[1])
                parent = parent[path_part]
            path_list[-1] = int(path_list[-1].split('>')[1]) if path_list[-1].startswith('<list>') else path_list[-1]
            if str(value[1]).split("'")[1] == 'bool':
                if value[2].lower() == 'false':
                    parent[path_list[-1]] = False
                elif value[2].lower() == 'true':
                    parent[path_list[-1]] = True
                else: parent[path_list[-1]] = str(value[2])
            else:
                parent[path_list[-1]] = self.convert_data_type(str(value[1]), value[2])
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(self.json_data, json_file, ensure_ascii=self.unicode_menubar_action.isChecked(), indent=self.format_parameter)
        self.update_tree()
    
    def convert_data_type(self, data_type, data):
        data_type = data_type.split("'")[1]
        try:
            if data_type == "int":
                data = int(data)
            elif data_type == "float":
                data = float(data)
            elif data_type == "str":
                data = str(data)
            else: data = None
        except:
                data = str(data)
        return data
    
    def test_convert(self, data_type, data):
        try:
            if data_type == 'bool':
                if data.lower() == "false" or data.lower() == "true":
                    return True
                else: return False
            elif data_type == 'None':
                if data.lower() == 'none' or data.lower() == 'null':
                    return True
                else: return False
            else:
                data_type(data)
                return True
        except:
            return False
    
    def data_type_change(self, item, data_type):
        path = self.get_select_dir_func(item)
        if path in self.save_change:
            self.save_change[path][1] = type(data_type)
        else: 
            self.save_change[path] = [path, type(data_type), item.text(1)]
    
    def save_as_func(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getSaveFileName(self, "另存为", "", "json Files (*.json)", options=options)
        if file_path:
            self.save_func(file_path)
            self.read_file_func(file_path)