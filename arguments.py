import argparse
from config import AVAILABLE_CSV_FIELDS, ENGINES, DEFAULT_PROXY, DEFAULT_OUTPUT, DEFAULT_MP_UNITS
import multiprocessing

def print_epilog():
    epilog = "Available CSV fields: \n\t"
    epilog += " ".join(AVAILABLE_CSV_FIELDS) + "\n"
    epilog += "Supported engines: \n\t"
    epilog += " ".join(ENGINES.keys()) + "\n"
    return epilog

def parse_arguments():
    parser = argparse.ArgumentParser(epilog=print_epilog(), formatter_class=argparse.RawTextHelpFormatter)
    
    parser.add_argument("--proxy", default=DEFAULT_PROXY, type=str, help="Set Tor proxy (default: 127.0.0.1:9050)")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, type=str, help="Output file format (default: output_$SEARCH_$DATE.txt)")
    parser.add_argument("--continuous_write", type=bool, default=False, help="Write progressively to output file")
    parser.add_argument("search", type=str, help="The search string or phrase")
    parser.add_argument("--limit", type=int, default=0, help="Max number of pages per engine to load")
    parser.add_argument("--engines", type=str, nargs="*", help="Engines to request (default: full list)")
    parser.add_argument("--exclude", type=str, nargs="*", help="Engines to exclude")
    parser.add_argument("--fields", type=str, nargs="*", help="Fields to output to CSV file")
    parser.add_argument("--field_delimiter", type=str, default=",", help="Delimiter for the CSV fields")
    parser.add_argument("--mp_units", type=int, default=DEFAULT_MP_UNITS, help=f"Number of processing units (default: {DEFAULT_MP_UNITS})")

    return parser.parse_args()
