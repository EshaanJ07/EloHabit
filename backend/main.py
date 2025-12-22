from fastapi import FastAPI #Import fastapi class from FastAPI Library
from uuid import uuid4 #Allows random IDs to be created that guarantees no collision

app = FastAPI() #Creates FastAPI application object

@app.get("/") #Local URL ending with / will call the function right below it (.get refers to the request)
def root(): #Root function: The function below .get, serves to return data, call functions, give response, etc.
    return {"message": "EloHabit backend is running"} #Returning a dictionary, standard return type for APIs (flexible)


#Temporary storage of habits
habits = []




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
def create_habits():
    habit_id = str(uuid4()) #Generates unique habit id
    habit_dict =  {"user_id": "temp_user_id",
            "habit_id": habit_id, 
            "habit_name": "temp_habit_name", 
            "days_per_week": 3,
    }
    habits.append(habit_dict)
    
    return habit_dict

#Frontend gets current user habits
@app.get("/api/habits")
def get_current_habits():
    return {"habits" : habits} #Habits will be stored in an array of dictionaries (from create_habits route)

#Frontend deletes current user habit
@app.delete("/api/habits/{habit_id}")
def delete_current_habits(habit_id):
    for i in range(len(habits)):
        if habits[i]["habit_id"] == habit_id:
            del habits[i]
            break

    return 







