import pytest

from logic import (
    Rank,
    get_rank_from_ae,
    calculate_habit_base,
    calculate_streak_mp,
    calculate_ae_rewarded,
)

# -----------------------
# get_rank_from_ae tests
# -----------------------

def test_get_rank_negative_raises():
    with pytest.raises(ValueError):
        get_rank_from_ae(-1)

@pytest.mark.parametrize("ae, expected_rank", [
    (0, Rank.MUD),
    (49, Rank.MUD),
    (50, Rank.CLAY),
    (149, Rank.CLAY),
    (150, Rank.BRONZE),
    (349, Rank.BRONZE),
    (350, Rank.IRON),
    (649, Rank.IRON),
    (650, Rank.GOLD),
    (1049, Rank.GOLD),
    (1050, Rank.PLATINUM),
    (1549, Rank.PLATINUM),
    (1550, Rank.DIAMOND),
])
def test_get_rank_boundaries(ae, expected_rank):
    assert get_rank_from_ae(ae) == expected_rank


# -----------------------
# calculate_habit_base tests
# -----------------------

@pytest.mark.parametrize("t", [0, -5, 481, 9999])
def test_habit_base_invalid_time_raises(t):
    with pytest.raises(ValueError):
        calculate_habit_base(t)

def test_habit_base_one_minute():
    # bracket 1: rate=5, so 1/5 = 0.2
    assert calculate_habit_base(1) == pytest.approx(0.2)

def test_habit_base_60_minutes():
    # 60/5 = 12
    assert calculate_habit_base(60) == pytest.approx(12.0)

def test_habit_base_61_minutes():
    # first 60 min: 60/5 = 12
    # next 1 min at rate=7: 1/7
    assert calculate_habit_base(61) == pytest.approx(12.0 + (1/7))

def test_habit_base_120_minutes():
    # 60/5 + 60/7
    assert calculate_habit_base(120) == pytest.approx((60/5) + (60/7))

def test_habit_base_480_minutes():
    # sum all brackets fully:
    # (60/5) + (60/7) + (60/8) + (60/14) + (240/17)
    expected = (60/5) + (60/7) + (60/8) + (60/14) + (240/17)
    assert calculate_habit_base(480) == pytest.approx(expected)

def test_habit_base_monotonicity_spot_check():
    assert calculate_habit_base(200) > calculate_habit_base(199)


# -----------------------
# calculate_streak_mp tests
# -----------------------

def test_streak_mp_non_int_raises():
    with pytest.raises(TypeError):
        calculate_streak_mp(3.5)

def test_streak_mp_negative_raises():
    with pytest.raises(ValueError):
        calculate_streak_mp(-1)

def test_streak_mp_zero_is_one():
    assert calculate_streak_mp(0) == pytest.approx(1.0)

def test_streak_mp_linear_growth():
    assert calculate_streak_mp(1) == pytest.approx(1.025)
    assert calculate_streak_mp(10) == pytest.approx(1.25)

def test_streak_mp_caps_at_two():
    assert calculate_streak_mp(40) == pytest.approx(2.0)
    assert calculate_streak_mp(400) == pytest.approx(2.0)


# -----------------------
# calculate_ae_rewarded tests
# -----------------------

def test_ae_rewarded_integration_small():
    # habit_time=60 => base 12.0
    # streak=0 => mp 1.0
    # int(12.0*1.0)=12
    assert calculate_ae_rewarded(60, 0) == 12

def test_ae_rewarded_truncates():
    # 1 minute => base 0.2
    # streak=1 => mp 1.025 => 0.205 -> int => 0
    assert calculate_ae_rewarded(1, 1) == 0
