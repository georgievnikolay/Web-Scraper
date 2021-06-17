from typing import List
import pandas as pd
import os

import string
from collections import defaultdict


class DataFormatter:
    """
    Currently only supports the TravelSmart blog and json files.
    Formats a number of articles scraped by a WebScraper object.
    Usage: import_file() -> format() -> export_to_json()
    """

    def __init__(self):  # pragma: no cover
        """
        Constructor.
        """
        self.df = None

    def import_file(self, file_name):
        """
        Pass the path to a json or csv file 
        to be imported as a Pandas DataFrame.
        """
        if not os.path.exists(file_name):
            print(f"{file_name} not found.")
            raise FileNotFoundError
        
        if file_name.endswith('.csv'):
            self.df = pd.read_csv(file_name)

        elif file_name.endswith('.json'):
            self.df = pd.read_json(file_name)

        else:
            raise IOError
    
    @staticmethod
    def format_date(date):
        """
        Extracts the date from a Timestamp object or str.
        Format: DD/MM/YYYY
        """
        if not date:
            return None
        
        date = str(date)
        return f"{date[8:10]}/{date[5:7]}/{date[0:4]}"
    
    @staticmethod
    def reduce_content(content):
        """
        Reduces a full article down to the first 3 paragraphs.
        Lines shorter than 80 characters are not counted as paragraphs.
        (This consideration is mainly to avoid headings.)
        """
        if not content:
            return None
        
        if isinstance(content, list):
            content = content[0]
            
        min_chars_in_line = 80
        content = content.split('\n')
        content = [line for line in content if len(line) > min_chars_in_line]
        content = content[:3]
        new_str = ""
        for line in content:
            new_str += line + '\n'
        return new_str

    @staticmethod
    def find_word_occurrences(content):
        """
        Returns a dictionary of the 3 most frequent words that are 
        at least 4 letters long. Ignores case and punctuation.
        To be called before content reduction.
        """
        if not content:
            return None
        
        if isinstance(content, list):
            content = content[0]

        content = content.lower().translate(content.maketrans('', '', string.punctuation))

        occurrences = defaultdict(int)

        for word in content.split():
            occurrences[word] += 1

        occurrences = sorted(occurrences.items(), key=lambda x: - x[1])
        valid_occur = [oc for oc in occurrences if len(oc[0]) >= 4][:3]

        return { word: str(occur) for word, occur in valid_occur }    

    def restructure_comments(self, row: pd.Series):
        """
        Combines a single article's comments with their authors.
        Leaves the resulting dict in the 'comment-author' column.
        """

        if row['comment-author'] is None:
            return row

        row['comment-author'] = self.format_comment_authors(row['comment-author'])
        
        if not isinstance(row['comment-text'], list):
            if pd.isnull(row['comment-author']):
                return row
            row['comment-text'] = [ row['comment-text'] ]
        
        row['comment-author'] = { auth : comm for auth, comm in zip(row['comment-author'], row['comment-text'])}
        return row

    @staticmethod
    def format_comment_authors(authors):
        """
        Extracts only the commenter's name from a more complex string.
        Currently specific to the TravelSmart comment section.
        """
        if authors is None:
            return None
        
        if not isinstance(authors, list):
            if pd.isnull(authors):
                return None
            authors = [authors]

        authors = [auth.split('\n')[1] + f"_{i+1}" for i, auth in enumerate(authors)]
        
        return authors

    def format(self):
        """
        Applies all formatting functions to the corresponding columns,
        then renames them as required.
        """
        self.df['date'] = self.df['date'].apply(self.format_date)
        
        self.df.insert(3, 'most_used_words', self.df['content'])
        self.df['most_used_words'] = self.df['most_used_words'].apply(self.find_word_occurrences)

        self.df['content'] = self.df['content'].apply(self.reduce_content)
        
        self.df.apply(self.restructure_comments, axis=1)
        self.df.drop('comment-text', axis=1, inplace=True)

        self.df.rename(columns={'headline' : 'title',
                                'date' : 'date_of_publishing',
                                'comment-author' : 'comments'}, inplace=True)

    def export_to_json(self, file_name): # pragma: no cover
        """
        Exports the current dataframe to the specified json file.
        To be called after formatting with format().
        """
        self.df.to_json(file_name, orient='records', indent=4, force_ascii=False)
