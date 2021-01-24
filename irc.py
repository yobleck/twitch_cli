#https://stackoverflow.com/questions/2968408/how-do-i-program-a-simple-irc-bot-in-python
import socket, sys, time, ssl, json;
def ltm():
    t = time.localtime();
    return str(t.tm_year) + "-" + str(t.tm_mon) + "-" + str(t.tm_mday);

class chat:
    def __init__(self, user):
        self.server = "irc.chat.twitch.tv";
        self.port = 6667;
        self.channel = "";
        self.nick = user;
        
        f = open("./api/client_info", "r"); #get chat password from file
        j = json.load(f);
        f.close();
        self.password = j["chat_pass"]; #not quite as much of an idiot   #https://dev.twitch.tv/docs/irc/guide#connecting-to-twitch-irc

        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        print("connecting");
        self.irc.connect((self.server, self.port));
        self.irc.setblocking(False);
        
        print("sending info");
        self.irc.send(bytes("PASS " + self.password + "\r\n", "utf-8"));
        self.irc.send(bytes("NICK "+ self.nick + "\n", "utf-8")); #sets nick
        #self.irc.send(bytes("USER " + self.nick + " " + self.nick + " " + self.nick + " :This is a test\n", "utf-8")); #user authentication
        print("info sent");
        
        
        f = open("./logs/" + ltm() + ".log","a"); #header for new log session
        f.write("\n" + time.ctime() + ": #####NEW SESSION#####\n");
        f.close();
        time.sleep(.3);
    
    
    def get_text(self):
        try:
            text = self.irc.recv(2040).decode("utf-8");
            
            if("PING" in text):
                self.irc.send(bytes("PONG " + text.split()[1] + "\r\n", "utf-8"));
            
            f = open("./logs/" + ltm() + ".log","a"); #logging
            f.write(time.ctime() + ": " + text + "\n");
            f.close();
            
            return text;

        except Exception as e:
            return "nothing new";
    
    
    def send_text(self, text, c_name):
        self.irc.send(bytes("PRIVMSG " + c_name + " :" + text + "\n", "utf-8"));
        
        f = open("./logs/" + ltm() + ".log","a"); #logging
        f.write(time.ctime() + ": MESSAGE SENT: " + text + "\n");
        f.close();
    
    
    def join(self, c_name):
        self.irc.send(bytes("JOIN " + str(c_name) + "\r\n", "utf-8")); #c_name must start with #
        
    def part(self, c_name):
        self.irc.send(bytes("PART " + str(c_name) + "\r\n", "utf-8"));
    
    def quit(self):
        self.irc.send(bytes("QUIT\n", "utf-8"));
    


"""
#testing
cht = chat(user="yobleck");
cht.jp_channel(j_p="JOIN", c_name="#heyzeusherestoast");

while(True):
    time.sleep(0.5);
    
    results = cht.get_text();
    
    if(results == "nothing new"):
        print("\033[F\33[2K" + results);
    else:
        print("\33[2K" + results);
    
    if("PING" in results):
        print("\33[2K PONGING\n");
"""
