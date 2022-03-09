from Labki1 import Zagadka, Solution

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    A = Zagadka(26)
    print(A.to_string())

    print(A.basic_compare([17, 7, 14, 1]))

    B = Solution()
    B.local_search(A)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
