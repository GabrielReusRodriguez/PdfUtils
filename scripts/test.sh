#!/usr/bin/env bash

PDF1=$(base64 -w0 ./pdfs/Pdf1.pdf)
PDF2=$(base64 -w0 ./pdfs/Pdf2.pdf)

echo "{\"jsonrpc\":\"2.0\",\"method\":\"mergePdf\",\"params\":{\"lista_b64Pdfs\":[{\"pdf\":\"$PDF1\"},{\"pdf\":\"$PDF2\"}]},\"id\":1}" > payload

curl -X POST http://127.0.0.1 \
  -H 'Content-Type: application/json' \
  --data-binary @payload
