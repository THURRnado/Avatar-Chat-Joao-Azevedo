from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import Qt

class CentralWidget(QWidget):
    def __init__(self, background_pixmap, parent=None):
        super().__init__(parent)
        self.background_pixmap = background_pixmap

    def paintEvent(self, event):
        painter = QPainter(self)
        if not self.background_pixmap.isNull():
            # Redimensiona o fundo para ocupar todo o espaço do widget
            scaled_pixmap = self.background_pixmap.scaled(
                self.size(),              # redimensiona conforme o tamanho da janela
                Qt.IgnoreAspectRatio,     # estica sem manter proporção
                Qt.SmoothTransformation   # suaviza a imagem ao redimensionar
            )

            # Desenha a imagem redimensionada ocupando todo o espaço
            painter.drawPixmap(0, 0, scaled_pixmap)

            # Escurece o fundo (opcional)
            painter.fillRect(self.rect(), QColor(0, 0, 0, 80))

        super().paintEvent(event)