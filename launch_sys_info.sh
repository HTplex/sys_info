#!/bin/bash

tmux new-session -d -s sys_info 
tmux send-keys -t sys_info:0 'conda activate sys_info' C-m
sleep 1
tmux send-keys -t sys_info:0 'python get_machine_status/src/post_info.py' C-m

