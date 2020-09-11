# -*- coding: utf-8 -*-
import scrapy


class ImoveiscaixaSpider(scrapy.Spider):
    name = 'imoveiscaixa'
    # allowed_domains = ['venda-imoveis.caixa.gov.br/listaweb/Lista_imoveis_SP.htm']
    start_urls = ['http://venda-imoveis.caixa.gov.br/listaweb/Lista_imoveis_SP.htm']

    def parse(self, response):
        
        links       = response.xpath('//a[contains(text(), "Detalhes")]')
        modalidades  = response.xpath('//table//tr/td[8]')[1:]

        for link, modalidade in zip(links, modalidades):

            link        = link.xpath('./@href').extract_first()
            modalidade  = modalidade.xpath('.//span/text()').extract_first()

            if modalidade.strip() == '2º Leilão SFI':
                print(link)


     

        # preciso saber a modalidade e pular a primeira linha de cabeçalho 
        # as páginas as vezes tem elementos e as vezes não... e varia de acordo com a modalidade; 



        # for item in links:
        #     link = item.xpath('./@href').extract_first()
        #     url = link.strip()
        #     # print(url)

            # if url is not None:             
            #     yield scrapy.Request(url=url, callback=self.parse_detail)
    
    def parse_detail(self, response):

        titulo          = response.xpath('//h5/text()').extract_first()
        valor_venda     = response.xpath('//h4/text()')[0].get()
        avaliacao       = response.xpath('//h4/text()')[1].get()

        yield {
            'titulo': titulo,
            'valor_venda': valor_venda,
            'avaliacao': avaliacao
        }

