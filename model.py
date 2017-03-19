from abc import ABCMeta, abstractmethod
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
        assert data.y is not None, "Missing y attribute"
        assert data.t is not None, "Missing t attribute"

        n, m = data.p.shape

        # validate data shapes
        assert (n, m) == data.q.shape, \
            "Not matching dimensions in p {} and q {}".format(data.p.shape, data.q.shape)
        assert m == data.y.shape[0], \
            "Not matching dimensions in p {} and y {}".format(data.p.shape, data.y.shape)
        assert n == data.t.shape[0], \
            "Not matching dimensions in p {} and t {}".format(data.p.shape, data.t.shape)

        # initialize problem variables
        self.prob = pulp.LpProblem("Market", pulp.LpMinimize)
        self.x = [[pulp.LpVariable("x_{}_{}".format(i + 1, j + 1), lowBound=0, cat="Integer") for j in range(m)]
                  for i in range(n)]
        costs = sum(self.x[i][j] * data.p[i][j] for i in range(n) for j in range(m))
        products_by_shops = [sum(self.x[i][j] * data.q[i][j] for j in range(m)) for i in range(n)]
        products_by_cats = [sum(self.x[i][j] * data.q[i][j] for i in range(n)) for j in range(m)]

        self.prob += costs
        for i in range(n):
            self.prob += (products_by_shops[i] <= data.t[i])
        for j in range(m):
            self.prob += (products_by_cats[j] >= data.y[j])

    def solve(self, verbose=False):
        print(self.prob)
        self.prob.solve()
        for var_list in self.x:
            for var in var_list:
                print(var.name, var.value())

    def dump(self, json_path):
        if not json_path.endswith(".json"):
            raise RuntimeError("Currently only json files supported")
        pass
