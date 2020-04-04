from binary_pendant import get_level_n_binary_pendant_neighbors
from zero_forcing import calculate_zero_forcing_nr

def main():
    for i in range(1, 4):
        print("Checking level {}".format(i))
        neighbors = get_level_n_binary_pendant_neighbors(i)
        n = len(neighbors) 
        zfn = calculate_zero_forcing_nr(neighbors, False) 
        print("n: {}, zfn: {}, ratio: {}".format(n, zfn, zfn / n))

if __name__ == "__main__":
    main()
