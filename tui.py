import os, re;
rows, columns = os.popen('stty size', 'r').read().split();
rows = int(rows); columns = int(columns);

def get_xy():
    return (columns, rows);

##########

#regex definitions that only need to be created once
pat_nick = re.compile(r"^:.*?!");
pat_msg = re.compile(r":[^:]*:(.*)");
pat_jp = re.compile(r"PART.*$|JOIN.*$");
e_filter = re.compile(r"[\U0000231A-\U00002B55\U0001F004-\U0001FAD6\U0001F170-\U0001F6F3\U0001F1E6-\U0001F1FC\U0001F3FB-\U0001F3FF]+");#emoji bad
pat_ansi = re.compile(r"\033\[.{1,2}m");

#ANSI Escape Sequences
reset = "\033[0m";
red = "\033[31m";
green = "\033[32m";
yellow = "\033[33m";
blue = "\033[34m";
hor_line = "\u2015"; #horizontal line with no breaks (technically Unicode not ANSI)

##########

def format_text(text): #TODO: embed colors here then filter them out of len() in format_display
    text = re.sub(r"[\n\t\r]*", "", text); #remove non alphanumeric chars
    text = re.sub(e_filter, "", text);
    
    if("PRIVMSG" in text): #condense user messages by stripping out extra info
        text = re.search(pat_nick, text).group(0) + ": " + re.search(pat_msg, text).group(1);
        return [ text[x:x+((columns//2)-1)] for x in range(0, len(text), (columns//2)-1) ]; #chop strings up into window width chunks
    
    if("PART" in text or "JOIN" in text): #simplify text for join and leave channel
        text = re.search(pat_nick, text).group(0) + " " + yellow + re.search(pat_jp, text).group(0) + reset;
        return [ text[x:x+((columns//2)-1)] for x in range(0, len(text), (columns//2)-1) ]; #chop strings up into window width chunks
    
    #if does not match any above just do minimum of splitting text
    return [ text[x:x+((columns//2)-1)] for x in range(0, len(text), (columns//2)-1) ]; #chop strings up into window width chunks

##########

def format_display(str_list, win_type, in_focus): #win_type= follows, chat
    if(type(str_list) is not list):
        raise Exception("input must be list");
    
    buff = ""; #moves cursor over to right middle of screen without overwriting left side if win_type="chat"
    border_color = green;
    content_color = green;
    border_move = "\033[" + str(columns//2) + "G";
    if("chat" in win_type):
        buff = "\033[1C"*(columns//2); #https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797    ANSI escape sequences
        border_color = blue;
        content_color = green;
        border_move = "\033[" + str(columns) + "G";
    
    
    output = "";
    output += buff + border_color + str(win_type) + "\u2015"*(columns//2-len(win_type)) + "\n"; #top border
    
    
    str_list = str_list[-(rows-3):]; #only get last set of lines that will fit on screen
    for x in str_list: #contents of chat
        output += buff + "|" + content_color + re.sub(pat_nick, red+r"\g<0>"+reset, x) + border_move + border_color + "|\n";
    #" "*( columns//2-2-len(str(x)) )
    
    filler_h = rows - len(str_list) -3;
    output += (buff + border_color + "|" + " "*(columns//2-1) + "|\n")*(filler_h); #fills out the bottom if chat doesn't go all the way down
    
    
    output += buff + border_color + "\u2015"*(columns//2) + reset; #bottom border
    
    return output;

##########

def format_bool(i_bool): #to make true values stand out from false values by color
    if(i_bool):
        return blue + str(i_bool) + reset;
    else:
        return str(i_bool);

"""
#testing
print(format_display([1,"CS",3,4,5,"RT",7,8], "follows", False));
print("\033[H");
print(format_display([1,2,"POGGERS",4,5,6,7,"bob"], "chat", True));
"""
