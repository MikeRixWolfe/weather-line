A simple site to put weather in your tmux status bar, or anywhere else.

## Usage

```
set -g status-interval 60
WEATHER='#(curl -s yoursite.tld/weather/<zipcode>)'
set -g status-right "$WEATHER | %H:%M %d-%b-%y"
```
