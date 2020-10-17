from flask import (
    Flask,
    render_template, 
    request, 
    redirect
    )
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json,socket,os

app = Flask(__name__)


# print(socket.gethostname())



def commit(db):
     with open('db.json','w') as createDB:
        json.dump(db, createDB, indent=4)

def sessionInfo():
    with open('session.txt') as filereader:
        dan = filereader.read()
        return dan.split()

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

@app.route('/logout', methods = ['POST', 'GET'])
def logout():
    try:
        with open('session.txt', 'r') as filereader:
            session = filereader
    except:
        return redirect('/register')
    os.remove('session.txt')
    return redirect('/')
@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        if request.form['login'] == '' or request.form['password'] == '': return render_template('register.html')
        with open('session.txt', 'w') as sessionfile:
            sessionfile.write(f'{request.form["login"]} {request.form["password"]}')
        return render_template('login.html')    

    else:
        return render_template('register.html')    

@app.route('/login', methods = ['POST', 'GET'])
def login():
    try:
        with open('session.txt', 'r') as filereader:
            session = filereader
    except:
        return redirect('/register')
    if request.method == 'POST':
        return render_template('login.html')

    else:
        return render_template('login.html')
@app.route('/connect', methods = ['POST', 'GET'])
def connect():
    try:
        with open('session.txt', 'r') as filereader:
            session = filereader
    except:
        return redirect('/register')
    session = sessionInfo()
    if request.method == 'POST':
        USER = request.form['username']
        if USER == '' or len(USER) >= 20: return redirect('/login')
        
        session = sessionInfo()
        print(session)
        if f'{session[0]}{session[1]}' not in db['users']:
            db['users'][f'{session[0]}{session[1]}'] = f'{USER}'
        
        Trigger = 0
        for i,j in db['users'].items():
            if j == USER and i != f'{session[0]}{session[1]}':
                Trigger+=1
        if Trigger == 0:
            for i,j in db['sms'].items(): 
                if j['username'] == db['users'][f'{session[0]}{session[1]}']:
                    db['sms'][f'{i}']['username'] = USER
            db['users'][f'{session[0]}{session[1]}'] = f'{USER}'
            commit(db)
        else:
            return render_template('login.html')
            
        return redirect('/connect')

    else:
        
        sms = db['sms']
        user = db['users']
        
        return render_template('index.html', sms = sms, mama = user[f'{session[0]}{session[1]}'], username = user[f'{session[0]}{session[1]}'],  user_len = len(db['users']))


@app.route('/', methods = ['POST', 'GET'])
def index():
    try:
        with open('session.txt', 'r') as filereader:
            session = filereader
    except:
        return redirect('/register')
    session = sessionInfo()
    try:
        db['users'][f'{session[0]}{session[1]}']
    except :
        return redirect('/login')
    if request.method == 'POST':
        user = db['users']
        sms_content = request.form['content']
        sms_user = user[f'{session[0]}{session[1]}']
        
        if sms_content == '' or len(sms_content) > 40: return redirect('/')
        if sms_user == '' : return redirect('/')


        db['sms'][f'{len(db["sms"])}'] = {'userIP': f'{session[0]}{session[1]}','content': sms_content, 'username': f'{db["users"][f"{session[0]}{session[1]}"]}', 'date_created': f'{datetime.utcnow}'}
        commit(db)
        
        return redirect('/')

        
    

    else:
        sms = db['sms']
        user = db['users']
        return render_template('index.html', sms = sms, mama = user[f'{session[0]}{session[1]}'], username = user[f'{session[0]}{session[1]}'], user_len = len(db['users']))
        
    

if __name__ == "__main__":
    app.run(debug=True)