import calendar


class myCalendar:
    def __init__(self):
        self.calendar = []
        self.startDay = 0
        self.endDay = 0

    def getCalander(self):
        return self.calendar

    def setCalander(self, year, month):
        before = self.makeCalendar(year, month-1)[-1]
        self.calendar = self.makeCalendar(year, month)
        self.calendar[0] = before + self.calendar[0]

        for i in range(7 - len(self.calendar[-1])):
            self.calendar[-1].append(i+1)

    def makeCalendar(self, year, month):
        result = []
        day = 0
        self.startDay, self.endDay = calendar.monthrange(year, month)

        tmp = []
        for i in range(6 - self.startDay):
            day += 1
            tmp.append(day)

        result.append(tmp)

        while True:
            rowList = []
            for i in range(7):
                day += 1
                rowList.append(day)

                if day == self.endDay:
                    result.append(rowList)
                    return result

            result.append(rowList)


if __name__ == '__main__':
    cal = myCalendar(2018, 12)
    cal.setCalander()
    print(cal.calendar)