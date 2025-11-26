import scrapy


from scrapy.spiders import SitemapSpider

class PnpCategorySpider(SitemapSpider):
    name = "pnp"
    sitemap_urls = ["https://www.pnp.co.za/sitemap.xml"]
    sitemap_follow = ["/https://cdn-prd-02.pnp.co.za/sys-master/root/hfe/hf0/29407478153246/CATEGORY-en-ZAR-14475868262960441156.xml"]

    def parse(self, response):
        yield {"category_url": response.url}
