import requests
from bs4 import BeautifulSoup
import re
import urllib.request, json
from Model.Scrappers import AbstractScrapper as AS
# class="review-content"
#?start=X where X = page_number*20

class AmazonScrapper(AS.AbstractScrapper):

    def scrapURL(self):
        super()