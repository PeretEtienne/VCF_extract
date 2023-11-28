import typing as t

from fastapi import HTTPException
from pydantic import BaseModel

from app.core.utils import logger

if t.TYPE_CHECKING:
    from vcf.model import Record

import traceback


class Variation(BaseModel):
    chrom: str
    pos: int
    vardb_id: str
    gene: t.Optional[str] = None
    category: t.Optional[str] = None
    cdna: t.Optional[str] = None
    aa: t.Optional[str] = None
    frequency: t.Optional[float] = None
    depth: t.Optional[int] = None

    def __init__(self, record: "Record"):
        result = {
            "chrom": record.CHROM,
            "pos": record.POS,
            "vardb_id": record.ID,
        }

        try:
            if (
                record.INFO.get("GENE")
                and isinstance(record.INFO.get("GENE"), list)
                and len(record.INFO["GENE"])
            ):
                result["gene"] = record.INFO["GENE"][0]

            if record.INFO.get("TYPE"):
                result["category"] = record.INFO["TYPE"]

            if record.INFO.get("Transcript") and record.INFO.get("MUT_cDNA"):
                result[
                    "cdna"
                ] = f"{record.INFO["Transcript"][0]}:{record.INFO["MUT_cDNA"][0]}"

            if record.INFO.get("MUT_AA"):
                result["aa"] = record.INFO["MUT_AA"][0]

            if len(record.samples):
                result["frequency"] = record.samples[0].data.VF
                result["depth"] = record.samples[0].data.DP
        except Exception as e:
            logger.error(traceback.format_exc())
            raise HTTPException(status_code=500, detail=str(e)) from e

        super().__init__(**result)
