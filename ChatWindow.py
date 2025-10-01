from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLabel,
    QVBoxLayout, QHBoxLayout, QLineEdit, QScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from ChatManager import ChatManager

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat com JA")
        self.setGeometry(100, 100, 1400, 900)
        self.setStyleSheet("background-color: #4f4e4e;")

        self.setup_ui()

        self.chat_manager = ChatManager(
            messages_layout=self.messages_layout,
            scroll_area=self.scroll_area,
            input_widget=self.message_input
        )

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10,10,10,10)
        main_layout.setSpacing(10)

        # Espaço para avatar
        left_spacer = QWidget()
        left_spacer.setFixedWidth(370)
        left_spacer.setStyleSheet("background-color: transparent;")

        # Layout do chat
        chat_layout = QVBoxLayout()
        chat_layout.setContentsMargins(0,0,0,0)
        chat_layout.setSpacing(10)

        # Scroll area para mensagens
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border:none; background-color: #6c6b6b;")
        self.scroll_area_widget = QWidget()
        self.scroll_area.setWidget(self.scroll_area_widget)

        # Layout interno das mensagens
        self.messages_layout = QVBoxLayout(self.scroll_area_widget)
        self.messages_layout.setAlignment(Qt.AlignBottom)  # mensagens crescem de baixo para cima
        self.messages_layout.setContentsMargins(10,10,10,10)
        self.messages_layout.setSpacing(10)

        # Área de digitação
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Digite sua mensagem...")
        self.message_input.setStyleSheet("""
            QLineEdit {
                background-color: #6c6b6b;
                border: 2px solid #4f4e4e;
                border-radius: 10px;
                padding: 15px;
                font-size: 14px;
                color: white;
                font-weight: bold;
            }
        """)
        self.message_input.returnPressed.connect(
            lambda: self.chat_manager.send_message(self.message_input.text())
        )

        # Adiciona scroll e input ao layout do chat
        chat_layout.addWidget(self.scroll_area)
        chat_layout.addWidget(self.message_input)

        # Adiciona spacer e chat ao layout principal
        main_layout.addWidget(left_spacer)
        main_layout.addLayout(chat_layout, 1)

        # Avatar
        self.avatar_label = QLabel(self)
        self.avatar_label.setFixedSize(350,350)
        self.avatar_label.move(20, self.height()-340)
        self.avatar_label.setStyleSheet("background-color: transparent; border:none; border-radius:20%;")
        self.load_avatar_image()

    def resizeEvent(self, event):
        if hasattr(self, 'avatar_label'):
            self.avatar_label.move(20, self.height()-340)
        super().resizeEvent(event)

    def load_avatar_image(self):
        pixmap = QPixmap("avatar/solo/avatarJA_parado.png")
        if not pixmap.isNull():
            self.avatar_label.setPixmap(pixmap.scaled(340,340, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.avatar_label.setText("Imagem\nnão\nencontrada")

    def set_avatar_speaking(self):
        pixmap = QPixmap("avatar/solo/avatarJA_falando.png")
        if not pixmap.isNull():
            self.avatar_label.setPixmap(pixmap.scaled(340, 340, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def set_avatar_idle(self):
        pixmap = QPixmap("avatar/solo/avatarJA_parado.png")
        if not pixmap.isNull():
            self.avatar_label.setPixmap(pixmap.scaled(340, 340, Qt.KeepAspectRatio, Qt.SmoothTransformation))
