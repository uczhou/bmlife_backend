# -*- coding: utf-8 -*-

# Scrapy settings for bmlife_bot project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Googlebot'

SPIDER_MODULES = ['bmlife_bot.spiders']
NEWSPIDER_MODULE = 'bmlife_bot.spiders'

ROBOTSTXT_OBEY = False

FILES_STORE = ''

# Configure item pipelines
ITEM_PIPELINES = {
    'bmlife_bot.pipelines.BmlifeImageDownloaderPipeline': 100,
    'bmlife_bot.pipelines.BmlifeBotPipeline': 200
}

# DOWNLOADER_MIDDLEWARES = {
#     'bmlife_bot.middlewares.BmlifeDownloaderMiddleware': 100
# }

DOWNLOAD_TIMEOUT = 60

IMAGES_STORE = ''
IMAGES_STORE_S3_ACL = 'public-read'

LOG_LEVEL = 'ERROR'
MEDIA_ALLOW_REDIRECTS = True

IMAGES_THUMBS = {
    'small': (50, 50),
    'big': (270, 270),
}
