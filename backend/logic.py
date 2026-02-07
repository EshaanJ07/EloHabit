from enum import Enum
from database import get_habit_count

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

def calculate_habit_base(habit_time: int) -> float:
    """Returns the base amount of AE rewarded based on habit time."""
    
    if not isinstance(habit_time, int) or isinstance(habit_time, bool):
        raise TypeError(f"Habit time must be an integer number of minutes, instead got {type(habit_time).__name__}.")
    
    if habit_time <= 0 or habit_time > 480:
        raise ValueError("Time to complete habit must be in between 1 minute and 8 hours.")
    
    #Tuple is formated such that (1 AE per x minutes, max minutes in this bracket)
    conversion_rate = [
        (5, 60), 
        (7, 60), 
        (8, 60),
        (14, 60), 
        (17, 240),
    ]
    
    habit_base = 0.0
    time_remaining = habit_time
    
    for rate, minute_range in conversion_rate:
        if time_remaining <= minute_range:
            habit_base += (time_remaining/rate)
            break
        else:
            time_remaining -= minute_range
            habit_base += (minute_range/rate)
    
    return habit_base

def calculate_streak_mp(habit_streak: int) -> float:
    """Returns the streak multiplier corresponding to a habit's streak. """
    
    if not isinstance(habit_streak, int) or isinstance(habit_streak, bool):
        raise TypeError(f"Habit streak must be an integer of streak, instead got {type(habit_streak).__name__}.")
    elif habit_streak < 0:
        raise ValueError("Habit streak cannot be less than 0.")
    
    return min(1 + (0.025 * habit_streak), 2)

def calculate_ae_rewarded(
        habit_time: int, 
        habit_streak: int
) -> int:
    """Calculates habit base and streak multiplier and calculates final AE rewarded."""
    
    habit_base = calculate_habit_base(habit_time)
    streak_mult = calculate_streak_mp(habit_streak)

    return int(habit_base * streak_mult)

def can_create_habit(user_id: str) -> bool:
    """Returns True if the user can make a new habit, otherwise returns false."""
    
    habit_count = get_habit_count(user_id)

    return habit_count < 5


"""
total_ae = 0
for i in range(1, 31):
    total_ae += calculate_ae_rewarded(300, i)
    total_ae += calculate_ae_rewarded(300, i)
    

#print(total_ae)
#print(get_rank_from_ae(total_ae))
"""
print(Rank.GOLD.min_ae)