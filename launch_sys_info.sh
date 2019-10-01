tmux new -s sys_info
tmux send-keys -t sys_info 'conda activate sys_info' C-m
tmux send-keys -t sys_info 'python get_machine_status/src/post_info.py' C-m
