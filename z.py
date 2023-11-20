import pyrebase
from datetime import datetime



config = {
  "apiKey": "AIzaSyDUqEFZgE0SMDzeERWnfxUR94yQC2hHEyk",
  "authDomain": "bookproject-b0709.firebaseapp.com",
  "databaseURL": "https://bookproject-b0709-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "bookproject-b0709",
  "storageBucket": "bookproject-b0709.appspot.com",
  "messagingSenderId": "650500330497",
  "appId": "1:650500330497:web:023f6bf511184b3b01dc00",
  "measurementId": "G-FTCHXJW7SK"
}

# firebase = pyrebase.initialize_app(config)
# authe = firebase.auth()
# database = firebase.database()
# ret_val = authe.create_user_with_email_and_password("tamjidzihan@gmail.com", "tamjid2014")
# now = datetime.now()
# pass_data = {"full_name": 'full_name', "username": 'username', "email": 'email',"approved": 1, "created_at": datetime.timestamp(now)}
# database.child('user').child(ret_val['localId']).set(pass_data)