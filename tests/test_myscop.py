import pytest
from myscop import MyAlldiff as A
from myscop import MyLinear as L
from myscop import MyModel
from myscop import MyQuadratic as Q


def test_binpacking(snapshot):
    items = [6, 5, 4, 3, 1, 2]  # item size
    num_bins = 3  # bin size
    m = MyModel()
    vv = m.addvars(len(items), range(num_bins))
    for b in range(num_bins):
        m.addcons(L(items, vv, b) <= 7)
    m.optimize()
    ans = [v.value for v in vv]
    snapshot.assert_match(ans)
    print(ans)


def test_quadratic(snapshot):
    m = MyModel()
    x, y, z = m.addvars(3, range(3))
    m.addcons(A([x, y, z]))
    for i, j in [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]:
        for v1, v2 in zip([x, x, y], [y, z, z]):
            if (v1 == x and v2 == y and i == 1 and j == 0) or (
                v1 == y and v2 == z and i == 0 and j == 2
            ):
                continue
            m.addcons(Q(1, [v1], i, [v2], j) <= 0)
    m.optimize()
    ans = [v.value for v in [x, y, z]]
    snapshot.assert_match(ans)
    print(ans)


def test_raises():
    m = MyModel()
    v = m.addvars(1, [0, 1])
    ln = L(1, v, 0)
    qd = Q(1, v, 0, v, 1)
    ad = A(v)
    with pytest.raises(AssertionError):
        m.addcons(ln)  # 「<= 0」がない
    with pytest.raises(AssertionError):
        ln + qd <= 0  # 異なるものを足している
    with pytest.raises(AssertionError):
        qd - ln <= 0  # 異なるものを引いている
    with pytest.raises(TypeError):
        ad <= 0  # 「<= 0」は使えない
