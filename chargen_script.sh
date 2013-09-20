#!/bin/bash

usage="\
./chargen_script.sh -r <race> -c <class> -v <version> [-n <num>]
                    [-p <prefix>] [--adom <path>]
                    [--load-delay <delay>] [--exit-delay <delay>]
                    [--talent-delay <delay>]
    -r <race>              : PC's race
    -c <class>             : PC's class
    -v <version>           : ADOM version (1.1.1 or 1.2.0)
    -n <num>               : number of character to generate (default=1000)
    -p <prefix>            : prefix for .vlg files (default=\"vlgs/\")
    --adom <path>          : path to ADOM folder (default=\"./\")
    --load-delay <delay>   : ADOM loading delay (s) (default=0.5)
    --exit-delay <delay>   : ADOM exit delay (s) (default=0.1)
    --talent-delay <delay> : delay for talent parsing (s) (default=0.5)"


num=1000
path="./"
prefix="vlgs/"

load_delay="0.5"
exit_delay="0.1"
talent_delay="0.5"

opts=`getopt -o v:n:r:c:p: --long adom:,load-delay:,exit-delay:,talent-delay: -- "$@"`

if [ $? -ne 0 ]; then
    echo "$usage"
    exit 1
fi

eval set -- "$opts"

while true
do
    case "$1" in
        -n) num=$2; shift 2;;
        -r) race=$2; shift 2;;
        -c) class=$2; shift 2;;
        -v) version=$2; shift 2;;
        -p) prefix=$2; shift 2;;
        --adom) path=$2; shift 2;;
        --load-delay) load_delay=$2; shift 2;;
        --exit-delay) exit_delay=$2; shift 2;;
        --talent-delay) talent_delay=$2; shift 2;;
        --) shift; break;;
    esac
done

if [ -z $race ]; then
    echo "Race not specified!"
    exit 1
fi

if [ -z $class ]; then
    echo "Class not specified!"
    exit 1
fi

if [ -z $version ]; then
    echo "Version not specified!"
    exit 1
fi

if [ $version != "1.1.1" -a $version != "1.2.0" ]; then
    echo "Invalid version!"
    exit 1
fi

if [ "$race" \> "l" -o "$race" \< "a" ]; then
    echo "Wrong race code, use 'a' to 'l'!"
    exit 1
fi

if [ "$class" \> "v" -o "$class" \< "a" ]; then
    echo "Wrong race code, use 'a' to 'v'!"
    exit 1
fi

if [ $num -lt 0 ]; then
    echo "Positive number required!"
    exit 1
fi

adom_exec=$path
src_vlg_path=$adom_exec
adom_exec="$adom_exec/adom"

if [ ! -x $adom_exec ]; then
    echo "./adom not found!"
    exit 1
fi

case "$race" in
    a) full_race="human" ;;
    b) full_race="trollish" ;;
    c) full_race="high elven" ;;
    d) full_race="gray elven" ;;
    e) full_race="dark elven" ;;
    f) full_race="dwarven" ;;
    g) full_race="hurthling" ;;
    h) full_race="gnomish" ;;
    i) full_race="orcish" ;;
    j) full_race="drakish" ;;
    k) full_race="mist elven" ;;
    l) full_race="ratling" ;;
esac

case "$class" in
    a) full_class="fighters" ;;
    b) full_class="paladins" ;;
    c) full_class="rangers" ;;
    d) full_class="thieves" ;;
    e) full_class="assasinds" ;;
    f) full_class="wizards" ;;
    g) full_class="priests" ;;
    h) full_class="bards" ;;
    i) full_class="monks" ;;
    j) full_class="healers" ;;
    k) full_class="weaponsmiths" ;;
    l) full_class="archers" ;;
    m) full_class="merchants" ;;
    n) full_class="farmers" ;;
    o) full_class="mindcrafters" ;;
    p) full_class="barbarians" ;;
    q) full_class="druids" ;;
    r) full_class="necromancers" ;;
    s) full_class="elementalists" ;;
    t) full_class="barbarians" ;;
    u) full_class="chaos knights" ;;
    v) full_class="duelists" ;;
esac

echo "
You are about to generate $num $full_race $full_class.
Vlg files will be placed into $PWD/$prefix as 1.vlg ... $num.vlg."
echo

read -p "Is everything right (y/n)? " -n 1 -r
echo
if [[ $REPLY =~ ^[Nn]$ ]]; then
    echo "Aborting."
    exit 0
fi

cur_path=$PWD
vlg_path="$PWD/$prefix"
if [ ! -d $vlg_path ]; then
    mkdir $vlg_path
fi

cd $path

tmux start-server
tmux new-session -d -s adom-chargen -x 80 -y 26

cd $cur_path

step=$[$num/10]

for i in `seq 1 $num`
do
    sleep $load_delay
    tmux send-keys "./adom|tee $cur_path/output" c-m
    sleep 0.1
    if [ $version == "1.2.0" ]; then
        tmux send-keys c-m
    fi
    tmux send-keys \ g \ sm"${race}${class}" \ r
    sleep $talent_delay
    talents=`python parse_output.py`
    for x in `seq 1 $talents`
    do
        tmux send-keys a
    done
    tmux send-keys $i c-m
    tmux send-keys \) Qy \ \ nnn
    sleep $exit_delay
    mv $src_vlg_path/$i.vlg $vlg_path/
    if [ ! $step == "0" ]; then
        iter_measure=$[$i % $step]
        iter_num=$[$i * 100 / $num]
        if [ $iter_measure == "0" ]; then
            echo "$iter_num% ($i characters) done!"
        fi
    fi
done


