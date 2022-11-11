import os, glob
from shutil import rmtree
import argparse
from termcolor import colored

parser = argparse.ArgumentParser(
    description='''------- File with useful commands -------''',
    epilog="""---------------- Bye bye ----------------"""
)
parser.add_argument(
    '-o',
    type=str,
    choices=['reset_all', 'reset_orders', 'reset_totals', 'reset_results'],
    default='reset_all', required=True,
    help='Option to delete some files'
)
args = parser.parse_args()

def reset_totals():
    if os.path.exists("totals"):
        rmtree("totals")
        print(colored("Totals dir deleted", "green"))
    if not os.path.exists('totals'):
        os.makedirs('totals')

def reset_orders():
    if os.path.exists("orders"):
        rmtree("orders")
        print(colored("Orders dir deleted", "green"))
    if not os.path.exists('orders'):
        os.makedirs('orders')

def reset_results():
    try:
        for f in glob.glob("results_core*.csv"):
            os.remove(f)
        print(colored("Results file deleted", "green"))
    except FileNotFoundError:
        pass

def reset_all():
    value = input("Are you sure you want to delete all? (y/n): ")
    if (value == "y"):
        reset_totals()
        reset_orders()
        reset_results()

if (args.o == "reset_all"):
    reset_all()
if (args.o == "reset_orders"):
    reset_orders()
if (args.o == "reset_results"):
    reset_results()
if (args.o == "reset_totals"):
    reset_totals()
