from PyQt6.QtWidgets import QLineEdit, QCompleter
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import Qt, QStringListModel
from potato.Color import *

class PotatoOmnibox(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.suggestions = []
        self.setup_ui()
        self.setup_completer()
        
    def setup_ui(self):
        self.setPlaceholderText("Search Brave or type a URL")
        self.setStyleSheet(f"""
            QLineEdit {{
                background-color: {POTATO_LIGHT};
                border: 2px solid {POTATO_ACCENT};
                border-radius: 20px;
                padding: 12px 48px 12px 16px;
                font-size: 16px;
                color: {TEXT_COLOR};
            }}
            QLineEdit:focus {{
                border: 2px solid {POTATO_DARK};
            }}
            QLineEdit:hover {{
                border: 2px solid {POTATO_PRIMARY};
            }}
        """)

        
    def setup_completer(self):
        common_sites = [
            "google.com", "youtube.com", "twitter.com",
            "instagram.com", "github.com", "soundcloud.com",
            "wikipedia.org", "amazon.com", "netflix.com",
            
        ]
        
        model = QStringListModel(common_sites)
        completer = QCompleter(model, self)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.setCompleter(completer)