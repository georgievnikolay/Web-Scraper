import re
from datetime import datetime
from collections import Counter


def arg_none_check(func):
    """
    The decorated function checks if any of its
    arguments are None, and returns None if so.
    """
    def wrapper(*args, **kwargs):
        for arg in args:
            if arg is None:
                return None
        
        return func(*args, **kwargs)
    
    return wrapper


class DataFormatter:
    """
    DataFormatter is used to format data received from the WebScraper class.
    
    It formats a list if dicts, each representing a blog post.
    - The 'headline' item is renamed to 'title'.
    - The 'date' item is renamed to 'date_of_publishing' and
      reduced from an iso-format string to only a date.
    - A 'most_used_words' item is generated from the content.
    - The 'content' item is reduced to only the first 3 paragraphs.
    - A 'comments' dict is generated from 'comment-author' and
      'comment-text', where each comment author is numbered 
      to preserve the comments' chronology.
    
    Usage:
    Instantiate -> set_author_extract_func() (if needed) -> format().
    """

    def __init__(self):
        self.author_extract_func = lambda s: s.split('\n')[1]

    def set_author_extract_func(self, func): # pragma: no cover
        """
        Provide a function that extracts only the author name
        from the website-specific comment-author string.
        The default pattern is "\nAuthor Name\n..." -> "Author Name"
        """
        self.author_extract_func = func

    @staticmethod
    @arg_none_check
    def format_date(date):
        """
        Transforms a datetime iso-format string into a date-only string.
        """
        try:
            return str(datetime.fromisoformat(date).date())
        except:
            return str(date)

    @staticmethod
    @arg_none_check
    def find_word_occurrences(content):
        """
        Returns a dictionary of the three most common words 
        in the provided content that are at least 4 letters long.
        """
        valid_words = [ word for word in re.split(r'\W+', content.lower()) if len(word) >= 4 ]
        return { word: occur for word, occur in Counter(valid_words).most_common(3) }
        
    @staticmethod
    @arg_none_check
    def reduce_content(content):
        """
        Reduces the provided content to only the first three paragraphs.
        A line must be more than 80 characters long to be included.
        """
        paragraphs = [line for line in content.split('\n') if len(line) > 80][:3]
        return "\n".join(paragraphs)
    
    @arg_none_check
    def extract_authors(self, authors):
        """
        Returns a list of only the names from each comment-author string.
        """
        return [self.author_extract_func(auth) for auth in authors]

    @staticmethod
    @arg_none_check
    def group_comments(authors, comments):
        """
        Returns a dict of 'author_n': 'comment' pairs.
        Each author is numbered to avoid duplication.
        """
        grouped_comments = dict()
        for i, auth in enumerate(authors):
            auth += f'_{i + 1}'
            grouped_comments[auth] = comments[i]

        return grouped_comments
    
    @staticmethod
    def unify_dtypes(article):
        """
        Makes sure each article item is in the expected datatype.
        The content is expected as a single string;
        comments and their authors are expected as lists.
        """
        if isinstance(article['content'], list):
            article['content'] = '\n'.join(article['content'])
        
        if not isinstance(article['comment-author'], list) \
                and article['comment-author'] is not None:
            article['comment-author'] = [article['comment-author']]
            article['comment-text'] = [article['comment-text']]
        
        return article

    def format(self, data):
        """
        Applies all formatting, renaming, and restructuring
        to the provided data and returns the result. 
        """
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
