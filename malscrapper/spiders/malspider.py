import scrapy
import random


class MalspiderSpider(scrapy.Spider):
    name = "malspider"
    allowed_domains = ["myanimelist.net"]
    start_urls = ["https://myanimelist.net/anime/1"]
    page_number = 1

    def parse(self, response):



        yield{

            'Anime_id' : self.page_number,
            'Title' : response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "h1_bold_none", " " ))]//strong/text()').get(),
            'Genres' : response.xpath('//div[@class="spaceit_pad"]/span[@class="dark_text" and (contains(text(), "Genres") or contains(text(), "Genre"))]/following-sibling::a/text()').getall(),
            'Type' : response.xpath('//div[@class="spaceit_pad"]/span[@class="dark_text" and contains(text(), "Type")]/following-sibling::a/text()').get(),
            'Episodes' : response.xpath('//div[@class="spaceit_pad"]/span[@class="dark_text" and contains(text(), "Episodes")]/following-sibling::text()').get().strip(),
            'Score' : response.xpath('//div[@class="fl-l score"]/div/text()').get(),
            'Rank' : response.xpath('//span[@class="numbers ranked"]/strong/text()').get(),
            'Members' : response.xpath('//span[@class="numbers members"]/strong/text()').get(),
            'Popularity' : response.xpath('//span[@class="numbers popularity"]/strong/text()').get(),
            'Season' : response.xpath('//span[@class="information season"]/a/text()').get(),
            'Studio' : response.xpath('//span[@class="information studio author"]/a/text()').get()
            }



        self.page_number += 1
        next_page_url = 'https://myanimelist.net/anime/' + str(self.page_number)
        #yield response.follow(next_page_url, callback=self.parse)
        yield scrapy.Request(url=next_page_url, callback=self.parse, errback=self.errback_handler)

    def errback_handler(self, failure):
        self.log('Error occurred while scraping page: {}'.format(failure.request.url))
        self.page_number += 1
        next_page_url = 'https://myanimelist.net/anime/' + str(self.page_number)
        yield scrapy.Request(url=next_page_url, callback=self.parse, errback=self.errback_handler)
