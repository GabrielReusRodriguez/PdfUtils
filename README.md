# PdfUtils

Servicio JSON-RPC para unir documentos PDF y devolver el resultado codificado en Base64.

## Requisitos

- Docker
- Docker Compose v2 (`docker compose`)

## Ejecutar con Docker Compose

Construir la imagen y arrancar el servicio:

```bash
docker compose up -d --build
```

El servicio queda disponible en:

```text
http://127.0.0.1:80
```

El puerto `80` del equipo se redirige al puerto `2202` del contenedor. Para consultar el estado y los logs:

```bash
docker compose ps
docker compose logs -f
```

Para detenerlo:

```bash
docker compose down
```

## API JSON-RPC

Las peticiones se realizan mediante `POST` con un cuerpo JSON-RPC 2.0.

### `mergePdf`

Une los PDFs recibidos en el orden indicado.

Parámetro `lista_b64Pdfs`:

- Array de objetos.
- Cada objeto debe contener la propiedad `pdf` con el contenido del PDF codificado en Base64.

Ejemplo usando dos archivos locales:

```bash
PDF1=$(base64 -w0 primer.pdf)
PDF2=$(base64 -w0 segundo.pdf)
curl -X POST http://127.0.0.1 \
  -H 'Content-Type: application/json' \
  -d "{\"jsonrpc\":\"2.0\",\"method\":\"mergePdf\",\"params\":{\"lista_b64Pdfs\":[{\"pdf\":\"$PDF1\"},{\"pdf\":\"$PDF2\"}]},\"id\":1}"
```

Respuesta correcta:

```json
{
  "jsonrpc": "2.0",
  "result": {
    "estado": "OK",
    "PDFFinal": "<PDF codificado en Base64>"
  },
  "id": 1
}
```

El valor de `result.PDFFinal` puede decodificarse para recuperar el PDF:

```bash
echo '<PDF codificado en Base64>' | base64 -d > resultado.pdf
```

## Tests

La suite usa `pytest` y comprueba la conversión Base64, la unión de páginas y la validación de una entrada vacía.

Ejecutarla dentro de Docker sin necesidad de instalar dependencias en el equipo host:

```bash
docker compose run --rm -T \
  -e PYTHONPATH=/usr/src/pdfUtils \
  -v "$PWD/tests:/usr/src/pdfUtils/tests:ro" \
  pdfutils pytest -v
```

Para instalar las dependencias en un entorno Python local:

```bash
python3 -m pip install -r requirements.txt
pytest -v
```

La configuración de pytest se encuentra en `pyproject.toml`. Define `src` como ruta de importación y `tests` como directorio de descubrimiento.

## Estructura

```text
Dockerfile              Imagen Docker del servicio
compose.yaml            Configuración de Docker Compose
pyproject.toml          Metadatos del proyecto y configuración de pytest
requirements.txt        Dependencias Python
src/pdfUtilsServer.py   Servidor JSON-RPC
tests/                  Tests automatizados
scripts/                Scripts de prueba manuales
.github/workflows/      Workflows de integración continua
```

## Licencia

PdfUtils se distribuye bajo la licencia **GNU General Public License v3.0 (GPL-3.0)**. Consulta el archivo [LICENSE](LICENSE) para conocer los términos completos.
