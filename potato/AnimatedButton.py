from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QToolButton
from potato.Color import *

class AnimatedButton(QToolButton):
    def __init__(self, text="", parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setStyleSheet(f"""
            QToolButton {{
                background-color: {POTATO_PRIMARY};
                border: none;
                border-radius: 20px;
                padding: 10px;
                font-size: 16px;
                color: {TEXT_COLOR};
            }}
            QToolButton:hover {{
                background-color: {POTATO_DARK};
                color: white;
            }}
            QToolButton:pressed {{
                background-color: {POTATO_ACCENT};
            }}
        """)

        
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(150)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    def enterEvent(self, event):
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        super().leaveEvent(event)