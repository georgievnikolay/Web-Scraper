import os

import pytest
from module.data_formatter import DataFormatter
import json

test_data_path = os.path.dirname(__file__)


def test_format_date(example_data_formatter: DataFormatter,
                     example_input_data, example_expected_data):

    result = example_data_formatter.format_date(example_input_data['date'])
    assert result == example_expected_data['date']

    example_data_formatter.format_date("non-date string")

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


def test_extract_authors(example_data_formatter: DataFormatter,
                                example_input_data, example_expected_data):

    result = example_data_formatter.extract_authors(example_input_data['authors'])
    assert result == example_expected_data['authors']

    result = example_data_formatter.extract_authors(None)
    assert result is None


def test_group_comments(example_data_formatter: DataFormatter,
                              example_comments):

    result = example_data_formatter.group_comments(*example_comments['input'])
    assert result == example_comments['expected']

    result = example_data_formatter.group_comments(None, None)
    assert result is None


def test_unify_dtypes(example_data_formatter: DataFormatter,
                            unify_dtypes_example):
    result = example_data_formatter.unify_dtypes(unify_dtypes_example['input'])
    assert result == unify_dtypes_example['expected']


@pytest.mark.parametrize('column', ['title', 'date_of_publishing', 'content', 'most_used_words', 'comments'])
def test_format(example_data_formatter: DataFormatter, example_formatted_data, column):
    with open(test_data_path + '/example.json', 'r') as f:
        example_input = json.load(f)

    result = example_data_formatter.format(example_input)

    i = 0
    for article in result:
        assert article[column] == example_formatted_data[i][column]
        i += 1

    assert i == len(example_formatted_data)
