import scrapy
from stackoverflow.items import StackoverflowItem

class StackoverflowSpider(scrapy.Spider): 
    name = 'so_spider'

    start_urls = [
       'https://stackexchange.com/leagues/1/year/stackoverflow/'
    ]

    def __init__(self, num_pages):
        self.num_pages = num_pages

    def parse(self, response):
        # handles pagination, calls parse_page for every page
        for i in range(1,int(self.num_pages)+1):
            yield scrapy.Request(response.url + f'?page={i}', callback=self.parse_page)

    def parse_page(self, response):
        name_list = response.xpath('//div[@class="userInfo"]/h2/a/text()').extract()
        # get all the links to the profiles by xpath
        link_list = response.xpath('//div[@class="userInfo"]//h2/a/@href').extract()
        # get meta info
        stats = response.xpath('//div[@class="statsWrapper"]')
        # extract all one after the other
        rank_number_list = stats.xpath('.//div[1]/span/text()').extract()
        change_list = stats.xpath('.//div[2]/span/text()').extract()
        total_rep_list = stats.xpath('.//div[3]/span/text()').extract()
        year_rep_list = stats.xpath('.//div[4]/span/text()').extract()
        # zip for iteration
        zip_list = zip(link_list, name_list, rank_number_list, change_list,
                       total_rep_list, year_rep_list)
        # call parse_profile for all links
        for link, name, rank_number, change, total_rep, year_rep in zip_list:
            request = scrapy.Request(url=link, callback=self.parse_profile)
            request.meta['name'] = name
            request.meta['rank_number'] = rank_number
            request.meta['change'] = change
            request.meta['total_rep'] = total_rep
            request.meta['year_rep'] = year_rep

            yield request

    def parse_profile(self, response):
        blog_link = response.xpath('//svg[@class="svg-icon iconLink"]\
                                    /parent::*/following-sibling::div\
                                    /a/@href').extract_first()
        # jump into top tags section
        top_tags = response.xpath('//div[contains(@class, "profile-top-tags")]\
                                   //div[contains(@class, "grid__fl1")]')
        # titles of the tags, e.g. "python"
        tag_titles = top_tags.xpath('./div/a/text()').extract()
        # scores for these tags
        scores = top_tags.xpath('./div[2]//span[contains(text(), "Score")]\
                                 /following-sibling::span/text()').extract()
        # number of posts for these tags
        posts = top_tags.xpath('./div[2]//span[contains(text(), "Posts")]\
                                /following-sibling::span/text()').extract()

        # load metas
        name = response.meta.get('name')
        rank_number = response.meta.get('rank_number')
        change = response.meta.get('change')
        total_rep = response.meta.get('total_rep')
        year_rep = response.meta.get('year_rep')

        # zip the lists
        zip_list = zip(tag_titles, scores, posts)

        item = StackoverflowItem()

        # one observation per list item
        for tag_title, score, num_posts in zip_list:
            item['name'] = name
            item['rank_number'] = rank_number
            item['blog_link'] = blog_link
            item['change'] = change
            item['total_rep'] = total_rep
            item['year_rep'] = year_rep
            item['tag_title'] = tag_title
            item['score'] = score
            item['number_posts'] = num_posts

            yield item

