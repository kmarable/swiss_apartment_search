from test.parsing_tests.TestListing import TestListing
from src.parser.listing.ImmobilierListing import ImmobilierListing
from src.utilities import response_from_text


class TestImmobilier(TestListing):
    def setUp(self):
        test = response_from_text('old immobilier text')
        self.parser = ImmobilierListing(test)

    def testNoAssets(self):
        response = response_from_text('lol')
        self.parser = ImmobilierListing(response)
        result = self.parser._getListingAssets()
        self.assertEqual(result, '', 'didnt correctly hand lack of listing assets')

    def testDisponibleDesMaintenant(self):
        input_text = '<span class="im__assets__title im__assets__title--big">  Disponible d�s maintenant										</span>'  # noqa
        response = response_from_text(input_text)
        self.parser = ImmobilierListing(response)
        result = self.parser.getAvailability()
        msg = 'getAvailability does not return todays date for maintenant'
        self.assertEqual(result, self.parser._getFirstDate([]), msg)
