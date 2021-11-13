# -*- coding: utf-8 -*-
import scrapy

CATEGORIES = ['ustecky-kraj', 'pardubicky-kraj', 'stredocesky-kraj',
              'praha', 'moravskoslezsky-kraj', 'zlinsky-kraj',
              'liberecky-kraj', 'plzensky-kraj', 'kralovehradecky-kraj',
              'karlovarsky-kraj', 'jihocesky-kraj', 'olomoucky-kraj',
              'jihomoravsky-kraj', 'kraj-vysocina']


class RealitybotSpider(scrapy.Spider):
    name = 'realitybot'

    start_urls = ['https://reality.idnes.cz/s/praha']

    def parse(self, response, **kwargs):
        reality_page_links = response.css('.c-products__inner a::attr(href)')
        yield from response.follow_all(reality_page_links, self.parse_reality)

        # next_page_links = response.css('a[class=\'btn paging__item next\']::attr(href)')
        # yield from response.follow_all(next_page_links, self.parse)

    def parse_reality(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        yield {
            'title': extract_with_css('.row-main .b-detail .b-detail__title span::text'),
            'location': extract_with_css('.row-main .b-detail .b-detail__info::text'),
            'price': extract_with_css('.row-main .b-detail .b-detail__price strong::text'),
            'land_area': extract_with_css(
                '.row-main div[class = \'b-definition-columns mb-0\'] dl dd:nth-of-type(8)::text'),
            'util_area': extract_with_css(
                '.row-main div[class = \'b-definition-columns mb-0\'] dl dd:nth-of-type(9)::text'),
            'num_of_rooms': extract_with_css(
                '.row-main div[class = \'b-definition-columns mb-0\'] dl dd:nth-of-type(12)::text'),
            'property': extract_with_css(
                '.row-main div[class = \'b-definition-columns mb-0\'] dl dd:nth-of-type(5)::text'),
            'building': extract_with_css(
                '.row-main div[class = \'b-definition-columns mb-0\'] dl dd:nth-of-type(3)::text'),
            # 'category': response.url
        }
