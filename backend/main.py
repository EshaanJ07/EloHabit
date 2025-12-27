from fastapi import FastAPI, HTTPException, Depends #Import fastapi class from FastAPI Library
from pydantic import BaseModel, Field
from uuid import uuid4 #Allows random IDs to be created that guarantees no collision


#Habit schema class that sets constraints on the data that JSON sends from frontend to backend (What a habit is supposed to look like)
class HabitBase(BaseModel): #Basemodel automaically verifies data, and any invalid data allows FastAPI to generate an HTTP error response
    habit_name: str = Field(..., min_length=1, description="Name of habit")
    days_per_week: int = Field(..., ge=1, le=7, description="Weekly frequency habit must be completed")

#Class inherited from HabitBase that defines the data format the user must conform to create a new habit
class HabitCreate(HabitBase):
    """Payload when user creates a new habit"""

#Schema class for validating partial updates to a user habit
class HabitUpdate(BaseModel):
    habit_name: str | None = Field(None, min_length=1, description="Updated habit name")
    days_per_week : int | None = Field(None, ge=1, le=7, description="Updated weekly frequency habit must be completed")

#Schema class that defines the entirety of a habit object, which includes backend-owned habit_id and user_id
class Habit(HabitBase):
    habit_id: str
    user_id: str


app = FastAPI() #Creates FastAPI application object


@app.get("/") #Local URL ending with / will call the function right below it (.get refers to the request)
def root(): #Root function: The function below .get, serves to return data, call functions, give response, etc.
    """Health check endpoint to verify backend is up and running"""
    
    return {"message": "EloHabit backend is running"} #Returning a dictionary, standard return type for APIs (flexible)


#Temporary storage of habits keyed by habit_id
habits: dict[str, Habit] = {} #Type hint annotation where habit_id functions as the key and a Habit object as the value

#Dependency functions ----------- (how the API knows who is requesting the route)
def get_current_user_id() -> str:
    return "temp_user_id"


#Dashboard Routes -----------
#Frontend gets current user information
@app.get("/api/me")
def get_current_user() -> dict[str, str]: #This function is intended to return a dictionary with keys and values of strings
    """Placeholder user information until authentication development"""
    
    return {
        "user_id": "temp_user_id",
        "username": "temp_username", 
        "rank": "temp_rank",
    }

#Frontend asks backend to create new habits
@app.post("/api/habits")
def create_habit(payload: HabitCreate) -> Habit: #Takes in HabitCreate argument with variable name payload to ensure correct data formatting of a habit
    """Create a habit tied to the current (placeholder) user and store it in memory"""
    
    habit_id = str(uuid4()) #Generates unique habit id
    habit = Habit(
        user_id="temp_user_id",
        habit_id=habit_id,
        habit_name=payload.habit_name,
        days_per_week=payload.days_per_week,
    )
    habits[habit_id] = habit
    return habit

#Frontend gets current user habits
@app.get("/api/habits")
def get_current_habits(
    user_id = Depends(get_current_user_id) 
) -> dict[str, list[Habit]]:
    """Returns all habits to the placeholder user."""
    
    return {
        "habits" : [h for h in habits.values() if h.user_id == user_id]
    } #Returns string "habits" with a list of all habit objects belonging to user

#Frontend asks backend to delete current user habit
@app.delete("/api/habits/{habit_id}") #The thing inside the brackets lets the API know what to extract and pass as a parameter
def delete_habit(
    habit_id: str, 
    user_id: str = Depends(get_current_user_id)
) -> dict[str, bool]:
    """Delete a habit if it exists and belongs to the user, otherwise return a 404 error"""
    habit = habits.get(habit_id) #Returns None if no key exists
    if habit is None or habit.user_id != user_id:
        raise HTTPException(status_code=404, detail="Habit not found") #Habit not found will send specific 404 error to frontend to deliver to user
        
    del habits[habit_id]
    return {"ok": True}
    
#Frontend asks backend to update habit
@app.patch("/api/habits/{habit_id}")
def update_habit(
    habit_id: str, 
    updates: HabitUpdate, 
    user_id = Depends(get_current_user_id)
) -> Habit: #Backend looks at the JSON body for updates since it is not in the URL path
    """Updates habit values sent by user and leaves unspecified fields untouched"""
    habit = habits.get(habit_id)
    if habit is None or habit.user_id != user_id:
        raise HTTPException(status_code=404, detail="Habit not found")

    updated_values = updates.model_dump(exclude_unset=True, exclude_none=True) #converts HabitUpdate object into a dict, and deletes any keys the user did not provide in fields AND keys where the values are None
    habits[habit_id] = habit.model_copy(update=updated_values) #creates a new and identical habit object, updates it with values of updated_values, and stores it in habits
    return habits[habit_id]




    







