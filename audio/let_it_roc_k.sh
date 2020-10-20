# Use ${NAME}N in OBS
# Usage ./let_it_roc_k.sh <name NAME_PREFIX> <port suffix>

NAME_PREFIX="$1"
PORT="$2"

pactl load-module module-null-sink sink_name="${NAME_PREFIX}N"
pacmd update-sink-proplist "${NAME_PREFIX}N" device.description="${NAME_PREFIX}N"
pactl load-module module-equalizer-sink sink_name="${NAME_PREFIX}E" sink_master="${NAME_PREFIX}N"
pacmd update-sink-proplist "${NAME_PREFIX}E" device.description="${NAME_PREFIX}E"
pactl load-module module-roc-sink-input sink=AE local_source_port="1000${PORT}" local_repair_port="1001${PORT}"
