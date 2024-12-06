import sys

from PyQt6.uic.uiparser import QtWidgets
from openpyxl import load_workbook
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget,
    QTableWidgetItem, QDockWidget, QFormLayout,
    QLineEdit, QWidget, QPushButton, QSpinBox,
    QMessageBox, QToolBar, QMessageBox, QDialogButtonBox, QVBoxLayout, QLabel, QTextEdit, QGridLayout
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QAction

import down_excel
import math_func


class MainWindow(QMainWindow):
    list_finally = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.accept = None
        self.setWindowTitle('Методы оптимизации')
        self.setWindowIcon(QIcon('color-swatch.png'))
        self.setGeometry(100, 100, 820, 450)

        layout = QGridLayout()
        self.setLayout(layout)

        self.input_address = QLineEdit(self)
        layout.addWidget(self.input_address, 0, 0)

        self.input = QTextEdit("")
        layout.addWidget(self.input, 2, 0)
        self.input.setReadOnly(True)
        self.input.hide()

        self.table = QTableWidget(self)
        self.setCentralWidget(self.table)
        layout.addWidget(self.table, 1, 0)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.table.setColumnCount(6)
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 50)
        self.table.setColumnWidth(2, 50)
        self.table.setColumnWidth(3, 50)
        self.table.setColumnWidth(4, 50)
        self.table.setColumnWidth(5, 120)
        self.table.setColumnWidth(6, 120)

        self.table.setHorizontalHeaderItem(3, QTableWidgetItem("1"))
        self.table.setHorizontalHeaderItem(4, QTableWidgetItem("2"))
        self.table.setHorizontalHeaderItem(5, QTableWidgetItem("Количество деталей\n в комплекте"))
        #self.table.setHorizontalHeaderItem(7, QTableWidgetItem("Лучшее сочетание"))

        self.table.setRowCount(3)

        dock = QDockWidget('Панель управления')
        dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

        # create form
        form = QWidget()
        layout = QFormLayout(form)
        form.setLayout(layout)

        btn_add = QPushButton('Загрузить')
        btn_add.clicked.connect(self.add_dock)
        layout.addRow(btn_add)

        btn_show = QPushButton('Показать/скрыть задание')
        btn_show.clicked.connect(self.show_task)
        layout.addRow(btn_show)

        btn_math = QPushButton('Решить')
        btn_math.clicked.connect(self.math_sim)
        layout.addRow(btn_math)

        btn_math_2raz = QPushButton('Максимальное количество деталей 2 размера')
        btn_math_2raz.clicked.connect(self.math_2raz)
        layout.addRow(btn_math_2raz)

        btn_math_new = QPushButton('Решить с измененными данными')
        btn_math_new.clicked.connect(self.math_sim_new)
        layout.addRow(btn_math_new)

        btn_load = QPushButton('Выгрузить')
        btn_load.clicked.connect(self.load_dock)
        layout.addRow(btn_load)

        toolbar = QToolBar('main toolbar')
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        dock.setWidget(form)

    def add_dock(self):
        try:
            addr_str = self.input_address.text()
            if addr_str == "":
                raise Exception
            doc = down_excel.ExcelReader(str(addr_str))
            self.list_to_num, self.list_equip, self.text_to_task = doc.reader()

            row = 0
            count = 0

            for num in range(15):
                item = self.list_to_num[num]
                self.table.setItem(row, count, QTableWidgetItem(str(item)))
                count += 1
                if num == 4 or num == 9:
                    row += 1
                    count = 0

            self.table.setItem(0, 5, QTableWidgetItem(str(self.list_equip[0])))
            self.table.setItem(1, 5, QTableWidgetItem(str(self.list_equip[1])))
            self.table.setItem(2, 5, QTableWidgetItem(str(self.list_equip[2])))
        except Exception:
            dlg = QMessageBox(self)
            dlg.setText(f'Вы либо не ввели адрес в строку адреса, либо по указанному адресу нет файла!')
            button = dlg.exec()

            if button == QMessageBox.StandardButton.Ok:
                print("OK!")

    def show_task(self):
        if self.input.isVisible() == True:
            self.input.hide()
        else:
            self.input.setText(self.text_to_task)
            self.input.show()


    def math_2raz(self):
        s = math_func.Math_func(self.list_to_num, self.list_equip)
        two_raz = s.how_much()
        sum = two_raz[0] + two_raz[1] + two_raz[2]
        dlg = QMessageBox(self)
        str_two_raz = f'Максимальное количество деталей полученных из раскройки 2 детали 1 способом {sum} \nИз них деталей 1 типа: {two_raz[0]}, 2 типа: {two_raz[1]}, 3 типа: {two_raz[2]}.'
        MainWindow.list_finally.append(str_two_raz)
        dlg.setText(str_two_raz)
        s.__del__()
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Ok:
            print("OK!")


    def math_sim(self):

        s = math_func.Math_func(self.list_to_num, self.list_equip)
        sim_str, self.first_quantity = s.calculate()

        first_str = f"Решение первого задания:\n{sim_str}\n. Максимальное количество комплектов: {self.first_quantity}."
        MainWindow.list_finally.append(first_str)
        self.table.setItem(3, 6, QTableWidgetItem(str(sim_str)))
        self.table.setItem(3, 5, QTableWidgetItem(str(self.first_quantity)))
        s.__del__()
        dlg = QMessageBox(self)
        dlg.setText(first_str)
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Ok:
            print("OK!")

    def math_sim_new(self):
        self.table.setItem(0, 5, QTableWidgetItem(str(4)))
        self.table.setItem(1, 5, QTableWidgetItem(str(3)))
        self.table.setItem(2, 5, QTableWidgetItem(str(3)))
        self.list_equip = [4, 3, 3]
        s = math_func.Math_func(self.list_to_num, self.list_equip)
        sim_str, self.second_quantity = s.calculate()
        self.table.setItem(3, 6, QTableWidgetItem(str(sim_str)))
        self.table.setItem(3, 5, QTableWidgetItem(str(self.second_quantity)))
        s.__del__()
        dlg = QMessageBox(self)
        second_string = f"Количество готовых комплектов: {self.second_quantity}. {sim_str} \n Количество комплектов уменьшилось на {self.first_quantity - self.second_quantity} ком.! "
        s_str = f"\nРешение задания c измененным количеством деталей в комплекте:\n{second_string}"
        MainWindow.list_finally.append(s_str)
        dlg.setText(second_string)
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Ok:
            print("OK!")

    def load_dock(self):
        list_f = MainWindow.list_finally
        down_excel.ExcelReader.xlsx_downloader(list_f)
        dlg = QMessageBox(self)
        dlg.setText(f'Данные загружены в папку с программой в файл appending.xlsx')

        button = dlg.exec()

        if button == QMessageBox.StandardButton.Ok:
            print("OK!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())