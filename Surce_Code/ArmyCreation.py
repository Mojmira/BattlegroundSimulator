def clear_file():
    open('army.txt', 'w').close()


def in_line(start_point, end, y, color, unit):
    with open('army.txt', 'a') as file:
        i = start_point
        for i in range(end + 1):
            file.writelines((str(i) + ',' + str(y) + ',' + unit + ',' + color + '\n'))
