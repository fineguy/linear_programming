# linear_programming
Here is a simple program for solving particular integer linear programming problems.

## Installation 
```
git clone https://github.com/fineguy/linear_programming
cd linear_programming
pip install -r requirements.txt
```

## Problems descriptions
Let I={1,...,n} be markets and J={1,...,m} – product types, d[j] – demand for product type "j". Our objective is to satisfy the demand for each product type with as little money spent as possible. However, there could be other conditions:
1. **Quantity problem**. Each market "i" sells product type "j" at a fixed price p[i][j] for a fixed amount of items q[i][j], but can't ship more than t[i] items at a time. 
2. **Discount problem**. Each market "i" sells product type "j" at a fixed price p[i][j] for one item and can also offer a discount t[i] if we order more than q[i] items in total.

## Usage examples
* Randomly generated data: `python run.py -n 10 -m 10 -o out.json`
* Data in json format: `python run.py -d test.json -v`

## List of files
* data_parser.py – classes for reading data;
* model.py – integer linear programming solver;
* run.py – main script;
* quantity.json, discount.json – sample data.
