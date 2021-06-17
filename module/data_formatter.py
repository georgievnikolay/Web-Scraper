import pandas as pd
import os

import string
from collections import defaultdict


class DataFormatter:

    def __init__(self):  # pragma: no cover
        """
        """
        self.df = None

    def import_file(self, file_name):
        """
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
    def format_date(date: pd.Timestamp):
        """
        """
        if not date:
            return None

        return f"{date.day}/{date.month}/{date.year}"
    
    @staticmethod
    def reduce_content(content):
        """
        """
        if not content:
            return None
            
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
        """
        if not content:
            return None
        
        content = content.lower().translate(content.maketrans('', '', string.punctuation))

        occurrences = defaultdict(int)

        for word in content.split():
            occurrences[word] += 1

        occurrences = sorted(occurrences.items(), key=lambda x: - x[1])
        valid_occur = [oc for oc in occurrences if len(oc[0]) >= 4][:3]

        return { word: str(occur) for word, occur in valid_occur }    

    def restructure_comments(self, row: pd.Series):
        """
        """

        if not row['comment-author'] or not row['comment-text']:
            return row

        row['comment-author'] = self.format_comment_authors(row['comment-author'])
        
        if not isinstance(row['comment-text'], list):
            row['comment-text'] = [ row['comment-text'] ]
        
        row['comment-author'] = { auth : comm for auth, comm in zip(row['comment-author'], row['comment-text'])}
        return row

    @staticmethod
    def format_comment_authors(authors):
        """
        """
        if not authors:
            return None

        if not isinstance(authors, list):
            authors = [authors]

        authors = [auth.split('\n')[1] + f"_{i+1}" for i, auth in enumerate(authors)]
        
        return authors

    def format(self):
        """
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
        """
        self.df.to_json(file_name, orient='records', indent=4, force_ascii=False)
