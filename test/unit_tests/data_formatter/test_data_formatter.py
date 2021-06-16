from module.data_formatter import DataFormatter

import pandas as pd

import os
import pytest


test_data_path = os.path.dirname(__file__)


@pytest.mark.parametrize("example_file", ["example.csv", "example.json"])
def test_import_file_positive(example_data_formatter: DataFormatter, example_file):
    example_data_formatter.import_file(os.path.join(
                                       test_data_path, example_file))
    
    assert isinstance(example_data_formatter.df, pd.DataFrame)


def test_import_file_negative(example_data_formatter: DataFormatter):
    with pytest.raises(FileNotFoundError):
        example_data_formatter.import_file('non-existant-file')

    with pytest.raises(IOError):
        example_data_formatter.import_file(os.path.join(
                                           test_data_path, 'example.xls')
                                           )

def test_format_date(example_data_formatter: DataFormatter, 
                     example_input_data, example_expected_data):    

    result = example_data_formatter.format_date(example_input_data['date'])
    assert result == example_expected_data['date']

    result = example_data_formatter.format_date(None)
    assert result is None

def test_find_word_occurrences(example_data_formatter: DataFormatter,
                               example_input_data, example_expected_data):

    result = example_data_formatter.find_word_occurrences(example_input_data['content'], 3, 4)
    assert result == example_expected_data['word_occurences']
    
    result = example_data_formatter.find_word_occurrences(None, 3, 4)
    assert result is None

def test_reduce_content(example_data_formatter: DataFormatter, 
                        example_input_data, example_expected_data):
    
    result = example_data_formatter.reduce_content(example_input_data['content'])
    assert result == example_expected_data['content']

    result = example_data_formatter.reduce_content(None)
    assert result is None
    
def test_format_comment_authors(example_data_formatter: DataFormatter, 
                                example_input_data, example_expected_data):
    
    result = example_data_formatter.format_comment_authors(example_input_data['authors'])
    assert result == example_expected_data['authors']

    result = example_data_formatter.format_comment_authors(example_input_data['authors'][0])
    assert result == [example_expected_data['authors'][0]]

    result = example_data_formatter.format_comment_authors(None)
    assert result is None

    