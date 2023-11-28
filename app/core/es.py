from elasticsearch import AsyncElasticsearch

from app.core.settings import settings


def get_es():
    return AsyncElasticsearch(
        settings.ELASTICSEARCH_URL,
        basic_auth=(settings.ELASTICSEARCH_USER, settings.ELASTICSEARCH_PASSWORD),
        verify_certs=False,
    )
