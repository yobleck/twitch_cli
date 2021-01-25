import json, requests;

f = open("./api/client_info.json", "r");
j_client = json.load(f);
f.close();
client_id = j_client["client-id"];
client_secret = j_client["client-secret"];
#print(client_id, client_secret);

f = open("./api/oauth.json", "r");
j_oauth = json.load(f);
f.close();
oauth_token = j_oauth["access_token"];

##########

def get_channel_info(c_name):
    headers = {"client-id": client_id, "Authorization": "Bearer " + oauth_token,};
    params = (("query", c_name),);
    
    response = requests.get("https://api.twitch.tv/helix/search/channels", headers=headers, params=params);
    #print(response.status_code);
    
    results = json.loads(response.text.rstrip()); #str -> json obj
    return results["data"][0];

##########

def get_user_info(c_name):
    headers = {"client-id": client_id, "Authorization": "Bearer " + oauth_token,};
    params = (("login", c_name),);
    
    response = requests.get("https://api.twitch.tv/helix/users", headers=headers, params=params);
    #print(response.status_code);
    if(response.status_code != requests.codes.ok):
        raise Exception("get_user_info returned: " + str(response.status_code) + " status code");
    
    results = json.loads(response.text.rstrip());
    return results;

##########

def get_user_follows(c_name, pagination): #pagination is None or string
    if(type(c_name) is str):
        user_id = int(get_user_info(c_name)["data"][0]["id"]); #convert user name to id type int
    elif(type(c_name) is int):
        user_id = c_name; #username is already user id
    else:
        raise Exception("c_name must be username as str or id as int. got: " + str(c_name) + " of type: " + str(type(c_name)));
    
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
        next_page = get_user_follows(user_id, results["pagination"]["cursor"]);
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
        #TODO: not actually sure what to do here
        pass;



#https://dev.twitch.tv/console/apps     my app
#https://dev.twitch.tv/docs/api/reference      actual api methods
#https://dev.twitch.tv/docs/authentication
#https://dev.twitch.tv/docs/authentication/getting-tokens-oauth
#
