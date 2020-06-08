import numpy as np

"""
FileManagement.py
================================
Plik z funkcjami zażądzającymi plikami
"""


def clear_file(name):
    """
    Czyści plik
    :return:
    """

    open(name, 'w').close()


def in_line(start_point, end, y, color, unit, name):
    """
    Ustawia jednostki w linii od start do end
    :param name: nazwa pliku
    :param start_point: początkowa pozycja x jednostek
    :param end: końcowa pozycja x jednostek
    :param y: wysokość na której mają być ustawione
    :param color: kolor jednostek
    :param unit: Rodzaj jednostki
    :return:
    """

    with open(name, 'a') as file:
        i = start_point
        for i in range(end + 1):
            file.writelines((str(i) + ',' + str(y) + ',' + unit + ',' + color + '\n'))


def to_file(string, name):
    """
    Wczytuje string do pliku
    :param name: nazwa pliku
    :param string: wczytywana treść do pliku
    :return:
    """
    with open(name, 'a') as file:
        file.writelines(string)
        file.close()


def read_from_file(name):
    """
    Czyta jednostki z pliku
    :param name: nazwa pliku
    :return: zwraca listę krotek z jednostkami
    """
    mylist = []
    with open(name, "r") as fp:
        for i in fp.readlines():
            tmp = i.split(',')
            mylist.append((int(tmp[0]), int(tmp[1]), tmp[2].strip(), tmp[3].strip()))
    return mylist
