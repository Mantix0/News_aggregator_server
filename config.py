
site_list = [
    {
        'name': 'StopGame',
        'logo': "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSs_O4gVAl9IAWuaOO8nJYvqJC1ogQzuvJYxedIL1bXEw&s",
        'link': 'https://rss.stopgame.ru/rss_news.xml',
        'content_selector': '#main-content > section._page-section_1jnog_471._section_12po9_6._content-section_12po9_13 > div._content_12po9_13',
        'tags_selector': '#main-content > section._page-section_1jnog_471._section_12po9_6._content-section_12po9_13 > div:nth-child(4) > div._tags_12po9_1558 > div',

        'additional_tags': ['Игры и киберспорт'],
        'delete_tags': ["span_icon"],
    },
    # {
    #     'name': 'RiaNews',
    #     'logo': "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSs_O4gVAl9IAWuaOO8nJYvqJC1ogQzuvJYxedIL1bXEw&s",
    #     'link': 'https://ria.ru/export/rss2/archive/index.xml',
    #     'content_selector': '#endless > div.endless__item.m-active > div > div > div > div.layout-article__over > div.layout-article__main > div > div:nth-child(1) > div.article__body.js-mediator-article.mia-analytics'
    # }
    {
        'name': 'Ведомости',
        'logo': "https://yandex.ru/images/search?img_url=https%3A%2F%2Feng.magram.ru%2Fupload%2Fiblock%2F5c5%2F5c5c585d19b82ed8af335d1235bb571e.jpg&pos=9&rpt=simage&text=vedomosti%20logo",
        'link': 'https://www.vedomosti.ru/rss/rubric/technology.xml',
        'content_selector': '#app > div.layout > div.layout__wrapper.full-width > div.layout__container--transformed.layout__container > div.layout__page > div > div > div:nth-child(1) > div > div.article__container > div > div > div > div:nth-child(2)',
        'additional_tags': ['Технологии'],
        'delete_tags': ["article-boxes-list__item"],
    },
]