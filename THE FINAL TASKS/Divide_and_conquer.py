def count_inversions(arr):
    def merge_sort_plus_count(arr, left, right):
        if left >= right:
            return 0

        mid = (left + right) // 2
        inv_count = merge_sort_plus_count(arr, left, mid)
        inv_count += merge_sort_plus_count(arr, mid + 1, right)
        # Счет инверсии при слиянии
        inv_count += merge_and_count(arr, left, mid, right)
        return inv_count

    def merge_and_count(arr, left, mid, right):
        left_part = arr[left:mid + 1]
        right_part = arr[mid + 1:right + 1]

        i = j = 0
        k = left
        inv_count = 0

        # Слияние и подсчет инверсий
        while i < len(left_part) and j < len(right_part):
            if left_part[i] <= right_part[j]:
                arr[k] = left_part[i]
                i += 1
            else:
                arr[k] = right_part[j]
                j += 1
                inv_count += (mid + 1) - (left + i)
            k += 1


        while i < len(left_part):
            arr[k] = left_part[i]
            i += 1
            k += 1

        while j < len(right_part):
            arr[k] = right_part[j]
            j += 1
            k += 1

        return inv_count

    return merge_sort_plus_count(arr, 0, len(arr) - 1)


n = int(input())
arr = list(map(int, input().split()))
print(count_inversions(arr))