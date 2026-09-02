import sys
from PySide6.QtWidgets import QApplication, QMainWindow

# Импортируем сгенерированный класс из файла
from loading_window.ui.ui_loading_window import Ui_MainWindow

class LoadingWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Инициализируем интерфейс
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Вызываем настройку событий и логики
        self.init_logic()

    def init_logic(self):
        # Обращаемся к элементам через self.ui.<objectName>
        self.ui.label.setText("Загрузка...")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = LoadingWindow()
    window.show()

    sys.exit(app.exec())