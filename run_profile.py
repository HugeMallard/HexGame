import pstats
from pstats import SortKey

p = pstats.Stats("restats")
p.sort_stats(SortKey.TIME).print_stats(30)
# print("")
p.sort_stats(SortKey.CUMULATIVE).print_stats(30)
