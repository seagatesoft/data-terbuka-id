from scrapy import Request, Spider

from data_terbuka_id.items import MasjidItemLoader


class SimasKemenagGoIdSpider(Spider):
    name = 'simas.kemenag.go.id'
    allowed_domains = ['kemenag.go.id']
    start_urls = ['http://simas.kemenag.go.id/index.php/profil/masjid/']
    url_template = 'http://simas.kemenag.go.id/index.php/profil/masjid/page/{offset}'

    def parse(self, response):
        for item in self.parse_items(response):
            yield item

        if not response.meta.get('pagination', False):
            for req in self.request_all_pages(response):
                yield req

    def parse_items(self, response):
        for i, sel in enumerate(response.xpath("//*[@id='the-list']/tr[./td]")):
            mil = MasjidItemLoader(selector=sel)
            mil.add_xpath('id_masjid', "./td[5]/text()")
            mil.add_xpath('nama_masjid', "./td[4]/a/text()")
            mil.add_xpath('link_detail', "./td[4]/a/@href")
            mil.add_xpath('kabupaten_kota', "./td[2]/text()")
            mil.add_xpath('kecamatan', "./td[3]/text()")
            mil.add_xpath('tipologi', "./td[6]/text()")
            mil.add_xpath('alamat', "./td[7]/text()")
            mil.add_xpath('luas_tanah', "./td[8]/text()")
            mil.add_xpath('status_tanah', "./td[9]/text()")
            mil.add_xpath('luas_bangunan', "./td[10]/text()")
            mil.add_xpath('tahun_berdiri', "./td[11]/text()")
            mil.add_xpath('jamaah', "./td[12]/text()")
            mil.add_xpath('imam', "./td[13]/text()")
            mil.add_xpath('khatib', "./td[14]/text()")
            mil.add_xpath('muazin', "./td[15]/text()")
            mil.add_xpath('remaja', "./td[16]/text()")
            mil.add_xpath('no_telepon', "./td[17]/text()")
            mil.add_xpath('keterangan', "./td[18]/text()")

            long_lat = sel.xpath("./comment()[2]").re(r'align="center">(-?[0-9.]+)</')

            try:
                mil.add_value('longitude', long_lat[0])
                mil.add_value('latitude', long_lat[1])
            except IndexError:
                self.logger.error(
                    "Can't get long-lat on %(url)s , element index = %(index)s",
                    {"url": response.url, "index": i},
                )
                from scrapy.shell import inspect_response
                inspect_response(response, self)

            yield mil.load_item()

    def request_all_pages(self, response):
        second_page_offset = response.xpath(
            "//div[has-class('paging')]/a[1]/@href"
        ).re(r'/page/(\d+)')

        if not second_page_offset:
            self.logger.error("Can't find second page offset on %(url)s", {"url": response.url})
            return

        last_page_offset = response.xpath(
            "//div[has-class('paging')]/a[contains(., 'Last')]/@href"
        ).re(r'/page/(\d+)')

        if not last_page_offset:
            self.logger.error("Can't find last page offset on %(url)s", {"url": response.url})
            return

        try:
            second_page_offset = int(second_page_offset[0])
            last_page_offset = int(last_page_offset[0])
        except ValueError:
            self.logger.error("Error when getting offsets on %(url)s", {"url": response.url})
            return

        offset, increment = second_page_offset, second_page_offset

        while offset <= last_page_offset:
            yield Request(
                self.url_template.format(offset=str(offset)),
                meta={'pagination': True, 'offset': offset},
                callback=self.parse_items,
            )
            offset += increment
