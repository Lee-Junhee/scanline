from canvas.exceptions import OutOfBoundsException

class Line:
    pic = None
    color = -1

    def __init__(self, pic, color):
        self.pic = pic
        self.color = color

    def oct1(self, x0, y0, z0, x1, y1, z1):
        if (x0 > x1):
            x0, y0, z0, x1, y1, z1 = x1, y1, z1, x0, y0, z0
        x = x0
        y = y0
        z = z0
        A = y1 - y0 
        B = x0 - x1
        C = (z0 - z1) / B
        d = 2 * A + B
        while (x <= x1):
            try:
                self.pic.plot(x, y, z self.color)
            except OutOfBoundsException:
                pass
            if (d > 0):
                y += 1
                d += 2 * B
            x += 1
            z += C
            d += 2 * A

    def oct2(self, x0, y0, z0, x1, y1, z1):
        if (y0 > y1):
            x0, y0, z0, x1, y1, z1 = x1, y1, z1, x0, y0, z0
        x = x0
        y = y0
        z = z0
        A = y1 - y0
        B = x0 - x1
        C = (z1 - z0) / A
        d = A + 2 * B
        while (y <= y1):
            try:
                self.pic.plot(x, y, z, self.color)
            except OutOfBoundsException:
                pass
            if (d < 0):
                x += 1
                d += 2 * A
            y += 1
            z += C 
            d += 2 * B

    def oct7(self, x0, y0, z0, x1, y1, z1):
        if (y1 > y0):
            x0, y0, z0, x1, y1, z1 = x1, y1, z1, x0, y0, z0
        x = x0
        y = y0
        z = z0
        A = y1 - y0
        B = x0 - x1
        C = (z1 - z0) / A
        d = A - 2 * B
        while (y >= y1):
            try:
                self.pic.plot(x, y, z, self.color)
            except OutOfBoundsException:
                pass
            if (d > 0):
                x += 1
                d += 2 * A
            y -= 1
            z -= C
            d -= 2 * B

    def oct8(self, x0, y0, z0, x1, y1, z1):
        if (x0 > x1):
            x0, y0, z0, x1, y1, z1 = x1, y1, z1, x0, y0, z0
        x = x0
        y = y0
        z = z0
        A = y1 - y0
        B = x0 - x1
        C = (z0 - z1) / B
        d = 2 * A - B
        while (x <= x1):
            try:
                self.pic.plot(x, y, z, self.color)
            except OutOfBoundsException:
                pass
            if (d < 0):
                y -= 1
                d -= 2 * B
            x += 1
            z += C
            d += 2 * A

    def drawLine(self, x0, y0, z0, x1, y1, z1):
        try:
            m = (y1 - y0) / (x1 - x0)
        except ZeroDivisionError:
            m = 2
        if (1 <= m):
            self.oct2(x0, y0, z0, x1, y1, z1)
        elif (0 <= m < 1):
            self.oct1(x0, y0, z0, x1, y1, z1)
        elif (-1 <= m < 0):
            self.oct8(x0, y0, z0, x1, y1, z1)
        else:
            self.oct7(x0, y0, z0, x1, y1, z1)

    def draw(self, matrix):
        lines = matrix.lines()
        for line in lines:
            self.drawLine(int(line[0]), int(line[1]), int(line[2]), 
                    int(line[3]), int(line[4]), int(line(5)))