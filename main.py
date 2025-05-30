import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog
from PyQt5.QtGui import QPainter, QImage, QPen
from PyQt5.QtCore import Qt, QPoint
from utils import send_to_mathpix, evaluate_latex, save_result_image

class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.image = QImage(400, 400, QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.last_point = QPoint()
        self.setFixedSize(400, 400)

    def mousePressEvent(self, event):
        self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        painter = QPainter(self.image)
        pen = QPen(Qt.black, 8, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)
        painter.drawLine(self.last_point, event.pos())
        self.last_point = event.pos()
        self.update()

    def paintEvent(self, event):
        canvas_painter = QPainter(self)
        canvas_painter.drawImage(self.rect(), self.image, self.image.rect())

    def save(self, path):
        self.image.save(path)

class MathApp(QWidget):
    def __init__(self):
        super().__init__()
        self.canvas = Canvas()
        self.save_button = QPushButton("Распознать и вычислить")
        self.save_button.clicked.connect(self.process_drawing)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.save_button)
        self.setLayout(layout)
        self.setWindowTitle("MathDraw AI")

    def process_drawing(self):
        path = "equation.png"
        self.canvas.save(path)
        latex_expr = send_to_mathpix(path)
        print("Распознано:", latex_expr)

        result = evaluate_latex(latex_expr)
        print("Результат:", result)

        save_result_image(latex_expr, result, "result.png")
        print("Сохранено изображение результата в result.png")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MathApp()
    window.show()
    sys.exit(app.exec_())
