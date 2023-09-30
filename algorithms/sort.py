def insert_sort( data, verbose=False):
    sz = len(data)
    for i in range(1,sz):
        key = data[i]
        j = i-1
        while (j >= 0) and data[j] > key:
            data[j+1] = data[j]
            j = j - 1
        data[j+1] = key
    return data

if __name__ == "__main__":
    pass