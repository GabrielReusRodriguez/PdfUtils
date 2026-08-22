FROM python:3-alpine

WORKDIR /usr/src/pdfUtils

EXPOSE 2202/tcp

#Instalamos las librerias necesarias con pip.
COPY requirements.txt .
COPY  ./src/*.py .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3" ,"/usr/src/pdfUtils/pdfUtilsServer.py"]