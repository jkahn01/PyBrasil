#!/usr/bin/env python

import sys, pprint

from Rankings import rankings
from Teams import teams
from DraftOrder import draft_order
from Results import results

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
			elif (result.Score1FT > result.Score2FT):
				scores[manager] += (num_teams - rankings[manager][result.Team1] + 1) * points_for_win
			elif (result.Score1FT < result.Score2FT):
				scores[manager] += (num_teams - rankings[manager][result.Team2] + 1) * points_for_win
			else:
				scores[manager] += ((num_teams - rankings[manager][result.Team1] + 1) * points_for_tie) + ((num_teams - rankings[manager][result.Team2] + 1) * points_for_tie)
	return scores

if __name__ == '__main__':
	draft_results = draft(rankings, teams, draft_order)
	confidence = score_confidence(rankings, results)
	pp = pprint.PrettyPrinter(indent=4)
	#print("Draft results:")
	#pp.pprint(draft_results)
	
	print("Confidence Results")
	pp.pprint(confidence)
