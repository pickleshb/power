#!/bin/bash
# POSIX

# Colours
RED='\033[0;31m'
LRED='\033[1;31m'
GREEN='\033[0;32m'
PURPLE='\033[0;35m'
PINK='\033[1;35m'
LCYAN='\033[1;36m'
WHITE='\033[1;37m'
SPINNERC='\033[1;33m'
NC='\033[0m' # No Colour

show_help() {
  echo " "
  echo -e "${LCYAN}This is your helpful help dialogue, here is some help:${NC}\n"
  echo -e "${LRED}-h | --help${NC}         ${WHITE}You should already know this one...${NC}"
  echo -e "${LRED}-l | --nolabels${NC}     ${WHITE}Suppresses label generation${NC}"
  echo -e "${LRED}-d | --nodiagram${NC}    ${WHITE}Stops the pretty diagram from bein drawn${NC}"
  echo -e "${LRED}-s | --nostats${NC}      ${WHITE}Stops the stats from being calculated${NC}\n"
}

spinner() {
  local pid=$1
  local delay=0.3
  while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
    sleep $delay
    printf "${SPINNERC}%c${NC}" "."
    sleep $delay
    printf "${SPINNERC}%c${NC}" ".."
    sleep $delay
    printf "${SPINNERC}%c${NC}" "..."
    sleep $delay
    printf "\b\b\b   \b\b\b"
  done
  printf "\b\b\b"
}

HELP=false
DIAGRAM=true
LABELS=true
STATS=true

while :; do
  case "$1" in
    -h | --help ) show_help; exit;;
    -l | --nolabels ) LABELS=false; shift;;
    -d | --nodiagram ) DIAGRAM=false; shift;;
    -s | --nostats ) STATS=false; shift;;
    -- ) shift; break;;
    -?* ) printf "${RED}WARN${NC}: Unknown option (ignored): ${GREEN}%s${NC}\n${PINK}-h | --help for help\n${NC}" "$1" >&2; shift;;
    * ) break ;;
  esac
done

if $DIAGRAM ; then
  ./diagram.py | unflatten -l 3  | dot -Tps2 | ps2pdf - > output/power.pdf &
  printf "\n${PURPLE}Generating power diagram${NC} "
  spinner $!
fi
if $LABELS ; then
  ./node-labels.py & 
  printf "\n${PURPLE}Generating labels for you${NC} " 
  spinner $!
fi
if $STATS ; then
  ./statistics.py &
  printf "\n${PURPLE}Generating network stats${NC} "
  spinner $!
fi

printf "\n${GREEN}Done${NC}\n"
