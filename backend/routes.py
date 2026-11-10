"""MongoDB-backed songs API. Seed data are inserted without deleting existing songs."""
from . import app
import json
import os
from pathlib import Path
from urllib.parse import quote_plus
from flask import jsonify, request
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from bson import json_util

host = os.environ.get('MONGODB_SERVICE', '127.0.0.1')
port = int(os.environ.get('MONGODB_PORT', '27017'))
username = os.environ.get('MONGODB_USERNAME')
password = os.environ.get('MONGODB_PASSWORD')
credentials = f'{quote_plus(username)}:{quote_plus(password)}@' if username and password else ''
uri = os.environ.get('MONGODB_URI', f'mongodb://{credentials}{host}:{port}/')
client = MongoClient(uri, serverSelectionTimeoutMS=5000)
db = client[os.environ.get('MONGODB_DATABASE', 'songs')]
db.songs.create_index('id', unique=True)
if os.environ.get('SEED_DATA', '1') == '1':
    with (Path(__file__).parent / 'data/songs.json').open() as f:
        for song in json.load(f):
            db.songs.update_one({'id': song['id']}, {'$setOnInsert': song}, upsert=True)

def parse_json(value):
    return json.loads(json_util.dumps(value))

def payload():
    value = request.get_json(silent=True)
    if not isinstance(value, dict):
        return None
    return {k: v for k, v in value.items() if k in ('id', 'title', 'lyrics')}

@app.get('/health')
def health():
    client.admin.command('ping')
    return jsonify(status='OK'), 200

@app.get('/count')
def count():
    return jsonify(count=db.songs.count_documents({})), 200

@app.get('/song')
def songs():
    return jsonify(songs=parse_json(list(db.songs.find({}, {'_id': 0}).sort('id', 1)))), 200

@app.get('/song/<int:id>')
def get_song_by_id(id):
    song = db.songs.find_one({'id': id}, {'_id': 0})
    return (jsonify(song), 200) if song else (jsonify(message=f'song with id {id} not found'), 404)

@app.post('/song')
def create_song():
    song = payload()
    if not song or type(song.get('id')) is not int or not isinstance(song.get('title'), str):
        return jsonify(message='An integer id and title are required'), 400
    try:
        db.songs.insert_one(dict(song))
    except DuplicateKeyError:
        return jsonify(Message=f"song with id {song['id']} already present"), 302
    return jsonify(song), 201

@app.put('/song/<int:id>')
def update_song(id):
    song = payload()
    if song is None or ('id' in song and song['id'] != id):
        return jsonify(message='Invalid JSON or mismatched id'), 400
    result = db.songs.update_one({'id': id}, {'$set': song})
    if not result.matched_count:
        return jsonify(message='song not found'), 404
    return jsonify(db.songs.find_one({'id': id}, {'_id': 0})), 201 if result.modified_count else 200

@app.delete('/song/<int:id>')
def delete_song(id):
    result = db.songs.delete_one({'id': id})
    return ('', 204) if result.deleted_count else (jsonify(message='song not found'), 404)
