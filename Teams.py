#!/usr/bin/env python

import json, urllib2

team_url = 'http://footballdb.herokuapp.com/api/v1/event/world.2014/teams'

def get_teams():
	team_dict = json.loads(urllib2.urlopen(team_url).read())
	teams = []
	for team in team_dict['teams']:
		teams.append(team['title'].replace(u'\xf4', u'o'))
	return teams

teams = get_teams()

if __name__ == '__main__':
	for team in get_teams():
		print team