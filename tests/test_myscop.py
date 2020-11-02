from myscop import MyLinear as L
from myscop import MyModel


def test_binpacking(snapshot):
    items = [6, 5, 4, 3, 1, 2]  # item size
    num_bins = 3  # bin size
    m = MyModel()
    vv = m.addvars(len(items), range(num_bins))
    for b in range(num_bins):
        m.addcons(1, L(items, vv, b) <= 7)
    m.optimize()
    ans = [v.value for v in vv]
    snapshot.assert_match(ans)
