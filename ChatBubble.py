from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPainter, QColor, QPolygon
from PySide6.QtCore import Qt, QPoint

class ChatBubble(QWidget):
    def __init__(self, text, is_user=False, parent=None):
        super().__init__(parent)
        self.is_user = is_user
        self.bg_color = QColor("#00897b") if is_user else QColor("#2d2d2d")
        self.text_color = Qt.white

        self.label = QLabel(text)
        self.label.setWordWrap(True)
        self.label.setStyleSheet("""
            color: white; 
            font-weight: bold; 
            font-family: system-ui; 
            font-size: 24px;   /* tamanho da fonte */
        """)
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.setContentsMargins(26, 20, 26, 20)  # espaço interno do balão
        self.setLayout(layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # dimensões do balão
        rect = self.rect()
        radius = 12
        triangle_size = 12
        
        # ajusta o retângulo para o triângulo lateral
        if self.is_user:
            bubble_rect = rect.adjusted(0, 0, -triangle_size, 0)  # triângulo à direita
        else:
            bubble_rect = rect.adjusted(triangle_size, 0, 0, 0)   # triângulo à esquerda

        # desenha o balão arredondado
        painter.setBrush(self.bg_color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(bubble_rect, radius, radius)

        # desenha o triângulo lateral
        triangle = QPolygon()
        if self.is_user:
            # triângulo à direita
            triangle.append(QPoint(bubble_rect.right(), bubble_rect.top() + 10))
            triangle.append(QPoint(bubble_rect.right() + triangle_size, bubble_rect.top() + 15))
            triangle.append(QPoint(bubble_rect.right(), bubble_rect.top() + 25))
        else:
            # triângulo à esquerda
            triangle.append(QPoint(bubble_rect.left(), bubble_rect.top() + 10))
            triangle.append(QPoint(bubble_rect.left() - triangle_size, bubble_rect.top() + 15))
            triangle.append(QPoint(bubble_rect.left(), bubble_rect.top() + 25))

        painter.drawPolygon(triangle)
        super().paintEvent(event)