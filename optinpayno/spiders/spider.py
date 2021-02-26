import scrapy

from scrapy.loader import ItemLoader
from ..items import OptinpaynoItem
from itemloaders.processors import TakeFirst


class OptinpaynoSpider(scrapy.Spider):
	name = 'optinpayno'
	start_urls = ['https://www.optinpay.no/blogg']

	def parse(self, response):
		post_links = response.xpath('//div[@class="post-header padding-all-over"]')
		for post in post_links:
			url = post.xpath('./h2/a/@href').get()
			date = post.xpath('./ul/li/span[@class="date-row"]/text()').get()
			yield response.follow(url, self.parse_post, cb_kwargs={'date':date})

	def parse_post(self, response, date):
		title = response.xpath('//h1/span/text()').get()
		description = response.xpath('//div[@class="section post-body"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=OptinpaynoItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
