#project 
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from binaz.items import HouseItem
from scrapy.http.request import Request
import json


class Binaaz(CrawlSpider):
    name = "binaz"
    page_count = 0
    ev_count = 1
    page = 1
    start_urls = [
        f"https://bina.az/alqi-satqi/menziller?page={i}" for i in range(1, 51)
    ]

    rules = (
        Rule(LinkExtractor(restrict_css='.slider_controls'), callback="parse_house"),
         Rule(LinkExtractor(restrict_css='span.next' ),follow=True)

    )

    def parse_house(self, response):

        house_item = HouseItem()

        house_item["evin_url"] = response.url
        house_item["ev_qiy"] = response.xpath('/html/body/div[3]/section/div/div[4]/div[2]/div/aside/div/div[1]/div[1]/div[1]/span[1]/text()').extract_first()
        house_item["ev_kur"] = response.xpath('/html/body/div[3]/section/div/div[4]/div[2]/div/aside/div/div[1]/div[1]/div[1]/span[2]/text()').extract_first()
        house_item["ev_kvm_degeri"] = response.xpath('/html/body/div[3]/section/div/div[4]/div[2]/div/aside/div/div[1]/div[1]/div[2]/text()').extract_first()
        house_item["kategoriya"] = response.css("span.product-properties__i-value::text")[0].extract() #response.xpath('/html/body/div[3]/section/div/div[4]/div[2]/div/main/section[3]/div/div/div[1]/span/text()').extract_first()
        house_item["mertebe"] = response.css("span.product-properties__i-value::text")[1].extract() #response.xpath('/html/body/div[3]/section/div/div[4]/div[2]/div/main/section[3]/div/div/div[2]/span/text()').extract_first()
        house_item["kvm"] = response.css("span.product-properties__i-value::text")[2].extract()#response.xpath('/html/body/div[3]/section/div/div[4]/div[2]/div/main/section[3]/div/div/div[3]/span/text()').extract_first()
        house_item["otaq"] = response.css("span.product-properties__i-value::text")[3].extract()#response.xpath('/html/body/div[3]/section/div/div[4]/div[2]/div/main/section[3]/div/div/div[4]/span/text()').extract_first()
        house_item["kupca"] = response.css("span.product-properties__i-value::text")[4].extract()#response.xpath('/html/body/div[3]/section/div/div[4]/div[2]/div/main/section[3]/div/div/div[5]/span/text()').extract_first()
        house_item["temir"] = response.css("span.product-properties__i-value::text")[5].extract()#response.xpath('/html/body/div[3]/section/div/div[4]/div[2]/div/main/section[3]/div/div/div[6]/span/text()').extract_first()
        house_item["ev_qeyd"] = response.xpath('/html/body/div[3]/section/div/div[4]/div[2]/div/main/section[4]/div/div/p/text()').extract()
        house_item["vasiteci_ad"] = response.css("div.product-owner__info-name::text , div.product-owner__residence-info-name::text").extract() #response.xpath('/html/body/div[3]/section/div/div[4]/div[2]/div/aside/div/div[1]/div[3]/div[1]/div[1]/div[1]/text() | /html/body/div[3]/section/div/div[4]/div[2]/div/aside/div/div[1]/div[4]/div[1]/div/a/div/div[1]/text()').extract()
        house_item['vasiteci_tipi'] =response.css("div.product-owner__info-region::text , div.product-owner__residence-info-region::text").extract()
        house_item["emlak_agentliyi"] =response.css("div.product-shop__owner-name::text").extract()
        phone_url = response.url + "/phones"
        yield Request(phone_url, callback=self.parse_phone, meta={'house_item': house_item})



    def parse_phone(self, response):
        house_item = response.meta['house_item']


        try:
            json_data = json.loads(response.body)
            phones = json_data.get('phones', [])
            phone_number = ", ".join(phones)
        except json.JSONDecodeError:
            phone_number = ''

        house_item["phones"] = phone_number

        yield house_item


