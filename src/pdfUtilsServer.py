#!/usr/bin/env python3

# -*- coding: utf-8 -*-

from jsonrpcserver import Success, method, serve, InvalidParams, Result, Error
import re

import base64
from PyPDF2 import PdfMerger
from io import StringIO
from io import BytesIO


def _b64Decode(b64String):
    base64_bytes = b64String.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    #message = message_bytes.decode('ascii')
    #return message
    return message_bytes

def _b64Encode(message_bytes):
    #message_bytes = string.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message

@method
def mergePdf( lista_b64Pdfs = [] ) -> Result:

    tamano = len(lista_b64Pdfs)
    if tamano == 0:
        return Error("error en parámetros")
    
    merger = PdfMerger()
    
    for b64Pdf in lista_b64Pdfs:
        bytesPdf = _b64Decode(b64Pdf["pdf"])
       # streamPdf = StringIO(bytesPdf)
        streamPdf = BytesIO(bytesPdf)
        merger.append(streamPdf)

    #stream_pdf_Final = StringIO()
    stream_pdf_Final = BytesIO()
    merger.write(stream_pdf_Final)
    merger.close()
    b64_output = _b64Encode(stream_pdf_Final.getvalue())
    result = { "estado" : "OK", "PDFFinal": b64_output}
    return Success(result)

def main():

    puerto = 2202
    host = "0.0.0.0"

    print("Iniciando server\n")
    serve(host,puerto)
    print("Fin del server")


if  __name__ == "__main__":
    main()