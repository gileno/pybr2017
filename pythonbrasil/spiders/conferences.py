# -*- coding: utf-8 -*-
import scrapy
import json
import urllib.parse

from selenium import webdriver

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import Identity, TakeFirst
from scrapy.loader import ItemLoader

from pythonbrasil.items import ConferenceItem, PaperItem


class ConferencesSpider(CrawlSpider):

    name = 'conferences'
    allowed_domains = ['www.ieee.org', 'ieeexplore.ieee.org']
    start_urls = ['http://www.ieee.org/conferences_events/conferences/search/index.html']
    rules = (
        Rule(
            LinkExtractor(allow='/conferences_events/conferences/conferencedetails/index.html'),
            callback='parse_conference',
        ),
        Rule(
            LinkExtractor(allow='/conferences_events/conferences/search/index.html')
        )
    )
    search = ''

    def start_requests(self):
        url = 'http://www.ieee.org/conferences_events/conferences/search/index.html'
        if self.search:
            formdata = {
                'KEYWORDS': self.search
            }
            yield scrapy.FormRequest(
                url=url, callback=self.parse, formdata=formdata, method='GET'
            )
        else:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_conference(self, response):
        name = response.xpath('//*[contains(@class, "box-lc-top-indent")]//h1/a/text()').extract_first()
        formdata = {
            'queryText': name,
            'pageNumber': "1",
            'newsearch': "true"
        }
        search_request = scrapy.FormRequest(
            url='http://ieeexplore.ieee.org/rest/search', method='POST',
            callback=self.parse_paper_search, body=json.dumps(formdata)
        )
        search_request.meta['page_number'] = 1
        search_request.meta['query_text'] = formdata['queryText']
        referer = 'http://ieeexplore.ieee.org/search/searchresult.jsp?'
        search_request.headers['Referer'] = referer + urllib.parse.urlencode(formdata)
        search_request.headers['Content-Type'] = 'application/json;charset=UTF-8'
        yield search_request

    def parse_paper_search(self, response):
        result = json.loads(response.text)
        for record in result['records']:
            item = PaperItem()
            item['title'] = record['title']
            item['conference'] = response.meta['query_text']
            item['url'] = 'http://ieeexplore.ieee.org%s' % record['documentLink']
            item['publication_year'] = record['publicationYear']
            item['publication_title'] = record['publicationTitle']
            item['article_number'] = record['articleNumber']
            item['publisher'] = record['publisher']
            authors = [author['preferredName'] for author in record['authors']]
            item['authors'] = ', '.join(authors)
            yield self.get_paper_details(item)

        page_number = response.meta['page_number'] + 1
        if result['endRecord'] < result['totalRecords']:
            formdata = {
                'queryText': response.meta['query_text'],
                'pageNumber': str(page_number),
                'newsearch': "true"
            }
            search_request = scrapy.FormRequest(
                url='http://ieeexplore.ieee.org/rest/search', method='POST',
                callback=self.parse_paper_search, body=json.dumps(formdata)
            )
            search_request.meta['page_number'] = page_number
            search_request.meta['query_text'] = formdata['queryText']
            referer = 'http://ieeexplore.ieee.org/search/searchresult.jsp?'
            search_request.headers['Referer'] = referer + urllib.parse.urlencode(formdata)
            search_request.headers['Content-Type'] = 'application/json;charset=UTF-8'
            yield search_request

    def get_paper_details(self, paper_item):
        driver = webdriver.PhantomJS("C:\\Users\\gileno\\phantomjs")
        driver.get(paper_item['url'])
        paper_item['abstract'] = driver.find_element_by_css_selector(".abstract-text").text
        keywords = driver.find_elements_by_css_selector(".doc-all-keywords-list-item span a")
        paper_item['keywords'] = ','.join([keyword.text for keyword in keywords])
        return paper_item