# linear_programming

## Summary
Here is a simple program for solving a particular integer linear programming problem.

## Usage examples
* python run.py -n 10 -m 10 -o out.json
* python run.py -d test.json -v


## Problem description
Let I={1,...,n} be markets and J={1,...,m} – product types. We have some demand for each product type d[i]. Each market "i" sells product type "j" at a fixed price p[i][j] for q[i][j] items, but can't ship more than t[i] items at a time. Our objective is to satisfy the demand for each product type with as little money spent as possible.

## List of files
* data_parser.py – classes for reading data;
* model.py – integer linear programming solver;
* run.py – main script;
* test.json – sample data.
