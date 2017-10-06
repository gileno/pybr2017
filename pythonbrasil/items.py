# -*- coding: utf-8 -*-

import scrapy


class ConferenceItem(scrapy.Item):

    table_name = 'conferences'
    url = scrapy.Field()
    name = scrapy.Field()
    dates = scrapy.Field()
    location = scrapy.Field()
    website = scrapy.Field()
    contact = scrapy.Field()
    code = scrapy.Field()
    attendance = scrapy.Field()


class PaperItem(scrapy.Item):

    table_name = 'papers'
    abstract = scrapy.Field()
    conference = scrapy.Field()
    keywords = scrapy.Field()
    title = scrapy.Field()
    publisher = scrapy.Field()
    publication_year = scrapy.Field()
    publication_title = scrapy.Field()
    article_number = scrapy.Field()
    url = scrapy.Field()
    authors = scrapy.Field()
