from flask import (
    Flask,
    render_template, 
    request, 
    redirect
    )
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json,socket

app = Flask(__name__)

def commit(db):
     with open('db.json','w') as createDB:
        json.dump(db, createDB, indent=4)



try:
    
    with open('db.json', 'r') as readDB:
        db = json.load(readDB)
    print('we have this one')
except:
    with open('db.json','w') as createDB:
        simple = {
            'users':{},
            'sms':{},
        }
        json.dump(simple, createDB, indent=4)
    with open('db.json', 'r') as readDB:
        db = json.load(readDB)
    print('created')
    

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        return render_template('login.html')

    else:
        return render_template('login.html')
@app.route('/connect', methods = ['POST', 'GET'])
def connect():
    if request.method == 'POST':
        USER = request.form['username']
        if USER == '' or len(USER) >= 20: return redirect('/login')

        if f'{socket.gethostbyname(socket.gethostname())}' not in db['users']:
            db['users'][f'{socket.gethostbyname(socket.gethostname())}'] = f'{USER}'

        Trigger = 0
        for i,j in db['users'].items():
            if j == USER and i != socket.gethostbyname(socket.gethostname()):
                Trigger+=1
        if Trigger == 0:
            for i,j in db['sms'].items(): 
                if j['username'] == db['users'][f'{socket.gethostbyname(socket.gethostname())}']:
                    db['sms'][f'{i}']['username'] = USER
            db['users'][f'{socket.gethostbyname(socket.gethostname())}'] = f'{USER}'
            commit(db)
        else:
            return render_template('login.html')
            
        return redirect('/connect')

    else:
        
        sms = db['sms']
        user = db['users']
        return render_template('index.html', sms = sms, mama = user[f'{socket.gethostbyname(socket.gethostname())}'], username = user[f'{socket.gethostbyname(socket.gethostname())}'],  user_len = len(db['users']))


@app.route('/', methods = ['POST', 'GET'])
def index():
    try:
        db['users'][f'{socket.gethostbyname(socket.gethostname())}']
    except :
        return redirect('/login')
    if request.method == 'POST':
        user = db['users']
        sms_content = request.form['content']
        sms_user = user[f'{socket.gethostbyname(socket.gethostname())}']
        
        if sms_content == '' or len(sms_content) > 40: return redirect('/')
        if sms_user == '' : return redirect('/')


        db['sms'][f'{len(db["sms"])}'] = {'userIP': f'{socket.gethostbyname(socket.gethostname())}','content': sms_content, 'username': f'{db["users"][f"{socket.gethostbyname(socket.gethostname())}"]}', 'date_created': f'{datetime.utcnow}'}
        commit(db)
        
        return redirect('/')

        
    

    else:
        sms = db['sms']
        user = db['users']
        return render_template('index.html', sms = sms, mama = user[f'{socket.gethostbyname(socket.gethostname())}'], username = user[f'{socket.gethostbyname(socket.gethostname())}'], user_len = len(db['users']))
        
    

if __name__ == "__main__":
    app.run(debug=True)
