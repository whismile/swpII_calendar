from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QLineEdit, QToolButton,
                             QSizePolicy, QLayout,
                             QGridLayout, QLabel,
                             QVBoxLayout, QHBoxLayout,
                             QTextEdit)

import calendar
import pickle
import calendarManager


class Button(QToolButton):

    def __init__(self, text, callback):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setText(text)

        self.clicked.connect(callback)

    def sizeHint(self):
        size = super(Button, self).sizeHint()
        size.setHeight(size.height() + 20)
        size.setWidth(max(size.width(), size.height()))
        return size


class Calendar(QWidget):

    def __init__(self, parent=None, year=2018, month=12):
        super().__init__(parent)

        # variables
        self.startDay = 0
        self.maxDay = 0
        self.currentYear = year; self.currentMonth = month; self.currentDay = 0
        self.fileRoot = ".\schedules.txt"
        self.schedule = {}

        try:
            self.schedule = pickle.load(open(self.fileRoot, "rb"))
            print(self.schedule)
        except EOFError:
            pass

        # main layout
        self.mainLayout = QHBoxLayout()
        self.mainLayout.setSizeConstraint(QLayout.SetFixedSize)

        # Left side Layout ================================
        self.leftLayout = QVBoxLayout()

        # handling month ===============================
        self.moveMonth = QHBoxLayout()

        self.previousBtn = Button("<", self.previousMonth)

        # showing Year and month
        self.showCurrentLabel = QLabel(str(self.currentYear) + " / " + str(self.currentMonth))
        self.showCurrentLabel.setAlignment(Qt.AlignCenter)

        self.nextBtn = Button(">", self.nextMonth)

        self.moveMonth.addWidget(self.previousBtn)
        self.moveMonth.addWidget(self.showCurrentLabel)
        self.moveMonth.addWidget(self.nextBtn)
        self.leftLayout.addLayout(self.moveMonth)
        # ==============================================

        # grid layout to appending date Buttons
        self.calendarGrid = QGridLayout()
        self.calendarGrid.setSizeConstraint(QLayout.SetFixedSize)
        self.leftLayout.addLayout(self.calendarGrid)

        # showing status
        self.statusLabel = QLabel("btn Status")
        self.leftLayout.addWidget(self.statusLabel)
        # ==================================================

        # Schedules layout ==================================
        self.scheduleLayout = QVBoxLayout()

        # setting scheduleBox to showing schedules
        self.scheduleBox = QTextEdit("Please Click any Date Button")
        self.scheduleBox.setAlignment(Qt.AlignLeft)
        self.scheduleBox.setReadOnly(True)
        self.scheduleLayout.addWidget(self.scheduleBox)

        # modifying schedule Button
        self.modifyBtn = Button("Modifying", self.modifying)
        self.scheduleLayout.addWidget(self.modifyBtn)
        # ==================================================

        # Set grid
        self.mCal = calendarManager.myCalendar()
        self.mCal.setCalander(self.currentYear, self.currentMonth)
        self.gridingDate(self.mCal.getCalander())

        self.mainLayout.addLayout(self.leftLayout)
        self.mainLayout.addLayout(self.scheduleLayout)
        self.setLayout(self.mainLayout)
        self.setWindowTitle("Calendar")

    def gridingDate(self, arr):
        # Append Day Buttons ===========================
        self.clearLayout(self.calendarGrid)
        self.showCurrentLabel.setText(str(self.currentYear) + " / " + str(self.currentMonth))
        before = True; after = True

        for row, column in enumerate(arr):
            for col, day in enumerate(column):
                btn = Button(str(day), self.btnEvent)
                btn.setEnabled(after)

                if before and day > 1:
                    btn.setEnabled(False)
                else:
                    before = False

                if not before and day is self.mCal.endDay:
                    after = False

                self.calendarGrid.addWidget(btn, row, col)
        # ===============================================

    def btnEvent(self):
        self.scheduleBox.setReadOnly(False)
        btn = self.sender()
        self.statusLabel.setText(btn.text() + " is Clicked.")
        self.currentDay = btn.text()

        target = str(self.currentYear) + str(self.currentMonth) + str(self.currentDay)
        if not self.schedule.get(target):
            self.scheduleBox.setText("None")
        else:
            self.scheduleBox.setText(self.schedule[target])

    def modifying(self):
        target = str(self.currentYear) + str(self.currentMonth) + str(self.currentDay)
        self.schedule[target] = self.scheduleBox.toPlainText()
        self.statusLabel.setText("modified")

    def previousMonth(self):
        btn = self.sender()
        print(btn.text())
        if self.currentMonth is 1:
            self.currentYear -= 1
            self.currentMonth = 12
        else:
            self.currentMonth -= 1

        self.mCal.year = self.currentYear
        self.mCal.month = self.currentMonth
        self.mCal.setCalander(self.currentYear, self.currentMonth)
        self.gridingDate(self.mCal.getCalander())

    def nextMonth(self):
        btn = self.sender()
        print(btn.text())
        if self.currentMonth is 12:
            self.currentYear += 1
            self.currentMonth = 1
        else:
            self.currentMonth += 1

        self.mCal.year = self.currentYear
        self.mCal.month = self.currentMonth
        self.mCal.setCalander(self.currentYear, self.currentMonth)
        self.gridingDate(self.mCal.getCalander())

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def closeEvent(self, event):
        pickle.dump(self.schedule, open(self.fileRoot, "wb"))


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    myCalendar = Calendar()
    myCalendar.show()
    sys.exit(app.exec_())
