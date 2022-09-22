from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient
import certifi

client = MongoClient('mongodb+srv://test:sparta@cluster0.fwrets3.mongodb.net/cluster0?retryWrites=true&w=majority',
                     tlsCAFile=certifi.where())
db = client.dbsparta_week1

from datetime import datetime


@app.route('/')
def home():
    return render_template('recommendation.html')


@app.route('/contents', methods=['GET'])
def show_music():
    music = list(db.peopleofmusic.find({}, {'_id': False}))
    return jsonify({'all_music': music})


@app.route('/contents', methods=['POST'])
def save_music():
    artist_receive = request.form['artist_give']
    song_receive = request.form['song_give']
    rec_receive = request.form['rec_give']

    file = request.files["file_give"]

    extension = file.filename.split('.')[-1]

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    filename = f'file-{mytime}'

    save_to = f'static/{filename}.{extension}'
    file.save(save_to)

    doc = {
        'artist': artist_receive,
        'song': song_receive,
        'rec': rec_receive,
        'file': f'{filename}.{extension}'
    }

    db.contents.insert_one(doc)

    return jsonify({'msg': '추천 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
