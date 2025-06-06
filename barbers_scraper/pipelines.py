# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BarbersScraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        price_string = adapter.get("price")
        adapter["price"] = float(price_string.replace(",", "").replace("\xa0", ""))

        return item
