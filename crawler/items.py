import scrapy


class CrawlerItem(scrapy.Item):
    job_title = scrapy.Field()
    job_category = scrapy.Field()
    client_name = scrapy.Field()
    fee = scrapy.Field()
    description = scrapy.Field()
