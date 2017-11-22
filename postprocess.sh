#!/bin/bash 

execute=$1
out=$2
csv=$3

#run_command="docker run --rm -i -v `pwd`:/scratch -w /scratch -u 0:0 parallelworks/energyplus:v8p6 python2"
run_command="docker run --rm -i -v `pwd`:/scratch -w /scratch  parallelworks/energyplus:v8p6 python2"

$run_command $execute $out $csv 
