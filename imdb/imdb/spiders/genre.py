# -*- coding: utf-8 -*-
import scrapy
import urlparse
from scrapy.http import Request
from bs4 import BeautifulSoup
import re

#Scrapes Horror genre films from imdb.

class GenreSpider(scrapy.Spider):
    name = "genre"
    allowed_domains = ["imdb.com"]
    start_urls = (
        'http://www.imdb.com/search/title?genres=horror&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=2406822102&pf_rd_r=14ASJAYH6Y7WBNTXHX3V&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_12',
    )

    def parse(self, response):

        #insert page scraping code here
        movie_links = response.css('h3[class=lister-item-header]>a::attr(href)').extract()
        for movie in movie_links:
            yield Request(urlparse.urljoin(response.url, movie), callback=self.parse_imdb_page)

        #Retrieve next page
        pagination = response.css('div[class=desc]>a::attr(href)').extract()
        print pagination
        for next_page in pagination:
            yield Request(urlparse.urljoin(response.url, next_page))

        pass

    # Parse movie page for review link
    def parse_imdb_page(self, response):

        #Retrieve movie title
        #movie_title = response.css('h1[itemprop=name]::attr(text)').extract()
        #self.log(movie_title)
        #print movie_title

        #Retrieve reviews url
        reviews_page = response.css('div.imdbRating>a::attr(href)').extract()

        yield Request(urlparse.urljoin(response.url, reviews_page[0]), callback=self.parse_reviews_page)

        pass

    #Parses review page for title and ratings
    def parse_reviews_page(self, response):

        #regular expression matching percent value
        percent_match = re.compile(r"%")

        #create a BeautifulSoup object from the response
        bsObj = BeautifulSoup(response.body)

        #retreive td elements with percentage ratings
        ratings = bsObj.findAll("td", attrs={"background": re.compile("rating/ruler.gif")})

        #retrieve number of votes
        rating_counts = [row.findPreviousSibling("td").get_text() for row in ratings if percent_match.search(row.get_text())]

        #retrieve rating # from 1 - 10
        rating_vals = [row.findNextSibling("td").get_text() for row in ratings if percent_match.search(row.get_text())]

        #retrieve percentage ratings
        ratings = [row.get_text() for row in ratings if percent_match.search(row.get_text())]

        #format ratings percent to remove unicode characters
        ratings_formatted = [rating.replace(u'\xa0',"") for rating in ratings]

        rating_dict = dict(zip(rating_vals, zip(rating_counts, ratings_formatted)))

        #Loads page data into csv
        yield {
            "title" : response.css("h1>a::text").extract(),
            "10 perc" : rating_dict["10"][1],
            "10 count" : rating_dict["10"][0],
            "9 perc" : rating_dict["9"][1],
            "9 count" : rating_dict["9"][0],
            "8 perc" : rating_dict["8"][1],
            "8 count" : rating_dict["8"][0],
            "7 perc" : rating_dict["7"][1],
            "7 count" : rating_dict["7"][0],
            "6 perc" : rating_dict["6"][1],
            "6 count" : rating_dict["6"][0],
            "5 perc" : rating_dict["5"][1],
            "5 count" : rating_dict["5"][0],
            "4 perc" : rating_dict["4"][1],
            "4 count" : rating_dict["4"][0],
            "3 perc" : rating_dict["3"][1],
            "3 count" : rating_dict["3"][0],
            "2 perc" : rating_dict["2"][1],
            "2 count" : rating_dict["2"][0],
            "1 perc" : rating_dict["1"][1],
            "1 count" : rating_dict["1"][0],
            "Averaged Rating": response.css('p>a[href*="user_rating"]::text').extract()
        }

        pass
