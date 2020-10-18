import json
import socket

# def commit(db):
#      with open('db.json','w') as createDB:
#         json.dump(db, createDB, indent=4)


# try:
    
#     with open('db.json', 'r') as readDB:
#         db = json.load(readDB)
#     print('we have this one')
# except:
#     with open('db.json','w') as createDB:
#         simple = {
#             'users':{},
#             'sms':{},
#         }
#         json.dump(simple, createDB, indent=4)
#     with open('db.json', 'r') as readDB:
#         db = json.load(readDB)
#     print('created')

# print(db['users'])
# db['users'][f'{socket.gethostbyname(socket.gethostname())}'] = 'dddd'

# commit(db)
print(socket.gethostname())