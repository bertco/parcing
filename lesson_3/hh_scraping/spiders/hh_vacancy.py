# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse

class HhVacancySpider(scrapy.Spider):
    name = 'hh_vacancy'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=1&st=searchVacancy&text=Data+scientist&from=suggest_post']

    def parse(self, response: HtmlResponse):
        pagination = response.css(
            'a.bloko-button.HH-Pager-Controls-Next.HH-Pager-Control'
        ).attrib

        next_link = pagination.get('href')
        if next_link is not None:
            yield response.follow(next_link, callback=self.parse)

        vacancy_pages = response.css(
            'div.vacancy-serp a.bloko-link.HH-LinkModifier::attr(href)'
        ).extract()

        for i in vacancy_pages:
            yield response.follow(i, callback=self.parse_vacancy_page)

    def parse_vacancy_page(self, response: HtmlResponse):
        title = response.css(
            'h1.header span.highlighted::text'
        ).extract()

        company_name = response.css(
            'a.vacancy-company-name span::text'
        ).extract_first()

        company_link = response.css(
            'a.vacancy-company-name::attr(href)'
        ).extract_first().split('?')[0]

        key_skills = response.css(
            'div.vacancy-section span.bloko-tag__section.bloko-tag__section_text::attr(title)'
        ).extract()

        salary = response.css(
            'div.vacancy-title p.vacancy-salary::text'
        ).extract_first()

        item = {
            'title': title,
            'company name': company_name,
            'hh url': company_link,
            'key skills': key_skills,
            'salary': salary
        }

        yield response.follow(company_link, callback=self.parse_company_page, cb_kwargs={'item': item})

    def parse_company_page(self, response: HtmlResponse, item):
        item['company_url'] = response.css(
            'div.HH-SidebarView-UrlContainer a.company-url::attr(href)'
        ).extract_first()

        yield item

