from polygon import Polygon
from canvas import Color
from line import Line
from random import randrange

class Matrix:
    view = None
    edges = None
    polygons = None
    stack = None

    class Fake:
        points = None

        def __init__(self):
            self.points = []

        def plot(self, x, y, z, color):
            row = [point for point in self.points if point[1] == y]
            if len(row):
                self.points.append([x, y, z])
            elif len(row[0]) == 3:
                if row[0] > x:
                    row[0].insert(0, z)
                    row[0].insert(0, y)
                    row[0].insert(0, x)
                else:
                    row[0].append(x)
                    row[0].append(y)
                    row[0].append(z)
            else:
                if row[0] > x:
                    row[0][0] = x
                    row[0][1] = y
                    row[0][2] = z
                elif row[3] < x:
                    row[0][3] = x
                    row[0][4] = y
                    row[0][5] = z

    def multiply(m1, m2, t=False):
        for i in range(len(m2[0])):
            col = [0, 0, 0, 0]
            for j in range(4):
                for k in range(4):
                    col[k] += m1[k][j] * m2[j][i]
            for j in range(4):
                m2[j][i] = col[j]
                if t:
                    m1[j][i] = col[j]

    def ident():
        return [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
                ]

    def __init__(self, view=(0, 0, 1)):
        self.view = view
        self.edges = [[], [], [], []]
        self.polygons = [[], [], [], []]
        self.stack = [[
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
                ]]

    def push(self):
        self.stack.append([[x for x in y] for y in self.stack[-1]])

    def pop(self):
        self.stack.pop(-1)

    def addPoint(matrix, point):
        for i in range(3):
            matrix[i].append(point[i])
        matrix[3].append(1)

    def addEdge(self, p1, p2):
        Matrix.addPoint(self.edges, p1)
        Matrix.addPoint(self.edges, p2)

    def addPolygon(self, p1, p2, p3):
        Matrix.addPoint(self.polygons, p1)
        Matrix.addPoint(self.polygons, p2)
        Matrix.addPoint(self.polygons, p3)

    def print(self):
        print("Edges: ")
        for i in range(4):
            for j in self.edges[i]:
                print("%.2f" % j, end = "\t", flush=True)
            print("")
        print("Polygons: ")
        for i in range(4):
            for j in self.polygons[i]:
                print("%.2f" % j, end = "\t", flush=True)
            print("")

    def addEdges(self, lines):
        matrix = self.edges
        for i in range(len(matrix[3]) // 2):
            lines.append([int(matrix[0][2 * i]), int(matrix[1][2 * i]), int(matrix[2][2 * i]) 
                    int(matrix[0][2 * i + 1]), int(matrix[1][2 * i + 1]), int(matrix[2][2 * i + 1])])
        self.edges = [[], [], [], []]

    def drawPolygons(self, line):
        matrix = self.polygons
        v = self.view
        for i in [3 * j for j in range(len(matrix[3]) // 3)]:
            n = Polygon.normal([matrix[x][i] for x in range(3)], [matrix[x][i + 1] for x in range(3)], [matrix[x][i + 2] for x in range(3)])
            if n[0] * v[0] + n[1] * v[1] + n[2] * v[2]  > 0:
                vertices = [[matrix[x][i + j] for x in range(3)] for j in range(3)]
                canvas = Fake()
                l = Line(canvas, Color(lambda x, y: 125 + randrange(130), lambda x, y: 125 + randrange(130), lambda x, y: 125 + randrange(130)))
                l.drawLine(vertices[0][0], vertices[0][1], vertices[0][2], vertices[1][0], vertices[1][1], vertices[1][2])
                l.drawLine(vertices[1][0], vertices[1][1], vertices[1][2], vertices[2][0], vertices[2][1], vertices[2][2])
                l.drawLine(vertices[2][0], vertices[2][1], vertices[2][2], vertices[0][0], vertices[0][1], vertices[0][2])
                l.pic = line.pic
                for point in canvas.points:
                    l.drawLine(point[0], point[1], point[2], point[3], point[4], point[5], point[6])
                    

        self.polygons = [[], [], [], []]

    def lines(self):
        l = []
        Matrix.multiply(self.stack[-1], self.edges)
        Matrix.multiply(self.stack[-1], self.polygons)
        self.addEdges(l)
        self.addPolygons(l)
        return l
    
    def draw(self, line):
        lines = []
        self.drawPolygons(line)
        for l in self.addEdges(lines):
            line.drawLine(l[0], l[1], l[2], l[3], l[4], l[5])