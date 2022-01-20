import scrapy
from bs4 import BeautifulSoup

from crawler.items import CrawlerItem


class LancersSpider(scrapy.Spider):

    name = 'lancers'
    allowed_domains = ['lancers.jp']
    start_urls = [f'https://www.lancers.jp/work/search{q}?open=1&ref=header_menu&show_description=1&sort=client&work_rank%5B%5D=0&work_rank%5B%5D=2&work_rank%5B%5D=3' for q in ['/system', '/web']]

    def parse(self, response):
        try:
            job_title = ''
            job_category = ''
            client_name = ''
            fee = ''
            description = ''

            soup = BeautifulSoup(response.text, 'html.parser')
            jobs = soup.find_all(name='div',attrs={'class': 'c-media__content__right'})

            crawling_url = response.url

            print(f'crawling: {crawling_url}')

            for job in jobs:

                # job_title
                if job.select('a.c-media__title'):
                    job_title = job.select('a.c-media__title')[0].span.get_text(strip=True)
                    # タグが付いているときの処理(タグを除外)
                    if job.select('ul.c-media__job-tags'):
                        tags = job.select('ul.c-media__job-tags')[0].get_text(strip=True)
                        job_title = job_title.replace(tags, '', 1)

                # job_category
                if job.select('a.p-search-job__division-link'):
                    job_category = job.select('a.p-search-job__division-link')[0].get_text(strip=True)

                # client_name
                if job.select('p.c-avatar__note'):
                    client_name = job.select('p.c-avatar__note')[0].get_text(strip=True)

                # fee
                if job.select('span.c-media__job-price'):
                    fee = job.select('span.c-media__job-price')[0].get_text(strip=True)

                # description
                if job.select('div.c-media__description'):
                    # タグが付いているときの処理(タグを除外)
                    if len(job.select('div.c-media__description')) == 1:
                        description = job.select('div.c-media__description')[0].get_text(strip=True)
                    else:
                        description = job.select('div.c-media__description')[1].get_text(strip=True)

                description = description.replace('\r', '').replace('\n', '')

                yield CrawlerItem(
                    job_title=job_title,
                    job_category=job_category,
                    client_name=client_name,
                    fee=fee,
                    description=description
                )

            # "次へ"のURLを取得し、再帰的にクローリング
            next_page = \
                soup.find(name='span', attrs={'class': 'pager__item--next'}).\
                    find(name='a', attrs='pager__item__anchor').get('href')
            if next_page is not None:
                # URLを絶対パスに変換
                next_page = response.urljoin(next_page)

                yield scrapy.Request(next_page, callback=self.parse)

        except Exception as e:
            http_status_code = response.status
            print(f'Http Status Code: {http_status_code}')
            print(f'ERROR: {e}')
            pass

        else:
            print('Successfully completed ')
