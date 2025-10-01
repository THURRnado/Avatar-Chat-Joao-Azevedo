from PySide6.QtWidgets import QLabel, QHBoxLayout, QWidget
from PySide6.QtCore import QTimer

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

        # Avatar "falando"
        main_window = self.scroll_area.window()  # pega a janela principal
        if hasattr(main_window, "set_avatar_speaking"):
            main_window.set_avatar_speaking()

        # Resposta do bot (simulação com delay)
        QTimer.singleShot(400, lambda: self.add_message("Resposta do bot", is_user=False))

        # Depois de 2 segundos, volta pro avatar parado
        QTimer.singleShot(800, lambda: main_window.set_avatar_idle())

        # Limpa input
        if self.input_widget:
            self.input_widget.clear()


    def add_message(self, text, is_user=False):
        # Cria o balão
        bubble = QLabel()
        bubble.setText(text)
        bubble.setWordWrap(True)
        bubble.setMaximumWidth(self.scroll_area.width())  # metade da tela
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
