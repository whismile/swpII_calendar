import unittest
from calendarCalculator import CalendarCalculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = CalendarCalculator()

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()