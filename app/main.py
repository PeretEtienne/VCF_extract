import pprint
from typing import TypedDict

from fastapi import FastAPI

import vcf

app = FastAPI()


class HomeResponse(TypedDict):
    Hello: str


@app.get("/")
def read_root() -> HomeResponse:
    test = "hey"
    print(test)
    uppercased = test.upper()

    return {"Hello": uppercased}


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
