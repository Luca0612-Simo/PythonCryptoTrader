import sys
from PyQt6.QtWidgets import QApplication
from presentation.Login import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
