import json, requests, sys;
from os import sched_getaffinity;
from multiprocessing import Pool;

cwd = sys.path[0] + "/";

#load info from files
f = open(cwd + "api/client_info.json", "r");
j_client = json.load(f);
f.close();
client_id = j_client["client-id"];
client_secret = j_client["client-secret"];
#print(client_id, client_secret);

f = open(cwd + "api/oauth.json", "r");
j_oauth = json.load(f);
f.close();
oauth_token = j_oauth["access_token"];

#load config
f = open(cwd + "config.json", "r");
j_config = json.load(f);
f.close();
username = j_config["username"];
#user_id has to be defined after get_user_info()
if(j_config["get_channel_info_threads"] == "default"):
    num_threads = len(sched_getaffinity(0));
else:
    num_threads = int(j_config["get_channel_info_threads"]);

##########

def get_stream_info(u_id):
    headers = {"client-id": client_id, "Authorization": "Bearer " + oauth_token,};
    params = (("user_id", u_id),);
    #params = (("query", c_name),);
    #response = requests.get("https://api.twitch.tv/helix/search/channels", headers=headers, params=params);
    response = requests.get("https://api.twitch.tv/helix/streams", headers=headers, params=params);
    
    results = json.loads(response.text.rstrip()); #str -> json obj
    #return results["data"][0];
    return results["data"];

#####

def get_stream_info_mp(i_list): #runs multiple instances of above function for speed
    with Pool(num_threads) as p:
        o_list = p.map(get_stream_info, i_list);
    return o_list;

##########

def get_user_info(u_type, u_id_name):
    headers = {"client-id": client_id, "Authorization": "Bearer " + oauth_token,};
    if(u_type == "login"):
        params = (("login", u_id_name),);
    if(u_type == "id"):
        params = (("id", u_id_name),);
    
    response = requests.get("https://api.twitch.tv/helix/users", headers=headers, params=params);
    #print(response.status_code);
    if(response.status_code != requests.codes.ok):
        raise Exception("get_user_info returned: " + str(response.status_code) + " status code");
    
    results = json.loads(response.text.rstrip());
    return results;

user_id = int(get_user_info("login", username)["data"][0]["id"]);

#####

def get_user_info_mp(i_list): #runs multiple instances of above function for speed
    with Pool(num_threads) as p:
        o_list = p.starmap( get_user_info, list(zip(["id"]*len(i_list), i_list)) );
    return o_list;

##########

def get_user_follows(pagination): #pagination is None or string
    headers = {"client-id": client_id, "Authorization": "Bearer " + oauth_token,};
    if(pagination):
        params = (("from_id", user_id),("first", 100),("after", pagination),);
    else:
        params = (("from_id", user_id),("first", 100),);
    
    response = requests.get("https://api.twitch.tv/helix/users/follows", headers=headers, params=params);
    #print(response.status_code);
    if(response.status_code != requests.codes.ok):
        raise Exception("get_user_follows returned: " + str(response.status_code) + " status code");
    
    results = json.loads(response.text.rstrip());
    
    if(results["pagination"]):
        next_page = get_user_follows(results["pagination"]["cursor"]);
        results["data"] += next_page["data"]; 
    
    return results;

##########

#use id and secret to get new oauth token or refresh old token
def get_fresh_oauth_token():
    r = requests.post("https://id.twitch.tv/oauth2/token", data={"client_id":client_id, 
                                                                 "client_secret":client_secret,
                                                                 "grant_type":"client_credentials"});
    if(r.status_code == requests.codes.ok): #TODO: potential formatting issues
        f = open("./api/oauth.json", "w");
        json.dump(r.text.rstrip(),f);
        f.close();
        return r.text;
    else:
        raise Exception("failed to get oauth token http status: " + str(r.status_code));

##########
#refresh old token
def validate_oauth_token():
    rv = requests.get("https://id.twitch.tv/oauth2/validate", headers = {"Authorization": "OAuth " + oauth_token,});
    expires = json.loads(rv.text.rstrip())["expires_in"];
    if(expires < 0):
        #TODO: not actually sure what to do here. might not work for app access token. just get new one?
        pass;



#https://dev.twitch.tv/console/apps     my app
#https://dev.twitch.tv/docs/api/reference      actual api methods
#https://dev.twitch.tv/docs/authentication
#https://dev.twitch.tv/docs/authentication/getting-tokens-oauth
#
