import calendar
import pickle

class myCalendar:
    def __init__(self):
        self._year = 0
        self._month = 0
        self.calendar = []
        self.startDay = 0
        self.endDay = 0
        self.schedule = {}

    def getCalander(self):
        return self.calendar

    def setYear(self, year):
        self._year = year

    def setMonth(self, month):
        self._month = month

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
        if self.startDay is not 6:
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

class myEvent:
    def __init__(self):
        self.title = ''
        self.place = ''
        self.date = ''
        self.discription = ''

    def setTitle(self, title):
        self.title = title

    def setPlace(self, place):
        self.place = place

    def setDate(self, date):
        self.date = date[:]

    def setDiscription(self, text):
        self.discription = text

    def getTitle(self):
        return self.title

    def getPlace(self):
        return self.place

    def getDate(self):
        return self.date

    def getDiscription(self):
        return self.discription

    def setEvent(self, title, place, date, discription):
        self.setTitle(title)
        self.setPlace(place)
        self.setDate(date)
        self.setDiscription(discription)

if __name__ == '__main__':
    cal = myCalendar()
    event = myEvent()
    event.setTitle("new")
    event.setPlace("kmu")
    event.setDate("2018")
    event.setDiscription("Test")

    print(cal.makeCalendar(2018, 12))
    cal.setCalander(2019, 9)
    print(cal.calendar)