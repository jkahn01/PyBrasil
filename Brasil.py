#!/usr/bin/env python

import sys

from Rankings import rankings
from Teams import teams
from DraftOrder import draft_order

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

if __name__ == '__main__':
	draft_results = draft(rankings, teams, draft_order)
	print draft_results