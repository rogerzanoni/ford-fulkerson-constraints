#!/usr/bin/env python2

import sys
import getopt
import re

def usage():
    print "Usage: ./parser.py -i <input_dataset> -o <output_dataset>"

def parse_file(input_path, output_path):
    input_file = open(input_path, 'r')
    content = input_file.read()
    input_file.close()

    output_file = open(output_path, 'w')
    customer_output_file = open(output_path+".customers", 'w')
    customer_dict = {}
    customer_idx = 0

    matches = re.findall("(Id: +)(\d+)(.*?)\n\s*\n", content, re.MULTILINE | re.DOTALL)

    reviews_re = re.compile("(reviews:)(.*?)\n\s*\n", re.MULTILINE | re.DOTALL)
    customers_re = re.compile("(cutomer: *)(\w+)( )", re.MULTILINE)

    for match in matches:
        match_str = "".join(match)+"\n\n"
        review_matches = reviews_re.findall(match_str)
        if len(review_matches) == 0:
            continue
        product_id = match[1]
        customer_matches = customers_re.findall(match_str)
        for customer_match in customer_matches:
            customer_id = customer_match[1]

            if not customer_id in customer_dict:
                customer_dict[customer_id] = str(customer_idx)
                customer_output_file.write(customer_id)
                customer_output_file.write(',')
                customer_output_file.write(str(customer_idx))
                customer_output_file.write('\n')
                customer_idx = customer_idx + 1

            output_file.write(customer_dict[customer_id])
            output_file.write(',')
            output_file.write(product_id)
            output_file.write('\n')

    output_file.close();
    customer_output_file.close();


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "i:o:h", ["input=", "output=", "help"])
    except getopt.GetoptError:
        usage()
        sys.exit(1)
    input_path, output_path = None, None
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-i", "--input"):
            input_path = arg
        elif opt in ("-o", "--output"):
            output_path = arg
    if input_path == None or output_path == None:
        usage()
        sys.exit(2)
    parse_file(input_path, output_path)

if __name__ == "__main__":
    main(sys.argv[1:])
