BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

USER_AGENT = 'crawler'

ROBOTSTXT_OBEY = True

CONCURRENT_REQUESTS = 10

DOWNLOAD_DELAY = 2

LOG_LEVEL = 'INFO'

ITEM_PIPELINES = {
    'crawler.pipelines.CrawlerCsvWriterPipeline': 10,
}