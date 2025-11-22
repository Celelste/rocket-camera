#!/bin/bash

SESSION="rocketcam"

# Create a unique filename for this run
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BASENAME="video_$TIMESTAMP"
OUTPUT_H264="$BASENAME.h264"
OUTPUT_MP4="$BASENAME.mp4"

tmux has-session -t $SESSION 2>/dev/null
if [ $? != 0 ]; then
    tmux new-session -d -s $SESSION "bash record_video.sh $OUTPUT_H264 $OUTPUT_MP4"
    echo "Recording started in tmux session '$SESSION'."
else
    echo "Session '$SESSION' already exists."
fi

echo "Detach safely. To stop recording: tmux attach -t $SESSION and type: stop"
