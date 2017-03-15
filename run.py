import argparse

from data_parser import JsonData
from model import Model


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data", required=True, help="path to file with data")
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()

    data = JsonData()
    data.init_from(args.data)

    model = Model()
    model.init_data(data)
