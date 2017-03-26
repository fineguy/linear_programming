import argparse

from data_parser import JsonData
from model import QuantityModel, DiscountModel


MODELS = {
    "quantity": QuantityModel,
    "discount": DiscountModel
}


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data", help="path to file with data")
    parser.add_argument("-n", "--markets", type=int, help="the number of markets")
    parser.add_argument("-m", "--products", type=int, help="the number of product types")
    parser.add_argument("-o", "--output", help="path to output")
    parser.add_argument("-t", "--type", required=True, choices=list(MODELS), help="model type")
    parser.add_argument("-v", "--verbose", action="store_true", help="print problem statement")
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    model = MODELS[args.type]()

    if args.data:
        data = JsonData()
        data.init_from(args.data)
        model.init_prob(data)
    else:
        model.init_random_prob(args.markets, args.products)

    model.solve(verbose=args.verbose)
    if args.output:
        model.dump(args.output)
