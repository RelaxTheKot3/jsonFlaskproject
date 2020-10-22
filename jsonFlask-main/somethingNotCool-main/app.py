from flask import (
    Flask,
    render_template, 
    request, 
    redirect
    )
    
from datetime import datetime
import json,socket,os

app = Flask(__name__)




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

@app.route('/delete', methods = ['POST', 'GET'])
def delete():
    # if request.method == 'POST':
    smisol = request.args.to_dict()   # request.args[f'{list(smisol)[0]}']
    db['sms'].pop(f'{request.args[f"{list(smisol)[0]}"]}')
    commit(db)


    return redirect('/')

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
        if f'{request.form["login"]}{request.form["password"]}' in db['users'] : return redirect('/connect') 
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
        
        return render_template('index.html', sms = sms, mama = user[f'{session[0]}{session[1]}'], username = user[f'{session[0]}{session[1]}'],  user_len = len(db['users']), suzers = db['users'])


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
        
        if sms_content == '' or sms_user == '' or len(sms_content) >= 201 : return redirect('/')

        # spaces = 0
        # for i in sms_content:
        #     if i == ' ':
        #         spaces +=1

        # if ' ' not in sms_content and len(sms_content) > 52 or spaces != len(sms_content) // 53:
        #     for i in range(0,len(sms_content), 53):
        #         spam = sms_content[i::]
        #         sms_content = sms_content[:i:] + '\n' + spam



        if len(db['sms']) != 0:
            smert = list(db['sms'])[len(db['sms'])-1]
        else:
            smert = -1
        db['sms'][f'{int(smert) + 1}'] = {'userIP': f'{session[0]}{session[1]}','content': sms_content, 'username': f'{db["users"][f"{session[0]}{session[1]}"]}', 'date_created': f'{datetime.utcnow()}'}
        commit(db)
        
        return redirect('/')

        
    

    else:
        sms = db['sms']
        user = db['users']
        return render_template('index.html', sms = sms, mama = user[f'{session[0]}{session[1]}'], username = user[f'{session[0]}{session[1]}'], user_len = len(db['users']), suzers = db['users'])
        
    

if __name__ == "__main__":
    app.run(debug=True)
