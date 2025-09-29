import sys
from PyQt6.QtWidgets import QApplication
from presentation.Login import LoginWindow
from presentation.Style import APP_STYLE

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLE)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
