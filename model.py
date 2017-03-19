from abc import ABCMeta, abstractmethod
import json
import numpy as np
import pulp


class BaseModel(metaclass=ABCMeta):
    @abstractmethod
    def init_prob(self, data):
        pass

    @abstractmethod
    def solve(self, verbose=False):
        pass

    @abstractmethod
    def dump(self, path_to_output):
        pass


class MarketModel(BaseModel):
    def init_prob(self, data):
        # validate attributes
        assert data.p is not None, "Missing p attribute"
        assert data.q is not None, "Missing q attribute"
        assert data.d is not None, "Missing y attribute"
        assert data.t is not None, "Missing t attribute"

        # validate data shapes
        assert data.p.shape == data.q.shape, \
            "Not matching dimensions in p {} and q {}".format(data.p.shape, data.q.shape)
        assert data.p.shape[1] == data.d.shape[0], \
            "Not matching dimensions in p {} and d {}".format(data.p.shape, data.d.shape)
        assert data.p.shape[0] == data.t.shape[0], \
            "Not matching dimensions in p {} and t {}".format(data.p.shape, data.t.shape)

        self._init(data.p, data.q, data.d, data.t)

    def init_random_prob(self, rows, cols):
        # TODO: come up with a better way for random initialization
        prices = np.random.rand(rows, cols) * 10
        quantities = np.random.randint(low=1, high=10, size=(rows, cols))
        demands = np.random.randint(low=1, high=10, size=cols)
        limits = np.random.randint(low=1, high=10, size=rows)
        self._init(prices, quantities, demands, limits)

    def _init(self, prices, quantities, demands, limits):
        """Initialize problem variables."""
        self.prob = pulp.LpProblem("Market", pulp.LpMinimize)
        n, m = prices.shape
        self.x = [[pulp.LpVariable("x_{}_{}".format(i + 1, j + 1), lowBound=0, cat="Integer") for j in range(m)]
                  for i in range(n)]

        costs = sum(self.x[i][j] * prices[i][j] for i in range(n) for j in range(m))
        products_by_shops = [sum(self.x[i][j] * quantities[i][j] for j in range(m)) for i in range(n)]
        products_by_cats = [sum(self.x[i][j] * quantities[i][j] for i in range(n)) for j in range(m)]

        self.prob += costs
        for i in range(n):
            self.prob += (products_by_shops[i] <= limits[i])
        for j in range(m):
            self.prob += (products_by_cats[j] >= demands[j])

    def solve(self, verbose=False, dump=False):
        if verbose:
            print(self.prob)

        self.prob.solve()

        # mandatory output
        for var_list in self.x:
            for var in var_list:
                print(var.name, var.value())

    def dump(self, json_path):
        if not json_path.endswith(".json"):
            raise RuntimeError("Currently only json files supported")

        json_out = dict()
        json_out["Problem"] = str(self.prob)
        json_out["Solution"] = {var.name: var.value() for var_list in self.x for var in var_list}

        with open(json_path, "w") as f:
            json.dump(json_out, f)
