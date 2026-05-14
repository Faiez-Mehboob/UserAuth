import json
import os

def Create_Notes_json():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(curr_dir,"notes.json")
    
    if os.path.exists(filepath):
        return
    else:
        with open(filepath,'w') as f:
            data ={"users": {}}
            json.dump(data,f,indent=4)
        return
    
    
def Save_Note(note, username):
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(curr_dir,"notes.json")
    
    if os.path.exists(filepath):
        with open(filepath,'r') as f:
            try:
                data = json.load(f)
            except Exception as e:
                print(f"Error Reading json file: {e}\n")
                return {
                    "success": False,
                    "error": f"Error Reading json file: {e}"
                }
        
        if username not in data["users"]:
            data["users"][username] = []
        
        updated = False
        for stored_note in data["users"][username]:
            if stored_note.get("note_id") == note.get("note_id"):
                stored_note["title"] = note["title"]
                stored_note["content"] = note["content"]
                
                updated=True
                break
        
        if not updated:
            data["users"][username].append(note)
        
        with open(filepath,'w') as f:
            try:
                json.dump(data,f,indent=4)
            except Exception as e:
                print(f"Error writing to json file: {e}\n")
                return {
                    "success": False,
                    "error": f"Error writing to json file: {e}"
                }
                
        return {
            "success":True,
            "error": "No error"
        }    
        
    else:
        print("json file not found\n")
        return {
            "success": False,
            "error": "json file not found"
        }


def Get_Notes(username):
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(curr_dir,"notes.json")
    
    if os.path.exists(filepath):
        with open(filepath,'r') as f:
            try:
                data = json.load(f)
            except Exception as e:
                print(f"Error Reading json file: {e}\n")
                return {
                    "success": False,
                    "error": f"Error Reading json file: {e}"
                }
        
        notes = data["users"].get(username,[])
        return {
            "success":True,
            "notes": notes
        }
        
    else:
        print("json file not found\n")
        return {
            "success": False,
            "error": "json file not found"
        }


def Delete_Note(noteid, username):
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(curr_dir,"notes.json")
    
    if os.path.exists(filepath):
        with open(filepath,'r') as f:
            try:
                data = json.load(f)
            except Exception as e:
                print(f"Error Reading json file: {e}\n")
                return {
                    "success": False,
                    "error": f"Error Reading json file: {e}"
                }
        
        if username not in data["users"]:
            return {
                "success": False,
                "error": "User NOT found"
            }

        stored_notes = data["users"][username]
        note_to_delete = None
        
        for note in stored_notes:
            if note.get("note_id")==noteid:
                note_to_delete=note
                break
        
        if note_to_delete:
            stored_notes.remove(note_to_delete)
        else:
            return {
                "success": False,
                "error": "note_id NOT found"
            }
        
        with open(filepath,'w') as f:
            try:
                json.dump(data,f,indent=4)
            except Exception as e:
                print(f"Error writing to json file: {e}\n")
                return {
                    "success": False,
                    "error": f"Error writing to json file: {e}"
                }
                
        return {
            "success":True,
            "error": "No error"
        }
               
    else:
        print("json file not found\n")
        return {
            "success": False,
            "error": "json file not found"
        }