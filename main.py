from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, 
                            QListWidget, QPushButton, QHBoxLayout, QTextEdit,
                            QInputDialog, QMenu, QDialog, QFormLayout, 
                            QLineEdit, QComboBox, QDialogButtonBox, QDesktopWidget)
from PyQt5.QtCore import Qt

class ListManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("List Manager")
        # Center window on screen
        screen = QDesktopWidget().screenGeometry()
        width = 500
        height = 400
        self.setGeometry(
            (screen.width() - width) // 2,
            (screen.height() - height) // 2,
            width,
            height
        )
  
        # Main widget and layout
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)
        
        # List widget
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.show_item_info)
        self.list_widget.itemDoubleClicked.connect(self.edit_test_item)
        self.main_layout.addWidget(self.list_widget)
              
        # Enable context menu
        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.show_context_menu)
        
        # gao.fubin add button
        self.button_layout2 = QHBoxLayout()
        self.test_btn1 = QPushButton("加载文件夹")
        self.button_layout2.addWidget(self.test_btn1)
        
        self.test_btn2 = QPushButton("另存为新项目")
        self.button_layout2.addWidget(self.test_btn2)

        self.test_btn3= QPushButton("检查合法性")
        self.button_layout2.addWidget(self.test_btn3)
        
        self.test_btn4= QPushButton("打开文件夹")
        self.button_layout2.addWidget(self.test_btn4)

        # Button controls
        self.button_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("Add Item")
        self.add_btn.clicked.connect(self.add_item)
        self.button_layout.addWidget(self.add_btn)
        
        self.remove_btn = QPushButton("Remove Item")
        self.remove_btn.clicked.connect(self.remove_item)
        self.button_layout.addWidget(self.remove_btn)
        
        self.up_btn = QPushButton("Move Up")
        self.up_btn.clicked.connect(self.move_up)
        self.button_layout.addWidget(self.up_btn)
        
        self.down_btn = QPushButton("Move Down")
        self.down_btn.clicked.connect(self.move_down)
        self.button_layout.addWidget(self.down_btn)


        
        self.main_layout.addLayout(self.button_layout2)
        self.main_layout.addLayout(self.button_layout)
        
        # Text display
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.main_layout.addWidget(self.text_display)
        
        # Add sample items
        self.add_item("测试节点1")
        self.add_item("测试节点2")
        self.add_item("测试节点3")
        
        self.setCentralWidget(self.main_widget)
    
    def add_item(self, text=None):
        if type(text) == str:
            self.list_widget.addItem(text)
        else:
            dialog = QDialog(self)
            dialog.setWindowTitle('Add Item')
            
            form = QFormLayout(dialog)
            
            name_edit = QLineEdit()
            desc_edit = QLineEdit()
            priority_combo = QComboBox()
            priority_combo.addItems(['Low', 'Medium', 'High'])
            tags_edit = QLineEdit()
            
            form.addRow('Name:', name_edit)
            form.addRow('Description:', desc_edit)
            form.addRow('Priority:', priority_combo)
            form.addRow('Tags (comma separated):', tags_edit)
            
            buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)
            form.addRow(buttons)
            
            if dialog.exec_() == QDialog.Accepted:
                name = name_edit.text().strip()
                if name:
                    item = self.list_widget.addItem(name)
                    data = {
                        'name': name,
                        'desc': desc_edit.text().strip(),
                        'priority': priority_combo.currentText(),
                        'tags': [t.strip() for t in tags_edit.text().split(',') if t.strip()]
                    }
                    self.list_widget.item(self.list_widget.count()-1).setData(Qt.UserRole, data)
    
    def remove_item(self, item=None):
        if type(item) == bool:  # Called from button
            print(type(item))
            current_row = self.list_widget.currentRow()
            if current_row >= 0:
                self.list_widget.takeItem(current_row)
        else: # Called from user
            print(type(item))
            current_row = self.list_widget.currentRow()
            if current_row >= 0:
                self.list_widget.takeItem(current_row)
    
    def move_up(self):
        current_row = self.list_widget.currentRow()
        if current_row > 0:
            item = self.list_widget.takeItem(current_row)
            self.list_widget.insertItem(current_row - 1, item)
            self.list_widget.setCurrentRow(current_row - 1)
    
    def move_down(self):
        current_row = self.list_widget.currentRow()
        if current_row < self.list_widget.count() - 1 and current_row >= 0:
            item = self.list_widget.takeItem(current_row)
            self.list_widget.insertItem(current_row + 1, item)
            self.list_widget.setCurrentRow(current_row + 1)
    
    def show_context_menu(self, pos):
        item = self.list_widget.itemAt(pos)
        if not item:
            return
            
        menu = QMenu()
        
        # Add menu actions
        delete_action = menu.addAction("删除节点")
        rename_action = menu.addAction("更改名称")
        add_dep_action = menu.addAction("添加依赖")
        copy_action = menu.addAction("复制")

        # gfb add action
        editItem_action = menu.addAction("编辑测试项")
        
        # Connect actions to handlers
        delete_action.triggered.connect(lambda: self.remove_item(item))
        rename_action.triggered.connect(lambda: self.rename_item(item))
        add_dep_action.triggered.connect(lambda: self.add_dependency(item))
        copy_action.triggered.connect(lambda: self.copy_item(item))
        editItem_action.triggered.connect(lambda: self.edit_test_item(item))
        
        menu.exec_(self.list_widget.mapToGlobal(pos))

    def rename_item(self, item):
        new_name, ok = QInputDialog.getText(self, '重命名', '输入新名称:', text=item.text())
        if ok and new_name:
            item.setText(new_name)
            
    def add_dependency(self, item):
        dep_name, ok = QInputDialog.getText(self, '添加依赖', '输入依赖名称:')
        if ok and dep_name:
            data = item.data(Qt.UserRole) or {}
            data.setdefault('deps', []).append(dep_name)
            item.setData(Qt.UserRole, data)
            
    def copy_item(self, item):
        self.list_widget.insertItem(self.list_widget.row(item) + 1, item.text())
        
    def edit_test_item(self, item):
        dialog = QDialog(self)
        dialog.setWindowTitle('编辑测试项')
        
        form = QFormLayout(dialog)
        
        # 创建表单字段
        id_edit = QLineEdit()
        name_edit = QLineEdit(item.text())
        uid_edit = QLineEdit()
        dep_edit = QLineEdit()
        
        # 获取现有数据
        data = item.data(Qt.UserRole) or {}
        
        # 设置现有值
        if data:
            id_edit.setText(data.get('id', ''))
            uid_edit.setText(data.get('uid', ''))
            dep_edit.setText(', '.join(data.get('deps', [])))
        
        # 创建下拉框
        required_combo = QComboBox()
        required_combo.addItems(['是', '否'])
        if data.get('required', False):
            required_combo.setCurrentText('是')
        else:
            required_combo.setCurrentText('否')
            
        enabled_combo = QComboBox()
        enabled_combo.addItems(['启用', '禁用'])
        if data.get('enabled', True):
            enabled_combo.setCurrentText('启用')
        else:
            enabled_combo.setCurrentText('禁用')
        
        # 添加表单行
        form.addRow('编号:', id_edit)
        form.addRow('名称:', name_edit)
        form.addRow('唯一ID:', uid_edit)
        form.addRow('依赖:', dep_edit)
        form.addRow('是否必须:', required_combo)
        form.addRow('使能情况:', enabled_combo)
        
        # 添加按钮
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        form.addRow(buttons)
        
        if dialog.exec_() == QDialog.Accepted:
            # 更新项目数据
            item.setText(name_edit.text())
            data.update({
                'id': id_edit.text(),
                'uid': uid_edit.text(),
                'deps': [d.strip() for d in dep_edit.text().split(',') if d.strip()],
                'required': required_combo.currentText() == '是',
                'enabled': enabled_combo.currentText() == '启用'
            })
            item.setData(Qt.UserRole, data)

    def show_item_info(self, item):
        # Get stored data
        data = item.data(Qt.UserRole)
        details = f"Name: {item.text()}\n"
        
        if data:
            details += f"Description: {data.get('desc', '')}\n"
            details += f"Priority: {data.get('priority', 'Not set')}\n"
            tags = data.get('tags', [])
            details += f"Tags: {', '.join(tags) if tags else 'None'}\n"
            
        details += f"Position: {self.list_widget.row(item) + 1}\n"
        details += f"Total Items: {self.list_widget.count()}"
        self.text_display.setPlainText(details)

if __name__ == "__main__":
    app = QApplication([])
    window = ListManager()
    window.show()
    app.exec_()
