import sys, os, time;
import getch, irc, tui, twitch_api;


f = open("./following/follows", "r");
follow_list = [x.rstrip() for x in f.readlines()];
f.close();
#print(follow_list);

#"""
chat = irc.chat("yobleck");
current_chat = "#heyzeusherestoast";
chat.jp_channel("JOIN", current_chat);
chat_list = [];


#misc vars
in_focus = "chat"; #or follows or info
is_visible = "follows"; #or info

#"""
running = True;
while(running):
    time.sleep(0.1);
    char = getch.getch_noblock();
    
    if(char in ["q", "\x1b"]):
        running = False;
        chat.jp_channel("PART", current_chat); 
        chat.quit();
    
    chat_list.append(chat.get_text()[:30]);
    
    print("\033[2J\033[H"); #clear screen and return cursor to 0,0
    print(tui.format_and_display(follow_list, "follows", False));
    print("\033[H"); #return cursor to 0,0
    print(tui.format_and_display(chat_list[-15:], "chat", True));

#end while loop
#"""
