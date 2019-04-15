from lib.fs import *

import argparse
import tempfile

# positional arguments:
# num_from_dir  <integer>       number of directories that will be created on client
# num_to_dir    <integer>       number of directories that will be created in OneDrive
#

parser = argparse.ArgumentParser()
parser.add_argument("num_to_dir")
args = parser.parse_args()

with tempfile.TemporaryDirectory(dir="test") as tmpdirname:
    print("Temp dir: " + tmpdirname)
    for i in range(0, int(args.num_to_dir)):
        print("Creating dir " + str(i))
        os.mkdir(tmpdirname)



