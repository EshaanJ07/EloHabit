from fastapi import FastAPI, HTTPException, Depends 
from uuid import uuid4 
from schemas import HabitCreate, HabitUpdate, Habit
from deps import get_current_user_id
from database import insert_habit, get_database_habit, delete_database_habit, update_database_habit, return_database_user_habits

app = FastAPI() 

@app.get("/") 
def root(): 
    """Health check endpoint to verify backend is up and running"""
    
    return {"message": "EloHabit backend is running"} 


#Temporary storage of habits keyed by habit_id
#habits: dict[str, Habit] = {} 

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
def create_habit(
    payload: HabitCreate,
    user_id: str = Depends(get_current_user_id),
) -> Habit:
    """Create a habit tied to the current (placeholder) user and store it in database"""
    
    habit_id = str(uuid4()) 
    habit = Habit(
        user_id=user_id,
        habit_id=habit_id,
        habit_name=payload.habit_name,
        days_per_week=payload.days_per_week,
    )
    
    insert_habit(habit)
    return habit

#Frontend gets current user habits
@app.get("/api/habits")
def get_current_habits(
    user_id: str = Depends(get_current_user_id),
) -> dict[str, list[Habit]]:
    """Returns all habits to the placeholder user."""
    
    return {
        "habits" : return_database_user_habits(user_id)
    } 

#Frontend asks backend to delete current user habit
@app.delete("/api/habits/{habit_id}") 
def delete_habit(
    habit_id: str, 
    user_id: str = Depends(get_current_user_id),
) -> dict[str, bool]:
    """Delete a habit if it exists and belongs to the user, otherwise return a 404 error"""
    
    if delete_database_habit(habit_id, user_id):
        return {"ok": True}
    
    raise HTTPException(status_code=404, detail="Habit not found")
    
#Frontend asks backend to update habit
@app.patch("/api/habits/{habit_id}")
def update_habit(
    habit_id: str, 
    updates: HabitUpdate, 
    user_id: str = Depends(get_current_user_id),
) -> Habit:
    """Updates habit values sent by user and leaves unspecified fields untouched"""
    
    habit = get_database_habit(habit_id, user_id)
    
    if habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")

    updated_values = updates.model_dump(exclude_unset=True, exclude_none=True) #converts HabitUpdate object into a dict, and deletes any keys the user did not provide in fields AND keys where the values are None
    updated_habit = habit.model_copy(update=updated_values) #creates a new and identical habit object, updates it with values of updated_values, and stores it in habits
    
    if not update_database_habit(habit_id, user_id, updated_habit):
        raise HTTPException(status_code=500, detail="Failed to update habit")
    
    return updated_habit