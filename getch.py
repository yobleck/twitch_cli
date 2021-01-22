import sys, tty, termios, select; 

def getch_noblock():
    fd = sys.stdin; #.fileno();
    old_settings = termios.tcgetattr(fd);
    #new_settings = termios.tcgetattr(fd);
    #new_settings[3] = new_settings[3] & ~termios.ECHO; #no echo
    try:
        tty.setcbreak(fd);
        r, _, _ = select.select([fd],[],[],.01); #timeout. smaller = more responsive but more cpu usage
        if(r):
            ch = sys.stdin.read(1);
        else:
            ch = -1;
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings);
    return ch;

"""
while True:
    ch = getch_noblock();
    print(ch,end="\n\033[F");
    if ch == "q":
        print("end");
        break; 
"""
