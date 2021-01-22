import os;
rows, columns = os.popen('stty size', 'r').read().split();
rows = int(rows); columns = int(columns);


def format_and_display(str_list, win_type, in_focus): #win_type= follows, info, chat
    if(type(str_list) is not list):
        raise Exception("input must be list");
    
    buff = "";
    if(win_type == "chat"):
        buff = "\033[1C"*(columns//2); #https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797    ANSI escape sequences 
    
    color = "";
    if(in_focus):
        color = "\033[34m";
    
    output = "";
    output += buff + color + str(win_type) + "\u2015"*(columns//2-len(win_type)) + "\n"; #\u2015 is a horizontal line with no breaks
    
    for x in str_list:
        output += buff + color + "|" + str(x) + " "*(columns//2-2-len(str(x))) + "|\n";
    
    filler_h = rows - len(str_list) -4; #shouldn't need the -5
    output += (buff + color + "|" + " "*(columns//2-2) + "|\n")*(filler_h);
    
    output += buff + color + "\u2015"*(columns//2) + "\033[0m";
    
    return output;

"""
print(format_and_display([1,"CS",3,4,5,"RT",7,8], "info", False));
print("\033[H");
print(format_and_display([1,2,"POGGERS",4,5,6,7,"bob"], "chat", True));
"""
