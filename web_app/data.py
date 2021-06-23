from module.data_handler import DataHandler
import math

class BlogData:
    blog_names = ('travelsmart','bozho','pateshestvenik','az_moga','igicheva')
    
    blogs = {
        'travelsmart' : None,
        'bozho' : None,
        'pateshestvenik' : None,
        'az_moga' : None,
        'igicheva' : None
    }

    class SingleBlog:
        def __init__(self, posts_per_page):
            self.posts_per_page = posts_per_page
            self.data = None
            self.num_pages = 0
            self.num_posts = 0

        def load_data(self, file_path):
            self.data = DataHandler.json_to_obj(file_path)
            
            for id, post in enumerate(self.data):
                post['id'] = id + 1
                post['content'] = post['content'].split('\n')
            
            self.num_pages = math.ceil(len(self.data) / self.posts_per_page)
            self.num_posts = len(self.data)

        def get_posts_on_page(self, page_num):
            first_post = (page_num - 1) * self.posts_per_page
            try:
                return self.data[first_post : first_post + self.posts_per_page]
            except IndexError:
                return None

        def get_post(self, post_id):
            return self.data[post_id - 1]

        def get_num_pages(self):
            return self.num_pages
        
        def get_num_posts(self):
            return self.num_posts

    @classmethod
    def reload_blogs(cls):
        for blog_name in cls.blog_names:
            new_blog = cls.SingleBlog(5)
            try:
                new_blog.load_data(f"output/{blog_name}_formatted.json")
            except:
                continue

            cls.blogs[blog_name] = new_blog
    
        cls.blogs = {k: v for k, v in cls.blogs.items() if v is not None}

    @classmethod
    def get_blogs(cls):
        cls.reload_blogs()
        return cls.blogs
