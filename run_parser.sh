#!/bin/sh

mkdir -p datasets
[ -e datasets/amazon-meta.txt ] || curl http://snap.stanford.edu/data/bigdata/amazon/amazon-meta.txt.gz -o datasets/amazon-meta.txt.gz
[ -e datasets/amazon-meta.txt ] || gunzip datasets/amazon-meta.txt.gz
[ -e datasets/parsed_input.txt ] || ./parser/parser.py -i datasets/amazon-meta.txt -o datasets/parsed_input.txt

TOTAL=$(wc -l datasets/parsed_input.txt | awk '{print $1}')
ZEROONEP=$(echo "($TOTAL*0.001)/1" | bc)
ONEP=$(echo "($TOTAL*0.01)/1" | bc)

ZEROONEEND=$(awk -v min=0 -v max=$TOTAL 'BEGIN{srand(); print int(min+rand()*(max-min+1))}')
head -n $ZEROONEEND datasets/parsed_input.txt | tail -$ZEROONEP > datasets/parsed_input01.txt

ONEEND=$(awk -v min=0 -v max=$TOTAL 'BEGIN{srand(); print int(min+rand()*(max-min+1))}')
head -n $ONEEND datasets/parsed_input.txt | tail -$ONEP > datasets/parsed_input1.txt
