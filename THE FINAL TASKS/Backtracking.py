def generate_partitions(n):
    def backtrack(start, path, remaining):
        if remaining == 0:
            print(' '.join(map(str, path)))
            return
        for num in range(start, remaining + 1):
            backtrack(num, path + [num], remaining - num)

    backtrack(1, [], n)


n = int(input())
generate_partitions(n)