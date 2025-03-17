#!/bin/bash
# PORTMASTER: starship-nightly.zip, Starship nightly.sh

XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}

if [ -d "/opt/system/Tools/PortMaster/" ]; then
  controlfolder="/opt/system/Tools/PortMaster"
elif [ -d "/opt/tools/PortMaster/" ]; then
  controlfolder="/opt/tools/PortMaster"
elif [ -d "$XDG_DATA_HOME/PortMaster/" ]; then
  controlfolder="$XDG_DATA_HOME/PortMaster"
else
  controlfolder="/roms/ports/PortMaster"
fi

source $controlfolder/control.txt
[ -f "${controlfolder}/mod_${CFW_NAME}.txt" ] && source "${controlfolder}/mod_${CFW_NAME}.txt"

# Set variables
GAMEDIR="/$directory/ports/starship-nightly"

> "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/update-log.txt") 2>&1

$controlfolder/harbourmaster install https://github.com/ben-willmore/PortMaster-MV-New/releases/download/SoH-nightly-latest/soh-nightly.zip
