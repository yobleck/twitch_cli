# twitch_cli
browse twitch, watch streams, interact with chat

## Requires
  - python 3.7+
  - ANSI escape character capable terminal
  - mpv video player


## Controls
  - "q" to quit
  - "w" and "s" to scroll channel selection
  - "p" to start playing stream with mpv
  - "c" to join or leave chat
  - "tab" to toggle chat typing mode
  - while typing "a-zA-Z0-9" are added to input buffer
  - "backspace" to remove last character from input buffer
  - "enter" to send input buffer as chat message
 
## TODO:
  - irc sometimes fails to connect. just restart (if no error in logs)
  - add proper color coding
  - add ability to send chat messages
  - tell if video is playing or closed to disallow opening multiple streams?
  - fix mpv being left as a zombie after closing
  - twitch api integration to get list of follows and live status
  - config file to allow changing of video player and other settings
