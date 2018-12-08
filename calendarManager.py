import calendar

class myCalendar:
    def __init__(self):
        self.calendar = []
        self.startDay = 0
        self.endDay = 0

    def getCalander(self):
        return self.calendar

    def setCalander(self, year, month):
        print("call makeCalendar")
        self.calendar = self.makeCalendar(year, month)

        # Append before month days first line
        if month == 1:
            endDay = calendar.monthrange(year - 1, 12)[1]

        else:
            endDay = calendar.monthrange(year, month - 1)[1]

        for i in range(7 - len(self.calendar[0])):
            self.calendar[0].insert(0, endDay - i)

        # Append after month days last line
        for i in range(7 - len(self.calendar[-1])):
            self.calendar[-1].append(i+1)

    def makeCalendar(self, year, month):
        newCalendar = []
        day = 0
        self.startDay, self.endDay = calendar.monthrange(year, month)

        # 1번째 줄은 첫째 날이 등장하기전까지 비어있기 때문에 따로 처리한다.
        firstLineCount = 6 - self.startDay
        newCalendar.append([x + 1 for x in range(firstLineCount)])
        day += firstLineCount

        # 2번째 줄부터는 7일 단위로 개행하면서 List를 채워나간다.
        while True:
            rowList = []
            for i in range(7):
                day += 1
                rowList.append(day)

                if day == self.endDay:
                    newCalendar.append(rowList)
                    return newCalendar

            newCalendar.append(rowList)


if __name__ == '__main__':
    cal = myCalendar()
    print(cal.makeCalendar(2018, 12))
    cal.setCalander(2018, 1)
    print(cal.calendar)