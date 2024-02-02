from unittest import TestCase
from ...utility import *

class CheckIfFieldsAreMissingTest(TestCase):
    def setUp(self):
        self.all_fields = [f'field{i}' for i in range(1, 11)]
        self.required_fields = ['field1','field3','field7','field8','field10']

    def test_no_required_fields_missing(self):
        # we need 0 to pass because it's not None
        data = {field: 0 for field in self.all_fields}
        self.assertEqual(check_if_fields_are_missing(data, self.required_fields), None)
    
    def test_required_fields_missing(self):
        # value of one required field is empty
        data1 = {field: 1 if field != 'field1' else None for field in self.required_fields}
        # value of all required fields are empty
        data2 = {field: '0' for field in self.all_fields if field not in self.required_fields}
        # the key value pair of one required field is empty
        data3 = {field: 'oof' for field in self.all_fields if field != 'field10'}
        self.assertEqual(check_if_fields_are_missing(data1, self.required_fields), {'message': f'The following fields are missing or empty: {self.required_fields[0]}.'})
        self.assertEqual(check_if_fields_are_missing(data2, self.required_fields), {'message': f'The following fields are missing or empty: {', '.join(self.required_fields)}.'})
        self.assertEqual(check_if_fields_are_missing(data3, self.required_fields), {'message': f'The following fields are missing or empty: {self.required_fields[-1]}.'})