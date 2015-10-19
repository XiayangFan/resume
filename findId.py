import requests, time, json

API_KEY = "497286e9-f643-4e1c-8028-3149a3887044";

def downloadMatchId(summoner_id):
	global API_KEY
	r = requests.get("https://na.api.pvp.net/api/lol/na/v2.2/matchlist/by-summoner/"+str(summoner_id)+"?api_key="+API_KEY)
	if r.status_code != 200:
		print("Time out, sleeping 10s");
		time.sleep(10);
		return downloadMatchId(summoner_id)

	return r.text;

"""
Returns -1 if the data is bad
"""
def getValidMatchId(match, seen_id):
	if(match["queue"] != "RANKED_TEAM_5x5"):
		return -1;
	match_id = int(match["match_id"]);
	if(match_id in seen_id):
		return -1;;
	return match_id;


def main():
	matches, summoners = init();
	try:
		for i in summoners.keys():
		m = downloadMatchId(i);
		j = json.loads(m);
		ml = j["matches"];
		for j in ml:
			match_id = getValidMatchId(j)
			if(match_id == -1):
				#Invalid match Id or seen, skip
				continue;
		matches.append(match_id)
		download_id_stats(match_id);
	except Exception as e:
		print(e)
		quit(matches);

	quit(matches)


def init():
	matches = [];
	players = {};
	try:
		f = open('matches.txt', 'r')
	except:
		return matches;

	g = open('players.txt', 'r')

	for line in f:
		matches.append(int(line.strip()));
	f.close();

	for line in g:
		x = line.strip().split("     ");
		players[int(x[1])] = x[0];
	g.close();
	return matches, players


def quit(matches):
	f = open('matches.txt', 'w');
	for match in matches:
		f.write(str(match));

	f.close()



def grade(k, d, a, duration, fb):
	kda_ratio = (k+d)/a;
	kda_score = 0;
	if(kda_ratio<.5):
		kda_score = 1
	else if(kda_ratio<1):
		kda_score = 2;
	else if(kda_ratio<2):
		kda_score = 3;
	else if(kda_ratio<4):
		kda_score = 4;
	else:
		kda_score = 5;

	d_mult = 0;
	if(duraion<1000):
		d_mult = -5;
	else if(duration<1500):
		d_mult = -4
	else if(duration<2000):
		d_mult = -2
	else:
		d_mult = -0
	
	d_mult = d*-1;

	fbonus = 0;
	if(fb):
		fbonus = 1;

	totalscore = kda_score+d_mult+fbonus

	if(totalscore<0):
		return 0;
	else if(totalscore>10):
		return 10;

	return totalscore;

main();
