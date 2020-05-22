from random import shuffle, choice
from linkedbst import LinkedBST as Tree
from time import time


def load_words(path):
    '''Return a list of words loaded from file'''
    with open(path) as file:
        words = file.readlines()
    return words


def test_tree_find(data: Tree, items):
    '''look for items in data and time it'''
    start = time()
    for item in items:
        data.find(item)
    end = time()
    return end - start


def test_list_find(data: list, items):
    '''look for items in data and time it'''
    start = time()
    for item in items:
        try:
            data.index(item)
        except ValueError:
            -1
    end = time()
    return end - start


def all_test(sorted_words, n=1000):
    '''
    Returns:
        timeX, де Х означає:

    a) час пошуку 10000 випадкових слів у впорядкованому за абеткою словнику
      (пошук у списку слів з використанням методів вбудованого типу list).

    b) час пошуку 10000 випадкових слів у словнику, який представлений
       у вигляді бінарного дерева пошуку.
       Бінарне дерево пошуку будується на основі послідовного додавання
       в дерево слів зі словника який впорядкований за абеткою.

    с) час пошуку 10000 випадкових слів у словнику, який представлений
       у вигляді бінарного дерева пошуку.
       Бінарне дерево пошуку будується на основі
       послідовного додавання в дерево слів зі словника
       який не впорядкований за абеткою
       (слова у дерево додаються випадковим чином).

    d) час пошуку 10000 випадкових слів у словнику, який представлений
       у вигляді збалансованого бінарного дерева пошуку.
    '''

    shuffled_words = sorted_words.copy()
    shuffle(shuffled_words)
    test_words = shuffled_words[:n]

    timeA = test_list_find(sorted_words, test_words)

    tree = Tree()
    for word in sorted_words:
        tree.add(word)
    timeB = test_tree_find(tree, test_words)

    tree.clear()
    for word in shuffled_words:
        tree.add(word)
    timeC = test_tree_find(tree, test_words)

    tree.rebalance()
    timeD = test_tree_find(tree, test_words)

    return timeA, timeB, timeC, timeD


def total_test(n=20) -> tuple:
    '''Run test multiple times, return average time'''
    sorted_words = load_words('words.txt')
    shuffle(sorted_words)
    sorted_words = sorted_words[:500]  # Tree objects can't be too large
    sorted_words.sort()
    timeA, timeB, timeC, timeD = 0, 0, 0, 0
    for i in range(n):
        tA, tB, tC, tD = all_test(sorted_words, 100)  # 100 words per subtest
        timeA += tA
        timeB += tB
        timeC += tC
        timeD += tD
    #  multiply by 100 (test is for 10000 words)
    timeA, timeB, timeC, timeD = timeA*100, timeB*100, timeC*100, timeD*100
    timeA, timeB, timeC, timeD = timeA/n, timeB/n, timeC/n, timeD/n
    return timeA, timeB, timeC, timeD


if __name__ == '__main__':
    timeA, timeB, timeC, timeD = total_test()
    print('час пошуку 10000 випадкових слів у:\n')
    print('\ta) впорядкованому за абеткою словнику:', timeA)
    print('\tb) у словнику, який представлений у вигляді бінарного дерева\
пошуку, побудованого на основі послідовного додавання:', timeB)
    print('\tc) у словнику, який представлений у вигляді бінарного дерева\
пошуку, побудованого на основі послідовного додавання в дерево слів зі \
словника який не впорядкований за абеткою:', timeC)
    print('\td) у словнику, який представлений у вигляді збалансованого \
бінарного дерева пошуку:', timeD)
