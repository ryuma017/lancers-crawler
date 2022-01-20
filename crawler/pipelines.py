import csv
from datetime import datetime

from itemadapter import ItemAdapter


class CrawlerCsvWriterPipeline:

    def open_spider(self, spider):
        f = open(f'crawling({datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}).csv', 'w')
        fieldnames = [
            'job_title',
            'job_category',
            'client_name',
            'fee',
            'description'
        ]
        self.f = f
        self.writer = csv.DictWriter(f, fieldnames=fieldnames)
        self.writer.writeheader()

    def close_spider(self, spider):
        self.f.close

    def process_item(self, item, spider):
        self.writer.writerow(ItemAdapter(item).asdict())
