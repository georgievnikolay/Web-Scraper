import re
from datetime import datetime
from collections import Counter

def arg_none_check(func):
    def wrapper(*args, **kwargs):
        for arg in args:
            if arg is None:
                return None
        
        return func(*args, **kwargs)
    
    return wrapper

class DataFormatter:
    def __init__(self):
        self.author_extract_func = lambda s: s.split('\n')[1]

    def set_author_extract_func(self, func): # pragma: no cover
        self.author_extract_func = func

    @staticmethod
    @arg_none_check
    def format_date(date):
        try:
            return str(datetime.fromisoformat(date).date())
        except:
            return str(date)

    @staticmethod
    @arg_none_check
    def find_word_occurrences(content):
        valid_words = [ word for word in re.split(r'\W+', content.lower()) if len(word) >= 4 ]
        return { word: occur for word, occur in Counter(valid_words).most_common(3) }
        
    @staticmethod
    @arg_none_check
    def reduce_content(content):
        paragraphs = [line for line in content.split('\n') if len(line) > 80][:3]
        return "\n".join(paragraphs)
    
    @arg_none_check
    def extract_authors(self, authors):
        return [self.author_extract_func(auth) for auth in authors]

    @staticmethod
    @arg_none_check
    def group_comments(authors, comments):
        grouped_comments = dict()
        for i, auth in enumerate(authors):
            auth += f'_{i + 1}'
            grouped_comments[auth] = comments[i]

        return grouped_comments
    
    @staticmethod
    def unify_dtypes(article):
        if isinstance(article['content'], list):
            article['content'] = '\n'.join(article['content'])
        
        if not isinstance(article['comment-author'], list) \
                and article['comment-author'] is not None:
            article['comment-author'] = [article['comment-author']]
            article['comment-text'] = [article['comment-text']]
        
        return article

    def format(self, data):
        for article in data:
            article = self.unify_dtypes(article)
            article['title'] = article.pop('headline')
            article['date_of_publishing'] = self.format_date(article.pop('date'))
            article['most_used_words'] = self.find_word_occurrences(article['content'])
            article['content'] = self.reduce_content(article.pop('content'))
            article['comment-author'] = self.extract_authors(article['comment-author'])
            article['comments'] = self.group_comments(article.pop('comment-author'),
                                                      article.pop('comment-text'))
        
        return data
