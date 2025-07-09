from PyQt6.QtWidgets import (QApplication, QMainWindow, QToolBar, QHBoxLayout, QWidget,
                              QVBoxLayout, QToolButton, QMenu, QProgressBar, QLabel)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, Qt, QTimer
from PyQt6.QtGui import QAction, QIcon, QKeySequence
from PyQt6.QtWebEngineCore import QWebEngineProfile
from potato.Color import *
from potato.AnimatedButton import AnimatedButton
from potato.PotatoOmnibox import PotatoOmnibox
from potato.PotatoTabBar import PotatoTabBar
import sys, os, threading


class PotatoBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.browsers = []
        self.current_browser_index = 0
        self.adblock_enabled = True
        self.setup_ui()
        self.load_styles()
        self.add_new_tab(QUrl("https://search.brave.com/"))

    def setup_ui(self):
        self.setWindowTitle("Potato Browser")
        self.setGeometry(100, 50, 1400, 900)
        self.setWindowIcon(QIcon("🌐"))

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.create_toolbar()
        layout.addWidget(self.toolbar)

        self.tab_bar = PotatoTabBar()
        self.tab_bar.tabCloseRequested.connect(self.close_tab)
        self.tab_bar.currentChanged.connect(self.switch_tab)
        self.tab_bar.newTabRequested.connect(self.add_new_tab)
        layout.addWidget(self.tab_bar)
        
        self.browser_container = QWidget()
        self.browser_layout = QHBoxLayout(self.browser_container)
        self.browser_layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.browser_container)
        self.create_status_bar()
        
    
    def create_toolbar(self):
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.toolbar.setFloatable(False)
        self.toolbar.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        self.toolbar.setStyleSheet(f"""
            QToolBar {{
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 {POTATO_LIGHT}, stop: 1 {POTATO_PRIMARY});
                border: none;
                padding: 8px 12px;
                spacing: 4px;
            }}
        """)

        nav_container = QWidget()
        nav_container.setStyleSheet(f"""
            QToolButton {{
                background-color: transparent;
                color: {TEXT_COLOR};
                font-size: 18px;
                padding: 8px 16px;
                border-radius: 16px;
                border: none;
            }}

            QToolButton:hover {{
                background-color: {POTATO_ACCENT}; 
                color: white; 
            }}

            QToolButton:disabled {{
                color: {POTATO_ACCENT};
                opacity: 0.5;
            }}
        """)
        nav_layout = QHBoxLayout(nav_container)
        nav_layout.setContentsMargins(0, 0, 16, 0)
        nav_layout.setSpacing(4)
        
        self.back_btn = QToolButton()
        self.back_btn.setIcon(QIcon("image/back.png"))
        self.back_btn.setToolTip("Back (Alt+Left)")
        self.back_btn.clicked.connect(self.go_back)
        self.back_btn.setEnabled(False)
        nav_layout.addWidget(self.back_btn)

        self.forward_btn = QToolButton()
        self.forward_btn.setIcon(QIcon("image/forward.png"))
        self.forward_btn.setToolTip("Forward (Alt+Right)")
        self.forward_btn.clicked.connect(self.go_forward)
        self.forward_btn.setEnabled(False)

        self.reload_btn = QToolButton()
        self.reload_btn.setIcon(QIcon("image/update.png"))
        self.reload_btn.setToolTip("Reload (F5)")
        self.reload_btn.clicked.connect(self.reload_page)
        nav_layout.addWidget(self.reload_btn)
                
        self.toolbar.addWidget(nav_container)

        url_container = QWidget()
        url_layout = QHBoxLayout(url_container)
        url_layout.setContentsMargins(0, 0, 0, 0)
        url_layout.setSpacing(8)

        self.security_widget = QWidget()
        self.security_widget.setFixedSize(24, 24)
        self.security_layout = QHBoxLayout(self.security_widget)
        self.security_layout.setContentsMargins(0, 0, 0, 0)
        
        self.security_icon = QLabel("🔒")
        self.security_icon.setFixedSize(16, 16)
        self.security_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.security_icon.setStyleSheet("color: #0d7377; font-size: 12px;")
        self.security_layout.addWidget(self.security_icon)
        
        url_layout.addWidget(self.security_widget)

        self.url_bar = PotatoOmnibox()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        url_layout.addWidget(self.url_bar)

        action_container = QWidget()
        action_layout = QHBoxLayout(action_container)
        action_layout.setContentsMargins(0, 0, 0, 0)
        action_layout.setSpacing(4)
        
        url_layout.addWidget(action_container)
        
        self.toolbar.addWidget(url_container)

        right_container = QWidget()
        right_layout = QHBoxLayout(right_container)
        right_layout.setContentsMargins(16, 0, 0, 0)
        right_layout.setSpacing(4)
        
        self.menu_btn = AnimatedButton("⋮")
        self.menu_btn.setStyleSheet(f"""
            QToolButton {{
                background-color: transparent;
                color: {TEXT_COLOR};
                font-size: 30px;
                padding: 8px 16px;
                border-radius: 16px;
                border: none;
            }}

            QToolButton:hover {{
                background-color: {POTATO_ACCENT}; 
                color: white; 
            }}

        """)
        self.menu_btn.clicked.connect(self.show_menu)
        right_layout.addWidget(self.menu_btn)
        
        self.toolbar.addWidget(right_container)

    def create_status_bar(self):
        self.status_bar = self.statusBar()
        self.status_bar.setStyleSheet(f"""
            QStatusBar {{
                background-color: {POTATO_LIGHT};
                border-top: 1px solid {POTATO_PRIMARY};
                color: {TEXT_COLOR};
                font-size: 12px;
            }}
        """)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMaximumHeight(3)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: transparent;
            }
            QProgressBar::chunk {
                background-color: #4285f4;
                border-radius: 1px;
            }
        """)
        
        progress_container = QWidget()
        progress_container.setFixedHeight(3)
        progress_layout = QHBoxLayout(progress_container)
        progress_layout.setContentsMargins(0, 0, 0, 0)
        progress_layout.addWidget(self.progress_bar)

        main_layout = self.centralWidget().layout()
        main_layout.insertWidget(main_layout.count() - 1, progress_container)

        self.status_label = QLabel("Ready")
        self.status_bar.addWidget(self.status_label)

        self.security_info = QLabel("")
        self.status_bar.addPermanentWidget(self.security_info)

    def add_new_tab(self, qurl=None, title="New Tab"):
        if qurl is None or isinstance(qurl, bool):
            qurl = QUrl("https://search.brave.com/")
        
        browser = QWebEngineView()
        browser.setUrl(qurl)

        profile = browser.page().profile()
        profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.NoCache)

        browser.urlChanged.connect(lambda url: self.update_url_bar(url))
        browser.titleChanged.connect(lambda title: self.update_tab_title(title))
        browser.loadStarted.connect(self.load_started)
        browser.loadProgress.connect(self.load_progress)
        browser.loadFinished.connect(self.load_finished)
        browser.iconChanged.connect(lambda icon: self.update_tab_icon(icon))

        self.browsers.append(browser)
        self.browser_layout.addWidget(browser)
        tab_index = self.tab_bar.add_tab(title)
        self.switch_tab(tab_index)
        self.update_navigation_buttons()

        return browser

    def close_tab(self, index):
        if len(self.browsers) > 1:
            browser = self.browsers.pop(index)
            browser.setParent(None)
            browser.deleteLater()
            self.tab_bar.remove_tab(index)
            if index == self.current_browser_index:
                if index >= len(self.browsers):
                    self.current_browser_index = len(self.browsers) - 1
                else:
                    self.current_browser_index = index
                    
                self.switch_tab(self.current_browser_index)
        else:
            self.close()

    def switch_tab(self, index):
        if 0 <= index < len(self.browsers):
            if 0 <= self.current_browser_index < len(self.browsers):
                self.browsers[self.current_browser_index].hide()

            self.current_browser_index = index
            browser = self.browsers[index]
            browser.show()

            self.update_url_bar(browser.url())
            self.update_navigation_buttons()
            self.update_security_indicator(browser.url())

    def current_browser(self):
        if 0 <= self.current_browser_index < len(self.browsers):
            return self.browsers[self.current_browser_index]
        return None

    def go_back(self):
        browser = self.current_browser()
        if browser and browser.page().history().canGoBack():
            browser.back()

    def go_forward(self):
        browser = self.current_browser()
        if browser and browser.page().history().canGoForward():
            browser.forward()

    def reload_page(self):
        browser = self.current_browser()
        if browser:
            browser.reload()

    def navigate_to_url(self):
        url = self.url_bar.text().strip()
        if not url:
            return

        if url.startswith(("http://", "https://")):
            final_url = url.lower()
        elif url.startswith("localhost") or url.startswith("127.0.0.1"):
            final_url = "http://" + url.lower()
        elif "." in url and " " not in url and not url.startswith("search "):
            final_url = "https://" + url.lower()
        else:
            final_url = f"https://search.brave.com/search?q={url.replace(' ', '+').lower()}"
        
        browser = self.current_browser()
        if browser:
            browser.setUrl(QUrl(final_url))

    def update_url_bar(self, qurl):
        current_browser = self.current_browser()
        if current_browser and current_browser == self.sender():
            self.url_bar.setText(qurl.toString())
            self.update_security_indicator(qurl)
            self.update_navigation_buttons()

    def update_tab_title(self, title):
        browser = self.sender()
        try:
            index = self.browsers.index(browser)
            self.tab_bar.update_tab_title(index, title)
        except ValueError:
            pass

    def update_tab_icon(self, icon):
        browser = self.sender()
        try:
            index = self.browsers.index(browser)
            self.tab_bar.update_tab_icon(index, icon)
        except ValueError:
            pass

    def update_security_indicator(self, qurl):
        if qurl.scheme() == "https":
            self.security_icon.setText("🔒")
            self.security_icon.setStyleSheet(f"color: {POTATO_DARK}; font-size: 12px;")
            self.security_info.setText("Connection is secure")
        elif qurl.scheme() == "http":
            self.security_icon.setText("⚠️")
            self.security_icon.setStyleSheet("color: #ea4335; font-size: 12px;")
            self.security_info.setText("Connection is not secure")
        else:
            self.security_icon.setText("!?")
            self.security_icon.setStyleSheet(f"color: {POTATO_ACCENT}; font-size: 12px;")
            self.security_info.setText("")

    def update_navigation_buttons(self):
        browser = self.current_browser()
        if browser:
            history = browser.page().history()
            self.back_btn.setEnabled(history.canGoBack())
            self.forward_btn.setEnabled(history.canGoForward())

    def load_started(self):
        browser = self.sender()
        try:
            index = self.browsers.index(browser)
            self.tab_bar.set_tab_loading(index, True)
            if index == self.current_browser_index:
                self.progress_bar.setVisible(True)
                self.progress_bar.setValue(0)
                self.status_label.setText("Loading...")
        except ValueError:
            pass

    def load_progress(self, progress):
        browser = self.sender()
        try:
            index = self.browsers.index(browser)
            if index == self.current_browser_index:
                self.progress_bar.setValue(progress)
                self.status_label.setText(f"Loading... {progress}%")
        except ValueError:
            pass

    def load_finished(self, success):
        browser = self.sender()
        try:
            index = self.browsers.index(browser)
            self.tab_bar.set_tab_loading(index, False)
            if index == self.current_browser_index:
                self.progress_bar.setVisible(False)
                if success:
                    self.status_label.setText("Done")
                else:
                    self.status_label.setText("Failed to load")
            
                QTimer.singleShot(3000, lambda: self.status_label.setText("Ready"))
        except ValueError:
            pass

    def show_menu(self):
        menu = QMenu(self)
        menu.setStyleSheet(f"""
            QMenu {{
                background-color: {POTATO_LIGHT};
                border: 0px solid {POTATO_ACCENT};
                padding: 8px 0;
                min-width: 200px;
            }}
            QMenu::item {{
                padding: 12px 24px;
                color: {TEXT_COLOR};
                font-size: 14px;
                border: none;
            }}
            QMenu::item:selected {{
                background-color: {POTATO_ACCENT};
                color: white;
            }}
            QMenu::separator {{
                height: 1px;
                background-color: {POTATO_ACCENT};
                margin: 8px 0;
            }}
        """)
        
        new_tab_action = QAction("New tab", self)
        new_tab_action.setShortcut(QKeySequence("Ctrl+T"))
        new_tab_action.triggered.connect(self.add_new_tab)
        menu.addAction(new_tab_action)
        
        new_window_action = QAction("New window", self)
        new_window_action.setShortcut(QKeySequence("Ctrl+N"))
        new_window_action.triggered.connect(self.new_window)
        menu.addAction(new_window_action)
        menu.addSeparator()

        zoom_menu = menu.addMenu("Zoom")
        
        zoom_in_action = QAction("Zoom in", self)
        zoom_in_action.setShortcut(QKeySequence("Ctrl++"))
        zoom_in_action.triggered.connect(self.zoom_in)
        zoom_menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction("Zoom out", self)
        zoom_out_action.setShortcut(QKeySequence("Ctrl+-"))
        zoom_out_action.triggered.connect(self.zoom_out)
        zoom_menu.addAction(zoom_out_action)
        
        zoom_reset_action = QAction("Reset zoom", self)
        zoom_reset_action.setShortcut(QKeySequence("Ctrl+0"))
        zoom_reset_action.triggered.connect(self.zoom_reset)
        zoom_menu.addAction(zoom_reset_action)
        
        menu.addSeparator()
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.triggered.connect(self.close)
        menu.addAction(exit_action)

        menu.exec(self.menu_btn.mapToGlobal(self.menu_btn.rect().bottomLeft()))

    def new_window(self):
        new_browser = PotatoBrowser()
        new_browser.setWindowIcon(QIcon("image/icon.png"))
        new_browser.show()

    def zoom_in(self):
        browser = self.current_browser()
        if browser:
            browser.setZoomFactor(browser.zoomFactor() + 0.1)

    def zoom_out(self):
        browser = self.current_browser()
        if browser:
            browser.setZoomFactor(max(0.1, browser.zoomFactor() - 0.1))

    def zoom_reset(self):
        browser = self.current_browser()
        if browser:
            browser.setZoomFactor(1.0)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_F5:
            self.reload_page()
        elif event.key() == Qt.Key.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
        elif event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_T:
                self.add_new_tab()
            elif event.key() == Qt.Key.Key_W:
                self.close_tab(self.current_browser_index)
            elif event.key() == Qt.Key.Key_L:
                self.url_bar.setFocus()
                self.url_bar.selectAll()
            elif event.key() == Qt.Key.Key_R:
                self.reload_page()
            elif event.key() == Qt.Key.Key_Plus:
                self.zoom_in()
            elif event.key() == Qt.Key.Key_Minus:
                self.zoom_out()
            elif event.key() == Qt.Key.Key_0:
                self.zoom_reset()        
        super().keyPressEvent(event)

    def closeEvent(self, event):
        os.system("taskkill /f /im server.exe")
        event.accept()

    def load_styles(self):
        with open("potato/style.qss", "r") as f:
            self.setStyleSheet(f.read())

if __name__ == "__main__":
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--proxy-server=socks5://127.0.0.1:9050"
    threading.Thread(target=lambda: os.system("cd Server && server.exe")).start()

    app = QApplication(sys.argv)
    app.setApplicationName("Potato Browser")
    
    window = PotatoBrowser()
    window.load_styles()
    window.setWindowIcon(QIcon("image/icon.png"))
    window.show()
    
    sys.exit(app.exec())