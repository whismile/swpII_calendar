from korean_lunar_calendar import KoreanLunarCalendar
class CalendarCalculator:
    def __init__(self):
        self.lunarCalculator = KoreanLunarCalendar()

    def isLunarMonth(self, year):
        if year % 4 == 0 and year % 100 != 0:
            return True

        elif year % 400 == 0:
            return True

        else:
            return False

    def toSolarDate(self, year, month, day):
        self.lunarCalculator.setLunarDate(year, month, day, self.isLunarMonth(year))
        formatedDate = self.formatDate(self.lunarCalculator.SolarIsoFormat())
        return formatedDate

    def formatDate(self, date):
        return tuple(map(int, date.split('-')))

    def getSolarHoliday(self, year, month, day, holiday):
        rawDate = self.toSolarDate(year, month, day)
        rawDate = (rawDate[1], rawDate[2], holiday)
        return  rawDate

if __name__ == "__main__":
    calendar = CalendarCalculator()
    print(calendar.getSolarHoliday(2018, 4, 8, "부처님오신날"))