import argparse
import sys

import pandas as pd

"""
Take a csv file with texts and return the analysis
where texts are tagged with a negativity score
"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_texts", help="Path to csv file with input texts", type=str, required=True)
    parser.add_argument("-o", "--output_texts", help="Path to csv file with output texts", type=str, required=True)
    args = parser.parse_args()
    print("%% Loading input texts...", file=sys.stderr)
    df = pd.read_csv(args.input_texts)
    print("%% Saving results...")
    df.to_csv(args.output_texts, sep="\t", index=False)
    print("%% Done")
