from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QInputDialog, QLineEdit
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtGui import QFont
import sys

# TODO изменить наследование окна с QMainWindow на QWidgets
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Оценочки")
        self.resize(400, 400)
        self.setFont(QFont("Comic Sans MS", 10, QFont.Bold))
        self.center_str = QLabel("#ШколаВнеПолитики")
        self.center_str.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.center_str)
        self.add_buttons()
        self.init_ui()

    def init_ui(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("students.sqlite")
        self.create_bd()
        self.show()

    def add_buttons(self):
        mark_button = QPushButton("добавить оценку", self)
        mark_button.resize(mark_button.sizeHint())
        mark_button.move(10, 10)
        mark_button.clicked.connect(self.mark_button)

        student_button = QPushButton("добавить ученика", self)
        student_button.resize(student_button.sizeHint())
        student_button.move(10, 50)
        student_button.clicked.connect(self.data_button)

        mark_button = QPushButton("Посмотреть таблицу", self)
        mark_button.resize(mark_button.sizeHint())
        mark_button.move(10, 90)
        # mark_button.clicked.connect(self.data_button)

    def create_bd(self):
        print(1)
        if not self.db.open():
            print("Не получилось открыть базу :(")
        self.query = QSqlQuery()
        print(2)
        self.query.exec("""CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            name TEXT NOT NULL,
            mark TEXT)
            """)
    
    def get_text(self):
        text, ok = QInputDialog.getText(self, "добавление ученика", "Введите имя ученика:", QLineEdit.Normal, "")
        if text != "" and ok:
            return text

    def data_button(self):
        name = self.get_text()
        self.query.prepare("INSERT INTO students (name) VALUES (?)")
        self.query.addBindValue(name)
        self.query.exec()

    def mark_button(self):
        names = self.get_name()
        name = self.get_choice(names)
        mark = self.get_mark()
        add_mark = self.get_grade(name, mark)
        self.update_mark(name, add_mark)

    def update_mark(self, name, mark):
        self.query.prepare("UPDATE students SET mark = (?) WHERE name = (?)")
        self.query.addBindValue(mark)
        self.query.addBindValue(name)
        self.query.exec()        

    def get_grade(self, name, mark):
        self.query.prepare("SELECT mark FROM students WHERE name = (?)")
        self.query.addBindValue(name)
        self.query.exec()
        while self.query.next():
            marks = self.query.value(self.query.record().indexOf("mark"))
            marks += f' {mark}'
        return marks


    def get_name(self):
        self.query.prepare("SELECT name FROM students")
        if not self.query.exec():
            print("Не получилось загрузить БД :(", self.query.lastError())
        names = []
        name_index = self.query.record().indexOf("name")
        while self.query.next():
            name = self.query.value(name_index)
            names.append(name)
        return names

    def get_choice(self, names):
        name, ok = QInputDialog.getItem(self, "ученики", "Выберите ученика:", names, 0, False)
        if ok:
            return name

    def get_mark(self):
        mark, ok = QInputDialog.getInt(self, "добавить оценку", "Выберите оценку:", 5, 2, 5, 1)
        if ok:
            return mark

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = Window()
    sys.exit(app.exec_())
