import json, requests, time

"""
Writes victories to the following players
"""

def idstats(id):
    r = requests.get("https://na.api.pvp.net/api/lol/na/v2.2/match/" + str(id) + "?api_key=497286e9-f643-4e1c-8028-3149a3887044")
    if r.status_code != 200:
        print("Time out, sleeping 10s");
        time.sleep(10);
        return idstats(id)
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






def grade(k, d, a, duration, fb):
    kda_ratio = (k+d)/a;
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
        d_mult = 5;
    elif(duration<1500):
        d_mult = 4
    elif(duration<2000):
        d_mult = 2
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
    

idstats(1581788407)