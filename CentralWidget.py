from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor

#PARTE QUE LIDA COM A PARTE DE FUNDO DO CHAT

class CentralWidget(QWidget):
    def __init__(self, background_pixmap, parent=None):
        super().__init__(parent)
        self.background_pixmap = background_pixmap

    def paintEvent(self, event):
        painter = QPainter(self)
        if not self.background_pixmap.isNull():
            # Centraliza a imagem no meio da janela, sem redimensionar
            pixmap_width = self.background_pixmap.width()
            pixmap_height = self.background_pixmap.height()
            widget_width = self.width()
            widget_height = self.height()

            # Calcula posição para centralizar
            x = (widget_width - pixmap_width) // 2
            y = (widget_height - pixmap_height) // 2

            # Desenha sem redimensionar
            painter.drawPixmap(x, y, self.background_pixmap)

            # Escurece o fundo (opcional)
            painter.fillRect(self.rect(), QColor(0, 0, 0, 80))

        super().paintEvent(event)