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
            # Desenha a imagem cobrindo toda a tela
            painter.drawPixmap(self.rect(), self.background_pixmap)
            # Escurece um pouco o fundo (opcional)
            painter.fillRect(self.rect(), QColor(0, 0, 0, 80))
        super().paintEvent(event)