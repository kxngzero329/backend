import scrapy
from scrapy.http import HtmlResponse

class PnpSpider(scrapy.Spider):
    name = "pnp"

    # sitemap with all categories
    sitemap_url = "https://cdn-prd-02.pnp.co.za/sys-master/root/hfe/hf0/29407478153246/CATEGORY-en-ZAR-14475868262960441156.xml"

    def start_requests(self):
        # start by requesting the sitemap
        yield scrapy.Request(self.sitemap_url, callback=self.parse_sitemap)

    def parse_sitemap(self, response):
        # extract all category URLs
        category_urls = response.xpath("//url/loc/text()").getall()
        for url in category_urls:
            yield scrapy.Request(
                url,
                meta={"playwright": True, "playwright_include_page": True},
                callback=self.parse_category
            )

    async def parse_category(self, response):
        page = response.meta["playwright_page"]

        # wait for the products to load
        await page.wait_for_selector("div.product-grid-item")
        html = await page.content()
        await page.close()

        # create new response with fully rendered HTML
        response = HtmlResponse(
            url=response.url,
            body=html,
            encoding="utf-8",
            request=response.request
        )

        # extract products
        for p in response.css("div.product-grid-item"):
            yield {
                "id": p.attrib.get("data-cnstrc-item-id"),
                "name": p.attrib.get("data-cnstrc-item-name"),
                "price": p.attrib.get("data-cnstrc-item-price"),
                "old_price": p.css("div.price.price_promo span.old::text").get(),
                "link": f"https://www.pnp.co.za{p.css('a.product-grid-item__image-container::attr(href)').get()}",
                "image": p.css("cx-media picture img::attr(src)").get(),
            }

        # pagination (if exists)
        next_page = response.css("a.pagination-next::attr(href)").get()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                meta={"playwright": True, "playwright_include_page": True},
                callback=self.parse_category
            )
