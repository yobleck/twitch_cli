import sys, json;
import twitch_api;

cwd = sys.path[0] + "/";

data = [{"user_name":x["to_name"],"user_id":x["to_id"]} for x in twitch_api.get_user_follows(None)["data"]]; #get list of follows

#get user display name all lowercase no special characters
login_list = twitch_api.get_user_info_mp([x["user_id"] for x in data]);
for x in range(len(data)):
    data[x]["display_name"] = login_list[x]["data"][0]["login"];

#write out to file
j = {"data":data};
f= open(cwd+ "following/follows.json","w");
json.dump(j,f);
f.close();
