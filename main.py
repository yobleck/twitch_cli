import sys, os, time, subprocess;
import getch, irc, tui, twitch_api;

f = open("./following/follows", "r");
follow_list = [x.rstrip() for x in f.readlines()];
f.close();


###chat vars
chat = irc.chat("yobleck");
current_chat = "#" + str(follow_list[0]);
#chat.join(current_chat);
chat_list = [];
last_chat = "placeholder";
in_chat = False;
input_text = "";


###ui vars
width, height = tui.get_xy();

follow_scroll = [0, height];
follow_select = 0;
playing = False;
channel_info = [];


running = True;
while(running):
    #time.sleep(0.01);
    char = getch.getch_noblock();
    
    if(char in ["q", "\x1b"]):
        running = False;
        chat.part(current_chat);
        chat.quit();
    
    #channel selection
    if(char == "w" and follow_select > 0):
        follow_select -= 1;
        current_chat = "#" + str(follow_list[follow_select]);
    
    if(char == "s" and follow_select < len(follow_list)-1):
        follow_select += 1;
        current_chat = "#" + str(follow_list[follow_select]);
    
    if(char == "c"):
        if(in_chat):
            chat.part(current_chat);
            in_chat = False;
        else:
           chat.join(current_chat);
           in_chat = True;
    
    if(char == "p" and not playing): #start stream
        playing = True;
        subprocess.Popen(["mpv", "https://www.twitch.tv/" + str(follow_list[follow_select])], #use Popen cause run is blocking
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL);
    
    
    #check to see if any new chat msg and add to list
    [chat_list.append(x) for x in tui.format_text(chat.get_text()) if x != "nothing new"];
    if(len(chat_list) > 2*height): #remove oldest messages to manage memory
        del chat_list[0];
    
    if(char != -1 or last_chat != chat_list[-1]):
        last_chat = chat_list[-1];
        #render contents on screen
        print("\033[2J\033[H", end=""); #clear screen and return cursor to 0,0
        print(tui.format_display(follow_list, "follows: " + str(follow_list[follow_select]), False));
        print("\033[H", end=""); #return cursor to 0,0
        print(tui.format_display(chat_list, "chat: " + str(current_chat), True));

#end while loop
print("\033[2J\033[H");
#"""
