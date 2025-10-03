from PySide6.QtWidgets import QLabel, QHBoxLayout, QWidget
from PySide6.QtCore import QTimer
from ChatResponse import ChatResponse
import pygame

class ChatManager:
    def __init__(self, messages_layout, scroll_area, input_widget=None):
        self.messages_layout = messages_layout
        self.scroll_area = scroll_area
        self.input_widget = input_widget

    def send_message(self, text):
        text = text.strip()
        if not text:
            return

        # Mensagem do usuário
        self.add_message(text, is_user=True)

        # Balão temporário "..."
        placeholder_bubble = self.add_message("...", is_user=False)
        main_window = self.scroll_area.window()
        main_window.set_avatar_thinking()

        def process_and_update():
            chat = ChatResponse()
            resposta_texto = chat.process(message=text)

            # Atualiza o balão "..." para a resposta real
            placeholder_bubble.setText(resposta_texto)

            # Avatar "falando"
            main_window.set_avatar_speaking()

            def tocar_audio_e_voltar_avatar():
                pygame.mixer.init()
                pygame.mixer.music.load(chat.audio_file)
                pygame.mixer.music.play()

                def check_audio():
                    if pygame.mixer.music.get_busy():
                        # ainda tocando, checa novamente em 100ms
                        QTimer.singleShot(100, check_audio)
                    else:
                        # áudio terminou
                        main_window.set_avatar_idle()  # volta avatar
                        pygame.mixer.music.stop()
                        pygame.mixer.quit()

                # inicia a checagem assíncrona
                QTimer.singleShot(100, check_audio)

            # Chama a função para tocar o áudio
            tocar_audio_e_voltar_avatar()

        # Roda o processamento em um timer (não trava a UI)
        QTimer.singleShot(100, process_and_update)


    def add_message(self, text, is_user=False):
        # Cria o balão
        bubble = QLabel()
        bubble.setText(text)
        bubble.setWordWrap(True)
        bubble.setMaximumWidth(self.scroll_area.width())  # limite da largura
        bubble.setStyleSheet("""
            QLabel {
                background-color: #4f4e4e;
                color: white;
                font-weight: bold;
                font-family: system-ui, -apple-system, sans-serif;
                padding: 16px 20px;
                border-radius: 18px;
                font-size: large;
            }
        """)

        # Cor e alinhamento
        bubble_layout = QHBoxLayout()
        if is_user:
            bubble.setStyleSheet(bubble.styleSheet() + "background-color: #008f7a;")
            bubble_layout.addStretch()
            bubble_layout.addWidget(bubble)
        else:
            bubble.setStyleSheet(bubble.styleSheet() + "background-color: #2d2d2d;")
            bubble_layout.addWidget(bubble)
            bubble_layout.addStretch()

        container = QWidget()
        container.setLayout(bubble_layout)

        # Adiciona ao layout e rola para o final
        self.messages_layout.addWidget(container)
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        )

        # Retorna o QLabel do balão para atualizar depois
        return bubble

