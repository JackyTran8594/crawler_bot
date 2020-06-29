from django.core.management.base import BaseCommand
from crawler_bot.spiders import alibaba_smartswitch, amazon_smartswitch, surveillance_video, tiki_product
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class Command(BaseCommand):
    help = "Release the spiders"

    def handle(self, *args, **options):
        process = CrawlerProcess(get_project_settings())
        process.crawl(alibaba_smartswitch)
        process.start()