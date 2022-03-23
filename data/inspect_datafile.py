import psyplot.project as psy
import sys
from pathlib import Path
import argparse

# Add path tot the icon-vis modules
data_dir = Path(Path(__file__).resolve().parents[1], 'modules')
sys.path.insert(1, str(data_dir))
from utils import show_data_vars


def print_vars(input_file):
    ds = psy.open_dataset(input_file,
                          engine='cfgrib',
                          backend_kwargs={
                              'indexpath': '',
                              'errors': 'ignore'
                          })
    show_data_vars(ds)


if __name__ == "__main__":

    # A) Parsing arguments

    ####################

    parser = argparse.ArgumentParser()
    parser.add_argument('--infile', '-i', dest = 'input_file',\
                            help = 'path to input file',\
                            default='')
    args = parser.parse_args()

    print_vars(args.input_file)
