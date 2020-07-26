#!/usr/bin/python3

def main(arr, low, high):
    set_i = False
    i = low # point first high or equal value position
    flag_value = arr[low]
    from_index = low + 1

    for j in range(from_index, high+1):
        if not set_i and arr[j] >= flag_value:
            i = j
            set_i = True            
        elif set_i and arr[j] <= flag_value:
            arr[i], arr[j] = arr[j], arr[i]
            i = i + 1
        print(arr)
        print("i: {0}, j: {1}".format(i, j))
    if i > low:    
        arr[low], arr[i-1] = arr[i-1], arr[low]
        print(arr)
        print("after move flag value, i: {0}, j: {1}".format(i, j))
    else:
        arr[low], arr[high] = arr[high], arr[low]
        print(arr)
        print("after move flag value, i: {0}, j: {1}".format(i, j))
        i = high + 1

    # split to two parts
    # first part is 

    print("one part => low: {0}, high: {1}".format(low, i - 2))
    print("two part => low: {0}, high: {1}".format(i, high))

    if low < i - 2 :
        main(arr, low, i-2)

    if i < high:
        main(arr, i, high)
    

if __name__ == '__main__':
    #arr = [3, 5, 4, 1, 2]
    #arr = [3, 5]
    #arr = [1, 3, 9, 8, 4, 3, 2, 4, 1]
    arr = [12, 1, 1, 2, 5, 66, 79, 1, 3, 5, 8, 12, 100, 99]
    main(arr, 0, len(arr) - 1)
    print(arr)
