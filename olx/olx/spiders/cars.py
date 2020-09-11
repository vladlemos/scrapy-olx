# -*- coding: utf-8 -*-
import scrapy


class CarsSpider(scrapy.Spider):
    name = 'cars'
    # allowed_domains = ['https://sp.olx.com.br']
    start_urls = ['https://pe.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios']

    # allowed_domains ='pe.olx.com.br'

    def parse(self, response):
       
        items = response.xpath('//ul[@id="ad-list"]/li')
       
        # self.log(len(items))
        for item in items:

            url = item.xpath('./a/@href').extract_first()

            if url is not None:             
                yield scrapy.Request(url=url, callback=self.parse_detail)
            
        next_page = response.xpath('//a[@data-lurker-detail="next_page"]/@href')

        if next_page:
            # apenas para mostrar em qual página está 
            self.log("### PAGINA DE PESQUISA: {}".format(next_page.extract_first()))
            
            yield scrapy.Request(
                url=next_page.extract_first(), 
                callback=self.parse
                )

           
    
    
    def parse_detail(self, response):
        # self.log(response.url)  
        title   = response.xpath('//title/text()').extract_first
        year    = response.xpath('//span[contains(text(), "Ano")]/following-sibling::a/text()').extract_first()
        fuel    = response.xpath('//span[contains(text(), "Combustível")]/following-sibling::a/text()').extract_first()
        doors   = response.xpath('//span[contains(text(),"Portas")]/following-sibling::span/text()').extract_first()

        yield {
            'title' : title,
            'year'  : year,
            'fuel'  : fuel,
            'doors' : doors,
        }

