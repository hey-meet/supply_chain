from backend.models.search import NewsCollection
from backend.services.search_service import search_service


def test_search_logistics_news():
    response = search_service.search_logistics_news()
    assert isinstance(response, NewsCollection)


def test_search_supply_chain_news():
    response = search_service.search_supply_chain_news()
    assert isinstance(response, NewsCollection)


def test_search_weather_news():
    response = search_service.search_weather_news()
    assert isinstance(response, NewsCollection)


def test_search_commodity_news():
    response = search_service.search_commodity_news()
    assert isinstance(response, NewsCollection)