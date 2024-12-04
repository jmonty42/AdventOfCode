import heapq
import json

from datetime import datetime, UTC

with open("leaderboard.json", "r") as file:
    leaderboard = json.load(file)

day_timelines = {}
member_scores = {}

for member in leaderboard["members"].values():
    member_scores[member["name"]] = 0
    for day, stars in member["completion_day_level"].items():
        if day not in day_timelines:
            day_timelines[day] = []
        for star_key, star_object in stars.items():
            ordinal = 'first'
            if star_key == '2':
                ordinal = 'second'
            heapq.heappush(day_timelines[day], (star_object["get_star_ts"], member["name"], ordinal))

for day in range(1,26):
    if str(day) in day_timelines:
        members_yet_to_earn_first_star = len(member_scores)
        members_yet_to_earn_second_star = len(member_scores)
        print("For Day {}'s challenge:".format(day))
        while day_timelines[str(day)]:
            unix_time, member, ordinal = heapq.heappop(day_timelines[str(day)])
            points_earned = members_yet_to_earn_first_star if ordinal == 'first' else members_yet_to_earn_second_star
            print("\tAt {}, {} earned their {} star, earning {} points, bringing their score to {}".format(
                datetime.fromtimestamp(unix_time, UTC).strftime("%H:%M:%S on %b %d (%Z)"),
                member, ordinal, points_earned, member_scores[member] + points_earned
            ))
            if ordinal == 'first':
                members_yet_to_earn_first_star -= 1
            else:
                members_yet_to_earn_second_star -= 1
            member_scores[member] += points_earned