#!/bin/bash

OUTPUT_H264="$1"
OUTPUT_MP4="$2"

libcamera-vid -t 0 -o "$OUTPUT_H264" &
PID=$!

echo "Type 'stop' to end recording."

while true; do
    read -r cmd
    if [ "$cmd" = "stop" ]; then
        kill $PID
        wait $PID 2>/dev/null
        break
    fi
done
