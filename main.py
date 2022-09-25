import tkinter.messagebox
from tkinter import *
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt

global areaHeight, areaWidth, nodesVertical, nodeHorizontal
canvasWidth = 700
canvasHeight = 500
canvasPadding = 50

class Error(Exception):
    """Base class for other exceptions"""
    pass

class ValueTooSmallError(Error):
    """Raised when the input value is too small"""
    pass

class ValueTooLargeError(Error):
    """Raised when the input value is too large"""
    pass

def coordinate_with_padding(coordinate):
    return coordinate + canvasPadding

def coordinates_with_padding(coordinates):
    return [coordinates[0] + canvasPadding, coordinates[1] + canvasPadding]

def create_circle(x, y, r, canvasName):
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1, fill="#111")

def UiComponents():
    root = Tk()
    style = ttk.Style()
    style.configure("TFrame", background='#fbfbfb')

    root.title('Paweł Basałygo')
    root.geometry("950x900")
    root.config(bg='#fbfbfb')

    mainFrame = ttk.Frame(root)
    mainFrame.grid()

    topFrame = ttk.LabelFrame(mainFrame, text='Parametry', style='TFrame')
    topFrame.grid(column=1, row=1, pady=5, padx=10)

    Label(topFrame, text='Implementacja MRS w celu obliczenia rozkładu temperatury w obszarze 2D',
          fg='black', bg='#fbfbfb', font=('Arial', 14)).grid(row=0, pady=12, columnspan=6)
    Label(topFrame, text='Wysokość: ', fg='black', bg='#fbfbfb', font=('Arial', 14)).grid(row=1, pady=12)
    Label(topFrame, text='Szerokość: ', fg='black', bg='#fbfbfb', font=('Arial', 14)).grid(row=2, pady=12)
    Label(topFrame, text='Liczba węzłów pion: ', fg='black', bg='#fbfbfb', font=('Arial', 14)).grid(column=2, row=1, pady=12)
    Label(topFrame, text='Liczba węzłów poziom: ', fg='black', bg='#fbfbfb', font=('Arial', 14)).grid(column=2, row=2, pady=12)
    Label(topFrame, text='Gęstość mocy cieplnej:  ', fg='black', bg='#fbfbfb', font=('Arial', 14)).grid(column=4, row=1, pady=12)

    areaHeight = Entry(topFrame)
    areaHeight.insert(END, 15)
    areaHeight.grid(column=1, row=1, ipady=3)

    areaWidth = Entry(topFrame)
    areaWidth.insert(END, 15)
    areaWidth.grid(column=1, row=2, ipady=3)

    nodesVertical = Entry(topFrame)
    nodesVertical.insert(END, 5)
    nodesVertical.grid(column=3, row=1, ipady=3)

    nodeHorizontal = Entry(topFrame)
    nodeHorizontal.insert(END, 5)
    nodeHorizontal.grid(column=3, row=2, ipady=3)

    densityCharge = Entry(topFrame)
    densityCharge.insert(END, 2)
    densityCharge.grid(column=5, row=1, ipady=3)

    def drawFrame():
        print('Drawing')

        canvas.delete('all')

        # Pobranie wartości z inputów
        try:
            Height = int(areaHeight.get())
            Width = int(areaWidth.get())
            verticalNodes = int(nodesVertical.get())
            horizontalNodes = int(nodeHorizontal.get())
            #temperatureDensity = int(densityCharge.get())
            if verticalNodes < 3 or horizontalNodes < 3:
                raise ValueTooSmallError
            if verticalNodes > 20 or horizontalNodes > 20:
                raise ValueTooSmallError
        except ValueTooSmallError:
            print("Podana liczba węzłów jest zbyt mała")
            return
        except ValueTooLargeError:
            print("Podana liczba węzłów jest zbyt duża")
            return
        except ValueError:
            print("Niewłaściwa wartość.")
            return

        # Obliczenie odległości między punktami
        nodesVerticalCoordinates = np.linspace(0, Width, verticalNodes)
        nodesHorizontalCoordinates = np.linspace(0, Height, horizontalNodes)

        nodeNumber = verticalNodes * horizontalNodes

        nodeCoordinates = []
        for horizontalElement in nodesHorizontalCoordinates:
            for verticalElement in nodesVerticalCoordinates:
                nodeCoordinates.append([verticalElement / Width * canvasWidth,
                                        horizontalElement / Height * canvasHeight])

        rectangleNumber = (verticalNodes - 1) * (horizontalNodes - 1)

        # Wyliczanie współrzędnych nodów.
        elementNode = []
        firstNode = 1
        secoundNode = 2
        thirdNode = verticalNodes + 1
        fourthNode = verticalNodes + 2

        for node in range(rectangleNumber):
            elementNode.append([firstNode, secoundNode, thirdNode, fourthNode])

            if (firstNode + 1) % (verticalNodes - 0) == 0:
                firstNode = firstNode + 2
                secoundNode = firstNode + 1
                thirdNode = firstNode + verticalNodes
                fourthNode = firstNode + verticalNodes + 1
            else:
                firstNode = firstNode + 1
                secoundNode = firstNode + 1
                thirdNode = thirdNode + 1
                fourthNode = fourthNode + 1

                # Rysowanie trójkątów
        for element in elementNode:
            points = [nodeCoordinates[element[0] - 1][0], nodeCoordinates[element[0] - 1][1],
                      nodeCoordinates[element[3] - 1][0], nodeCoordinates[element[3] - 1][1]]
            canvas.create_rectangle(points, outline='gray')

        lp = 1
        for node in nodeCoordinates:
            create_circle(node[0], node[1], 5, canvas)
            canvas.create_text(node[0], node[1] + 10, fill="black", font="Times 12", text=lp)#punkty na siatce
            lp = lp + 1

    def solve():
        boundaryTop = boundaryTopInput.get()
        boundaryTop = float(boundaryTop)
        boundaryLeft = boundaryLeftInput.get()
        boundaryLeft = float(boundaryLeft)
        boundaryRight = boundaryRightInput.get()
        boundaryRight = float(boundaryRight)
        boundaryBottom = boundaryBottomInput.get()
        boundaryBottom = float(boundaryBottom)
        temperatureDensity = densityCharge.get()
        temperatureDensity = float(temperatureDensity)
        Height = areaHeight.get()
        Height = float(Height)

        wl = boundaryLeft
        wp = boundaryRight
        wd = boundaryBottom
        wg = boundaryTop
        omega = 1.6

        nx = int(nodeHorizontal.get())
        ny = int(nodesVertical.get())

        A = np.zeros((nx, ny))
        A[A[0].size - 1] = wg
        A[0] = wd
        A[:, ny-1] = wp
        A[:, 0] = wl

        for k in range(10):
            for i in range(1, nx - 1):
                for j in range(1, ny - 1):
                    A[i, j] = A[i, j] + omega / 4 * (A[i + 1, j] + A[i - 1, j]) + omega / 4 * (
                                A[i, j - 1] + A[i, j + 1] - 4 * A[i, j] + ((Height*Height)*temperatureDensity))

        x = np.linspace(0, 1, nx)
        y = np.linspace(0, 1, ny)

        plt.contourf(x, y, A)
        plt.axis('scaled')
        plt.colorbar()
        plt.show()


    drawGridButton = Button(topFrame, text='RYSUJ SIATKĘ', width=20, bg='#66ff66', borderwidth=0, fg='black', font=('Arial', 12, 'bold'),
                            command=drawFrame).grid(row=4, column=0, columnspan=3, pady=10)

    calculateButton = Button(topFrame, text='OBLICZ', width=20, bg='#66ff66', borderwidth=0, fg='black', font=('Arial', 12, 'bold'),
                             command=solve).grid(row=4, column=3, columnspan=3, pady=10)

    bottomFrame = ttk.Frame(mainFrame)
    bottomFrame.grid(column=1, row=2)

    boundaryTopInput = Entry(bottomFrame, width=5)
    boundaryTopInput.grid(column=1, row=1, columnspan=3)
    boundaryLeftInput = Entry(bottomFrame, width=5)
    boundaryLeftInput.grid(column=1, row=2)
    boundaryRightInput = Entry(bottomFrame, width=5)
    boundaryRightInput.grid(column=3, row=2)
    boundaryBottomInput = Entry(bottomFrame, width=5)
    boundaryBottomInput.grid(column=1, row=3, columnspan=3)

    canvasFrame = ttk.Frame(bottomFrame)
    canvasFrame.grid(column=2, row=2)

    canvas = Canvas(canvasFrame, width=canvasWidth, height=canvasHeight, bg="white")
    canvas.pack()

    root.mainloop()


if __name__ == "__main__":
    UiComponents()
