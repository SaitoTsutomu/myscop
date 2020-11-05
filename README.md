The myscop is wrapper of SCOP.

SCOP is Solver for COnstraint Programing.

Need scop and scop.py.

https://logopt.com/scop2/

## Example(bin packing)

```
from myscop import MyModel, MyLinear as L

items = [6, 5, 4, 3, 1, 2]  # item size
num_bins = 3  # bin size
m = MyModel()
vv = m.addvars(len(items), range(num_bins))
for b in range(num_bins):
    m.addcons(L(items, vv, b) <= 7)
m.optimize()
ans = [v.value for v in vv]
print(ans)  # ['2', '0', '1', '1', '2', '0']
```

## Example(alldiff & quadratic)

```
from myscop import inf, MyModel, MyAlldiff as A, MyQuadratic as Q

m = MyModel()
m.Params.TimeLimit = 0.1
x, y, z = m.addvars(3, range(3))
m.addcons(A([x, y, z]), weight=inf)
for i, j in [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]:
    for v1, v2 in zip([x, x, y], [y, z, z]):
        if v1 == x and v2 == y and i == 1 and j == 0:
            continue
        m.addcons(Q(1, [v1], i, [v2], j) <= 0)
m.optimize()
ans = [v.value for v in [x, y, z]]
print(ans)  # ['1', '0', '2']
```
