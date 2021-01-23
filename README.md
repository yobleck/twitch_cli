# twitch_cli
browse twitch, watch streams, interact with chat

## Requires
  - python 3.7+
  - ANSI escape character capable terminal
  - mpv video player


## controls
  - "q" to quit
  - "w" and "s" to scroll channel selection
  - "p" to start playing stream with mpv
  - "c" to join or leave chat
 
## TODO:
  - add proper color coding
  - fix input issues (not regsistering/latency)
  - screen flicker when polling rate is too high (only update screen when list change?)
  - add ability to send chat messages
  - tell if video is playing or closed to disallow opening multiple streams?
  - fix a variety of regex issues
  - twitch api integration to get list of follows and live status
  - config file to allow changing of video player and other settings
