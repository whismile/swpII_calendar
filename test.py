from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QLineEdit, QToolButton,
                             QSizePolicy, QLayout,
                             QGridLayout, QLabel,
                             QVBoxLayout, QHBoxLayout)

import calendar


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

    def __init__(self, parent=None):
        super().__init__(parent)

        # variables
        self.startDay = 0
        self.maxDay = 0
        self.dateSet = self.makeDateSet()[:]

        # main layout
        self.mainLayout = QHBoxLayout()
        self.mainLayout.setSizeConstraint(QLayout.SetFixedSize)

        # Left side Layout
        self.leftLayout = QVBoxLayout()

        # grid layout to appending date Buttons
        self.calendarGrid = QGridLayout()
        self.calendarGrid.setSizeConstraint(QLayout.SetFixedSize)

        # Schedules layout
        self.scheduleLayout = QVBoxLayout()

        # showing status
        self.statusLabel = QLabel("btn Status")

        # setting scheduleBox to showing schedules
        self.scheduleBox = QLineEdit("Please Click any Date Button")
        self.scheduleBox.setReadOnly(True)
        self.scheduleBox.setAlignment(Qt.AlignLeft)
        self.scheduleLayout.addWidget(self.scheduleBox)

        # Append Day Buttons ===========================
        for row, column in enumerate(self.dateSet):
            for col, day in enumerate(column):
                btn = Button(day, self.btnEvent)
                self.calendarGrid.addWidget(btn, row, col)
        # ===============================================

        self.leftLayout.addLayout(self.calendarGrid)
        self.leftLayout.addWidget(self.statusLabel)

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

    def btnEvent(self):
        btn = self.sender()
        self.statusLabel.setText(btn.text() + " is Clicked.")


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    myCalendar = Calendar()
    myCalendar.show()
    sys.exit(app.exec_())
