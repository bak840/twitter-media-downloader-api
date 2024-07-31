# Twitter Media Downloader Server

A web API exposing an endpoint to get the videos' URLs of a tweet from its ID

## Local

Run with:  
`poetry run uvicorn main:app`

Caution: the --reload option breaks the app

## Docker

Build image:  
`docker build -t tmd-webapi .`

Run container:  
`docker run -p 8000:8080 -it -e API_KEY=H9zjnSlgrZyhbE2O5cko tmd-webapi`

`poetry run uvicorn main:app --host 0.0.0.0`

`poetry run uvicorn main:app --host 0.0.0.0 --ssl-keyfile="H:\Workspace\certs\bakinator-key.pem" --ssl-certfile="H:\Workspace\certs\bakinator.pem"`
