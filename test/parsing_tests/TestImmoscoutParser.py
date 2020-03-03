from test.parsing_tests.TestListing import TestListing
from src.parser.Immoscout import ImmoscoutListing
from src.utilities import response_from_text


class TestImmoscout(TestListing):
    def setUp(self):
        test = response_from_text('old immoscout text')
        self.parser = ImmoscoutListing(test)
