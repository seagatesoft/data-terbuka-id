# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item
from scrapy.loader import ItemLoader
from scrapylib.processors import default_input_processor, default_output_processor


class MasjidItem(Item):
    id_masjid = Field()
    nama_masjid = Field()
    link_detail = Field()
    kabupaten_kota = Field()
    kecamatan = Field()
    tipologi = Field()
    alamat = Field()
    luas_tanah = Field()
    status_tanah = Field()
    luas_bangunan = Field()
    tahun_berdiri = Field()
    jamaah = Field()
    imam = Field()
    khatib = Field()
    muazin = Field()
    remaja = Field()
    no_telepon = Field()
    keterangan = Field()
    longitute = Field()
    latitude = Field()


class MasjidItemLoader(ItemLoader):
    default_item_class = MasjidItem
    default_input_processor = default_input_processor
    default_output_processor = default_output_processor
