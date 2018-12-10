from korean_lunar_calendar import KoreanLunarCalendar


class CalendarCalculator:
    def __init__(self):
        self.lunarCalculator = KoreanLunarCalendar()

    def isLunarMonth(self, year: int) -> bool:
        '''
        Judge lunar month
        :param year: the year
        :return: boolean type data
        '''
        if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
            return True

        #if ((i % 4 == 0 & & i % 100 != 0) | | i % 400 == 0)

        #elif year % 400 == 0:
            #return True

        else:
            return False

    def toSolarDate(self, year: int, month: int, day: int):
        '''
        Convert from lunar date to solar date
        :param year: lunar date of year
        :param month: lunar date of month
        :param day: lunar date of day
        :return: lunar date with tuple which have 3 arguments
        '''
        self.lunarCalculator.setLunarDate(year, month, day, self.isLunarMonth(year))
        formatedDate = self.formatDate(self.lunarCalculator.SolarIsoFormat())
        return formatedDate

    def toLunarDate(self, year: int, month: int, day: int) -> tuple:
        '''
        Convert from solar date to lunar date
        :param year: solar date of year
        :param month: solar date of month
        :param day: solar date of day
        :return: solar date with tuple which have 3 arguments
        '''
        self.lunarCalculator.setSolarDate(year, month, day)
        formatedDate = self.formatDate(self.lunarCalculator.LunarIsoFormat())
        return formatedDate

    def formatDate(self, date: str) -> tuple:
        '''
        Format string type to tuple
        :param date: string type value date ex) '2018-12-9'
        :return: tuple which have 3 arguments ex) (2018, 12, 9)
        '''
        return tuple(map(int, date.split('-')))

    def getSolarHoliday(self, year: int, month: int, day: int, holiday: str) -> tuple:
        rawDate = self.toSolarDate(year, month, day)
        rawDate = (rawDate[1], rawDate[2], holiday)
        return  rawDate

    def getToLunarDate(self, year, month, day):
        self.lunarCalculator.setSolarDate(year, month, day)
        return self.lunarCalculator.LunarIsoFormat()

    def parseDate(self, date: str) -> tuple:
        day = date[len(date) - 2:]
        month = date[len(date) - 4:len(date) - 2]
        year = date[:len(date)-4]

        if month[0] == '0':
            month = month[1]

        if day[0] == '0':
            day = day[1]

        return (int(year), int(month), int(day))

if __name__ == "__main__":
    calendar = CalendarCalculator()
    print(calendar.getSolarHoliday(2018, 4, 8, "부처님오신날"))
    print(calendar.toLunarDate(2018, 12, 31))
    print(calendar.isLunarMonth(2018))