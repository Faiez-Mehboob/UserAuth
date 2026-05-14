from flask import Blueprint, render_template, request, session, url_for, redirect, flash, current_app, jsonify
import socket
import json

dash = Blueprint('dash',__name__)

@dash.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    return render_template('dashboard.html',username=session['user'])


@dash.route('/logout', methods=['GET','POST'])
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


@dash.route('/change_password', methods=['POST'])
def change_password():
    AuthHOST=current_app.config.get('AuthHOST')
    AuthPORT=current_app.config.get('AuthPORT')
    
    data=request.get_json()
    data["username"] = session['user']
    data["route"] = "change_password"
    
    with socket .socket(socket.AF_INET,socket.SOCK_STREAM) as ServSock:
        try:
            ServSock.connect((AuthHOST,AuthPORT))
            ServSock.send(json.dumps(data).encode())
        except Exception:
            response = {
                "success": False,
                "error": "Error Connecting to Server!"
            }
            return jsonify(response)
        
        
        try:
            response=json.loads(ServSock.recv(4096).decode())
        except Exception:
            response={
                "success": False,
                "error": "Server Connection Timed Out!"
            }
            return jsonify(response)
                                
        return jsonify(response)


@dash.route('/save_note', methods=['POST'])
def save_note():
    AuthHOST=current_app.config.get('AuthHOST')
    AuthPORT=current_app.config.get('AuthPORT')
    
    username=session['user']   
    note=request.json
    
    data={
        "username": username,
        "route": "save_note",
        "note": note
    }

    json_data=json.dumps(data)
    
    try:
        ServSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        ServSock.connect((AuthHOST,AuthPORT))
        ServSock.send(json_data.encode())
    
    except Exception as e:
        print(f"Error Connecting to Server: {e}\n")
        return {
            "success": False,
            "error": f"Error Connecting to Server: {e}"
        }
    
    try:
        json_response = ServSock.recv(4096).decode()
    except Exception as e:
        print(f"Connection Error: {e}\n")
        return {
            "success": False,
            "error": f"Connection Error: {e}"
        }  
    
    ServSock.close()
    
    response = json.loads(json_response)
    
    return jsonify(response)



@dash.route('/delete_note', methods=['POST'])
def delete_note():
    AuthHOST=current_app.config.get('AuthHOST')
    AuthPORT=current_app.config.get('AuthPORT')
    
    username=session['user']
    data = request.json
    data["username"] = username
    data["route"] = "delete_note"
    
    
    json_data=json.dumps(data)

    try:
        ServSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        ServSock.connect((AuthHOST,AuthPORT))
        ServSock.send(json_data.encode())
    
    except Exception as e:
        print(f"Error Connecting to Server: {e}\n")
        return {
            "success": False,
            "error": f"Error Connecting to Server: {e}"
        }
    try:
        json_response = ServSock.recv(4096).decode()
    except Exception as e:
        print(f"Connection Error: {e}\n")
        return {
            "success": False,
            "error": f"Connection Error: {e}"
        }  
    
    ServSock.close()
    
    response = json.loads(json_response)
    
    return jsonify(response)
    

@dash.route('/get_notes', methods=['GET','POST'])
def get_notes():
    AuthHOST=current_app.config.get('AuthHOST')
    AuthPORT=current_app.config.get('AuthPORT')
    
    username=session['user']
    data = {
        "username": username,
        "route": "get_notes"
    }
    
    json_data=json.dumps(data)
    
    try:
        ServSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        ServSock.connect((AuthHOST,AuthPORT))
        ServSock.send(json_data.encode())
    
    except Exception as e:
        print(f"Error Connecting to Server: {e}\n")
        return {
            "success": False,
            "error": f"Error Connecting to Server: {e}"
        }
    
    try:
        json_response = ServSock.recv(4096).decode()
    except Exception as e:
        print(f"Connection Error: {e}\n")
        return {
            "success": False,
            "error": f"Connection Error: {e}"
        }  
    
    ServSock.close()
    
    response = json.loads(json_response)
    
    return jsonify(response)
    
