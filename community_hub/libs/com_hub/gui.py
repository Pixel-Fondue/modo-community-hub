try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import (QMainWindow, QApplication, QTabWidget, QWidget, QVBoxLayout,
                                   QTabBar)
except ImportError:
    from PySide.QtCore import Qt
    from PySide.QtGui import (QMainWindow, QApplication, QTabWidget, QWidget, QVBoxLayout, QTabBar)

# Kit imports
from com_hub import utils
from com_hub.prefs import Text, KEYS, CSS
from com_hub.gui_utils import build_tab


class CommunityHub(QMainWindow):

    def __init__(self):
        super(CommunityHub, self).__init__(None)
        self.setWindowTitle(Text.title)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.resize(450, 300)
        self.authors = utils.load_resource(KEYS.authors)
        # Initialize GUI args
        self.tabs = QTabWidget()
        self.build_ui()

        # Display the UI
        self.show()

    def build_ui(self):
        self.setStyleSheet(CSS)
        base_widget = QWidget(self)
        base_layout = QVBoxLayout(base_widget)
        base_layout.setContentsMargins(2, 2, 2, 2)
        base_widget.setLayout(base_layout)

        # Generate Tabs
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.tab_close)
        self.tabs.setObjectName("Tabs")
        base_layout.addWidget(self.tabs)

        for i, tab_type in enumerate((KEYS.kits, KEYS.videos, KEYS.social)):
            tab = build_tab(tab_type)
            self.tabs.addTab(tab, tab_type)
            # Remove the close button from these core tabs
            self.tabs.tabBar().setTabButton(i, QTabBar.RightSide, None)

        self.setCentralWidget(base_widget)

    def closeEvent(self, event):
        """PySide method: Handle closing the UI"""
        self.close()
        event.accept()

    def tab_close(self, index):
        """Handle closing Author tabs."""
        if index > 2:  # Keep 0-2 locked.
            # Ge the widget attached to the tab
            tab_widget = self.tabs.widget(index)
            # Remove tab from tab widget
            self.tabs.removeTab(index)
            # Destroy widget as it's no longer needed.
            del tab_widget


if __name__ == "__main__":
    """Used to test this UI outside of Modo"""
    import sys

    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)

    window = CommunityHub()

    sys.exit(app.exec_())
