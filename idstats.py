import json
import urllib2
def idstats(id):
    response = urllib2.urlopen("https://na.api.pvp.net/api/lol/na/v2.2/match/" + str(id) + "?api_key=497286e9-f643-4e1c-8028-3149a3887044")
    data = json.load(response)
    for i in range(0,4):
        summoner = data["participantIdentities"][i]["player"]["summonerId"]
        team = data["participants"][i]["teamId"]
        team1 = 0
        if data["teams"][0]["teamId"] == team:
            team1 = 0
        else:
            team1 = 1
        f = open(str(summoner) + ".txt", "a")
        f.write("Kills:" + str(data["participants"][i]["stats"]["kills"]) + ", Assists:" + str(data["participants"][i]["stats"]["assists"]) + ", Deaths:" + str(data["participants"][i]["stats"]["deaths"]) + ", matchDuration" + str(data["matchDuration"]) + ", blood" + data["teams"][i]["firstBlood"])
        f.write("\n")
        f.close()
idstats(1581788407)
