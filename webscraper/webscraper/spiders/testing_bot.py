# -*- coding: utf-8 -*-
import scrapy


# toto je jednoduchý testovací bot, jehož chování je stejné jako chování třídy realityBot, nicméně aby demonstrace
# funkcionality nemusela běžet hodinu, byl vytvořen tento bot, který scrapuje pouze jednu url a nepokračuje na další
# stránky pomocí next_page_link

# zároveň je otestovaný pomocí spider.Contracts
class TestingBotSpider(scrapy.Spider):
    name = 'testingbot'

    def __init__(self, name=None, **kwargs):
        super().__init__(name)
        self.url = ""

    def start_requests(self):
        self.start_urls = ['https://reality.idnes.cz/s/praha']

        for url in self.start_urls:
            self.url = url
            yield scrapy.Request(self.url, self.parse, meta={'region': url.split("/")[-1]})

    def parse(self, response, **kwargs):
        """ This function parses a response. Then it goes and parses each reality listed on the page.

            @url https://reality.idnes.cz/s/praha/
            @returns requests 1 20
            @scrapes title location price region land_area util_area building building_type floor property
        """

        reality_page_links = response.css('.c-products__inner a::attr(href)')
        yield from response.follow_all(reality_page_links, self.parse_reality, meta=response.meta)

    def parse_reality(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        scraped_info = {
            'title': extract_with_css('.row-main .b-detail .b-detail__title span::text'),
            'location': extract_with_css('.row-main .b-detail .b-detail__info::text'),
            'price': extract_with_css('.row-main .b-detail .b-detail__price strong::text'),
            'region': response.meta['region'],
        }

        util_area = False
        land_area = False
        property_info = False
        building_info = False
        floors_info = False
        building_type_info = False

        util_area_idx = 0
        land_area_idx = 0
        property_info_idx = 0
        building_info_idx = 0
        floors_info_idx = 0
        building_type_info_idx = 0

        for x in range(3, 12):
            if extract_with_css('.row-main div[class = \'b-definition-columns mb-0\'] '
                                'dl dt:nth-of-type(' + str(x) + ')::text') == 'Užitná plocha':
                util_area = True
                util_area_idx = x
            if extract_with_css('.row-main div[class = \'b-definition-columns mb-0\'] '
                                'dl dt:nth-of-type(' + str(x) + ')::text') == 'Plocha pozemku':
                land_area = True
                land_area_idx = x
            if extract_with_css('.row-main div[class = \'b-definition-columns mb-0\'] '
                                'dl dt:nth-of-type(' + str(x) + ')::text') == 'Konstrukce budovy':
                building_info = True
                building_info_idx = x
            if extract_with_css('.row-main div[class = \'b-definition-columns mb-0\'] '
                                'dl dt:nth-of-type(' + str(x) + ')::text') == 'Typ komerční nemovitosti':
                building_type_info = True
                building_type_info_idx = x
            if extract_with_css('.row-main div[class = \'b-definition-columns mb-0\'] '
                                'dl dt:nth-of-type(' + str(x) + ')::text') == 'Podlaží':
                floors_info = True
                floors_info_idx = x
            if extract_with_css('.row-main div[class = \'b-definition-columns mb-0\'] '
                                'dl dt:nth-of-type(' + str(x) + ')::text') == 'Vlastnictví':
                property_info = True
                property_info_idx = x

        if land_area:
            scraped_info['land_area'] = extract_with_css(
                '.row-main div[class = \'b-definition-columns mb-0\'] '
                'dl dd:nth-of-type(' + str(land_area_idx) + ')::text')
        if not land_area:
            scraped_info['land_area'] = ""

        if util_area:
            scraped_info['util_area'] = extract_with_css(
                '.row-main div[class = \'b-definition-columns mb-0\']'
                ' dl dd:nth-of-type(' + str(util_area_idx) + ')::text')
        if not util_area:
            scraped_info['util_area'] = ""

        if building_info:
            scraped_info['building'] = extract_with_css(
                '.row-main div[class = \'b-definition-columns mb-0\']'
                ' dl dd:nth-of-type(' + str(building_info_idx) + ')::text')

        if not building_info:
            scraped_info["building"] = ""

        if building_type_info:
            scraped_info['building_type'] = extract_with_css(
                '.row-main div[class = \'b-definition-columns mb-0\']'
                ' dl dd:nth-of-type(' + str(building_type_info_idx) + ')::text')

        if not building_type_info:
            scraped_info['building_type'] = ""

        if floors_info:
            scraped_info['floor'] = extract_with_css(
                '.row-main div[class = \'b-definition-columns mb-0\']'
                ' dl dd:nth-of-type(' + str(floors_info_idx) + ')::text')

        if not floors_info:
            scraped_info['floor'] = ""

        if property_info:
            scraped_info['property'] = extract_with_css(
                '.row-main div[class = \'b-definition-columns mb-0\']'
                ' dl dd:nth-of-type(' + str(property_info_idx) + ')::text')

        if not property_info:
            scraped_info['property'] = ""

        yield scraped_info
