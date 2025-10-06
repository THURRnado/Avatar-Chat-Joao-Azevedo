from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, 
    QLineEdit, QScrollArea
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QPainter, QColor

from ChatManager import ChatManager


# ================= Central Widget com fundo =================
class CentralWidget(QWidget):
    def __init__(self, background_pixmap, parent=None):
        super().__init__(parent)
        self.background_pixmap = background_pixmap

    def paintEvent(self, event):
        painter = QPainter(self)
        if not self.background_pixmap.isNull():
            # Desenha a imagem cobrindo toda a tela
            painter.drawPixmap(self.rect(), self.background_pixmap)
            # Escurece um pouco o fundo (opcional)
            painter.fillRect(self.rect(), QColor(0, 0, 0, 80))
        super().paintEvent(event)


# ================= Janela Principal =================
class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat com JA")
        self.setGeometry(100, 100, 1280, 720)

        # Fundo
        self.background_pixmap = QPixmap("avatar/fundo_farol/fundo_ja_farol.png")
        
        # Central widget com fundo
        central_widget = CentralWidget(self.background_pixmap)
        self.setCentralWidget(central_widget)

        # Configura UI
        self.setup_ui(central_widget)

        # Chat manager
        self.chat_manager = ChatManager(
            messages_layout=self.messages_layout,
            scroll_area=self.scroll_area,
            input_widget=self.message_input
        )

        # Avatar Animation
        self.speaking_frames = [
            "avatar/solo/avatar_ja_falando_sf_1024_1024.png",
            "avatar/solo/avatar_ja_falando2_sf_1024_1024.png"
        ]
        self.current_frame = 0
        self.speaking_timer = QTimer()

        self.avatar_state = "idle"
        self.set_avatar_idle()  # inicia com avatar idle

    # ================= Setup UI =================
    def setup_ui(self, central_widget):
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Espaço para avatar
        left_spacer = QWidget()
        left_spacer.setFixedWidth(720)
        left_spacer.setStyleSheet("background-color: transparent;")

        # Layout do chat
        chat_layout = QVBoxLayout()
        chat_layout.setContentsMargins(0, 0, 0, 200)
        chat_layout.setSpacing(10)

        # Scroll area para mensagens
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(
            "background-color: rgba(108, 107, 107, 0); border:none;"
        )
        self.scroll_area_widget = QWidget()
        self.scroll_area.setWidget(self.scroll_area_widget)

        # Layout interno das mensagens
        self.messages_layout = QVBoxLayout(self.scroll_area_widget)
        self.messages_layout.setAlignment(Qt.AlignBottom)
        self.messages_layout.setContentsMargins(10, 10, 10, 10)
        self.messages_layout.setSpacing(10)

        # Área de digitação
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Digite sua mensagem...")
        self.message_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(108, 107, 107, 0);
                border: 2px solid #4f4e4e;
                border-radius: 10px;
                padding: 15px;
                font-size: 14px;
                color: white;
                font-weight: bold;
            }
        """)
        self.message_input.returnPressed.connect(
            lambda: (self.chat_manager.send_message(self.message_input.text()),
                     self.message_input.clear())
        )

        chat_layout.addWidget(self.scroll_area)
        chat_layout.addWidget(self.message_input)

        main_layout.addWidget(left_spacer)
        main_layout.addLayout(chat_layout, 1)

        # Avatar
        self.avatar_label = QLabel(self)
        self.avatar_label.setFixedSize(650, 650)
        self.avatar_label.move(200, self.height() - 550)
        self.avatar_label.setStyleSheet(
            "background-color: transparent; border:none; border-radius:20%;"
        )

    # ================= Redimensionamento =================
    def resizeEvent(self, event):
        if hasattr(self, 'avatar_label'):
            self.avatar_label.move(200, self.height() - 550)
        super().resizeEvent(event)

    # ================= Estados do avatar =================
    def set_avatar_idle(self):
        self.speaking_timer.stop()
        self.avatar_state = "idle"
        self.load_avatar_image("avatar/solo/avatar_ja_base_sf_1024_1024.png")

    def set_avatar_thinking(self):
        self.speaking_timer.stop()
        self.avatar_state = "thinking"
        self.load_avatar_image("avatar/solo/avatar_ja_pensando_sf_1024_1024.png")

    def set_avatar_speaking(self):
        self.avatar_state = "speaking"
        self.current_frame = 0
        self.speaking_timer.singleShot(200, self.update_speaking_avatar)

    # ================= Helper =================
    def load_avatar_image(self, path):
        pixmap = QPixmap(path)
        if not pixmap.isNull():
            self.avatar_label.setPixmap(
                pixmap.scaled(500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
        else:
            self.avatar_label.setText("Imagem\nnão\nencontrada")

    def update_speaking_avatar(self):
        if self.avatar_state != "speaking":
            self.speaking_timer.stop()
            return

        pixmap = QPixmap(self.speaking_frames[self.current_frame])
        if not pixmap.isNull():
            self.avatar_label.setPixmap(
                pixmap.scaled(650, 650, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )

        self.current_frame += 1
        if self.current_frame >= len(self.speaking_frames):
            self.current_frame = 0

        self.speaking_timer.singleShot(2000, self.update_speaking_avatar)
