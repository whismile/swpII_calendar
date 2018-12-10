import unittest
from calendarManager import MyCalendar, MyEvent

class TestCalendarManager(unittest.TestCase):
    def setUp(self):
        self.myCalendar = MyCalendar()
        self.myEvent = MyEvent()
        self.calendarCatalog = {
            '2018.12' : [[1],
                   [2, 3, 4, 5, 6, 7, 8],
                   [9, 10, 11, 12, 13, 14, 15],
                   [16, 17, 18, 19, 20, 21, 22],
                   [23, 24, 25, 26, 27, 28, 29],
                   [30, 31],],

            '1945.5' : [[1, 2, 3, 4, 5],
                   [6, 7, 8, 9, 10, 11, 12],
                   [13, 14, 15, 16, 17, 18, 19],
                   [20, 21, 22, 23, 24, 25, 26],
                   [27, 28, 29, 30, 31],],

            '2037.9' : [[1, 2, 3, 4, 5],
                        [6, 7, 8, 9, 10, 11, 12],
                        [13, 14, 15, 16, 17, 18, 19],
                        [20, 21, 22, 23, 24, 25, 26],
                        [27, 28, 29, 30]]
        }

        self.calendarDone = {
            '2018.12': [[25, 26, 27, 28, 29, 30, 1],
                        [2, 3, 4, 5, 6, 7, 8],
                        [9, 10, 11, 12, 13, 14, 15],
                        [16, 17, 18, 19, 20, 21, 22],
                        [23, 24, 25, 26, 27, 28, 29],
                        [30, 31, 1, 2, 3, 4, 5], ],

            '1945.5': [[29, 30, 1, 2, 3, 4, 5],
                       [6, 7, 8, 9, 10, 11, 12],
                       [13, 14, 15, 16, 17, 18, 19],
                       [20, 21, 22, 23, 24, 25, 26],
                       [27, 28, 29, 30, 31, 1, 2], ],

            '2037.9': [[30, 31, 1, 2, 3, 4, 5],
                       [6, 7, 8, 9, 10, 11, 12],
                       [13, 14, 15, 16, 17, 18, 19],
                       [20, 21, 22, 23, 24, 25, 26],
                       [27, 28, 29, 30, 1, 2, 3]]
        }

    def tearDown(self):
        pass

    def testMakeCalendar(self):
        self.assertEqual(self.myCalendar.makeCalendar(2018, 12), self.calendarCatalog['2018.12'])
        self.assertEqual(self.myCalendar.makeCalendar(1945, 5), self.calendarCatalog['1945.5'])
        self.assertFalse(self.myCalendar.makeCalendar("1945", 5), self.calendarCatalog['1945.5'])
        self.assertFalse(self.myCalendar.makeCalendar("1945", "5"), self.calendarCatalog['1945.5'])
        self.assertFalse(self.myCalendar.makeCalendar(1945, "5"), self.calendarCatalog['1945.5'])
        self.assertEqual(self.myCalendar.makeCalendar(2037, 9), self.calendarCatalog['2037.9'])

    def testSetCalendar(self):
        # Append before month days first line
        self.myCalendar.setCalander(2018, 12)
        self.assertEqual(self.myCalendar.calendar, self.calendarDone['2018.12'])
        self.myCalendar.setCalander(1945, 5)
        self.assertEqual(self.myCalendar.calendar, self.calendarDone['1945.5'])
        self.myCalendar.setCalander(2037, 9)
        self.assertEqual(self.myCalendar.calendar, self.calendarDone['2037.9'])

if __name__ == '__main__':
    unittest.main()