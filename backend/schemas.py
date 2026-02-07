from pydantic import BaseModel, Field
from enum import Enum

class Weekday(Enum):
    MON = "Mon"
    TUE = "Tue"
    WED = "Wed"
    THU = "Thu"
    FRI = "Fri"
    SAT = "Sat"
    SUN = "Sun"


#Habit schema class that sets constraints on the data that JSON sends from frontend to backend (What a habit is supposed to look like)
class HabitBase(BaseModel): #Basemodel automaically verifies data, and any invalid data allows FastAPI to generate an HTTP error response
    habit_name: str = Field(
        ..., 
        min_length=1, 
        description="Name of habit",
    )
    sched_days: list[Weekday] = Field(
        ..., 
        min_items=1, 
        max_items=7,
        description="Select the days of the week you wish to complete this habit",
    )
    habit_time: int = Field(
        ...,
        ge=1,
        le=480,
        description="Estimate the number of minutes to complete this habit",
    )

#Class inherited from HabitBase that defines the data format the user must conform to create a new habit
class HabitCreate(HabitBase):
    """Payload when user creates a new habit"""

#Schema class for validating partial updates to a user habit
class HabitUpdate(HabitBase):
    habit_name: str | None = Field(
        None, 
        min_length=1, 
        description="Updated habit name",
    )
    sched_days: list[Weekday] | None = Field(
        None, 
        min_items=1, 
        max_items=7,
        description="Select the days of the week you wish to complete this habit",
    )
    habit_time: int | None = Field(
        None,
        ge=1,
        le=480,
        description="Estimate the number of minutes to complete this habit",
    )

#Schema class that defines the entirety of a habit object, which includes backend-owned habit_id and user_id
class Habit(HabitBase):
    habit_id: str
    user_id: str
    habit_streak: int = 0