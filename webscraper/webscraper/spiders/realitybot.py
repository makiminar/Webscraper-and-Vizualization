# -*- coding: utf-8 -*-
import scrapy


class RealitybotSpider(scrapy.Spider):
    name = 'realitybot'

    def __init__(self, name=None, **kwargs):
        super().__init__(name)
        self.url = ""
        self.page = ""

    def start_requests(self):
        self.start_urls = ['https://reality.idnes.cz/s/praha',
                           'https://reality.idnes.cz/s/ustecky-kraj',
                           'https://reality.idnes.cz/s/pardubicky-kraj',
                           'https://reality.idnes.cz/s/stredocesky-kraj',
                           'https://reality.idnes.cz/s/moravskoslezsky-kraj',
                           'https://reality.idnes.cz/s/zlinsky-kraj',
                           'https://reality.idnes.cz/s/liberecky-kraj',
                           'https://reality.idnes.cz/s/plzensky-kraj',
                           'https://reality.idnes.cz/s/kralovehradecky-kraj',
                           'https://reality.idnes.cz/s/karlovarsky-kraj',
                           'https://reality.idnes.cz/s/jihocesky-kraj',
                           'https://reality.idnes.cz/s/olomoucky-kraj',
                           'https://reality.idnes.cz/s/jihomoravsky-kraj',
                           'https://reality.idnes.cz/s/kraj-vysocina']

        for url in self.start_urls:
            self.url = url
            self.page = self.url.split("/")[-1]
            yield scrapy.Request(self.url, self.parse, meta={'region': url.split("/")[-1]})

    def parse(self, response, **kwargs):
        reality_page_links = response.css('.c-products__inner a::attr(href)')
        rqst = response.follow_all(reality_page_links, self.parse_reality, meta=response.meta)
        yield from rqst

        # next_page_links = response.css('a[class=\'btn paging__item next\']::attr(href)')
        # yield from response.follow_all(next_page_links, self.parse)

    def parse_reality(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        scraped_info = {
            'title': extract_with_css('.row-main .b-detail .b-detail__title span::text'),
            'location': extract_with_css('.row-main .b-detail .b-detail__info::text'),
            'price': extract_with_css('.row-main .b-detail .b-detail__price strong::text'),
            'region': response.meta['region'],
            'property': extract_with_css(
                '.row-main div[class = \'b-definition-columns mb-0\'] dl dd:nth-of-type(5)::text'),
            'building': extract_with_css(
                '.row-main div[class = \'b-definition-columns mb-0\'] dl dd:nth-of-type(3)::text')
        }
        util_area = False
        land_area = False

        util_area_idx = 0
        land_area_idx = 0

        for x in range(6, 12):
            if extract_with_css('.row-main div[class = \'b-definition-columns mb-0\'] '
                                'dl dt:nth-of-type(' + str(x) + ')::text') == 'Užitná plocha':
                util_area = True
                util_area_idx = x
            if extract_with_css('.row-main div[class = \'b-definition-columns mb-0\'] '
                                'dl dt:nth-of-type(' + str(x) + ')::text') == 'Plocha pozemku':
                land_area = True
                land_area_idx = x

        if land_area and util_area:

            scraped_info['land_area'] = extract_with_css(
                '.row-main div[class = \'b-definition-columns mb-0\'] '
                'dl dd:nth-of-type(' + str(land_area_idx) + ')::text')
            scraped_info['util_area'] = extract_with_css(
                '.row-main div[class = \'b-definition-columns mb-0\']'
                ' dl dd:nth-of-type(' + str(util_area_idx) + ')::text')
            yield scraped_info
        if land_area:
            scraped_info['land_area'] = extract_with_css(
                '.row-main div[class = \'b-definition-columns mb-0\'] '
                'dl dd:nth-of-type(' + str(land_area_idx) + ')::text')
            scraped_info['util_area'] = ""
            yield scraped_info
        if util_area:
            scraped_info['land_area'] = ""
            scraped_info['util_area'] = extract_with_css(
                '.row-main div[class = \'b-definition-columns mb-0\']'
                ' dl dd:nth-of-type(' + str(util_area_idx) + ')::text')
            yield scraped_info

        scraped_info['land_area'] = ""
        scraped_info['util_area'] = ""
        yield scraped_info