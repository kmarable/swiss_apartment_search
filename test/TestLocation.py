import unittest
from src.location import M1Line, M1Stop, getRankedList
import pandas as pd


class TestM1Stop(unittest.TestCase):
    def setUp(self):
        self.stop = M1Stop('Renens', (46.53678583814642, 6.579422241802945))

    def testGetDistance(self):
        result = self.stop.getDistance((46.5377597, 6.5742702))
        expected = 400.0
        self.assertTrue(abs(result-expected) < 100)

    def testGetApproxTravelTime(self):
        result = self.stop.getApproxTravelTime((46.5377597, 6.5742702))
        expected = 4
        self.assertTrue(abs(result-expected) < 2)


class TestM1Line(unittest.TestCase):
    def testInitializeLine(self):
        line = M1Line()
        self.assertTrue(len(line.stops) == 15)
        self.assertIsInstance(line.stops, list)
        self.assertIsInstance(line.stops[0], M1Stop)

    def setUp(self):
        self.line = M1Line()

    def testGetClosest(self):
        input = (46.5263148, 6.5673744)
        result_name, result_time = self.line.getNearestM1Stop(input)
        print(result_time)
        self.assertEqual(result_name, 'Bassenges')
        self.assertTrue(abs(result_time - 4) < 1)

    def testgetDFofNearestStops(self):
        input = [(0, 46.5263148, 6.5673744), (1, 46.5386958, 6.5784506)]
        result = self.line.getDFofNearestStops(input)
        expected = pd.DataFrame(columns=['NearestStop', 'TimeToNearestStop'],
                                data=[['Bassenges',  4.237774],
                                      ['Renens', 2.884841]], index=[0, 1])
        print(expected)
        pd.testing.assert_frame_equal(result, expected)

    def testGetRankedList_OrderedIn(self):
        input = [1, 2, 3, 4, 5]
        result = getRankedList(input)
        self.assertEqual([0, 1, 2, 3, 4], result)

    def testGetRankedList_UnOrderedIn(self):
        input = [3, 6, 2, 5, 9, 1]
        result = getRankedList(input)
        self.assertEqual([2, 4, 1, 3, 5, 0], result)

    def testGetRankedList_ListWithDoubles(self):
        input = [2, 6, 2, 6, 9, 1]
        result = getRankedList(input)
        self.assertEqual([1, 3, 2, 4, 5, 0], result)
