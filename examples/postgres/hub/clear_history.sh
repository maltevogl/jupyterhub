#!/bin/bash
for x in $(seq $1 -1 $2);
do 
  history -d $1;
done
