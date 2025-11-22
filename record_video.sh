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
        echo "Converting to MP4..."
        MP4Box -add "$OUTPUT_H264" "$OUTPUT_MP4" >/dev/null 2>&1
        echo "MP4 saved as $OUTPUT_MP4"
        break
    fi
done
