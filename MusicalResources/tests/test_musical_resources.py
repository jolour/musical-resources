"""Tests for MusicalResources package"""

from MusicalResources import pitches_and_durations_resources as pitdur
import unittest

ROW_BOULEZ_NUMBERS=[3, 2, 9, 8, 7, 6, 4, 1, 0, 10, 5, 11]
ROW_BOULEZ_NOTES=['dis', 'd', 'a', 'gis', 'g', 'fis', 'e', 'cis', 'c', 'ais', 'f', 'b']
MATRIX_BOULEX_NUMBERS=[[3, 2, 9, 8, 7, 6, 4, 1, 0, 10, 5, 11],
                       [4, 3, 10, 9, 8, 7, 5, 2, 1, 11, 6, 0],
                       [9, 8, 3, 2, 1, 0, 10, 7, 6, 4, 11, 5],
                       [10, 9, 4, 3, 2, 1, 11, 8, 7, 5, 0, 6],
                       [11, 10, 5, 4, 3, 2, 0, 9, 8, 6, 1, 7],
                       [0, 11, 6, 5, 4, 3, 1, 10, 9, 7, 2, 8],
                       [2, 1, 8, 7, 6, 5, 3, 0, 11, 9, 4, 10],
                       [5, 4, 11, 10, 9, 8, 6, 3, 2, 0, 7, 1],
                       [6, 5, 0, 11, 10, 9, 7, 4, 3, 1, 8, 2],
                       [8, 7, 2, 1, 0, 11, 9, 6, 5, 3, 10, 4],
                       [1, 0, 7, 6, 5, 4, 2, 11, 10, 8, 3, 9],
                       [7, 6, 1, 0, 11, 10, 8, 5, 4, 2, 9, 3]]
MATRIX_BOULEX_NOTES=[['dis', 'd', 'a', 'gis', 'g', 'fis', 'e', 'cis', 'c', 'ais', 'f', 'b'],
                      ['e', 'dis', 'ais', 'a', 'gis', 'g', 'f', 'd', 'cis', 'b', 'fis', 'c'],
                      ['a', 'gis', 'dis', 'd', 'cis', 'c', 'ais', 'g', 'fis', 'e', 'b', 'f'],
                      ['ais', 'a', 'e', 'dis', 'd', 'cis', 'b', 'gis', 'g', 'f', 'c', 'fis'],
                      ['b', 'ais', 'f', 'e', 'dis', 'd', 'c', 'a', 'gis', 'fis', 'cis', 'g'],
                      ['c', 'b', 'fis', 'f', 'e', 'dis', 'cis', 'ais', 'a', 'g', 'd', 'gis'],
                      ['d', 'cis', 'gis', 'g', 'fis', 'f', 'dis', 'c', 'b', 'a', 'e', 'ais'],
                      ['f', 'e', 'b', 'ais', 'a', 'gis', 'fis', 'dis', 'd', 'c', 'g', 'cis'],
                      ['fis', 'f', 'c', 'b', 'ais', 'a', 'g', 'e', 'dis', 'cis', 'gis', 'd'],
                      ['gis', 'g', 'd', 'cis', 'c', 'b', 'a', 'fis', 'f', 'dis', 'ais', 'e'],
                      ['cis', 'c', 'g', 'fis', 'f', 'e', 'd', 'b', 'ais', 'gis', 'dis', 'a'],
                      ['g', 'fis', 'cis', 'c', 'b', 'ais', 'gis', 'f', 'e', 'd', 'a', 'dis']]

class TestPitDur(unittest.TestCase):
    """Class for testing pitches_and_durations_resources"""
    
    def test_get_row(self):
        """Tests for function get_row"""
        self.assertEqual(pitdur.get_row([[1,2],[3,4]], 0), [1,2])
        self.assertEqual(pitdur.get_row([[1,2],[3,4]], 1), [3,4])

    def test_get_column(self):
        """Tests for function get_column"""
        self.assertEqual(pitdur.get_column([[1,2],[3,4]], 0), [1,3])
        self.assertEqual(pitdur.get_column([[1,2],[3,4]], 1), [2,4])    
    
    def test_convert_number_to_note(self):
        """Test the function convert_number_to_note"""
        self.assertEqual(pitdur.convert_number_to_note(0), 'c')
        self.assertEqual(pitdur.convert_number_to_note(6), 'fis')

    def test_convert_note_to_number(self):
        """Test the function convert_note_to_number"""
        self.assertEqual(pitdur.convert_note_to_number('d'), 2)
        self.assertEqual(pitdur.convert_note_to_number('gis'), 8)

    def test_get_index_of_note_in_row(self):
        """Tests for function get_index_of_note_in_row"""
        self.assertEqual(pitdur.get_index_of_note_in_row('fis', ROW_BOULEZ_NOTES), 5)
        self.assertEqual(pitdur.get_index_of_note_in_row('fis', ROW_BOULEZ_NUMBERS), 5)
        
    def test_convert_notes_to_numbers(self):
        """Tests for function convert_notes_to_numbers"""
        self.assertEqual(pitdur.convert_notes_to_numbers(ROW_BOULEZ_NOTES), ROW_BOULEZ_NUMBERS)
        
    def test_convert_numbers_to_notes(self):
        """Tests for function convert_numbers_to_notes"""
        self.assertEqual(pitdur.convert_numbers_to_notes(ROW_BOULEZ_NUMBERS), ROW_BOULEZ_NOTES)
        
    def test_create_12_tone_matrix(self):
        """Tests for function convert_numbers_to_notes"""
        self.assertEqual(pitdur.create_12_tone_matrix(ROW_BOULEZ_NUMBERS), MATRIX_BOULEX_NUMBERS)
        self.assertEqual(pitdur.create_12_tone_matrix(ROW_BOULEZ_NOTES), MATRIX_BOULEX_NUMBERS)
        self.assertEqual(pitdur.create_12_tone_matrix(ROW_BOULEZ_NUMBERS, True), MATRIX_BOULEX_NOTES)
        self.assertEqual(pitdur.create_12_tone_matrix(ROW_BOULEZ_NUMBERS, False), MATRIX_BOULEX_NUMBERS)
        self.assertEqual(pitdur.create_12_tone_matrix(ROW_BOULEZ_NOTES, True), MATRIX_BOULEX_NOTES)
        self.assertEqual(pitdur.create_12_tone_matrix(ROW_BOULEZ_NOTES, False), MATRIX_BOULEX_NUMBERS)
        
    def test_interval_differences_in_half_tones(self):
        """Tests for function interval_differences_in_half_tones"""
        self.assertEqual(pitdur.interval_differences_in_half_tones(ROW_BOULEZ_NOTES), [11, 7, 11, 11, 11, 10, 9, 11, 10, 7, 6])
        self.assertEqual(pitdur.interval_differences_in_half_tones(ROW_BOULEZ_NUMBERS), [11, 7, 11, 11, 11, 10, 9, 11, 10, 7, 6])