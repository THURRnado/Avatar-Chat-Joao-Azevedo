from PySide6.QtWidgets import QLabel, QHBoxLayout, QWidget

class ChatManager:
    def __init__(self, messages_layout, scroll_area, input_widget=None):
        self.messages_layout = messages_layout
        self.scroll_area = scroll_area
        self.input_widget = input_widget  # Opcional, para limpar depois de enviar

    def send_message(self, text):
        text = text.strip()
        if not text:
            return

        # Adiciona mensagem do usuário
        self.add_message(text, is_user=True)

        # Aqui você pode adicionar resposta do bot
        self.add_message("Resposta do bot", is_user=False)

        # Limpa o input se fornecido
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
