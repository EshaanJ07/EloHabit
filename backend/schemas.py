from pydantic import BaseModel, Field
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