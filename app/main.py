import pprint
import time

from elasticsearch import AsyncElasticsearch, helpers
from fastapi import FastAPI
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

import vcf

app = FastAPI()


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


@app.get(path="/")
async def read_root():
    with open("vcf/KDM39442_59040_492838_467052_base_sort.vcf") as f:
        vcf_reader = vcf.Reader(f)
        variations = list(vcf_reader)

        es = get_es()

        start = time.time()
        documents = [
            {
                "chrom": v.CHROM,
                "pos": v.POS,
                "id": v.ID,
            }
            for v in variations
        ]
        end_list = time.time() - start

        print("end_list", end_list)

        start = time.time()
        result = await helpers.async_bulk(es, documents, index="variations")
        print("end_bulk", time.time() - start)

        print(result)
        return result


@app.get("/search")
async def get_variations():
    es = get_es()

    result = await es.search(index="variations", query={"match_all": {}})
    return result


@app.get("/delete")
async def delete_variations():
    es = get_es()

    result = await es.delete_by_query(index="variations", query={"match_all": {}})
    return result


@app.get("/vcf")
def read_vcf():
    with open("vcf/KDM39442_59040_492838_467052_base_sort.vcf") as f:
        vcf_reader = vcf.Reader(f)

        variants = list(vcf_reader)

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(vars(variants[0]))

        pp.pprint(vars(variants[5]))

        # print("first variant:", variants[0].samples)
        # print("11 variant", variants[10].samples)

        # variant = variants[5]
        # print("CHROM", variant.CHROM)
        # print("POS", variant.POS)
        # print("ID", variant.ID)
        # print("REF", variant.REF)
        # print("ALT", variant.ALT)
        # print("QUAL", variant.QUAL)
        # print("FILTER", variant.FILTER)
        # print("INFO", variant.INFO)
        # print("FORMAT", variant.FORMAT)
        # print("samples", variant.samples)
        # print("Gene : ", variant.INFO["GENE"])

        # all_types = [v.INFO["TYPE"] for v in variants]
        # unique_types = set(all_types)

        # print("all_types", unique_types)

        # print("frequency", variants[0].samples[0].data.VF)
        # print(len(variants))

        return "test"
