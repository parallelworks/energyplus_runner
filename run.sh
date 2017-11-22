#!/bin/bash 

execute=$1
input=$2
casename=$3
out=$4
csv=$5 

#run_command="docker run --rm -i -v `pwd`:/scratch -w /scratch -u 0:0 parallelworks/energyplus:v8p6 python2"
run_command="docker run --rm -i -v `pwd`:/scratch -w /scratch  parallelworks/energyplus:v8p6 python2"
echo $run_command
echo "--------------------------"
$run_command  $execute $input $casename $out $csv 
