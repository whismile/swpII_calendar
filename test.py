from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QLineEdit, QToolButton,
                             QSizePolicy, QLayout,
                             QGridLayout, QLabel,
                             QVBoxLayout, QHBoxLayout,
                             QTextEdit, QComboBox,
                             QToolBar)

import pickle
from calendarManager import myCalendar, myEvent
import time


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

    def __init__(self, parent=None, year=int(time.strftime('%Y', time.localtime(time.time()))),
                 month=int(time.strftime('%m', time.localtime(time.time())))):
        super().__init__(parent)

        # variables
        self.displayCalendar = myCalendar()
        self.startDay = 0
        self.maxDay = 0
        self.currentYear = year
        self.currentMonth = month
        self.currentDay = 0
        self.fileRoot = "/home/yongjoon/kmu/swpII_calendar/schedules.txt"

        try:
            scheduleFile = open(self.fileRoot, "rb")
            self.displayCalendar.schedule = pickle.load(scheduleFile)
            print(self.displayCalendar.schedule)

        except EOFError:
            pass

        # main layout
        self.mainLayout = QHBoxLayout()
        # self.mainLayout.setSizeConstraint(QLayout.SetFixedSize)

        # Left side Layout ================================
        self.leftLayout = QVBoxLayout()

        # handling month ----------------------------------
        self.moveMonth = QHBoxLayout()

        self.previousBtn = Button("<", self.previousMonth)

        # showing Year and month
        self.showCurrentLabel = QLabel(str(self.currentYear) + " / " + str(self.currentMonth))
        self.showCurrentLabel.setAlignment(Qt.AlignCenter)

        self.nextBtn = Button(">", self.nextMonth)

        self.moveMonth.addStretch()
        self.moveMonth.addWidget(self.previousBtn)
        self.moveMonth.addWidget(self.showCurrentLabel)
        self.moveMonth.addWidget(self.nextBtn)
        self.moveMonth.addStretch()
        self.leftLayout.addLayout(self.moveMonth)
        self.leftLayout.addStretch()
        # -------------------------------------------------

        # Set Day of Week
        self.weekDayLayout = QHBoxLayout()
        enumDays = ["일", "월", "화", "수", "목", "금", "토"]

        for i in enumDays:
            label = QLabel(i)
            label.setAlignment(Qt.AlignCenter)
            self.weekDayLayout.addWidget(label)

        self.leftLayout.addLayout(self.weekDayLayout)

        # grid layout to appending date Buttons
        self.calendarGrid = QGridLayout()
        self.calendarGrid.setSizeConstraint(QLayout.SetFixedSize)
        self.leftLayout.addLayout(self.calendarGrid)
        self.leftLayout.addStretch(7)

        # showing status
        self.statusLabel = QLabel("btn Status")
        self.leftLayout.addWidget(self.statusLabel)
        # ==================================================

        # Schedules layout ==================================
        self.scheduleLayout = QVBoxLayout()
        self.titleBox = QHBoxLayout()
        self.titleLabel = QLabel("title: ")
        self.titleLineEdit = QLineEdit()
        self.titleBox.addWidget(self.titleLabel)
        self.titleBox.addWidget(self.titleLineEdit)

        self.placeBox = QHBoxLayout()
        self.placeLabel = QLabel("place: ")
        self.placeLineEdit = QLineEdit()
        self.placeBox.addWidget(self.placeLabel)
        self.placeBox.addWidget(self.placeLineEdit)

        self.dateBox = QHBoxLayout()
        self.dateLabel = QLabel("date: ")
        self.dateLineEdit = QLineEdit()
        self.dateBox.addWidget(self.dateLabel)
        self.dateBox.addWidget(self.dateLineEdit)

        self.discription = QHBoxLayout()
        self.content = QTextEdit()
        self.contentLabel = QLabel("content: ")
        self.discription.addWidget(self.contentLabel)
        self.discription.addWidget(self.content)

        self.scheduleLayout.addLayout(self.titleBox)
        self.scheduleLayout.addLayout(self.placeBox)
        self.scheduleLayout.addLayout(self.dateBox)
        self.scheduleLayout.addLayout(self.discription)
        # modifying schedule Button
        self.modifyBtn = Button("Modifying", self.modifying)
        self.scheduleLayout.addWidget(self.modifyBtn)
        # ==================================================

        # Set grid
        self.displayCalendar.setCalander(self.currentYear, self.currentMonth)
        self.renderDate(self.displayCalendar.getCalander())

        self.mainLayout.addLayout(self.leftLayout)
        self.mainLayout.addLayout(self.scheduleLayout)
        self.setLayout(self.mainLayout)
        self.setWindowTitle("Calendar")

    def renderDate(self, newCalendar):
        # =========== Append Day Buttons ===============
        self.clearLayout(self.calendarGrid)
        self.showCurrentLabel.setText(str(self.currentYear) + " / " + str(self.currentMonth))
        toggle = True

        # Enroll button
        for row, column in enumerate(newCalendar):
            for col, day in enumerate(column):
                btn = Button(str(day), self.btnEvent)

                # deactivate button condition
                if toggle:
                    if day != 1:
                        btn.setEnabled(False)

                    else:
                        toggle = False

                else:
                    if (row == len(newCalendar) - 1) and (day // 10 == 0):
                        btn.setEnabled(False)

                # 공휴일은 빨간색으로 설정해준다.
                if col == 0 and (row != 0 or day == 1):
                    btn.setStyleSheet('color: red;')

                self.calendarGrid.addWidget(btn, row, col)
        # ===============================================

    def btnEvent(self):
        btn = self.sender()
        self.statusLabel.setText("Day: " + btn.text() + " is Clicked.")
        self.currentDay = btn.text()

        target = "-".join([str(self.currentYear), str(self.currentMonth), str(self.currentDay)])
        targetEvent = self.displayCalendar.schedule.get(target)

        if not targetEvent:
            self.titleLineEdit.setText("None")

        else:
            self.titleLineEdit.setText(targetEvent.getTitle())
            self.placeLineEdit.setText(targetEvent.getPlace())
            self.dateLineEdit.setText(targetEvent.getDate())
            self.content.setText(targetEvent.getDiscription())


    def modifying(self):
        newEvent = myEvent()
        eventList = [self.titleLineEdit.text(),
                     self.placeLineEdit.text(),
                     self.dateLineEdit.text(),
                     self.content.toPlainText(),]

        newEvent.setEvent(*eventList)

        target = "-".join([str(self.currentYear), str(self.currentMonth), str(self.currentDay)])
        self.displayCalendar.schedule[target] = newEvent
        self.statusLabel.setText("modified")

    # rendering previous month calendar
    def previousMonth(self):
        btn = self.sender()
        print(btn.text())

        if self.currentMonth is 1:
            self.currentYear -= 1
            self.currentMonth = 12

        else:
            self.currentMonth -= 1

        self.displayCalendar.setYear(self.currentYear)
        self.displayCalendar.setMonth(self.currentMonth)
        self.displayCalendar.setCalander(self.currentYear, self.currentMonth)
        self.renderDate(self.displayCalendar.getCalander())

    # rendering next month calendar
    def nextMonth(self):
        btn = self.sender()
        print(btn.text())
        if self.currentMonth is 12:
            self.currentYear += 1
            self.currentMonth = 1
        else:
            self.currentMonth += 1

        self.displayCalendar.setYear(self.currentYear)
        self.displayCalendar.setMonth(self.currentMonth)
        self.displayCalendar.setCalander(self.currentYear, self.currentMonth)
        self.renderDate(self.displayCalendar.getCalander())

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def closeEvent(self, event):
        with open(self.fileRoot, "wb") as file:
            pickle.dump(self.displayCalendar.schedule, file)

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    myCalendar = Calendar()
    myCalendar.show()
    sys.exit(app.exec_())
