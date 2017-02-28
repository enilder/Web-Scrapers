# -*- coding: utf-8 -*-
import scrapy
import urlparse
from scrapy.http import Request


class RatingsSpider(scrapy.Spider):
    name = "ratings"
    allowed_domains = ["imdb.com"]
    start_urls = (
        'http://www.imdb.com/showtimes/location?ref_=inth_ov_sh_sm',
    )

    def parse(self, response):

        movies = response.css('div.title>a[href*="showtimes/title"]::attr(href)').extract()
        for movie in movies:
            print movie
            yield Request(urlparse.urljoin(response.url, movie), callback=self.parse_movie)

        pass

    def parse_movie(self, response):
        title = response.css('h4[itemprop=name]>a::attr(href)').extract()
        self.log(title)
        print title
        yield Request(urlparse.urljoin(response.url, title[0]), callback=self.parse_imdb_page)

        pass


    def parse_imdb_page(self,response):

        #reviews_page = response.css('div#quicklinksMainSection>a[href*=reviews]::attr(href)').extract()
        movie_title = response.css('h1[itemprop=name]::attr(text)').extract()
        reviews_page = response.css('div.imdbRating>a::attr(href)').extract()
        self.log(movie_title)
        print movie_title
        yield Request(urlparse.urljoin(response.url, reviews_page[0]), callback=self.parse_reviews)

        pass

    def parse_reviews(self, response):
        ten_ratings = response.css('tr>td[background*=ruler]>img::attr(text)').extract()
        one_ratings = response.css('tr:nth-child(11)>td[background*=ruler]>img::attr(text)').extract()
        print "10 ratings %s\t 1 ratings %s" % (ten_ratings[0], one_ratings[0])

        pass
