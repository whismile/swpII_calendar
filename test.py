from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QLineEdit, QToolButton,
                             QSizePolicy, QLayout,
                             QGridLayout, QLabel,
                             QVBoxLayout, QHBoxLayout,
                             QTextEdit)

import calendar
import pickle


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
        self.dateSet = self.makeDateSet(year, month)[:]
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

        # showing Year and month
        self.showCurrentLabel = QLabel(str(self.currentYear) + " / " + str(self.currentMonth))
        self.showCurrentLabel.setAlignment(Qt.AlignCenter)
        self.leftLayout.addWidget(self.showCurrentLabel)

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
        self.gridingDate(self.dateSet)

        self.mainLayout.addLayout(self.leftLayout)
        self.mainLayout.addLayout(self.scheduleLayout)
        self.setLayout(self.mainLayout)
        self.setWindowTitle("Calendar")

    def setMonthRange(self, year=2018, month=12):
        monthRange = calendar.monthrange(year, month)
        self.startDay = monthRange[0]
        self.maxDay = monthRange[1]

    def makeDateSet(self, year=2018, month=12):
        self.setMonthRange(year, month)
        day = 1
        first = False

        tmp = []
        result = []
        while day <= self.maxDay:
            if not first:
                for i in range(self.startDay + 1):
                    tmp.append("")
                tmp.append(str(day))
                result.append(tmp)
                tmp = []

                day += 1; first = True
            else:
                tmp.append(str(day))
                day += 1
                if len(tmp) > 6:
                    result.append(tmp)
                    tmp = []

        if len(tmp) is not 0:
            result.append(tmp)

        return result

    def gridingDate(self, arr):
        # Append Day Buttons ===========================
        self.clearLayout(self.calendarGrid)

        arr = self.makeDateSet(self.currentYear, self.currentMonth)

        for row, column in enumerate(arr):
            for col, day in enumerate(column):
                btn = Button(day, self.btnEvent)
                if day is "":
                    btn.setEnabled(False)
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
        print(self.schedule)

    def previousMonth(self):
        if self.currentMonth > 1:
            self.currentMonth -= 1
        else:
            self.currentYear -= 1
            self.currentMonth = 12



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
