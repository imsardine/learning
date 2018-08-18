from .matchers import *

def test_hello_world(shell):
    shell.src('index.html', """
    <html>
      <h1>Hello, World!</h1>
      <a href="next.html">Next</a>
    </html>
    """)

    shell.src('next.html', """
    <html>
      <h1>Hello, Scrapy!</h1>
    </html>
    """)

    shell.src('myspider.py', """
    import scrapy

    class MySpider(scrapy.Spider):
        name = 'myspider'
        start_urls = ['http://localhost:8000']

        def parse(self, response):
            yield {'title': response.css('h1 ::text').extract_first()}

            for next_page in response.css('a'):
                yield response.follow(next_page, self.parse)
    """)

    with shell.spawn('python -m SimpleHTTPServer 8000'):
        r = shell.run('scrapy runspider myspider.py')
        assert r.err == like("""
        ... INFO: Scrapy 1.5.1 started (bot: scrapybot)
        ... INFO: Enabled extensions:
        ... INFO: Enabled downloader middlewares:
        ... INFO: Enabled spider middlewares:
        ... INFO: Enabled item pipelines:
        ... INFO: Spider opened
        ... DEBUG: Crawled (200) <GET http://localhost:8000> (referer: None)
        ... DEBUG: Scraped from <200 http://localhost:8000>
        {'title': u'Hello, World!'}
        ... DEBUG: Crawled (200) <GET http://localhost:8000/next.html> (referer: http://localhost:8000)
        ... DEBUG: Scraped from <200 http://localhost:8000/next.html>
        {'title': u'Hello, Scrapy!'}
        ... INFO: Closing spider (finished)
        ... INFO: Dumping Scrapy stats:
        ... INFO: Spider closed (finished)
        """)

