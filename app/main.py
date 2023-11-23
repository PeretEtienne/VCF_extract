import io
import logging

from elasticsearch import AsyncElasticsearch, helpers
from fastapi import FastAPI, UploadFile
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

import vcf

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    ELASTICSEARCH_URL: str = Field(default=...)
    ELASTICSEARCH_USER: str = Field(default=...)
    ELASTICSEARCH_PASSWORD: str = Field(default=...)

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()


def get_es():
    return AsyncElasticsearch(
        settings.ELASTICSEARCH_URL,
        basic_auth=(settings.ELASTICSEARCH_USER, settings.ELASTICSEARCH_PASSWORD),
        verify_certs=False,
    )


@app.post(path="/extract")
async def extract_variations(file: UploadFile):
    file_content = await file.read()
    vcf_reader = vcf.Reader(io.TextIOWrapper(io.BytesIO(file_content)))
    variations = list(vcf_reader)

    es = get_es()

    documents = [
        {
            "chrom": v.CHROM,
            "pos": v.POS,
            "id": v.ID,
        }
        for v in variations
    ]

    result = await helpers.async_bulk(es, documents, index="variations")

    return result


@app.get("/search")
async def get_variations():
    es = get_es()

    result = await es.search(index="variations", query={"match_all": {}})
    return result


@app.delete(path="/variations")
async def delete_variations():
    es = get_es()

    result = await es.delete_by_query(index="variations", query={"match_all": {}})
    return result
