from PyQt6.QtWidgets import QHBoxLayout, QWidget
from PyQt6.QtCore import pyqtSignal
from potato.Color import *
from potato.AnimatedButton import AnimatedButton
from potato.PotatoTab import PotatoTab

class PotatoTabBar(QWidget):
    tabCloseRequested = pyqtSignal(int)
    currentChanged = pyqtSignal(int)
    newTabRequested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.tabs = []
        self.current_index = 0
        self.setup_ui()
        
    def setup_ui(self):
        self.setFixedHeight(36)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {POTATO_PRIMARY};
                border-bottom: 1px solid {POTATO_DARK};
            }}
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.tab_container = QWidget()
        self.tab_layout = QHBoxLayout(self.tab_container)
        self.tab_layout.setContentsMargins(0, 0, 0, 0)
        self.tab_layout.setSpacing(0)
        layout.addWidget(self.tab_container)

        self.new_tab_btn = AnimatedButton("+")
        self.new_tab_btn.setFixedSize(36, 36)
        self.new_tab_btn.clicked.connect(self.newTabRequested.emit)
        self.new_tab_btn.setStyleSheet("""
            QToolButton {
                background-color: transparent;
                border: none;
                border-radius: 18px;
                font-size: 18px;
                font-weight: bold;
                color: #5f6368;
            }
            QToolButton:hover {
                background-color: #e8eaed;
                color: #202124;
            }
        """)
        layout.addWidget(self.new_tab_btn)
        
        layout.addStretch()
        
    def add_tab(self, title="New Tab"):
        index = len(self.tabs)
        tab = PotatoTab(title, index)
        tab.closeRequested.connect(self.tabCloseRequested.emit)
        tab.mousePressEvent = lambda e: self.set_current_tab(index)
        
        self.tabs.append(tab)
        self.tab_layout.addWidget(tab)
        self.set_current_tab(index)
        
        return index
        
    def remove_tab(self, index):
        if 0 <= index < len(self.tabs):
            tab = self.tabs.pop(index)
            tab.setParent(None)
            tab.deleteLater()

            for i, t in enumerate(self.tabs):
                t.index = i

            if index == self.current_index and self.tabs:
                if index >= len(self.tabs):
                    self.set_current_tab(len(self.tabs) - 1)
                else:
                    self.set_current_tab(index)
            elif index < self.current_index:
                self.current_index -= 1
                
    def set_current_tab(self, index):
        if 0 <= index < len(self.tabs):
            if 0 <= self.current_index < len(self.tabs):
                self.tabs[self.current_index].set_active(False)
            self.current_index = index
            self.tabs[index].set_active(True)
            self.currentChanged.emit(index)
            
    def update_tab_title(self, index, title):
        if 0 <= index < len(self.tabs):
            self.tabs[index].set_title(title)
            
    def update_tab_icon(self, index, icon):
        if 0 <= index < len(self.tabs):
            self.tabs[index].set_favicon(icon)
            
    def set_tab_loading(self, index, loading):
        if 0 <= index < len(self.tabs):
            self.tabs[index].set_loading(loading)