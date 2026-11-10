# Songs microservice — Backend Development Capstone

Completed educational implementation based on the IBM Developer Skills Network course template. Prepared by Sabina Zhumagaliyeva with AI coding assistance. Original template attribution and license are retained.

## Run

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
flask --app app run --port 5000
```

For Songs, start MongoDB and configure its connection before starting Flask.

## API

- `GET /health` and `GET /count`
- `GET /song` and `GET /song/<id>`
- `POST /song` creates a validated item
- `PUT /song/<id>` updates an item
- `DELETE /song/<id>` deletes an item

```sh
pytest -v
docker build -t songs .
docker run --rm -p 3000:3000 songs
```

The Songs service uses MongoDB and a unique integer `id` index. Startup seeds missing course examples without deleting existing songs. Set `MONGODB_URI` (or `MONGODB_SERVICE`, `MONGODB_PORT`, `MONGODB_USERNAME`, `MONGODB_PASSWORD`); `MONGODB_DATABASE` defaults to `songs`. Credentials are environment configuration, never committed.

CRUD operations have been exercised against an actual local MongoDB database.

This is a course demonstration, not a production service. It has no public write authorization and should run only in a temporary isolated lab. Python dependencies were updated from the old template to the versions actually tested with Python 3.12. Cloud availability is temporary and must be verified separately from local tests.
