# -*- coding: utf-8 -*-
"""
***********************************************************************************************************************
                                                spider_process.py
Class wrapper that adds the following functionality:
A spider can be run from a script using the scrapy.crawler.CrawlerProcess class. As their docummentation says,
the class inherits from CrawlerRunner, and adds support for starting a Twisted `reactor`_ and handling shutdown signals,
like the keyboard interrupt command Ctrl-C. It also configures top-level logging.
It's useful to use it instead of spider_runner if you don't care about different handlers on shutdown situations,
as the install_shutdown_handlers function is used. This is the best option if the spider that is being run from a script 
is not inside a daemon, as it can mess the shutdown of both.
Every crawl is executed in a different thread.
***********************************************************************************************************************
"""

from multiprocessing import Process
import scrapy
from scrapy.crawler import CrawlerProcess

class SpiderProcess(object):
	
	def __init__(self):
		self.process = CrawlerProcess()
		
    def _crawl(self, **kwargs):
        spider = kwargs.pop('spider')
        self.crawler.crawl(spider, **kwargs)
        self.crawler.start()
		self.crawler.stop()

    def run(self, spider, **kwargs):
        kwargs['spider'] = spider
        p = Process(target=self._crawl, kwargs=kwargs)
        p.start()
        p.join()       
