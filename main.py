from ChatWindow import ChatWindow
import sys
from PySide6.QtWidgets import QApplication

app = QApplication(sys.argv)
    
window = ChatWindow()
window.show()

sys.exit(app.exec())