n = int(input())
costs = [int(input()) for _ in range(n)]

# dp[i][j] - минимальная стоимость для первых i дней с j купонами
INF = float('inf')
dp = [[INF] * (n + 2) for _ in range(n + 1)]
dp[0][0] = 0  # 0 дней, 0 купонов - стоимость 0

for i in range(1, n + 1):
    current_cost = costs[i - 1]
    for j in range(n + 1):
        if dp[i - 1][j] == INF:
            continue

        if current_cost > 500:
            if j + 1 <= n:
                if dp[i][j + 1] > dp[i - 1][j] + current_cost:
                    dp[i][j + 1] = dp[i - 1][j] + current_cost
        else:
            if dp[i][j] > dp[i - 1][j] + current_cost:
                dp[i][j] = dp[i - 1][j] + current_cost

        if j > 0:
            if dp[i][j - 1] > dp[i - 1][j]:
                dp[i][j - 1] = dp[i - 1][j]


min_cost = INF
best_coupons = 0
for j in range(n + 1):
    if dp[n][j] <= min_cost:
        min_cost = dp[n][j]
        best_coupons = j


coupon_days = []
i = n
j = best_coupons
remaining_coupons = best_coupons
while i > 0:
    current_cost = costs[i - 1]
    # был ли использован купон в день i?
    if j < n + 1 and dp[i - 1][j + 1] == dp[i][j]:
        coupon_days.append(i)
        j += 1
    # был ли купон получен в день i?
    elif current_cost > 500 and j > 0 and dp[i - 1][j - 1] + current_cost == dp[i][j]:
        j -= 1
    i -= 1

coupon_days.sort()

print(min_cost, len(coupon_days))
if coupon_days:
    print(' '.join(map(str, coupon_days)))
else:
    print()