#!/usr/bin/env python3

import pytest
from google_calendar import GoogleCalendar


def test_list_calendars():
    calendar = GoogleCalendar()
    calendar.get_calendars()

    calendar_summary = [x['summary'] for x in calendar.calendar_list]
    assert 'Testing' in calendar_summary

def test_event_calendars():
    calendar = GoogleCalendar()

    assert 'Test 1' ==  calendar.get_events()