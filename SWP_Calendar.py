from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QLineEdit, QToolButton,
                             QSizePolicy, QLayout,
                             QGridLayout, QLabel,
                             QVBoxLayout, QHBoxLayout,
                             QTextEdit, QComboBox,
                             QSpinBox, QStackedWidget,
                             QMessageBox)

import pickle
from calendarManager import MyCalendar, MyEvent
import time
import os


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

        # Set Schedule Layout Components ===============
        self.scheduleLayout = QVBoxLayout()
        # -------------------------------
        self.titleBox = QHBoxLayout()
        self.titleLabel = QLabel("title: "); self.titleLineEdit = QLineEdit()
        # -------------------------------
        self.placeBox = QHBoxLayout()
        self.placeLabel = QLabel("place: "); self.placeLineEdit = QLineEdit()
        # -------------------------------
        self.dateBox = QHBoxLayout()
        self.dateLabel = QLabel("time:"); self.fromHour = QSpinBox(); self.fromMin = QSpinBox()
        self.toHour = QSpinBox(); self.toMin = QSpinBox()
        # -------------------------------
        self.discription = QHBoxLayout()
        self.contentLabel = QLabel("content: ")
        self.content = QTextEdit()
        # -------------------------------
        self.modifyBtn = Button("Modifying", self.modifying)
        # ==============================================

        self.displayCalendar = MyCalendar()
        self.startDay = 0
        self.maxDay = 0
        self.currentYear = year
        self.currentMonth = month
        self.currentDay = 0
        self.firstClick = True
        self.displayCalendar.loadHoliday()
        self.today = time.localtime()

        if os.name == 'nt':
            self.fileRoot = ".\schedules.txt"

        else:
            self.fileRoot = "./schedules/schedules.txt"

        try:
            scheduleFile = open(self.fileRoot, "rb")
            self.displayCalendar.schedule = pickle.load(scheduleFile)
            print(self.displayCalendar.schedule)

        except EOFError:
            pass

        # main layout
        self.mainLayout = QHBoxLayout()

        # Left side Layout ================================
        self.leftLayout = QVBoxLayout()

        # Stacked Widget Part -----------------------------
        # Setting Stacked Widget(like a switching Tabs)
        self.setSchedule = QWidget()
        self.lunaDate = QWidget()

        # Design And Setting Actions each Tab. if want to Append any action, plz input the action in here.
        self.setScheduleUI()
        self.lunaDateUI()

        # Appending tabs in Stack
        self.Stack = QStackedWidget()
        self.Stack.addWidget(self.setSchedule)
        self.Stack.addWidget(self.lunaDate)

        # Switching Button layout Design And binding button with action.
        self.tabLayout = QHBoxLayout()
        self.tabLayout.addWidget(Button("스케쥴러", lambda: self.display(0)))
        self.tabLayout.addWidget(Button("음력", lambda: self.display(1)))

        for i in range(self.tabLayout.count()):
            self.tabLayout.itemAt(i).widget().setStyleSheet('font-size: 8pt')

        self.leftLayout.addLayout(self.tabLayout)
        # -------------------------------------------------

        # handling Year & month ----------------------------------
        self.moveMonth = QHBoxLayout()

        self.previousBtn = Button("<", self.previousMonth)

        # showing Year and month using Combobox(Year range: 1980 ~ 2040, Month range: 1, 12)
        self.yearCombo = QComboBox()
        self.yearCombo.addItems([str(x) for x in range(1980, 2041)])
        self.yearCombo.setCurrentText(str(self.currentYear))

        self.monthCombo = QComboBox()
        self.monthCombo.addItems([str(x) for x in range(1, 13)])
        self.monthCombo.setCurrentText(str(self.currentMonth))

        self.nextBtn = Button(">", self.nextMonth)

        self.moveMonth.addStretch()
        self.moveMonth.addWidget(self.previousBtn)
        self.moveMonth.addWidget(self.yearCombo)
        self.moveMonth.addWidget(self.monthCombo)
        self.moveMonth.addWidget(self.nextBtn)
        self.moveMonth.addStretch()
        self.leftLayout.addLayout(self.moveMonth)
        self.leftLayout.addStretch()
        # -------------------------------------------------

        # Set Day of Week ---------------------------------
        self.weekDayLayout = QHBoxLayout()
        enumDays = ["일", "월", "화", "수", "목", "금", "토"]

        for i in enumDays:
            label = QLabel(i)
            label.setAlignment(Qt.AlignCenter)
            self.weekDayLayout.addWidget(label)

        self.leftLayout.addLayout(self.weekDayLayout)
        # -------------------------------------------------

        # grid layout to appending date Buttons
        self.calendarGrid = QGridLayout()
        self.calendarGrid.setSizeConstraint(QLayout.SetFixedSize)
        self.leftLayout.addLayout(self.calendarGrid)
        self.leftLayout.addStretch(7)

        # showing status
        self.statusLabel = QLabel("btn Status")
        self.leftLayout.addWidget(self.statusLabel)
        # ==================================================

        # Set grid
        self.displayCalendar.setCalander(self.currentYear, self.currentMonth)
        self.renderDate(self.displayCalendar.getCalander())

        # Set ComboBox Changing Event
        self.yearCombo.currentTextChanged.connect(lambda: self.selectionChanged())
        self.monthCombo.currentTextChanged.connect(lambda: self.selectionChanged())

        self.mainLayout.addLayout(self.leftLayout)
        self.mainLayout.addWidget(self.Stack)
        self.Stack.setCurrentIndex(0)   # default Tab -> set calendar
        self.setLayout(self.mainLayout)
        self.setWindowTitle("Calendar")

    def renderDate(self, newCalendar):
        # =========== Append Day Buttons ===============
        self.clearLayout(self.calendarGrid)
        todayYear = self.today.tm_year
        todayMonth = self.today.tm_mon
        todayDay = self.today.tm_mday
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

                # set today button color
                if (self.currentYear, self.currentMonth, day) == (todayYear, todayMonth, todayDay):
                    btn.setStyleSheet('font-style: italic;')

                # if this day have any event represent event
                key = '-'.join([str(self.currentYear), str(self.currentMonth), str(day)])
                if key in self.displayCalendar.schedule.keys() and btn.isEnabled():
                    btn.setStyleSheet('color: blue;')
                    btn.setStyleSheet('background-color: skyblue;')
                    btn.setToolTip(self.displayCalendar.schedule[key].getTitle())

                for restMonth, restDay, title in self.displayCalendar.holidays:
                    if restMonth == self.currentMonth and restDay == day and btn.isEnabled():
                        if key in self.displayCalendar.schedule.keys() and btn.isEnabled():
                            btn.setStyleSheet('background-color: skyblue; color: red;')
                            btn.setToolTip(title)

                        else:
                            btn.setStyleSheet('color: red;')
                            btn.setToolTip(title)
                            break

                # 공휴일은 빨간색으로 설정해준다.
                if col == 0 and btn.isEnabled():
                    btn.setStyleSheet('color: red;')

                self.calendarGrid.addWidget(btn, row, col)
        # ===============================================
        self.displayCalendar.enrollHoliday(self.currentYear)
        self.displayCalendar.loadHoliday()

    def btnEvent(self):
        # self.showingWidget(self.scheduleLayout)

        self.setFixedSize(self.mainLayout.sizeHint())

        btn = self.sender()
        self.statusLabel.setText("Day: " + btn.text() + " is Clicked.")
        self.currentDay = btn.text()

        target = "-".join([str(self.currentYear), str(self.currentMonth), str(self.currentDay)])
        targetEvent = self.displayCalendar.schedule.get(target)

        if not targetEvent:
            self.titleLineEdit.setText("None")
            self.placeLineEdit.clear()
            self.fromHour.setValue(0)
            self.fromMin.setValue(0)
            self.toHour.setValue(0)
            self.toMin.setValue(0)
            self.content.clear()

        else:
            self.titleLineEdit.setText(targetEvent.getTitle())
            self.placeLineEdit.setText(targetEvent.getPlace())

            timeSet = targetEvent.getDate().split(",")
            self.fromHour.setValue(int(timeSet[0]))
            self.fromMin.setValue(int(timeSet[1]))
            self.toHour.setValue(int(timeSet[2]))
            self.toMin.setValue(int(timeSet[3]))

            self.content.setText(targetEvent.getDescription())

    def modifying(self):
        newEvent = MyEvent()
        eventList = [self.titleLineEdit.text(),
                     self.placeLineEdit.text(),
                     ",".join([str(self.fromHour.value()), str(self.fromMin.value()),
                               str(self.toHour.value()), str(self.toMin.value())]),
                     self.content.toPlainText(),
                     ]

        newEvent.setEvent(*eventList)

        target = "-".join([str(self.currentYear), str(self.currentMonth), str(self.currentDay)])
        self.displayCalendar.schedule[target] = newEvent
        self.statusLabel.setText("modified")

    # rendering previous month calendar
    def previousMonth(self):
        if self.currentMonth is 1:
            self.currentYear -= 1
            self.yearCombo.setCurrentText(str(self.currentYear))
            self.currentMonth = 12
            self.monthCombo.setCurrentText(str(self.currentMonth))

        else:
            self.currentMonth -= 1
            self.monthCombo.setCurrentText(str(self.currentMonth))

    # rendering next month calendar
    def nextMonth(self):
        if self.currentMonth is 12:
            self.currentYear += 1
            self.yearCombo.setCurrentText(str(self.currentYear))
            self.currentMonth = 1
            self.monthCombo.setCurrentText(str(self.currentMonth))
        else:
            self.currentMonth += 1
            self.monthCombo.setCurrentText(str(self.currentMonth))

    def selectionChanged(self):
        self.currentYear = int(self.yearCombo.currentText())
        self.currentMonth = int(self.monthCombo.currentText())

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
        keys = []
        myEvent = self.displayCalendar.schedule

        for target in myEvent.keys():
            title = myEvent[target].title
            place = myEvent[target].place
            discription = myEvent[target].getDescription()

            if (title, place, discription) == ('', '', ''):
                keys.append(target)

        for target in keys:
            del self.displayCalendar.schedule[target]

        with open(self.fileRoot, "wb") as file:
            pickle.dump(self.displayCalendar.schedule, file)

    def setScheduleUI(self):
        # Schedules layout ==================================
        self.titleBox.addWidget(self.titleLabel)
        self.titleBox.addWidget(self.titleLineEdit)

        self.placeBox.addWidget(self.placeLabel)
        self.placeBox.addWidget(self.placeLineEdit)

        self.fromHour.setRange(0, 24)
        self.toHour.setRange(0, 24)
        self.fromMin.setRange(0, 59)
        self.toMin.setRange(0, 59)

        self.fromHour.valueChanged.connect(lambda: self.toHour.setRange(self.fromHour.value(), 24))
        # self.toHour.valueChanged.connect(lambda: self.fromHour.setRange(0, self.toHour.value()))

        self.fromMin.valueChanged.connect(lambda: self.toMin.setRange(self.fromMin.value(), 59))
        # self.toMin.valueChanged.connect(lambda: self.fromMin.setRange(0, self.toMin.value()))

        self.dateBox.addWidget(self.dateLabel)
        self.dateBox.addWidget(self.fromHour); self.dateBox.addWidget(self.fromMin)
        self.dateBox.addWidget(QLabel("    ~ "))
        self.dateBox.addWidget(self.toHour); self.dateBox.addWidget(self.toMin)

        self.contentLabel.setAlignment(Qt.AlignTop)
        self.discription.addWidget(self.contentLabel)
        self.discription.addWidget(self.content)

        self.scheduleLayout.addLayout(self.titleBox)
        self.scheduleLayout.addLayout(self.placeBox)
        self.scheduleLayout.addLayout(self.dateBox)
        self.scheduleLayout.addLayout(self.discription)
        # modifying schedule Button
        self.scheduleLayout.addWidget(self.modifyBtn)
        self.setSchedule.setLayout(self.scheduleLayout)

    def lunaDateUI(self):
        month_31 = [1, 3, 5, 7, 8, 10, 12]

        layout = QVBoxLayout()
        #layout.addWidget(QLabel("Luna Date"))
        topLayout = QHBoxLayout()
        self.yearSpinner = QSpinBox(); self.yearSpinner.setRange(1980, 2040)
        self.monthSpinner = QSpinBox(); self.monthSpinner.setRange(1, 12)
        self.daySpinner = QSpinBox()

        self.yearSpinner.setValue(self.today.tm_year)
        self.monthSpinner.setValue(self.today.tm_mon)
        self.daySpinner.setValue(self.today.tm_mday)

        self.monthSpinner.valueChanged.connect(
            lambda: self.daySpinner.setRange(1, self.displayCalendar.getMaxday(self.yearSpinner.value(), self.monthSpinner.value())
                                        )
        )

        self.modeComboBox = QComboBox()
        self.modeComboBox.addItems(["양력 -> 음력", "음력 -> 양력"])
        convertBtn = Button("convert", self.lunarBtnEvent)
        resetBtn = Button("reset", self.lunarBtnEvent)

        bottomLayout = QVBoxLayout()
        titleBox = QHBoxLayout()
        solarBox = QHBoxLayout()
        lunarBox = QHBoxLayout()
        self.todayLabel = QLabel("오늘의 날짜정보")
        self.todayLabel.setStyleSheet('color: red; font-size: 18px;')
        solarLabel = QLabel("양력날짜")
        solarLabel.setStyleSheet('color: gray;')
        todaySolarDay = "%04d-%02d-%02d" % (self.today.tm_year, self.today.tm_mon, self.today.tm_mday)
        self.solarDateLabel = QLabel(todaySolarDay)
        lunarLabel = QLabel("음력날짜")
        lunarLabel.setStyleSheet('color: gray;')
        self.lunarDateLabel = QLabel(self.displayCalendar.calculator.getToLunarDate(
            self.today.tm_year, self.today.tm_mon, self.today.tm_mday
        ))

        titleBox.addWidget(self.todayLabel)
        solarBox.addWidget(solarLabel)
        solarBox.addWidget(self.solarDateLabel)
        lunarBox.addWidget(lunarLabel)
        lunarBox.addWidget(self.lunarDateLabel)
        bottomLayout.addLayout(titleBox)
        bottomLayout.addLayout(solarBox)
        bottomLayout.addLayout(lunarBox)

        topLayout.addWidget(self.yearSpinner); topLayout.addWidget(self.monthSpinner); topLayout.addWidget(self.daySpinner)
        topLayout.addWidget(self.modeComboBox)
        topLayout.addWidget(convertBtn)
        topLayout.addWidget(resetBtn)

        layout.addStretch()
        layout.addLayout(bottomLayout)
        layout.addLayout(topLayout)
        layout.addStretch()
        self.lunaDate.setLayout(layout)

    def display(self, i):
        self.Stack.setCurrentIndex(i)

    def hidingWidget(self, layout):
        for i in range(layout.count()):
            item = layout.itemAt(i)

            if item.widget() is not None:
                layout.itemAt(i).widget().hide()

            elif item.layout() is not None:
                self.hidingWidget(layout.itemAt(i).layout())

    def showingWidget(self, layout):
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item.widget() is not None:
                layout.itemAt(i).widget().show()
            elif item.layout() is not None:
                self.showingWidget(layout.itemAt(i).layout())

    def lunarBtnEvent(self):
        btn = self.sender()
        key = btn.text()

        if key == 'reset':
            self.todayLabel.setText('오늘의 날짜정보')
            self.todayLabel.setStyleSheet('color: red; font-size: 18px;')

        elif key == 'convert':
            if self.modeComboBox.currentIndex() is 0:
                self.todayLabel.setText("양력 {}년 {}월 {}일".format(
                    self.yearSpinner.value(), self.monthSpinner.value(), self.daySpinner.value()))
                self.todayLabel.setStyleSheet('font-weight: bold; color: black; font-size: 12px;')
                lunarDate = self.displayCalendar.calculator.getToLunarDate(
                    self.yearSpinner.value(), self.monthSpinner.value(), self.daySpinner.value()
                )
                self.solarDateLabel.setText(
                    str(self.yearSpinner.value()) + "-" +
                    str(self.monthSpinner.value()) + "-" +
                    str(self.daySpinner.value()))
                self.lunarDateLabel.setText(lunarDate)
            else:
                self.todayLabel.setText("음력 {}년 {}월 {}일".format(
                    self.yearSpinner.value(), self.monthSpinner.value(), self.daySpinner.value()))
                self.todayLabel.setStyleSheet('font-weight: bold; color: black; font-size: 12px;')
                solarDate = self.displayCalendar.calculator.toSolarDate(
                    self.yearSpinner.value(), self.monthSpinner.value(), self.daySpinner.value()
                )
                self.solarDateLabel.setText(str(solarDate[0]) + "-" + str(solarDate[1]) + "-" + str(solarDate[2]))
                self.lunarDateLabel.setText(
                    str(self.yearSpinner.value()) + "-" +
                    str(self.monthSpinner.value()) + "-" +
                    str(self.daySpinner.value()))

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    myCalendar = Calendar()
    myCalendar.setStyleSheet('background-color: white;')
    myCalendar.show()
    sys.exit(app.exec_())