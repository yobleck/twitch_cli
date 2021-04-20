import sys, os, time, json, subprocess;
import getch, irc, tui, twitch_api; #local imports
from distutils.util import strtobool;

cwd = sys.path[0] + "/";

#load config
f = open(cwd + "config.json", "r");
j_config = json.load(f);
f.close();
username = j_config["username"];
if(strtobool(j_config["run_initial_startup"])):
    print("running intial set up...");
    subprocess.run(["python", "initial_startup.py"],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL);
    j_config["run_initial_startup"] = "False";
    f = open(cwd+ "config.json", "w"); json.dump(j_config, f, indent=2); f.close();

#load follows
f = open(cwd+ "following/follows.json", "r");
j_follows = json.load(f);
f.close();
follow_list = j_follows["data"];


print("loading follows live status...");
follow_live = twitch_api.get_stream_info_mp([x["user_id"] for x in follow_list]); #get follow live status

for x in range(len(follow_list)):
    if(follow_live[x]):
        follow_list[x]["is_live"] = True; #TODO: if live then "i" key to draw temp window with stream info when selected
    else:
        follow_list[x]["is_live"] = False;


###chat vars
chat = irc.chat(username);
highlighted_chat = "#" + str(follow_list[0]["display_name"]);
current_chat = "";
chat_list = [];
last_chat = "placeholder";
in_chat_room = False;
typing = False;
input_text = "";


###ui vars
width, height = tui.get_xy();

follow_scroll = [0, height-3];
follow_select = 0;
playing = False;
channel_info = [];


running = True;
while(running):
    #time.sleep(0.01);
    char = getch.getch_noblock();
    
    if(char in ["q", "\x1b"] and not typing):
        running = False;
        chat.part(current_chat);
        chat.quit();
    
    #channel selection
    if(char == "w" and follow_select > 0 and not typing):
        follow_select -= 1;
        highlighted_chat = "#" + str(follow_list[follow_select]["display_name"]);
        if(follow_select < follow_scroll[0]):
            follow_scroll[0] -= 1; follow_scroll[1] -= 1; #scrolling list up
    
    if(char == "s" and follow_select < len(follow_list)-1 and not typing):
        follow_select += 1;
        highlighted_chat = "#" + str(follow_list[follow_select]["display_name"]);
        if(follow_select >= follow_scroll[1]):
            follow_scroll[0] += 1; follow_scroll[1] += 1; #scrolling list down
    
    #join and leave chat
    if(char == "c" and not typing):
        if(in_chat_room):
            chat.part(current_chat);
            current_chat = "";
            in_chat_room = False;
        else:
           chat.join(highlighted_chat);
           current_chat = highlighted_chat;
           in_chat_room = True;
    
    #start stream
    if(char == "p" and not playing and not typing):
        playing = True;
        sp = subprocess.Popen(["mpv", "https://www.twitch.tv/" + str(follow_list[follow_select]["display_name"])], #uses Popen cause run blocks
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL);
    if("sp" in globals()):
        if(sp.poll() is not None):
            del sp;
            playing = False;
    
    
    #send chat messages
    if(typing and char != -1): #input text but disallow some special characters
        if(char not in ["\t", "\n", "\r"] and len(input_text) < width-len(username)-4): #limit length for testing
            input_text += char;
        if(char == "\x7f"): #backspace
            input_text = input_text[:-2];
    if(char == "\t"): #toggle typing mode
        if(typing):
            typing = False;
        elif(not typing):
            typing = True;
    if(char == "\n" and input_text and current_chat): #send message
        chat.send_text(input_text, current_chat);
        [chat_list.append(x) for x in tui.format_text(":" + username + "!: " + input_text)];
        input_text = "";
    
    
    #check to see if any new chat msg and add to list
    [chat_list.append(x) for x in tui.format_text(chat.get_text()) if x != "nothing new"];
    if(len(chat_list) > 2*height): #remove oldest messages to manage memory
        del chat_list[0];
    
    #only updates screen when something happens.
    if(char != -1 or last_chat != chat_list[-1]): #IF YOU ARE SEEING THIS THEN IRC FAILED TO CONNECT JUST TRY AGAIN
        last_chat = chat_list[-1]; #TODO: this line will indicate crash if chat did not connect properly
        ###render contents on screen###
        print("\033[2J\033[H", end=""); #clear screen and return cursor to 0,0
        
        #get correct name from json list and part of list that is on screen
        print(tui.format_display([x["display_name"] + " " + tui.format_bool(x["is_live"]) for x in follow_list[follow_scroll[0]:follow_scroll[1]]],
                                 "follows: " + str(follow_list[follow_select]["display_name"]), False));
        
        print("\033[H", end=""); #return cursor to 0,0
        
        print(tui.format_display(chat_list, "chat: " + str(current_chat) + " type=" + str(typing), True));
        
        print("\033[F\033[33m" + username + ": " + input_text + "\033[0m");

#end while loop
print("\033[2J\033[H");
#"""
