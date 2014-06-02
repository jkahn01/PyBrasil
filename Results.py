#!/usr/bin/env python

import json, urllib2

rounds_url = 'http://footballdb.herokuapp.com/api/v1/event/world.2014/rounds'
game_base_url = 'http://footballdb.herokuapp.com/api/v1/event/world.2014/round/'

class Game:
	def __repr__ (self):
		return '{0} {1}-{2} {3}'.format(self.Team1, self.Score1FT, self.Score2FT, self.Team2)

class Round:
	pass

def load_results():
	games = []
	rounds = []
	results = []
	round_dict = json.loads(urllib2.urlopen(rounds_url).read())
	for round in round_dict['rounds']:
		r = Round()
		r.number = round['pos']
		if 'Matchday' in (round['title']):
			r.type = 'Group'
		elif 'Match for third' in (round['title']):
			r.type = '3rd place'
		else:
			r.type = 'Elimination'
		rounds.append(r)
	for round in rounds:
		result_url = game_base_url + str(round.number)
		result_dict = json.loads(urllib2.urlopen(result_url).read())
		for result in result_dict['games']:
			g = Game()
			g.Team1 = result["team1_title"].replace(u'\xf4', u'o')
			g.Team2 = result["team2_title"].replace(u'\xf4', u'o')
			g.Score1FT = result["score1"]
			g.Score2FT = result["score2"]
			g.Score1OT = result["score1ot"] if result["score1ot"] is not None else 0
			g.Score2OT = result["score2ot"] if result["score2ot"] is not None else 0
			g.Score1PK = result["score1p"] if result["score1p"] is not None else 0
			g.Score2PK = result["score2p"] if result["score2p"] is not None else 0
			g.round = round
			results.append(g)
	return results

results = load_results()

if __name__ == '__main__':
	print load_results()