from PyQt6.QtWidgets import QHBoxLayout, QWidget, QLabel, QToolButton
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon
from potato.Color import *

class PotatoTab(QWidget):
    closeRequested = pyqtSignal(int)
    
    def __init__(self, title="New Tab", index=0):
        super().__init__()
        self.index = index
        self.title = title
        self.is_active = False
        self.is_loading = False
        self.favicon = None
        self.setup_ui()
        
    def setup_ui(self):
        self.setFixedSize(240, 36)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: transparent;
                border: none;
            }}
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 4, 0)
        layout.setSpacing(8)
        
        self.favicon_label = QLabel()
        self.favicon_label.setFixedSize(16, 16)
        self.favicon_label.setText("🌐")
        self.favicon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.favicon_label)
        
        self.title_label = QLabel(self.title)
        self.title_label.setStyleSheet(f"""
            QLabel {{
                color: {TEXT_COLOR};
                font-size: 14px;
                font-weight: 400;
                background-color: transparent;
                border: none;
            }}
        """)
        layout.addWidget(self.title_label)
        
        self.close_btn = QToolButton()
        self.close_btn.setIcon(QIcon("image/close.png"))
        self.close_btn.setFixedSize(20, 20)
        self.close_btn.setStyleSheet(f"""
            QToolButton {{
                background-color: transparent;
                border: none;
                border-radius: 10px;
                color: {TEXT_COLOR};
            }}
            QToolButton:hover {{
                background-color: {POTATO_ACCENT};
                color: white;
            }}
        """)
        self.close_btn.clicked.connect(lambda: self.closeRequested.emit(self.index))
        layout.addWidget(self.close_btn)
        
    def set_active(self, active):
        self.is_active = active
        if active:
            self.setStyleSheet(f"""
                QWidget {{
                    background-color: {POTATO_LIGHT};
                    border-top: 2px solid {POTATO_DARK};
                    border-left: 1px solid {POTATO_ACCENT};
                    border-right: 1px solid {POTATO_ACCENT};
                    border-bottom: none;
                    border-radius: 8px 8px 0 0;
                }}
            """)
            self.title_label.setStyleSheet(f"""
                QLabel {{
                    color: {TEXT_COLOR};
                    font-size: 14px;
                    font-weight: 500;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QWidget {{
                    background-color: {POTATO_PRIMARY};
                    border: none;
                    border-radius: 8px 8px 0 0;
                }}
                QWidget:hover {{
                    background-color: {POTATO_ACCENT};
                }}
            """)
            self.title_label.setStyleSheet(f"""
                QLabel {{
                    color: {TEXT_COLOR};
                    font-size: 14px;
                    font-weight: 400;
                }}
            """)
            
    def set_title(self, title):
        self.title = title
        if len(title) > 25:
            title = title[:25] + "..."
        self.title_label.setText(title)
        
    def set_favicon(self, icon):
        if icon and not icon.isNull():
            pixmap = icon.pixmap(16, 16)
            self.favicon_label.setPixmap(pixmap)
        else:
            self.favicon_label.setText("🌐")
            
    def set_loading(self, loading):
        self.is_loading = loading
        if loading:
            self.favicon_label.setText("⟳")
        else:
            self.favicon_label.setText("🌐")