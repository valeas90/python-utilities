# -*- coding: utf-8 -*-
"""
***********************************************************************************************************************
                                                save_screenshot.py

It contains the function that allows to capture the screen into an image.

***********************************************************************************************************************
"""

import os
from selenium import webdriver
from selenium.webdriver import *
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from PIL import Image

def save():
	path_to_image = '/my/path/'
	logging_path = 'project/logs'
	phantom_config_file = 'project/etc/phantomjs.json'
	url_to_save = 'http://www.google.es'
	capabilities=DesiredCapabilities.PHANTOMJS.copy()
	driver = webdriver.PhantomJS(desired_capabilities=capabilities,
								 service_log_path=os.path.join(logging_path, 'ghostdriver.log'),
								 service_args=['--ssl-protocol=any',
											   '--config=%s' % os.path.join(phantom_config_file)])
	driver.set_window_size(1280, 1024)
	driver.get(url_to_save)

	path_to_image_big = path_to_image.replace('.png', '_BIG.png')
	driver.save_screenshot(path_to_image_big)

	im = Image.open(path_to_image_big)
	region = im.crop((100,120,1200,700))
	region.save(path_to_image, "PNG")

	driver.quit()
