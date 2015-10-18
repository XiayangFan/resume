import requests, time, json

API_KEY = "1c0e4fac-8ffe-4968-b8eb-f65145e2fc89";

def request_name(name):
	global API_KEY;
	r = requests.get("https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/"+name+"?api_key="+API_KEY)
	if(r.status_code == 404):
		print("Missing player: "+name);
		return None;
	if(r.status_code != 200):
		print("Time out, sleeping 10s")
		time.sleep(10);
		return request_name(name);
	return r;

f = open('list_of_names', 'r');
h = open('id.txt', 'w')
users = [];
for line in f:
	line = line.strip();
	users.append(line);
	r = request_name(line);
	if(r == None):
		continue;
	g = open('players/'+line+'.txt', 'w');
	g.write(r.text);
	g.close();
	j = json.loads(r.text);
	for i in j.keys():
		h.write(str(j[i]["id"])+"\n");


f.close();