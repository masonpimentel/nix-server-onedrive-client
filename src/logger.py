from lib.debugging import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("message")
parser.add_argument("type")
args = parser.parse_args()

print_message(args.message, "CRONJOB", args.type)
