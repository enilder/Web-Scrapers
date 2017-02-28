# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re


class BasicSpider(scrapy.Spider):
    name = "ratings_page"
    allowed_domains = ["imdb.com"]
    start_urls = (
        'http://www.imdb.com/title/tt4425200/ratings?ref_=tt_ov_rt',
    )

    def parse(self, response):
        percent_match = re.compile(r"%")
        #print "Crawling page..."
        #print response.body

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

        """

        for key, v in rating_dict.items():
            print key, v[0], v[1]
            yield {
                "rating" : key,
                "rating %": v[1],
                "rating count": v[0]
            }
        """
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
            "1 count" : rating_dict["1"][0]
        }


        pass
