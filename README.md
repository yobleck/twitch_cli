# twitch_cli
browse twitch, watch streams, interact with chat

## Requires
  - python 3.7+
  - python requests module
  - ANSI escape character capable terminal
  - mpv video player
  
## Notes
  To connect to the irc server you must get an oauth password from: https://twitchapps.com/tmi/
  and put it in ./api/client_info in the chat_pass section
  
  Make user the config var "run_initial_setup" is "True" the first time you run the program, and give it some time. This is caused by some annoying twitch api design choices.
  
  In order to get client id and secret for the api follow these instructions: https://dev.twitch.tv/docs/api/
  
  api startup causes moderate cpu and network spike as it gets live status of all follows
  
  mpv stutters on startup. pausing the stream for a second allows it to build up a buffer
  
  irc sometimes fails to connect. just restart (if no error in logs)


## Controls
  - "q" to quit
  - "w" and "s" to scroll channel selection
  - "p" to start playing stream with mpv
  - "c" to join or leave chat
  - "tab" to toggle chat typing mode
  - while typing "a-zA-Z0-9"(limited special chars) are added to input buffer (screen refresh sometimes eaths inputs. just try again)
  - "backspace" to remove last character from input buffer
  - "enter" to send input buffer as chat message

## Config
  - username should be your username as seen in twitch chat
  - get_channel_info_threads should be "default" or a number from 1 to number of cpu threads(examples 4, 8, 16)
 
## TODO:
  - irc sometimes fails to connect
  - add proper color coding (sorta works but crude)
  - rewrite api interface to ask for info on multiple channels at the same time instead of sending multiple requests
  - check for live status every x amount of time
  - config file to allow changing of video player, username, network threads and other settings
