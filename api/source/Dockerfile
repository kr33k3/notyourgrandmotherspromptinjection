FROM python:3.10.13-alpine

## Install pip, pip package deps, and healthcheck dependencies
RUN apk add -U py-pip curl gcc g++ unixodbc-dev gnupg
RUN pip install --upgrade pip

## Install production-grade hosting dependencies
RUN pip install gunicorn

## Install ODBC Driver
#Download the desired package(s)
RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/msodbcsql17_17.10.5.1-1_amd64.apk
RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/mssql-tools_17.10.1.1-1_amd64.apk

#(Optional) Verify signature, if 'gpg' is missing install it using 'apk add gnupg':
RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/msodbcsql17_17.10.5.1-1_amd64.sig
RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/mssql-tools_17.10.1.1-1_amd64.sig

RUN curl https://packages.microsoft.com/keys/microsoft.asc  | gpg --import -
RUN gpg --verify msodbcsql17_17.10.5.1-1_amd64.sig msodbcsql17_17.10.5.1-1_amd64.apk
RUN gpg --verify mssql-tools_17.10.1.1-1_amd64.sig mssql-tools_17.10.1.1-1_amd64.apk

#Install the package(s)
RUN apk add --allow-untrusted msodbcsql17_17.10.5.1-1_amd64.apk
RUN apk add --allow-untrusted mssql-tools_17.10.1.1-1_amd64.apk


## Install API
WORKDIR /app
COPY . /app
RUN pip --no-cache-dir install -r requirements.txt

## Expose API port
EXPOSE 8000

## Run API and check health
ENTRYPOINT [ "gunicorn", "--workers=4", \
              "--bind=0.0.0.0", \
              "--access-logfile", "-", \
              "--error-logfile", "-", \
              "--logger-class", "logging_wrapper.gunicorn_filter.CustomGunicornLogger", \
              "--timeout", "600", \
              "app:app" ]
HEALTHCHECK --start-period=1s --interval=5s --timeout=1s \
  CMD curl 0.0.0.0:8000/health/
