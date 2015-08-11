#!/bin/sh

./run_parser.sh

python2 maxflow.py -d datasets/parsed_input1.txt -c 40 -p 10-100 -s 10
