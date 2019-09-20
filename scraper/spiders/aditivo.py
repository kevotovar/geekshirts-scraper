# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver


class AditivoSpider(scrapy.Spider):
    name = 'aditivo'
    start_urls = [
        # 'https://aditivo.mx/collections/playera-chavas-mexico',
        'https://aditivo.mx/collections/playera-chavos-mexico'
    ]
    allowed_domains = ['aditivo.mx']
    base_url = 'https://aditivo.mx'

    def __init__(self):
        self.driver = webdriver.Chrome()

    def parse(self, response):
        products = response.css('div.ci > a')
        for product in products:
            product_link = product.css('::attr(href)').get()
            yield response.follow('{}{}'.format(self.base_url, product_link), callback=self.parse_product)
        next_link = response.css(
            '#pagination > a:last-child::attr(href)').get()
        next_link_text = response.css(
            '#pagination > a:last-child::text').get()
        if next_link and next_link_text == '>':
            yield response.follow('{}{}'.format(self.base_url, next_link), callback=self.parse)

    def parse_product(self, response):
        self.driver.get(response.url)
        self.driver.implicitly_wait(1)
        yield dict(
            title=self.driver.find_element_by_xpath('//div[1]/h1').text,
            price=response.css('#product-price > span::text').get(),
            sku=self.driver.find_element_by_css_selector(
                'span.variant-sku').text,
            material=response.css(
                '#product-description > div.rte > p:nth-child(1)::text').get()
        )
