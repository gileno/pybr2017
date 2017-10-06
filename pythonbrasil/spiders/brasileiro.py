# -*- coding: utf-8 -*-
import scrapy

from scrapy_splash import SplashRequest


SCRIPT = '''
function main(splash)
    splash:init_cookies(splash.args.cookies)
    local click_button = splash:jsfunc([[
        function(page) {
        	for(var i = 0; i < page - 1; i++) {
        		$(".next_page a").click();
        	}
        }
    ]])
    assert(splash:go(splash.args.url))
    assert(splash:wait(1))
    click_button(splash.args.page)
    assert(splash:wait(1))
    return {
        url = splash:url(),
        cookies = splash:get_cookies(),
        html = splash:html(),
    }
end
'''

class BrasileiroSpider(scrapy.Spider):
    name = 'brasileiro'
    allowed_domains = ['futpedia.globo.com']

    def start_requests(self):
        yield SplashRequest(
            'http://futpedia.globo.com/campeonato/campeonato-brasileiro',
            self.parse, endpoint='execute', args={'lua_source': SCRIPT, 'page': 3}
        )

    def parse(self, response):
        self.log(response.xpath("//title/text()").extract_first())
        row = response.xpath(
            "//div[contains(@class, 'lista-edicoes')]//table//tr[1]//span/text()"
        )
        self.log('Quem foi o campeão de 87?')
        self.log(row.extract_first().upper())
