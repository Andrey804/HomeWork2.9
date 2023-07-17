import scrapy
import re


class MainSpider(scrapy.Spider):

    name = 'main'
    start_urls = ['http://quotes.toscrape.com/']

    # names_authors = set()

    def parse(self, response):
        quotes = response.css('div[class=quote]')

        for quote in quotes:
            author_name = quote.xpath('span[2]/small/text()').get()

            tags = [t.get() for t in quote.css('a[class=tag]::text')]
            quote_text = quote.xpath('span[1]/text()').get()
            author_url = self.start_urls[0] + quote.xpath('span[2]/a/@href').get()

            # print(1, author_name)
            # print(2, tags)
            # print(3, quote_text)
            # print(4, author_url)


            yield scrapy.Request(author_url, callback=self.author_parse)
            # print(5, author)

        # for n in range(2, 11):
        #     url = f'{self.start_urls[0]}/page/{n}'
        #
        #     yield scrapy.Request(url=url)
        #     print(f"scraped page {url}")

    def author_parse(self, response):
        fullname = response.xpath('/html/body/div/div[2]/h3/text()').get()
        born_date = response.xpath('/html/body/div/div[2]/p[1]/span[1]/text()').get()
        born_location = response.xpath('/html/body/div/div[2]/p[1]/span[2]/text()').get()
        description = response.xpath('/html/body/div/div[2]/div/text()').get()

        # print(5.1, fullname)
        # print(5.2, born_date)
        # print(5.3, born_location)
        # print(5.4, description)

        return {'fullname': fullname,
                'born_date': born_date,
                'born_location': born_location,
                'description': description}





