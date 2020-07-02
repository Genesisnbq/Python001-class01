# Scrapy settings for maoyan_scrapy_xpath project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'maoyan_scrapy_xpath'

SPIDER_MODULES = ['maoyan_scrapy_xpath.spiders']
NEWSPIDER_MODULE = 'maoyan_scrapy_xpath.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'maoyan_scrapy_xpath (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'Host': 'maoyan.com',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cookie': '__mta=142391181.1593291039315.1593620523153.1593621068534.36; uuid_n_v=v1; '
              'uuid=DB5A5E00B8B711EA8A833903D31672830D67A9B14A884D14BA873711FA60C96A; '
              '_lxsdk_cuid=172f78bdffc72-0e8930ceabf6f6-4353760-144000-172f78bdffdc8; '
              '_lxsdk=DB5A5E00B8B711EA8A833903D31672830D67A9B14A884D14BA873711FA60C96A; '
              'mojo-uuid=8ae196871f15954ff9f1914dbf9e67fb; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; '
              '_csrf=1459910ea9e2827735bceb3899a35eeef1b9186c297bcbbffb8c205af06c03c9; mojo-session-id={'
              '"id":"9af1eefe6d2e6e8e2bb2f027846d60d8","time":1593628341769}; '
              'lt=kqOeLYZPqN8BO500cITbZArQylcAAAAAAwsAAFLgn5r8PChs7X53KhW0EblXSBu6N4phDIEXpL1q0SBdGNFk49fpsjFtq94l2kQDAA; lt.sig=RcLesAV2u3rVE5J7XHYs_Ece_5o; mojo-trace-id=3; __mta=142391181.1593291039315.1593621068534.1593628361012.37; _lxsdk_s=1730b84cd8d-3b5-0da-8da%7C1765851443%7C15 '
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'maoyan_scrapy_xpath.middlewares.MaoyanScrapyXpathSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'maoyan_scrapy_xpath.middlewares.MaoyanScrapyXpathDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'maoyan_scrapy_xpath.pipelines.MaoyanScrapyXpathPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
