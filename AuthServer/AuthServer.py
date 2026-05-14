import socket
import threading
import json
from bcrypt import gensalt,hashpw,checkpw
from src_db.Models import User, engine
from sqlalchemy.orm import sessionmaker
from src_json.Notes import Create_Notes_json, Save_Note, Get_Notes, Delete_Note
import argparse

Session = sessionmaker(bind=engine)

ServStatus=True
parser=argparse.ArgumentParser()
parser.add_argument('--Host', help='Set authentication server host', default='localhost')
parser.add_argument('--Port', help='Set authentication server port',type=int, default=9999)
args= parser.parse_args()

def CreateServer():
    HOST = args.Host
    PORT = args.Port
    try:
        Server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        Server.bind((HOST,PORT))
        Server.listen(100)
        Server.settimeout(2)
        
        print(f"Running Server on {socket.gethostbyname(HOST)}:{PORT}! type 'exit' to shutdown\n")
        return Server
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
        

def HandleClient(Clsock,ClAddr):
    try:
        data=Clsock.recv(4096).decode()
        data=json.loads(data)
        
        
        if data["route"]=="change_password":
            print(f"Connected to: {ClAddr}")
            print(f"{data}")   
            
            response=Change_Password(data=data)
            
            print(f"response: {response}\n")
            Clsock.send(json.dumps(response).encode())
    
        elif data["route"]=="signup":
            print(f"Connected to: {ClAddr}\n")
            print(f"{data}")
            
            response=Signup(data=data)
            print(f"response: {response}\n")
            
            Clsock.send(response.encode())
        
        elif data["route"]=="login" :
            print(f"Connected to: {ClAddr}")
            print(f"{data}")
            
            response=Login(data=data)
            print(f"response: {response}\n")
            
            Clsock.send(response.encode())

        elif data["route"]=="save_note":
            print(f"Connected to: {ClAddr}")
            print(f"{data}")
            
            response=Save_Note(note=data["note"],username=data["username"])
            print(f"response: {response}\n")
            
            Clsock.send(json.dumps(response).encode())

        elif data["route"]=="get_notes":
            print(f"Connected to: {ClAddr}")
            print(f"{data}")
            
            response=Get_Notes(data["username"])
            print(f"response: {response}\n")
            
            Clsock.send(json.dumps(response).encode())
        
        elif data["route"]=="delete_note":
            print(f"Connected to: {ClAddr}")
            print(f"{data}")
            
            response=Delete_Note(data["note_id"], data["username"])
            print(f"response: {response}\n")
            
            Clsock.send(json.dumps(response).encode())

    except Exception as e:
        print(f"Error handling Client: {e}\n")
    
    finally:
        Clsock.close()

def Login(data):
    session = Session()
    
    username=data['username']
    passwd=data['passwd']
    
    result = session.query(User).filter(User.username==username).first()
    session.close() 
    
    if(result):
        if(checkpw(passwd.encode('utf-8'),result.passwd)):
            return "Success"
        else:
            return "Failure"
    else:
        return "Failure"
    
def Signup(data):
    session = Session()
    
    username=data['username']
    passwd=data['passwd']
    result = session.query(User).filter(User.username==username).first() 

    if result is None:
        passwd=passwd.encode('utf-8')
        salt=gensalt()
        hashedpasswd=hashpw(password=passwd,salt=salt)
        
        user=User(username=username,passwd=hashedpasswd)
        
        session.add(user)    
        session.commit()
        session.close()
        
        return "Success"
    else:
        return "Failure"



def Change_Password(data):
    session= Session()
    
    username = data['username']
    current_password = data['current_password']
    new_password = data['new_password']
    
    result = session.query(User).filter(User.username==username).first()
    
    if result and checkpw(current_password.encode('utf-8'),result.passwd):
        salt=gensalt()
        hashed_new_password=hashpw(password=new_password.encode('utf-8'),salt=salt)
        
        result.passwd = hashed_new_password
        session.commit()
        session.close()
        
        response = {    
            "success": True,
            "error": "No Error"
        }
        return response
    
    else:
        response = {
            "success": False,
            "error": "Current Password is Incorrect"
        }
        return response


def ServerShutdown():
    global ServStatus
    while True:
        command=input()
        if(command.lower()=="exit"):
            print("Server shutdown initiated.\n")   
            ServStatus=False
            return
        

if __name__=="__main__":
    Server=CreateServer()
    Create_Notes_json()
    
    ShutdownThread=threading.Thread(target=ServerShutdown,daemon=True)
    ShutdownThread.start()
    
    while ServStatus:
        try:
            Clsock, ClAddr= Server.accept()
            Clthread=threading.Thread(target=HandleClient,args=(Clsock,ClAddr),daemon=True)
            Clthread.start()
        except socket.timeout:
            continue
            
    Server.close()
    print("Server stopped.\n")