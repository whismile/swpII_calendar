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

    def getMaxday(self, year, month):
        return calendar.monthrange(year, month)[1]

    def setYear(self, year):
        self._year = year

    def setMonth(self, month):
        self._month = month

    def setCalander(self, year, month):
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
        if not (isinstance(year, int) and isinstance(month, int)):
            return False

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
            (12, 25, "크리스마스"),
        ]

        lunarHoliday = [
            self.calculator.getSolarHoliday(year, 1, 1, "설날"),
            self.calculator.getSolarHoliday(year, 4, 8, "부처님오신날"),
            self.calculator.getSolarHoliday(year, 8, 15, "추석")
        ]

        for month, day, title in lunarHoliday[::-1]:
            lunarHoliday.append((month, day - 1, title))
            lunarHoliday.append((month, day + 1, title))

        holidays = holiday[:] + lunarHoliday[:]

        try:
            with open("./schedules/holiday.txt", "wb") as f:
                pickle.dump(holidays, f)
        except:
            return False

    def loadHoliday(self):
        try:
            with open('./schedules/holiday.txt', 'rb') as f:
                self.holidays = pickle.load(f)
        except:
            return False


class MyEvent:
    def __init__(self):
        self.title = ''
        self.place = ''
        self.date = ''
        self.description = ''

    def setTitle(self, title):
        self.title = title

    def setPlace(self, place):
        self.place = place

    def setDate(self, date):
        self.date = date[:]

    def setDescription(self, text):
        self.description = text

    def getTitle(self):
        return self.title

    def getPlace(self):
        return self.place

    def getDate(self):
        return self.date

    def getDescription(self):
        return self.description

    def setEvent(self, title, place, date, description):
        self.setTitle(title)
        self.setPlace(place)
        self.setDate(date)
        self.setDescription(description)


if __name__ == '__main__':
    cal = MyCalendar()
    print(cal.makeCalendar(2037, 9))
    cal.enrollHoliday(2018)
    for i in cal.holidays:
        print(i)