import io

from elasticsearch import helpers
from fastapi import FastAPI, UploadFile
from pydantic import ValidationError

import vcf
from app.core.es import get_es
from app.schemas.variation import Variation

app = FastAPI(debug=True)


@app.post(path="/extract")
async def extract_variations(file: UploadFile):
    file_content = await file.read()
    vcf_reader = vcf.Reader(io.TextIOWrapper(io.BytesIO(file_content)))
    variations = list(vcf_reader)

    es = get_es()

    documents = []
    try:
        documents = [Variation(v).model_dump() for v in variations]
    except ValidationError as e:
        return {"errors": e.errors()}

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
