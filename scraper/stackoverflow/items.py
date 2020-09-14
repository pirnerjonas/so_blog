# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class StackoverflowItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    rank_number = scrapy.Field()
    blog_link = scrapy.Field()
    change = scrapy.Field()
    total_rep = scrapy.Field()
    year_rep = scrapy.Field()
    tag_title = scrapy.Field()
    score = scrapy.Field()
    number_posts = scrapy.Field()
