from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtCore import Qt


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