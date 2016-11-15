# -*- coding: utf-8 -*-
"""
***********************************************************************************************************************
                                                proxy_middleware.py

It contains the scrapy middleware that alters the requests,
adding a proxy that gets its settings from a ConfigParser instance.

The ConfigParser instance must be like this:
[proxy_config]
user = proxy_user
pass = proxy_pass
address = http://proxy.addres.com
port = proxy_port

Proper use should be the following:
The spider receives a parameter with the config.cfg path, in the constructor it instantiates ConfigParser, 
and uses readfp(open(path)). The results are added to self.conf variable.

The middleware can be added in two different ways. 
-If the spider is inside a scrapy project, it should be listed on the 
settings.py file under the DOWNLOADER_MIDDLEWARES dictionary.
DOWNLOADER_MIDDLEWARES = {
    'project_name.pipelines.CustomProxyMiddleware': 100,
}
-If the spider is run without a project, either with scrapy runspider name.py or from script, it has to add it before 
the constructor, using the custom_settings dictionary, like any other thing such as User Agents.
custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {CustomProxyMiddleware.__module__ + '.' +CustomProxyMiddleware.__name__:100},
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    }

***********************************************************************************************************************
"""

class CustomProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta['proxy'] = '%s:%s' % (spider.conf.get('proxy_config', 'address'),
                                           spider.conf.get('proxy_config', 'port'))
        request.headers['Proxy-Authorization'] = 'Basic ' + \
                                                 base64.b64encode('%s:%s' % (spider.conf.get('proxy_config', 'user'),
                                                                             spider.conf.get('proxy_config', 'pass')))
