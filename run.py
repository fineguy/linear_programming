import argparse

from data_parser import JsonData
from model import MarketModel


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data", required=True, help="path to file with data")
    parser.add_argument("-o", "--output", help="path to output")
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()

    data = JsonData()
    data.init_from(args.data)

    model = MarketModel()
    model.init_prob(data)
    model.solve(verbose=True)
    if args.output:
        model.dump(args.output)
