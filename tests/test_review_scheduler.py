from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import pytest

from app.services.review_scheduler import (
    calculate_next_interval,
    schedule_next_review,
    process_review
)

"""
Test cases for calculate_next_interval
"""
def test_again_resets_to_zero():
    assert calculate_next_interval(14, "AGAIN") == 0


def test_ok_moves_one_stage_forward():
    assert calculate_next_interval(1, "OK") == 3


def test_easy_moves_two_stages_forward():
    assert calculate_next_interval(1, "EASY") == 7


def test_ok_caps_at_one_year():
    assert calculate_next_interval(365, "OK") == 365


def test_easy_caps_at_one_year():
    assert calculate_next_interval(224, "EASY") == 365

def test_invalid_decision_raises_error():
    with pytest.raises(ValueError):
        calculate_next_interval(1, "INVALID")

"""
Test cases for schedule_next_review
"""

def test_schedule_one_day_review_at_next_local_midnight():
    now = datetime(
        2026, 9, 16,
        19, 30,
        tzinfo=timezone.utc
    )

    result = schedule_next_review(
        1,
        now,
        "Europe/Dublin"
    )

    expected = datetime(
        2026, 9, 16,
        23, 0,
        tzinfo=timezone.utc
    )

    assert result == expected

def test_schedule_three_day_review_at_local_midnight():
    now = datetime(
        2026, 9, 16,
        19, 30,
        tzinfo=timezone.utc
    )

    result = schedule_next_review(
        3,
        now,
        "Europe/Dublin"
    )
    """
    At first, I thought that the 17th has to be in the expected date,
    but because we are returning the UTC time, the dublin time will be 17/09/26 00:00 while UTC will be 16/09/26 23:00
    """

    expected = datetime(
        2026, 9, 18,
        23, 0,
        tzinfo=timezone.utc
    )

    assert result == expected


def test_schedule_three_day_review_at_local_midnight():
    now = datetime(
        2026, 9, 16,
        19, 30,
        tzinfo=timezone.utc
    )

    result = schedule_next_review(
        3,
        now,
        "Europe/Dublin"
    )

    expected = datetime(
        2026, 9, 18,
        23, 0,
        tzinfo=timezone.utc
    )

    assert result == expected

def test_schedule_three_day_review_at_local_midnight():
    now = datetime(
        2026, 9, 16,
        19, 30,
        tzinfo=timezone.utc
    )

    result = schedule_next_review(
        3,
        now,
        "Europe/Dublin"
    )

    expected = datetime(
        2026, 9, 18,
        23, 0,
        tzinfo=timezone.utc
    )

    assert result == expected



def test_process_review_combines_interval_and_schedule():
    now = datetime(
        2026, 9, 16,
        19, 30,
        tzinfo=timezone.utc
    )

    result = process_review(
        1,
        "EASY",
        now,
        "Europe/Dublin"
    )

    assert result["interval_days"] == 7

    expected_review_time = datetime(
        2026, 9, 22,
        23, 0,
        tzinfo=timezone.utc
    )

    assert result["next_review_at"] == expected_review_time


"""
Tests for process_review function
"""

def test_process_review_easy_from_one_day():
    now = datetime(
        2026, 9, 16,
        19, 30,
        tzinfo=timezone.utc
    )

    result = process_review(
        1,
        "EASY",
        now,
        "Europe/Dublin"
    )

    assert result["interval_days"] == 7

    expected_review_time = datetime(
        2026, 9, 22,
        23, 0,
        tzinfo=timezone.utc
    )

    assert result["next_review_at"] == expected_review_time


def test_process_review_again():
    now = datetime(
        2026, 9, 16,
        19, 30,
        tzinfo=timezone.utc
    )

    result = process_review(
        14,
        "AGAIN",
        now,
        "Europe/Dublin"
    )

    assert result["interval_days"] == 0
    assert result["next_review_at"] == now

def test_process_review_ok():
    now = datetime(
        2026, 9, 16,
        19, 30,
        tzinfo=timezone.utc
    )

    result = process_review(
        3,
        "OK",
        now,
        "Europe/Dublin"
    )

    assert result["interval_days"] == 7