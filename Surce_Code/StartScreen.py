import pygame
import math

"""
StartScreen.py
================================================================
Tutaj znajduje sie ekran startowy, na ktorym ustawia sie wojska
"""

pygame.init()


class Button:
    """
    Klasa dla wszystkich przyciskow

    Arg:
    pos_x: pozycja przycisku w oknie wzgledem osi x
    pos_y: pozycja przycisku w oknie wzgledem osi y
    width: szerokosc przycisku
    height wysokosc przycisku
    color: kolor przycisku
    text: teks wyswietlany na przycisku
    """

    def __init__(self, pos_x, pos_y, width, height, color, text):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(pos_x, pos_y, width, height)
        self.text = text
        self.font = pygame.font.SysFont('Arial', 20)

    def getRect(self):
        """
        Getter prostokata
        :return: prostokat potrzebny jako argument funkcji rysujacej
        """
        return self.rect

    def addText(self):
        """
        rysuje tekst na przycisku
        :return:
        """
        displayWindow.blit(self.font.render(self.text, True, (0, 0, 0)),
                           (self.pos_x + self.width / 2 - 10, self.pos_y))
        pygame.display.update()


class Unit(Button):
    """
    Klasa na jednostki
    """

    def __init__(self, pos_x, pos_y, width, height, color, text):
        super().__init__(pos_x, pos_y, width, height, color, text)


class GUIButton(Button):
    """Przyciski menu"""

    def __init__(self, pos_x, pos_y, width, height, color, text):
        super().__init__(pos_x, pos_y, width, height, color, text)

    def chooseButton(self):
        """
        Po kliknieciu, zmienia kolor przycisku na zaznaczony
        :return:
        """
        if self.color == red:
            self.color = lightRed
        elif self.color == blue:
            self.color = lightBlue
        elif self.color == darkRed:
            self.color = red
        elif self.color == black:
            self.color = grey

    def uncheckButton(self):
        """
        Odznacza przycisk
        :return:
        """
        if self.color == lightRed:
            self.color = red
        elif self.color == lightBlue:
            self.color = blue
        elif self.color == red:
            self.color = darkRed
        elif self.color == grey:
            self.color = black


"""
Duzo zmiennych, ktore niekoniecznie powinny byc w tym miejscu
"""

"Wymiary"
displayWidth = 800
displayHeight = 600
fieldSize = 20  # liczba kratek
menuWidth = 600 / 20
menuX = min(displayWidth, displayHeight)

"Kolory:"
blue = pygame.Color("#00AAB2")
lightBlue = pygame.Color("#4da6ff")
lightRed = pygame.Color("#ff6666")
red = pygame.Color("red")
darkRed = pygame.Color("#b30000")
green = pygame.Color("#33cc33")
black = pygame.Color('black')
grey = pygame.Color("#4b4b4b")

"Ustawienia okna"
displayWindow = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("Battleground Simulator")
clock = pygame.time.Clock()
displayWindow.fill(pygame.Color("white"))


"Zainicjowanie przyciskow menu:"
infantryRed = GUIButton(menuX + 20, 20, menuWidth, menuWidth, red, "I")
infantryBlue = GUIButton(menuX + 40 + menuWidth,
                         20,
                         menuWidth,
                         menuWidth,
                         blue, "I")
archerRed = GUIButton(menuX + 20,
                      20 + 20 + menuWidth,
                      menuWidth,
                      menuWidth,
                      red, "A")
archerBlue = GUIButton(menuX + 40 + menuWidth,
                       20 + 20 + menuWidth,
                       menuWidth,
                       menuWidth,
                       blue, "A")
cavalryRed = GUIButton(menuX + 20,
                       20 + 40 + 2 * menuWidth,
                       menuWidth,
                       menuWidth,
                       red, "C")
cavalryBlue = GUIButton(menuX + 40 + menuWidth,
                        20 + 40 + 2 * menuWidth,
                        menuWidth,
                        menuWidth,
                        blue, "C")
barrier = GUIButton(menuX + 20 + menuWidth,
                    20 + 40 + 4 * menuWidth,
                    menuWidth,
                    menuWidth,
                    black, "R")
deleteButton = GUIButton(menuX + 20 + menuWidth,
                         20 + 40 + 6 * menuWidth,
                         3 * menuWidth,
                         menuWidth,
                         darkRed, "Del")
startButton = GUIButton(menuX + 20 + menuWidth,
                        20 + 40 + 9 * menuWidth,
                        3 * menuWidth,
                        menuWidth,
                        green, "Start")
"Listy z przyciskami"
menuButtons = [infantryRed, infantryBlue, archerRed, archerBlue, cavalryRed, cavalryBlue, barrier]
extraButtons = [deleteButton, startButton]
"Slownik na jednostki"
Units = {}

"Altualnie wybrany przycisk"
chosenButton = deleteButton
mode = "None"  # "Add" - dodawanie, "Del" - usuwanie
currentColor = red
currentType = "None"


def drawGrid(number):
    blockSize = min(displayHeight, displayWidth) / number
    for x in range(number):
        for y in range(number):
            rect = pygame.Rect(x * blockSize, y * blockSize,
                               blockSize, blockSize)
            pygame.draw.rect(displayWindow, pygame.Color("black"), rect, 1)


def addUnit(keyX, keyY, width):
    """
    Inicjowanie i dodawanie nowo utworzonej jednostki do slownika
    :param keyX: numer kratki w ktorej ma byc jednostka
    :param keyY: numer kratki w ktorej ma byc jednostka
    :param width: rozmiar jednostki
    :return:
    """
    x = keyX * width
    y = keyY * width
    Units[keyX, keyY] = Unit(x, y, width, width, currentColor, currentType)
    print("added at", keyX, keyY)


def removeUnit(keyX, keyY):
    """
    Usuwanie jednostki ze slowika
    :param keyX: numer kratki w ktorej jest jednostka
    :param keyY: numer kratki w ktorej jest jednostka
    :return:
    """
    Units.pop((keyX, keyY), None)
    print("del at", keyX, keyY, len(Units))
    displayWindow.fill(pygame.Color("white"))
    drawGrid(fieldSize)


def convert_to_hex(rgba_color):
    """
    Zmiana koloru
    :param rgba_color: kolor w rgba (domyslny dla pygame.Color())
    :return: kolor w hex (latwiejszy dla mesy)
    """
    red = rgba_color[0]
    green = rgba_color[1]
    blue = rgba_color[2]
    return '0x{r:02x}{g:02x}{b:02x}'.format(r=red, g=green, b=blue)


def getString():
    """
    Zwraca dane jednostek, w formacie zgodnym z odczytywanym przez model
    :return: (str)
    """
    line = ""
    for (x, y), unit in Units.items():
        line += str(x)
        line += ","
        line += str(y)
        line += ","
        line += unit.text
        line += ",#"
        tmp = convert_to_hex(unit.color)
        line += tmp[2:]
        line += "\n"
    return line


finished = False
drawGrid(fieldSize)



"""
Głowna petla
===============================
Dziala do czasu zamkniecia okna
"""
while not finished:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos
            print(mouseX, mouseY)
            if mouseX > menuX:
                for button in menuButtons:
                    if button.pos_x <= mouseX <= button.pos_x + button.width:
                        if button.pos_y <= mouseY <= button.pos_y + button.height:
                            mode = "Add"
                            currentColor = button.color
                            currentType = button.text
                            chosenButton.uncheckButton()
                            chosenButton = button
                            button.chooseButton()
                            break
                for button in extraButtons:
                    if button.pos_x <= mouseX <= button.pos_x + button.width:
                        if button.pos_y <= mouseY <= button.pos_y + button.height:
                            if button.text == "Del":
                                mode = "Del"
                                chosenButton.uncheckButton()
                                chosenButton = button
                                button.chooseButton()
                                break
                            else:
                                finished = True  # start main program
            else:
                if mode == "Add":
                    addUnit(math.floor(mouseX / (menuX / fieldSize)),
                            math.floor(mouseY / (menuX / fieldSize)),
                            menuX / fieldSize)
                elif mode == "Del":
                    removeUnit(math.floor(mouseX / (menuX / fieldSize)),
                               math.floor(mouseY / (menuX / fieldSize)))

    for button in menuButtons:
        pygame.draw.rect(displayWindow, button.color, button.getRect(), 0)
        button.addText()

    for button in extraButtons:
        pygame.draw.rect(displayWindow, button.color, button.getRect(), 0)
        button.addText()

    for unit in Units.values():
        pygame.draw.rect(displayWindow, unit.color, unit.getRect(), 0)
        unit.addText()

    pygame.display.update()
    clock.tick(30)

"""Gdzies tutaj bedzimy odpalali model"""
print(getString())
print("quitting...")
pygame.quit()
