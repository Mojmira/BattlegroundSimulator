import numpy as np

"""
FileManagement.py
================================
Plik z funkcjami zażądzającymi army.txt
"""


def clear_file():
    """
    Czyści plik
    :return:
    """

    open('army.txt', 'w').close()


def in_line(start_point, end, y, color, unit):
    """
    Ustawia jednostki w linii od start do end
    :param start_point: początkowa pozycja x jednostek
    :param end: końcowa pozycja x jednostek
    :param y: wysokość na której mają być ustawione
    :param color: kolor jednostek
    :param unit: Rodzaj jednostki
    :return:
    """

    with open('army.txt', 'a') as file:
        i = start_point
        for i in range(end + 1):
            file.writelines((str(i) + ',' + str(y) + ',' + unit + ',' + color + '\n'))


def from_start_menu(string):
    """
    Wczytuje string do pliku
    :param string: wczytywana treść do pliku
    :return:
    """
    with open('army.txt', 'a') as file:
        file.writelines(string)
        file.close()


def read_from_file():
    """
    Czyta jednostki z pliku
    :return: zwraca listę krotek z jednostkami
    """
    mylist = []
    with open('army.txt', "r") as fp:
        for i in fp.readlines():
            tmp = i.split(',')
            mylist.append((int(tmp[0]), int(tmp[1]), tmp[2].strip(), tmp[3].strip()))
    return mylist