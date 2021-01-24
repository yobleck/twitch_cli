import sys, os, time, subprocess;
import getch, irc, tui;#, twitch_api;

f = open("./following/follows", "r");
follow_list = [x.rstrip() for x in f.readlines()];
f.close();


###chat vars
chat = irc.chat("yobleck");
highlighted_chat = "#" + str(follow_list[0]);
current_chat = "";
chat_list = [];
last_chat = "placeholder";
in_chat_room = False;
typing = False;
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
    
    if(char in ["q", "\x1b"] and not typing):
        running = False;
        chat.part(current_chat);
        chat.quit();
    
    #channel selection
    if(char == "w" and follow_select > 0 and not typing):
        follow_select -= 1;
        highlighted_chat = "#" + str(follow_list[follow_select]);
    
    if(char == "s" and follow_select < len(follow_list)-1 and not typing):
        follow_select += 1;
        highlighted_chat = "#" + str(follow_list[follow_select]);
    
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
        subprocess.Popen(["mpv", "https://www.twitch.tv/" + str(follow_list[follow_select])], #use Popen cause run is blocking
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); #TODO: properly kill process after exit (no zombies allowed)
    
    #send chat messages
    if(typing and char != -1): #input text but disallow some special characters
        if(char not in ["\t", "\n", "\r"]):
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
        last_chat = chat_list[-1];
        #render contents on screen
        print("\033[2J\033[H", end=""); #clear screen and return cursor to 0,0
        print(tui.format_display(follow_list, "follows: " + str(follow_list[follow_select]), False));
        print("\033[H", end=""); #return cursor to 0,0
        print(tui.format_display(chat_list, "chat: " + str(current_chat) + " typing=" + str(typing), True));
        print("\033[Finput: " + input_text);

#end while loop
print("\033[2J\033[H");
#"""
