import unittest
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from calendarCalculator import CalendarCalculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = CalendarCalculator()

    def tearDown(self):
        pass

    def testIsLunarMonth(self):
        self.assertFalse(self.calculator.isLunarMonth(2018))
        self.assertTrue(self.calculator.isLunarMonth(2016))
        self.assertTrue(self.calculator.isLunarMonth(2400))
        self.assertFalse(self.calculator.isLunarMonth(2033))

    def testFormatDate(self):
        testDate = '2018-12-10'
        self.assertEqual(self.calculator.formatDate(testDate), (2018, 12, 10))

        testDate = '2000-09-01'
        self.assertEqual(self.calculator.formatDate(testDate), (2000, 9, 1))

        testDate = '2000-10-31'
        self.assertEqual(self.calculator.formatDate(testDate), (2000, 10, 31))

    def testParseDate(self):
        testDate = "20181231"
        self.assertEqual(self.calculator.parseDate(testDate), (2018, 12, 31))

        testDate = "2001231"
        self.assertEqual(self.calculator.parseDate(testDate), (200, 12, 31))

        testDate = "21231"
        self.assertEqual(self.calculator.parseDate(testDate), (2, 12, 31))

        testDate = "00081231"
        self.assertEqual(self.calculator.parseDate(testDate), (8, 12, 31))

    def testToSolarDate(self):
        self.assertEqual(self.calculator.toSolarDate(2018, 12, 10), (2019, 1, 15))
        self.assertEqual(self.calculator.toSolarDate(2037, 11, 25), (2037, 12, 31))
        self.assertEqual(self.calculator.toSolarDate(1999, 11, 12), (1999, 12, 19))

    def testToLunarDate(self):
        self.assertEqual(self.calculator.toLunarDate(2018, 12, 11), (2018, 11, 5))
        self.assertEqual(self.calculator.toLunarDate(2021, 8, 3), (2021, 6, 25))
        self.assertEqual(self.calculator.toLunarDate(1945, 2, 22), (1945, 1, 10))
        self.assertEqual(self.calculator.toLunarDate(2037, 11, 15), (2037, 10, 9))

    def testGetSolarHoliday(self):
        self.assertEqual(self.calculator.getSolarHoliday(2018, 8, 15, "추석"), (9, 24, "추석"))
        self.assertEqual(self.calculator.getSolarHoliday(2018, 1, 1, "설날"), (2, 16, "설날"))
        self.assertEqual(self.calculator.getSolarHoliday(2018, 4, 8, "부처님오신날"), (5, 22, "부처님오신날"))

if __name__ == '__main__':
    unittest.main()