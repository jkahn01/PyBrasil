#!/usr/bin/env python

import sys, pprint, json, smtplib

from Rankings import rankings
from Teams import teams
from DraftOrder import draft_order
from Results import results, round_value
from email.mime.text import MIMEText

num_teams = len(teams)
points_for_win = 3
points_for_tie = 1

def draft(rankings, teams, draft_order):
	results = {}
	taken_teams = []
	round = 0
	while (len(taken_teams) != len(teams)):
		for manager in draft_order:
			if (manager not in results):
				results[manager] = {}
			manager_rankings = rankings[manager]
			for team in sorted(manager_rankings, key=manager_rankings.get):
				if (team not in taken_teams):
					taken_teams.append(team)
					results[manager][team] = round+1
					break
		draft_order.reverse()
		round += 1
	return results

def score_confidence(rankings, results):
	managers = rankings.keys()
	scores = {}
	for manager in managers:
		if manager not in scores:
			scores[manager] = 0
		for result in results:
			if result.Score1FT is None:
				continue
			elif result.round.type == '3rd place':
				continue
			elif (result.Score1FT > result.Score2FT):
				scores[manager] += (num_teams - rankings[manager][result.Team1] + 1) * points_for_win
			elif (result.Score1FT < result.Score2FT):
				scores[manager] += (num_teams - rankings[manager][result.Team2] + 1) * points_for_win
			else:
				scores[manager] += ((num_teams - rankings[manager][result.Team1] + 1) * points_for_tie) + ((num_teams - rankings[manager][result.Team2] + 1) * points_for_tie)
	return scores

def score_draft(draft_results, results):
	managers = draft_results.keys()
	scores = {}
	score_multiplier = 1
	for manager in managers:
		if manager not in scores:
			scores[manager] = 0
		for result in results:
			if result.Score1FT is None:
				continue
			elif (result.Score1FT + result.Score1OT + result.Score1PK > result.Score2FT + result.Score1OT + result.Score1PK):
				scores[manager] += points_for_win * draft_results[manager][result.Team1] * round_value(result.round.type) if result.Team1 in draft_results[manager] else 0
			elif (result.Score1FT + result.Score1OT + result.Score1PK < result.Score2FT + result.Score1OT + result.Score1PK):
				scores[manager] += points_for_win * draft_results[manager][result.Team2] * round_value(result.round.type) if result.Team2 in draft_results[manager] else 0
			else:
				scores[manager] += points_for_tie * draft_results[manager][result.Team1] * round_value(result.round.type) if result.Team1 in draft_results[manager] else 0
				scores[manager] += points_for_tie * draft_results[manager][result.Team2] * round_value(result.round.type) if result.Team2 in draft_results[manager] else 0
	return scores


if __name__ == '__main__':
	draft_results = draft(rankings, teams, draft_order)
	confidence = score_confidence(rankings, results)
	draft = score_draft(draft_results, results)
	pp = pprint.PrettyPrinter(indent=4)
	print("Confidence Results")
	pp.pprint(confidence)
	print("Draft Results")
	pp.pprint(draft)

        #email results
        subject = 'Latest results'
        from_address = 'noreply@alexalexiou.com'
        to_addresses = ['alex.alexiou@gmail.com', 'jason.kahn@gmail.com', 'alex2iou@yahoo.com']
        confidence_string = json.dumps( confidence, sort_keys = True, indent = 2, separators=('\n', ':') )
        msg = MIMEText( confidence_string )
        msg['Subject'] = subject
        msg['From'] = from_address
        msg['To'] = ",".join( to_addresses )
        s = smtplib.SMTP('localhost')
        s.sendmail( from_address, to_addresses, msg.as_string() )
        s.quit()
