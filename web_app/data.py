from module.data_handler import DataHandler
import os


all_posts = DataHandler.json_to_obj(os.path.join('output/travelsmart_formatted.json'))
for id, post in enumerate(all_posts):
    post['id'] = id


def get_posts_on_page(page_num, num_posts):
    first_post = (page_num - 1) * num_posts
    try:
        return all_posts[first_post : first_post + num_posts]
    except IndexError:
        return None
