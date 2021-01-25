import sys, os, time, subprocess;
from multiprocessing import Pool;
import getch, irc, tui, twitch_api;


follow_bad_name = [x["to_name"] for x in twitch_api.get_user_follows("yobleck", None)["data"]]; #get list of follows
#this list uses the wrong name format

print("loading follows...");
with Pool(len(os.sched_getaffinity(0))) as p:
    follow_list = p.map(twitch_api.get_channel_info, follow_bad_name);


###chat vars
chat = irc.chat("yobleck");
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
        subprocess.Popen(["mpv", "https://www.twitch.tv/" + str(follow_list[follow_select]["display_name"])], #uses Popen cause run is blocking
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); #TODO: properly kill process after exit (no zombies allowed)
    
    #send chat messages
    if(typing and char != -1): #input text but disallow some special characters
        if(char not in ["\t", "\n", "\r"] and len(input_text) < width-9): #limit length for testing
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
        input_text = "";
    
    
    #check to see if any new chat msg and add to list
    [chat_list.append(x) for x in tui.format_text(chat.get_text()) if x != "nothing new"];
    if(len(chat_list) > 2*height): #remove oldest messages to manage memory
        del chat_list[0];
    
    if(char != -1 or last_chat != chat_list[-1]): #only updates screen when something happens
        last_chat = chat_list[-1]; #TODO: this line will indicate crash if chat did not connect properly
        ###render contents on screen###
        print("\033[2J\033[H", end=""); #clear screen and return cursor to 0,0
        
        #get correct name from json list and part of list that is on screen
        print(tui.format_display([x["display_name"] + " live:" + str(x["is_live"]) for x in follow_list[follow_scroll[0]:follow_scroll[1]]],
                                 "follows: " + str(follow_list[follow_select]["display_name"]), False));
        
        print("\033[H", end=""); #return cursor to 0,0
        
        print(tui.format_display(chat_list, "chat: " + str(current_chat) + " typing=" + str(typing), True));
        
        print("\033[Finput: \033[33m" + input_text + "\033[0m");

#end while loop
print("\033[2J\033[H");
#"""
