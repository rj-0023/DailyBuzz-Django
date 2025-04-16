
def apii():
    from newsapi import NewsApiClient

    # Init
    news_api = NewsApiClient(api_key='6700bcdf33c04aa5aebd2c7e870df3e3')

    # /v2/top-headlines
    top_headlines = news_api.get_top_headlines(q='market',
                                            category='business',
                                            language='en',
                                            country='us')

    # # /v2/everything
    # all_articles = news_api.get_everything(q='bitcoin',
    #                                     from_param='2025-04-01',
    #                                     to='2025-04-14',
    #                                     language='en',
    #                                     sort_by='relevancy',
    #                                     page=2)

    # /v2/top-headlines/sources
    # sources = news_api.get_sources()
    print(top_headlines["articles"])
    return(top_headlines)

apii()