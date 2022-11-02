import sys
import os
from shutil import rmtree

import argparse

parser = argparse.ArgumentParser(
    description='''------- File with useful commands -------''',
    epilog="""---------------- Bye bye ----------------"""
)
parser.add_argument(
    'reset_all', type=str, default='reset_all',
    help='Deletes all folders'
)
parser.add_argument(
    'reset_totals', type=str, default='reset_totals',
    help='Deletes totals folder'
)
parser.add_argument(
    'reset_orders', type=str, default='reset_orders',
    help='Deletes orders folder'
)
parser.add_argument(
    'reset_results', type=str, default='reset_results',
    help='Deletes results file'
)
args=parser.parse_args()


def reset_totals():
    if os.path.exists("totals"):
        rmtree("totals")
    if not os.path.exists('totals'):
        os.makedirs('totals')

def reset_orders():
    if os.path.exists("orders"):
        rmtree("orders")
    if not os.path.exists('orders'):
        os.makedirs('orders')

def reset_results():
    try:
        os.remove("results.csv")
    except FileNotFoundError:
        pass

def reset_all():
    reset_totals()
    reset_orders()
    reset_results()

if (sys.argv[1] == "reset_all"):
    reset_all()
if (sys.argv[1] == "reset_orders"):
    reset_orders()
if (sys.argv[1] == "reset_results"):
    reset_results()
if (sys.argv[1] == "reset_totals"):
    reset_totals()
