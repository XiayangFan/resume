import requests, time, json

import urllib2

API_KEY = "497286e9-f643-4e1c-8028-3149a3887044";


"""
Given a match ID, writes to the appropriate files.
"""
def idstats(ids):
    r = requests.get("https://na.api.pvp.net/api/lol/na/v2.2/match/" +str(ids)+ "?api_key=497286e9-f643-4e1c-8028-3149a3887044")
    if r.status_code != 200:
        print(r.status_code)
        if(r.status_code == 404):
            print(ids)
        print("Time out, sleeping 10s, IDSTATS")
        time.sleep(10);
        return idstats(ids)
    data = json.loads(r.text)
    winning_id = 0;
    winning_team = data["teams"][0]["winner"];
    if(winning_team):
        winning_team = data["teams"][0]["teamId"];
    else:
        winning_id = 1;
        winning_team = data["teams"][1]["teamId"];

    players = data["participants"];
    losers = [];
    grades = {}
    for p in players:
        p_id = p["participantId"];
        summonerId = data["participantIdentities"][p_id-1]["player"]["summonerId"];
        if(p["teamId"] != winning_team):
            losers.append(summonerId)
            continue;
        kills = int(p["stats"]["kills"])
        assists = int(p["stats"]["assists"])
        death = int(p["stats"]["deaths"])
        match_duration = int(data["matchDuration"])
        fb = data["teams"][winning_id]["firstBlood"];
        grades[summonerId] = grade(kills, death, assists, match_duration, fb);
        
    for i in grades.keys():
        f = open('./players/'+str(i), 'a')
        loser_str = "";
        for j in losers:
            loser_str = loser_str+" "+str(j)
        f.write(str(grades[i])+" "+loser_str+"\n");
        f.close();



def downloadMatches(summoner_id):
    global API_KEY
    r = requests.get("https://na.api.pvp.net/api/lol/na/v2.2/matchlist/by-summoner/"+str(summoner_id)+"?beginTime=1444794610796&endTime=1445399410796&rankedQueues=RANKED_SOLO_5x5&seasons=SEASON2015&api_key="+API_KEY)
    if r.status_code != 200:
        print(r.status_code);
        if(r.status_code == 404):
            print(summoner_id)
        print("Time out, sleeping 10s");
        time.sleep(10);
        return downloadMatches(summoner_id)

    return r.text;

"""
Returns -1 if the data is not a ranked solo RANKED_SOLO_5x5
or the match has already been recorded.
"""
def getValidMatchId(match, seen_id):
    if(match["queue"] != "RANKED_SOLO_5x5"):
        return -1;
    match_id = int(match["matchId"]);
    if(match_id in seen_id):
        return -1;
    return match_id;


def main():
    matches, summoners = init();
    try:
        for i in summoners:
            m = downloadMatches(i);
            j = json.loads(m);
            try:
                ml = j["matches"];
            except Exception as e:
                continue;
            count = 0;
            for j in ml:
                if(count>10):
                    count = 0;
                    break;
                match_id = getValidMatchId(j, matches)
                if(match_id == -1):
                    continue;

                count = count+1;
                matches.append(match_id)
                idstats(match_id);
    except Exception as e:
        print(e)
        raise(e)
        quit(matches);

    quit(matches)


def init():
    matches = [];
    players = [];
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
        players.append(int(x[1]));
    g.close();
    return matches, players


def quit(matches):
    f = open('matches.txt', 'w');
    for match in matches:
        f.write(str(match));

    f.close()





def grade(k, d, a, duration, fb):
    if(d<1):
        d = 1;
    kda_ratio = (k+a)/d;
    kda_score = 0;
    if(kda_ratio<.5):
        kda_score = 1
    elif(kda_ratio<1):
        kda_score = 2;
    elif(kda_ratio<2):
        kda_score = 3;
    elif(kda_ratio<4):
        kda_score = 4;
    else:
        kda_score = 5;

    d_mult = 0;
    if(duration<1000):
        d_mult = 4;
    elif(duration<1500):
        d_mult = 2
    elif(duration<2000):
        d_mult = 1
    else:
        d_mult = 0;

    fbonus = 0;
    if(fb):
        fbonus = 1;

    totalscore = kda_score+d_mult+fbonus

    if(totalscore<0):
        return 0;
    elif(totalscore>10):
        return 10;

    return totalscore;

main();


