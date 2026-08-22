#!/usr/bin/env python3

import base64
from io import BytesIO

import pytest
from PyPDF2 import PdfReader, PdfWriter

import pdfUtilsServer


@pytest.fixture
def make_pdf():
    def create_pdf(page_count):
        writer = PdfWriter()
        for _ in range(page_count):
            writer.add_blank_page(width=72, height=72)
        output = BytesIO()
        writer.write(output)
        return output.getvalue()

    return create_pdf


def test_base64_helpers_round_trip(make_pdf):
    pdf_bytes = make_pdf(1)

    encoded = pdfUtilsServer._b64Encode(pdf_bytes)

    assert pdfUtilsServer._b64Decode(encoded) == pdf_bytes


def test_merge_pdf_combines_all_pages(make_pdf):
    first_pdf = base64.b64encode(make_pdf(1)).decode("ascii")
    second_pdf = base64.b64encode(make_pdf(2)).decode("ascii")

    result = pdfUtilsServer.mergePdf(
        [{"pdf": first_pdf}, {"pdf": second_pdf}]
    )
    merged_result = result._value.result
    merged_pdf = base64.b64decode(merged_result["PDFFinal"])

    assert merged_result["estado"] == "OK"
    assert len(PdfReader(BytesIO(merged_pdf)).pages) == 3


def test_merge_pdf_without_documents_reports_invalid_input():
    with pytest.raises(TypeError):
        pdfUtilsServer.mergePdf([])
