from fastapi import FastAPI #Import fastapi class from FastAPI Library
from uuid import uuid4 #Allows random IDs to be created that guarantees no collision

app = FastAPI() #Creates FastAPI application object

@app.get("/") #Local URL ending with / will call the function right below it (.get refers to the request)
def root(): #Root function: The function below .get, serves to return data, call functions, give response, etc.
    return {"message": "EloHabit backend is running"} #Returning a dictionary, standard return type for APIs (flexible)


#Temporary storage of habits
habits = {}




#Dashboard Routes -----------

#Frontend gets current user information
@app.get("/api/me")
def get_current_user():
    return {"user_id": "temp_user_id",
            "username": "temp_username", 
            "rank": "temp_rank",
    }

#Frontend asks backend to create new habits
@app.post("/api/habits")
def create_habit():
    habit_id = str(uuid4()) #Generates unique habit id
    habit_dict =  {"user_id": "temp_user_id",
            "habit_id": habit_id, 
            "habit_name": "temp_habit_name", 
            "days_per_week": 3,
    }
    habits[habit_id] = habit_dict
    
    return habit_dict

#Frontend gets current user habits
@app.get("/api/habits")
def get_current_habits():
    return {"habits" : list(habits.values())}

#Frontend asks backendto delete current user habit
@app.delete("/api/habits/{habit_id}") #The thing inside the brackets lets the API know what to extract and pass as a parameter
def delete_current_habits(habit_id: str):
    if habit_id in habits:
        del habits[habit_id]
        return {"ok": True}
    
    return {"ok": False}

#Frontend asks backend to update habit
@app.patch("/api/habits/{habit_id}")
def update_habit(habit_id: str, updates: dict): #Backend looks at the JSON body for updates since it is not in the URL path
    if habit_id in habits:
        for key in updates:
            habits[habit_id][key] = updates[key]
        return habits[habit_id]
    
    return {"ok": False}

    







