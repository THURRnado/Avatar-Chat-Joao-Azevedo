from PySide6.QtWidgets import QHBoxLayout, QWidget
from PySide6.QtCore import QTimer
from ChatResponse import ChatResponse
import pygame
from ChatBubble import ChatBubble
from avatar_server import iniciar_servidor

#ESSA PARTE SERA A RESPONSAVEL COM A COMUNICACAO COM A IA

class ChatManager:
    def __init__(self, messages_layout, scroll_area, input_widget=None):
        self.messages_layout = messages_layout
        self.scroll_area = scroll_area
        self.input_widget = input_widget

        # Inicia o servidor Flask local
        iniciar_servidor(self)

    def clear_messages(self):
        while self.messages_layout.count():
            item = self.messages_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def send_message(self, text, confirm):
        text = text.strip()
        if not text:
            return
        
        self.clear_messages()

        # Mensagem do usuário
        if confirm:
            self.add_message(text, is_user=True)

        # Balão temporário "..."
        placeholder_bubble = self.add_message("...", is_user=False)
        main_window = self.scroll_area.window()
        main_window.set_avatar_thinking()

        def process_and_update():

            chat = ChatResponse()
            if confirm:
                resposta_texto = chat.process(message=text)
            else:
                resposta_texto = chat.process(message='')

            # Atualiza o balão "..." para a resposta real
            placeholder_bubble.label.setText(resposta_texto)

            # Avatar "falando"
            main_window = self.scroll_area.window()
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
        bubble = ChatBubble(text, is_user)
        
        bubble_layout = QHBoxLayout()
        if is_user:
            bubble_layout.addStretch()
            bubble_layout.addWidget(bubble)
        else:
            bubble_layout.addWidget(bubble)
            bubble_layout.addStretch()

        container = QWidget()
        container.setLayout(bubble_layout)

        self.messages_layout.addWidget(container)
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        )
        return bubble

