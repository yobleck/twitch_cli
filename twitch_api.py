import json, requests;

f = open("./api/client_info", "r");
j = json.load(f);
f.close();
client_id = j["client-id"];
client_secret = j["client-secret"];
#print(client_id, client_secret);

#use id and secret to get oauth token or refresh old token

def get_info():
    headers = {"client-id": client_id, "Authorization": "Bearer " + client_secret,}; #should be oauth token not secret
    params = (("query", "yobleck"),);
    
    response = requests.get("https://api.twitch.tv/helix/search/channels", headers=headers, params=params);
    
    print(response);

#get_info();



#https://dev.twitch.tv/console/apps

#https://dev.twitch.tv/docs/authentication
#https://dev.twitch.tv/docs/authentication/getting-tokens-oauth
#
