from enum import Enum
from database import *
from schemas import HabitCreate, HabitUpdate, Habit
from uuid import uuid4

#Domain Exception -> Defining a new type of error that can be raised, that behaves exactly like a type of exception
class HabitLimitExceeded(Exception):
    pass

class HabitNotFound(Exception):
    pass


class Rank(Enum): #Classifying Rank as its own type, where the types of ranks become objects with various metadeta
    MUD = 0
    CLAY = 50
    BRONZE = 150
    IRON = 350
    GOLD = 650
    PLATINUM = 1050
    DIAMOND = 1550
    AMETHYST = 2150
    CHAMPION = 2850
    POWERHOUSE = 3650

    @property #Allows doing rank.min_ae to turn into an int, not a function
    def min_ae(self) -> int: #Allowing .min_ae to be used instead of .value for future scalability and clarity
        return self.value

def get_rank_from_ae(user_ae: int) -> Rank:
    """Returns the rank corresponding to the amount of AE."""
    
    if not isinstance(user_ae, int) or isinstance(user_ae, bool):
        raise TypeError(f"AE must be an integer of rank points, instead got {type(user_ae).__name__}.")

    if user_ae < 0:
        raise ValueError("AE cannot be negative.")

    for rank in reversed(list(Rank)):
        if user_ae >= rank.min_ae:
            return rank
    
    #Defensive programming, theoretically this line should never execute
    raise RuntimeError("Rank cannot be determined.") 

def calc_base_ae(habit_time: int) -> float:
    """Returns the base amount of AE rewarded based on habit time."""
    
   #Tuple is formated such that (1 AE per x minutes, max minutes in this bracket)
    conversion_rate = [
        (5, 60), 
        (7, 60), 
        (8, 60),
        (14, 60), 
        (17, 240),
    ]
    
    base_ae = 0.0
    time_remaining = habit_time
    
    for rate, minute_range in conversion_rate:
        if time_remaining <= minute_range:
            base_ae += (time_remaining/rate)
            break
        else:
            time_remaining -= minute_range
            base_ae += (minute_range/rate)
    
    return base_ae

def calc_streak_mp(habit_streak: int) -> float:
    """Returns the streak multiplier corresponding to a habit's streak. """
    
    if habit_streak < 0:
        raise ValueError("Habit streak cannot be less than 0.")
    
    return min(1 + (0.025 * habit_streak), 2)

def calc_ae_rewarded(
    habit_time: int, 
    habit_streak: int
) -> int:
    """Calculates base ae and streak multiplier and calculates final AE rewarded."""
    
    base_ae = calc_base_ae(habit_time)
    streak_mult = calc_streak_mp(habit_streak)

    return int(base_ae * streak_mult)

def assert_can_create_habit(user_id: str) -> None:
    """Returns True if the user can make a new habit, otherwise returns false."""
    
    habit_count = get_habit_count(user_id)

    if habit_count >= 5:
        raise HabitLimitExceeded(f"User already has {habit_count}/5 habits.")

def create_habit_for_user(
    user_id: str,
    payload: HabitCreate,
) -> Habit:
    """Create a habit tied to the user, if allowed."""
    
    assert_can_create_habit(user_id)
     
    habit = Habit(
        user_id=user_id,
        habit_id=str(uuid4()),
        habit_name=payload.habit_name,
        sched_days=payload.sched_days,
        habit_time=payload.habit_time,
    )
    
    insert_habit(habit)
    return habit

def delete_habit_for_user(
    habit_id: str,
    user_id: str,
) -> None:
    """Delete a habit tied to the user, if allowed."""
    deleted = delete_database_habit(habit_id, user_id)
    
    if not deleted:
        raise HabitNotFound(f"Habit {habit_id} not found.")
    






"""
Add
total_ae = 0
for i in range(1, 31):
    total_ae += calculate_ae_rewarded(300, i)
    total_ae += calculate_ae_rewarded(300, i)
    

#print(total_ae)
#print(get_rank_from_ae(total_ae))
"""
