#!/bin/bash

for y in `seq 1 10000`
do
		sleep 0.5
		tmux send-keys ./adom\|tee \ output c-m
		sleep 0.1
		tmux send-keys \ g \ smjb \ r
		sleep 0.5
		talents=`python parse_output.py`
		for x in `seq 1 $talents`
		do
			tmux send-keys a
		done
		tmux send-keys $y c-m
		tmux send-keys \) Qy \ \ nnn
done

mv *.vlg vlgs/
