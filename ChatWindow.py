from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, 
    QLineEdit, QScrollArea
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap

from CentralWidget import CentralWidget
from ChatManager import ChatManager
import os
import soundfile as sf
import numpy as np


# ----------- Função para carregar frames -----------
def load_frames_from_folder(folder_path):
    frames = [
        os.path.join(folder_path, f)
        for f in sorted(os.listdir(folder_path))
        if f.lower().endswith(".png")
    ]
    return frames



# ========================= Janela Principal =========================
class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat com JA")
        self.setGeometry(390, 15, 1200, 1024)

        self.avatar_zoom = 1.3

        # Fundo
        self.background_pixmap = QPixmap("avatar/background/cartoon/gabinete_pessoal_cartoon_desfocado.png")

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

        # Frames do avatar
        self.avatar_frames = {
            "idle": load_frames_from_folder("avatar/solo/avatar_parado(new)"),
            "thinking": load_frames_from_folder("avatar/solo/avatar_pensando"),
            "speaking": load_frames_from_folder("avatar/solo/avatar_falando(new)"),
        }

        self.current_frame = 0

        # ---- Timer NOVO para sincronizar áudio -> frames ----
        self.audio_volume_timer = QTimer()
        self.audio_volume_timer.setInterval(40)
        self.audio_volume_timer.timeout.connect(self.update_speaking_from_audio)

        # Controle do áudio
        self.audio_data = None
        self.audio_index = 0
        self.audio_sample_rate = 1

        # Timer antigo (idle e thinking)
        self.avatar_timer = QTimer()
        self.avatar_interval = 2000
        self.avatar_state = "idle"
        self.avatar_timer.timeout.connect(self.update_avatar_frame)
        self.set_avatar_idle()



    # ========================= Setup UI =========================
    def setup_ui(self, central_widget):
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Espaço para avatar
        left_spacer = QWidget()
        left_spacer.setFixedWidth(700)
        left_spacer.setStyleSheet("background-color: transparent;")

        # Layout do chat
        chat_layout = QVBoxLayout()
        chat_layout.setContentsMargins(0, 0, 0, 480)
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
            lambda: (self.chat_manager.send_message(self.message_input.text(), confirm=True),
                     self.message_input.clear())
        )

        chat_layout.addWidget(self.scroll_area)
        chat_layout.addWidget(self.message_input)

        main_layout.addWidget(left_spacer)
        main_layout.addLayout(chat_layout, 1)

        # Avatar
        self.avatar_label = QLabel(self)
        self.avatar_label.setFixedSize(1000, 1000)
        self.avatar_label.move(0, self.height() - 850) # <-- altera altura do avatar
        self.avatar_label.setStyleSheet(
            "background-color: transparent; border:none; border-radius:20%;"
        )



    # =================== Redimensionamento do avatar ===================
    def resizeEvent(self, event):
        if hasattr(self, 'avatar_label'):
            base_y = self.height() - 850 # <-- altera altura do avatar
            self.avatar_label.move(0, base_y - int(getattr(self, 'breath_offset', 0)))
        super().resizeEvent(event)



    # =================== Estados (idle, thinking, speaking) ===================
    def set_avatar_idle(self):
        self.avatar_timer.stop()
        self.audio_volume_timer.stop()
        self.avatar_state = "idle"
        self.avatar_interval = 5000
        self.show_current_frame()
        self.avatar_timer.start(self.avatar_interval)

    def set_avatar_thinking(self):
        self.avatar_timer.stop()
        self.audio_volume_timer.stop()
        self.avatar_state = "thinking"
        self.avatar_interval = 2000
        self.show_current_frame()
        self.avatar_timer.start(self.avatar_interval)

    def set_avatar_speaking(self, wav_path):
        """
        ATIVA a sincronização pelo áudio.
        """
        self.avatar_timer.stop()
        self.avatar_state = "speaking"

        # Carrega o áudio
        self.audio_data, self.audio_sample_rate = sf.read(wav_path)
        if len(self.audio_data.shape) > 1:
            self.audio_data = self.audio_data.mean(axis=1)

        self.audio_index = 0

        self.audio_volume_timer.start()



    # =================== Mostrar frame ===================
    def show_current_frame(self):
        if self.avatar_state not in self.avatar_frames:
            return
        frames = self.avatar_frames[self.avatar_state]
        if not frames:
            return

        self.current_frame = (self.current_frame + 1) % len(frames)
        pixmap = QPixmap(frames[self.current_frame])
        if not pixmap.isNull():
            size = int(700 * self.avatar_zoom)
            self.avatar_label.setPixmap(
                pixmap.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )



    # =================== (idle/thinking) ===================
    def update_avatar_frame(self):
        self.show_current_frame()
        self.avatar_timer.setInterval(self.avatar_interval)



    # =================== Sincronização com o áudio ===================
    def update_speaking_from_audio(self):
        if self.audio_data is None:
            return
        
        chunk_size = 1024
        chunk = self.audio_data[self.audio_index:self.audio_index + chunk_size]
        self.audio_index += chunk_size

        if len(chunk) == 0:
            self.set_avatar_idle()
            return

        volume = np.linalg.norm(chunk) * 10
        frames = self.avatar_frames["speaking"]

        THRESHOLD = 20

        target_frame = 1 if volume > THRESHOLD else 0

        if target_frame != self.current_frame:
            self.current_frame = target_frame
            pix = QPixmap(frames[self.current_frame])
            self.avatar_label.setPixmap(
                pix.scaled(
                    int(700 * self.avatar_zoom),
                    int(700 * self.avatar_zoom),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )