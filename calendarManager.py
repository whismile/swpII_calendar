import calendar
from calendarCalculator import CalendarCalculator
import pickle

class MyCalendar:
    def __init__(self):
        self.calculator = CalendarCalculator()
        self._year = 0
        self._month = 0
        self.calendar = []
        self.startDay = 0
        self.endDay = 0
        self.schedule = {}
        self.holidays = []

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

    def enrollHoliday(self, year):
        holiday = [
            (1, 1, "신정"),
            (3, 1, "삼일절"),
            (5, 5, "어린이날"),
            (6, 6, "현충일"),
            (8, 15, "광복절"),
            (10, 3, "개천절"),
            (10, 9, "한글날"),
            (12, 25, "크리스마스")
        ]

        lunarHoliday = [
            self.calculator.getSolarHoliday(year, 1, 1, "설날"),
            self.calculator.getSolarHoliday(year, 4, 8, "부처님오신날"),
            self.calculator.getSolarHoliday(year, 8, 15, "추석"),
        ]

        self.holidays = holiday[:] + lunarHoliday[:]

        with open("./holiday.txt", "wb") as f:
            pickle.dump(self.holidays, f)

class MyEvent:
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
    pass