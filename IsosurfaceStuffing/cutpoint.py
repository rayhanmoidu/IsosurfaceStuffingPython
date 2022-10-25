import point

class Cutpoint():
    def __init__(self, x, y, point1: point.Point, point2: point.Point ):
        self.x = x
        self.y = y
        self.point1 = point1
        self.point2 = point2

    def isContainedByVertex(self, vertex: point.Point):
        if (vertex.x == self.point1.x and vertex.y==self.point1.y):
            return True

        if (vertex.x == self.point2.x and vertex.y==self.point2.y):
            return True
        return False