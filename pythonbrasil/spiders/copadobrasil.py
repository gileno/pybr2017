# -*- coding: utf-8 -*-
import scrapy

from scrapy_splash import SplashRequest


class CopadobrasilSpider(scrapy.Spider):
    name = 'copadobrasil'
    allowed_domains = ['globoesporte.globo.com']
    
    def start_requests(self):
        yield SplashRequest(
            url='http://globoesporte.globo.com/mg/futebol/'\
                'copa-do-brasil/jogo/27-09-2017/cruzeiro-flamengo/',
            callback=self.parse, args={'wait': 2}
        )

    def parse(self, response):
        self.log(
            response.xpath(
                "//*[contains(@class, 'cabecalho-jogo')]/span/text()"
            ).extract_first()
        )
