import calendar

class myCalendar:
    def __init__(self, year, month):
        self.year = year
        self.month = month
        self.calendar = []

    def getCalander(self):
        return self.calendar

    def setCalander(self):
        before = self.makeCalendar(self.year, self.month-1)[-1]
        self.calendar = self.makeCalendar(self.year, self.month)
        self.calendar[0] = before + self.calendar[0]

        for i in range(7 - len(self.calendar[-1])):
            self.calendar[-1].append(i+1)

    def makeCalendar(self, year, month):
        result = []
        day = 0
        startDay, endDay = calendar.monthrange(year, month)

        tmp = []
        for i in range(6 - startDay):
            day += 1
            tmp.append(day)

        result.append(tmp)

        while True:
            rowList = []
            for i in range(7):
                day += 1
                rowList.append(day)

                if day == endDay:
                    result.append(rowList)
                    return result

            result.append(rowList)



cal = myCalendar(2018, 12)
cal.setCalander()
print(cal.calendar)