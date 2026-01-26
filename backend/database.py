import sqlite3
from schemas import Habit


conn: sqlite3.Connection = sqlite3.connect('elohabit.db', check_same_thread=False) #Creates elohabit.db database if it doesn't exist, otherwise opens it

#Table creation
with conn:
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS habits (
        habit_id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        habit_name TEXT NOT NULL,
        days_per_week INTEGER NOT NULL
        ) """)

#Database Functions
def insert_habit(habit: Habit) -> None:
    """Inserts a habit into database table"""

    with conn: #Transaction
        c = conn.cursor() #Cursors kept local and short-lived prevent future multiple request errors, all work is done within the same transaction

        c.execute(
            "INSERT INTO habits (habit_id, user_id, habit_name, days_per_week) " \
            "VALUES (:habit_id, :user_id, :habit_name, :days_per_week)",
            {
                "habit_id": habit.habit_id, 
                "user_id": habit.user_id, 
                "habit_name": habit.habit_name, 
                "days_per_week": habit.days_per_week,
            },
        )

def get_database_habit(
        habit_id: str, 
        user_id: str,
) -> Habit | None:
    """Returns a habit if it exists in database, otherwise returns None"""

    with conn:
        c = conn.cursor()

        c.execute(
            "SELECT habit_id, user_id, habit_name, days_per_week FROM habits " \
            "WHERE habit_id = :habit_id AND user_id = :user_id", 
            {
                "habit_id": habit_id, 
                "user_id": user_id,
            },
        )
        
        row = c.fetchone()
        
    if row is None: #Checking if habit exists in table
        return None
    
    return Habit(
        habit_id=row[0],
        user_id=row[1],
        habit_name=row[2],
        days_per_week=row[3],
    )

def delete_database_habit(
        habit_id: str, 
        user_id: str,
) -> bool:
    """Deletes user habit from database, if valid"""

    with conn:
        c = conn.cursor()

        c.execute(
            "DELETE FROM habits " \
            "WHERE habit_id = :habit_id AND user_id = :user_id", 
            {
                "habit_id": habit_id, 
                "user_id": user_id,
            },
        )
        
        return c.rowcount == 1 #Checks if one row has been affected by the last SQL statement

def update_database_habit(
        habit_id: str, 
        user_id: str, 
        updated_habit: Habit,
) -> bool:
    """Updates user habit and returns True if update was successful"""
    
    with conn:
        c = conn.cursor()
        
        c.execute(
            "UPDATE habits " \
            "SET habit_name = :habit_name, " \
            "days_per_week = :days_per_week " \
            "WHERE habit_id = :habit_id AND user_id = :user_id", 
            {
                "habit_id": habit_id, 
                "user_id": user_id,
                "habit_name": updated_habit.habit_name,
                "days_per_week": updated_habit.days_per_week,
            },
        )
        
        return c.rowcount == 1 #Checking if update was successful
       
def return_database_user_habits(user_id: str) -> list[Habit]:
    """Returns a list of Habit objects belonging to the user"""

    with conn:
        c = conn.cursor()
        c.execute(
            "SELECT habit_id, user_id, habit_name, days_per_week FROM habits " \
            "WHERE user_id = :user_id", 
            {"user_id": user_id},
        )
        
        return [Habit(tup[0], tup[1], tup[2], tup[3]) for tup in c.fetchall()]