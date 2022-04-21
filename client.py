def test_ybg(ybg, m, n):
    xbg = [[0] * n] * m
    for i in range(m):
        j: int
        for j in range(n):
            if i == 0 and j == 0:
                xbg[i][j] = ybg[i][j]
                continue
            mm = float("inf")
            if (i > 0):
                mm = min(mm, xbg[i - 1][j])
            if(j > 0):
                mm = min(mm, xbg[i][j - 1])

                xbg[i][j] = mm + ybg[i][j]
        return ybg[-1][-1]


ybg = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]

print(test_ybg(ybg, 3, 3))