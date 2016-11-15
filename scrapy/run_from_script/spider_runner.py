# -*- coding: utf-8 -*-
"""
***********************************************************************************************************************
                                                spider_runner.py

Class wrapper that adds the following functionality:

A spider can be run from a script using the scrapy.crawler.CrawlerRunner class. As their docummentation says,
you need to control the Twisted Reactor bu your own. It's useful to use it instead of spider_process if you can't allow 
different handlers on shutdown situations, as the install_shutdown_handlers function is not used.
Every crawl is executed in a different thread.
Doesn't mather were the class is instantiated, as long as the run() method is used inside the desired script.

***********************************************************************************************************************
"""

from multiprocessing import Process
import scrapy
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner

class SpiderRunner(object):

    def _crawl(self, **kwargs):
        spider = kwargs.pop('spider')
        self.crawler = CrawlerRunner()

        self.crawler.crawl(spider, **kwargs)
        d = self.crawler.join()
        d.addBoth(lambda _: reactor.stop())
        reactor.run()

    def run(self, spider, **kwargs):
        kwargs['spider'] = spider
        p = Process(target=self._crawl, kwargs=kwargs)
        p.start()
        p.join()
