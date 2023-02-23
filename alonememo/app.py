from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
import random
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbjungle

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')

@app.route('/memo', methods=['GET'])
def read_memos():
    result = list(db.memos.find({},{'_id' : 0}).sort('like', -1))
    return jsonify({'result':'success', 'memos':result})

## API 역할을 하는 부분

@app.route('/memo', methods=['POST'])
def post_memos():
    title_receive = request.form['title_give'] 
    text_receive = request.form['text_give'] 
    id_receive = str(random.randrange(1,1000))
    like_receive = 0
    memo = {'title':title_receive, 'text':text_receive, 'memo_id':id_receive, 'like':like_receive} 
    db.memos.insert_one(memo)

    return jsonify({'result': 'success'})


@app.route('/memo/del', methods=['POST'])
def memo_delete():
    del_receive = request.form['del_id']
    db.memos.delete_one({'memo_id':del_receive})
    return jsonify({'result': 'success'})


@app.route('/memo/edit', methods=['POST'])
def memo_edit():
    title_edit = request.form['title_give'] 
    text_edit = request.form['text_give'] 
    id_edit = request.form['id_give'] 
    db.memos.update_one({'memo_id':id_edit},{'$set':{'title':title_edit}})
    db.memos.update_one({'memo_id':id_edit},{'$set':{'text':text_edit}})
    return jsonify({'result': 'success'})


@app.route('/memo/like', methods=['POST'])
def memo_like():
    id_like = request.form['id_give'] 
    like_memo = db.memos.find_one({'memo_id':id_like})
    new_like = like_memo['like']+1
    db.memos.update_one({'memo_id':id_like},{'$set':{'like':new_like}})
    return jsonify({'result': 'success'})


if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)