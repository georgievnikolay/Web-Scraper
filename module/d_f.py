import json
import re
from datetime import datetime
from collections import Counter

class DataFormatter:
    def __init__(self, file_name):
        with open(file_name, 'r') as f:
            self.data = json.load(f)

        self.author_extract_func = lambda s: s.split('\n')[1]

    def set_author_extract_func(self, func):
        self.author_extract_func = func

    @staticmethod
    def format_date(date):
        try:
            return str(datetime.fromisoformat(date).date())
        except:
            return str(date)

    @staticmethod
    def find_word_occurrences(content):
        valid_words = [ word for word in re.split(r'\W+', content.lower()) if len(word) >= 4 ]
        return { word: occur for word, occur in Counter(valid_words).most_common(3) }
        
    @staticmethod
    def reduce_content(content):
        paragraphs = [line for line in content.split('\n') if len(line) > 80][:3]
        return "\n".join(paragraphs)
    
    def extract_authors(self, authors):
        if authors is None:
            return None

        return [self.author_extract_func(auth) for auth in authors]

    @staticmethod
    def group_comments(authors, comments):
        if comments is None:
            return None
        
        grouped_comments = dict()
        for i, auth in enumerate(authors):
            auth += f'_{i + 1}'
            grouped_comments[auth] = comments[i]

        return grouped_comments
    
    def unify_dtypes(self, article):
        if isinstance(article['content'], list):
            article['content'] = ''.join(article['content'])
        
        if not isinstance(article['comment-author'], list) \
                and article['comment-author'] is not None:
            article['comment-author'] = [article['comment-author']]
            article['comment-text'] = [article['comment-text']]
        
        return article

    def format(self):
        for article in self.data:
            article = self.unify_dtypes(article)
            article['title'] = article.pop('headline')
            article['date_of_publishing'] = self.format_date(article.pop('date'))
            article['most_used_words'] = self.find_word_occurrences(article['content'])
            article['content'] = self.reduce_content(article.pop('content'))
            article['comment-author'] = self.extract_authors(article['comment-author'])
            article['comments'] = self.group_comments(article.pop('comment-author'),
                                                      article.pop('comment-text'))
    
    def export_to_json(self, file_name):
        with open(file_name, 'w') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)
    
    
formatter = DataFormatter('output/travelsmart.json')
formatter.format()
formatter.export_to_json('output/travelsmart_out.json')