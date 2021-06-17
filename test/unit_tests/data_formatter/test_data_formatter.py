import os

import pandas as pd
from pandas.core.frame import DataFrame
import pytest
from module.data_formatter import DataFormatter

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

    result = example_data_formatter.find_word_occurrences(example_input_data['content'])
    assert result == example_expected_data['word_occurences']

    result = example_data_formatter.find_word_occurrences(None)
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


def test_restructure_comments(example_data_formatter: DataFormatter,
                              example_comment_frame):

    result = example_data_formatter.restructure_comments(example_comment_frame['input'].iloc[0])
    assert result.equals(example_comment_frame['expected'].iloc[0])

    result = example_data_formatter.restructure_comments(example_comment_frame['input'].iloc[1])
    assert result.equals(example_comment_frame['expected'].iloc[1])


@pytest.mark.parametrize('column', ['title', 'date_of_publishing', 'content', 'most_used_words', 'comments'])
def test_format(example_data_formatter: DataFormatter, example_data_frame, column):
    example_data_formatter.import_file(test_data_path + '/example.json')

    example_data_formatter.format()

    assert example_data_formatter.df[column].equals(example_data_frame[column])
