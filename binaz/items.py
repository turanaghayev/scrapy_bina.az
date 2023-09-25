# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


from scrapy import Item, Field


class HouseItem(Item):
    evin_url = Field()
    ev_qiy = Field()
    ev_kur = Field()
    ev_kvm_degeri = Field()
    kategoriya = Field()
    mertebe = Field()
    kvm = Field()
    otaq = Field()
    kupca = Field()
    temir = Field()
    ev_qeyd = Field()
    vasiteci_ad = Field()
    vasiteci_tipi = Field()
  #  company=Field()
    phones= Field()
    emlak_agentliyi = Field()