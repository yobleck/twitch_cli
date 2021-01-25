# twitch_cli
browse twitch, watch streams, interact with chat

## Requires
  - python 3.7+
  - ANSI escape character capable terminal
  - mpv video player
  
  To connect to the irc server you must get an oauth password from: https://twitchapps.com/tmi/
  and put it in ./api/client_info in the chat_pass section
  
  (NOTE: api currently not implemented)
  
  In order to get client id and secret for the api follow these instructions: https://dev.twitch.tv/docs/api/
  
  api startup causes moderate cpu and network spike as it gets live status of all follows


## Controls
  - "q" to quit
  - "w" and "s" to scroll channel selection
  - "p" to start playing stream with mpv
  - "c" to join or leave chat
  - "tab" to toggle chat typing mode
  - while typing "a-zA-Z0-9"(limited special chars) are added to input buffer (screen refresh sometimes eaths inputs. just try again)
  - "backspace" to remove last character from input buffer
  - "enter" to send input buffer as chat message
 
## TODO:
  - irc sometimes fails to connect. just restart (if no error in logs)
  - add proper color coding (sorta works but crude)
  - tell if video is playing or closed to disallow opening multiple streams?
  - fix mpv being left as a zombie after closing
  - check for live status every x amount of time
  - config file to allow changing of video player, username, network threads and other settings
