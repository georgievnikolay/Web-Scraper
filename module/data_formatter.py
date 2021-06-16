import pandas as pd
import os

import string
from collections import defaultdict

class DataFormatter:

    def __init__(self): # pragma: no cover
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
    def find_word_occurrences(content, num_words, min_len):
        """
        """
        if not content:
            return None
        
        content = content.lower().translate(content.maketrans('', '', string.punctuation))

        occurences = defaultdict(int)

        for word in content.split():
            occurences[word] += 1

        occurences = sorted(occurences.items(), key=lambda x: - x[1])
        valid_occur = [oc for oc in occurences if len(oc[0]) >= min_len][:num_words]

        return { word: occur for word, occur in valid_occur }

    def restructure_comments(self):
        """
        """
        pass

    @staticmethod
    def format_comment_authors(authors):
        """
        """
        if not authors:
            return None

        if not isinstance(authors, list):
            authors = [authors]

        authors = [auth.split('\n')[1] for auth in authors]

        return authors

    def format(self):
        """
        """
        pass

    def export_to_json(self):
        """
        """
        pass



# formatter = DataFormatter()
# formatter.import_file('output/travelsmart.json')
# print(formatter.df['date'])