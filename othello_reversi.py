import sys
from PyQt5.QtWidgets import QWidget, QMainWindow,QApplication, QAction,\
                        QMessageBox, QHBoxLayout, QLabel, QPushButton, QColorDialog , qApp, QTextBrowser
from PyQt5.QtGui import QIcon, QDesktopServices, QColor, QFont
from PyQt5.QtCore import QSize, QUrl, Qt

coords = [0, 60, 120, 180, 240, 300, 360, 420]

tableCoords = []

diffs = [(-60, -60), (0, -60), (60, -60), (-60, 0),
         (60, 0), (-60, 60), (0, 60), (60, 60)]

directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
              (0, 1), (1, -1), [1, 0], (1, 1)]

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.content = Reversi()
        self.setCentralWidget(self.content)

        self.initMW()

    def initMW(self):
        menubar = self.menuBar()
        menubar.setStyleSheet("background-color: white;"
                              "color: black")
        file = menubar.addMenu("About")

        github = QAction("Github Codes", self)
        github.triggered.connect(self.openUrl)
        github.setStatusTip("Click To Connect Github and View The Codes")
        file.addAction(github)

        exitAct = QAction("Quit", self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip("Click to quit")
        exitAct.triggered.connect(qApp.quit)
        file.addAction(exitAct)

        self.statusBar()
        self.setStyleSheet("background-color: white")
        self.move(250, 100)
        self.setFixedSize(780, 535)
        self.setWindowTitle('Reversi | Selman Y.')
        self.show()

    def openUrl(self):
        url = QUrl("https://github.com/kmnsys/Reversi_Othello")
        if not QDesktopServices.openUrl(url):
            QMessageBox.warning(self, 'Open Url', 'Could not Open Url')


class Reversi(QWidget):

    def __init__(self):
        super().__init__()

        self.wbTurn = 2

        self.initRV()

    def initRV(self):
        col = QColor(25, 196, 99)

        hbox = QHBoxLayout()

        self.labelBoard = QLabel()
        self.labelTools = QLabel()
        hbox.addWidget(self.labelBoard)
        hbox.addWidget(self.labelTools)

        self.labelBoard.resize(500, 500)
        self.labelBoard.setMinimumWidth(480.9)
        self.labelTools.setMinimumWidth(200)

        self.setLayout(hbox)

        btnColl = QPushButton("LEFT", self.labelTools)
        btnColl.clicked.connect(self.showDialog)
        btnColl.setGeometry(150, 144, 60, 60)
        btnColl.setStyleSheet("""border-style: outset;
                                border-radius: 30px;
                                border-width: 4px;
                                font: 10px;
                                color: black""")

        btnColr = QPushButton("RIGHT", self.labelTools)
        btnColr.clicked.connect(self.showDialog)
        btnColr.setGeometry(150, 268, 60, 60)
        btnColr.setStyleSheet("""border-style: outset;
                                        border-radius: 30px;
                                        border-width: 4px;
                                        font: 10px;
                                        color: black""")

        self.labelBoard.setStyleSheet("QWidget { background-color: %s }"
                                      % col.name())
        self.labelTools.setStyleSheet("""background-color: #f1f2ae;
                                         border-left-style: outset;
                                         border-top-style: outset;
                                         border-radius: 30px;
                                         border-width: 60px;
                                         border-color: beige""""")

        self.b = QPushButton(self.labelTools)
        self.b.setGeometry(10, 70, 100, 100)
        self.b.setStyleSheet("""
                                border-style: outset;
                                border-radius: 50px;
                                border-width: 6px;
                                border-color: black;
                                font: 45px;
                                color: black 
                                """)

        self.w = QPushButton(self.labelTools)
        self.w.setGeometry(10, 190, 100, 100)
        self.w.setStyleSheet("""
                                border-style: outset;
                                border-radius: 50px;
                                border-width: 6px;
                                border-color: white;
                                font: 45px;
                                color: white""")

        self.e = QPushButton(self.labelTools)
        self.e.setGeometry(10, 310, 100, 100)
        self.e.setStyleSheet("""
                                border-style: outset;
                                border-radius: 50px;
                                border-width: 6px;
                                border-color: green;
                                font: 45px;
                                color: green
                                """)
        self.turn = QTextBrowser(self)
        self.turn.setGeometry(538, 26, 200, 40)
        self.turn.setStyleSheet(""""border-style: outset;
                                    border-width: 5px;
                                    border-color: white;
                                    font: 20px;
                                    """)
        font = QFont()
        font.setPointSize(14)
        self.turn.setText("BEYAZ")
        self.turn.setFont(font)
        self.turn.setAlignment(Qt.AlignCenter)


        self.lists()
        self.table()
        self.score()

    def lists(self):
        self.colorTable = [[] for i in range(8)]
        self.buttons = [[] for i in range(8)]

        for i in range(8):
            for j in range(8):
                self.buttons[i].append("self.b" + str(i + 1) + "_" + str(j + 1))
                if (i, j) == (3, 4) or (i, j) == (4, 3):
                    self.colorTable[i].append(1)
                elif (i, j) == (3, 3) or (i, j) == (4, 4):
                    self.colorTable[i].append(2)
                else:
                    self.colorTable[i].append(0)
                exec("%s = %d" % (str(self.buttons[i][j]), 1))

        self.zeroColTab = []

    def table(self):

        m = 0
        n = 0
        for i in coords:
            for j in coords:
                self.buttons[m][n] = QPushButton(self.labelBoard)
                self.buttons[m][n].resize(60, 60)
                self.buttons[m][n].move(*(j, i))
                self.buttons[m][n].setStyleSheet("""border-style: outset;
                                              border-width: 5px;
                                              border-radius: 4px;    
                                              border-color: beige 
                                              """)
                if (m, n) == (3, 4) or (m, n) == (4, 3):
                    self.buttons[m][n].setIcon(QIcon("black.png"))
                    self.buttons[m][n].setIconSize(QSize(48, 48))
                elif (m, n) == (3, 3) or (m, n) == (4, 4):
                    self.buttons[m][n].setIcon(QIcon("white.png"))
                    self.buttons[m][n].setIconSize(QSize(48, 48))
                else:
                    self.zeroColTab.append((j, i))
                tableCoords.append((j, i))
                self.buttons[m][n].clicked.connect(self.reverse)
                if n == 7:
                    m += 1
                    n = -1
                n += 1
        self.clickableButtons()

    def ifNearButton(self, crdnt):
        nearButtons = []
        nearButtonColors = []
        for i in range(8):
            nearcoord = (crdnt[0] + diffs[i][0], crdnt[1] + diffs[i][1])
            if nearcoord in tableCoords:
                nearButtons.append(nearcoord)
                positionx =  self.placeinList(tableCoords.index(nearcoord))[0]
                positiony =  self.placeinList(tableCoords.index(nearcoord))[1]
                nearButtonColors.append(self.colorTable[positionx][positiony])

        if 1 in nearButtonColors or 2 in nearButtonColors:
            return [True, nearButtons]
        else:
            return [False, nearButtons]

    def reverse(self):
        sender = self.sender()
        senderCoords = (sender.x(), sender.y())

        if senderCoords in self.zeroColTab and self.ifNearButton(senderCoords)[0] is True and True in self.validMoveDirects(senderCoords, self.wbTurn)[0]:
            self.zeroColTab.remove(senderCoords)
            sx = tableCoords.index(senderCoords)
            pcx = self.placeinList(sx)[0]
            pcy = self.placeinList(sx)[1]

            if self.wbTurn == 2:
                sender.setIcon(QIcon("white.png"))
                sender.setIconSize(QSize(48, 48))
                self.colorTable[pcx][pcy] = 2
                self.turn.setText("SİYAH")
                self.turn.setAlignment(Qt.AlignCenter)
                h = self.validMoveDirects(senderCoords, self.wbTurn)

                for i in range(8):
                    pcx = self.placeinList(sx)[0]
                    pcy = self.placeinList(sx)[1]
                    if h[0][i] == True:
                        j = h[1][i]
                        addx = directions[i][0]
                        addy = directions[i][1]
                        for k in range(j):
                            pcx = pcx + addx
                            pcy = pcy + addy
                            self.buttons[pcx][pcy].setIcon(QIcon("white.png"))
                            self.buttons[pcx][pcy].setIconSize(QSize(48, 48))
                            self.colorTable[pcx][pcy] = 2

            elif self.wbTurn == 1:
                sender.setIcon(QIcon("black.png"))
                sender.setIconSize(QSize(48, 48))
                self.colorTable[pcx][pcy] = 1
                self.turn.setText("BEYAZ")
                self.turn.setAlignment(Qt.AlignCenter)
                h = self.validMoveDirects(senderCoords, self.wbTurn)

                for i in range(8):
                    pcx = self.placeinList(sx)[0]
                    pcy = self.placeinList(sx)[1]
                    if h[0][i] == True:
                        j = h[1][i]
                        addx = directions[i][0]
                        addy = directions[i][1]
                        for k in range(j):
                            pcx = pcx + addx
                            pcy = pcy + addy
                            self.buttons[pcx][pcy].setIcon(QIcon("black.png"))
                            self.buttons[pcx][pcy].setIconSize(QSize(48, 48))
                            self.colorTable[pcx][pcy] = 1

            self.score()
            self.clickables.remove(senderCoords)
            self.clear()
            self.wbTurn = 3 - self.wbTurn
            self.clickableButtons()
            if len(self.clickables) == 0:
                self.wbTurn = 3- self.wbTurn
                self.clickableButtons()
        self.gameOver()

    def clickableButtons(self):
        self.clickables =[]

        for i in self.zeroColTab:
            if self.ifNearButton(i)[0] is True and True in self.validMoveDirects(i, self.wbTurn)[0]:
                indx = self.placeinList(tableCoords.index(i))[0]
                indy = self.placeinList(tableCoords.index(i))[1]

                self.buttons[indx][indy].setIcon(QIcon("avs.png"))
                self.buttons[indx][indy].setIconSize(QSize(32, 32))

                self.clickables.append(i)

    def clear(self):
        for i in self.clickables:
            indx = self.placeinList(tableCoords.index(i))[0]
            indy = self.placeinList(tableCoords.index(i))[1]

            self.buttons[indx][indy].setIcon(QIcon())

    def validMoveDirects(self, senderCoords, col):
        truthTable = [[], []]
        newl = []
        for direct in directions:
            xi = self.placeinList(tableCoords.index(senderCoords))[0] + direct[0]
            yi = self.placeinList(tableCoords.index(senderCoords))[1] + direct[1]

            if self.inTable(xi, yi) == False:
                truthTable[0].append(False)
                truthTable[1].append(0)
            else:
                if self.colorTable[xi][yi] == col:
                    truthTable[0].append(False)
                    truthTable[1].append(0)
                else:
                    while self.inTable(xi, yi) == True:
                        if self.colorTable[xi][yi] != 0:
                            newl.append(self.colorTable[xi][yi])

                            if self.colorTable[xi][yi] ==col:
                                break
                        else:
                            break
                        xi = xi + direct[0]
                        yi = yi + direct[1]

                    if len(newl) <= 1:
                        truthTable[0].append(False)
                        truthTable[1].append(0)
                    elif newl[-1]!=col:
                        truthTable[0].append(False)
                        truthTable[1].append(0)
                    else:
                        truthTable[0].append(True)
                        truthTable[1].append(len(newl) - 1)
                    newl = []
        return truthTable

    def score(self):
        self.white = 0
        self.black = 0
        self.remain = 0
        for i in self.colorTable:
            self.white = self.white + i.count(2)
            self.black = self.black + i.count(1)
            self.remain= self.remain + i.count(0)

        self.w.setText(str(self.white))
        self.b.setText(str(self.black))
        self.e.setText(str(self.remain))


    def gameOver(self):
        if self.remain == 0:
            if self.white > self.black:
                QMessageBox.information(self, "GAME OVER", "WHITE WIN \n" + "********************************\n"  + "White = "
                                        + str(self.white) + "\nBlack = " + str(self.black))
            elif self.black >self.white:
                QMessageBox.information(self,"GAME OVER", "BLACK WIN\n"+ "********************************\n"+ "Black = " + str(self.black)
                                        + "\nWhite = " + str(self.white))
            else:
                QMessageBox.information(self, "GAME OVER", "\n********************************" + "DRAW" )


    def inTable(self, xi, yi):
        z = [0, 1, 2, 3, 4, 5, 6, 7]
        if xi in z and yi in z:
            return True
        else:
            return False

    def placeinList(self, num):
        x = int(str(num / 8)[0])
        y = num % 8
        return [x, y]

    def showDialog(self):
        sender =self.sender()
        senderText = sender.text()
        col = QColorDialog.getColor() #This line pops up the QColorDialog.

        if col.isValid():
            if senderText == "LEFT":
                self.labelBoard.setStyleSheet("QWidget { background-color: %s }"
                               % col.name())
            else:
                self.labelTools.setStyleSheet("""background-color: """ + col.name() + """;border-left-style: outset;
                                                         border-top-style: outset;
                                                         border-radius: 30px;
                                                         border-width: 60px;
                                                         border-color: beige""")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gm = MainWindow()
    sys.exit(app.exec_())
