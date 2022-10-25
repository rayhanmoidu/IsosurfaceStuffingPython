from cmath import inf, sqrt
from operator import truediv
from pickle import FALSE
import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from cutpoint import Cutpoint
import point
import triangle
import random
import decimal
import math
import freetype

# next steps
# reread article and make sure about step 4 of algo
# try with equilateral triangle


screenWidth = 1000
screenHeight = 500
triangleSideLength = 60
circleRadius = 200
circleOffset = circleRadius + ((500 - (2 * circleRadius)) / 2)
alpha = 30

w,h= screenWidth,screenHeight

vertices = []
triangles = []
trianglesToConsider = []
perimeterTriangles = []
cutpoints = []
anglesFrequencies = {}


def distanceFromIsoSurface(x, y):
    return distanceFromCircle(x, y)

def setupTriangles():
    createNewEquilateralTriangles(0, 0, "all", "normal")

def createNewEquilateralTriangles(curX, curY, key, orientation):
    if curX <screenWidth and curY<screenHeight:
        point1 = point.Point(curX, curY)
        point2 = point.Point(curX+triangleSideLength, curY)
        if orientation=="normal":
            point3 = point.Point(curX+triangleSideLength+(triangleSideLength/2), curY+ (math.sqrt(3)/2*triangleSideLength))
            point4 = point.Point(curX+(triangleSideLength/2), curY+ (math.sqrt(3)/2*triangleSideLength))
        else:
            point3 = point.Point(curX+(triangleSideLength/2), curY+ (math.sqrt(3)/2*triangleSideLength))
            point4 = point.Point(curX-(triangleSideLength/2), curY+ (math.sqrt(3)/2*triangleSideLength))

        vertices.append(point1)
        vertices.append(point2)
        vertices.append(point3)
        vertices.append(point4)

        if orientation !="normal":
            triangle1 = triangle.Triangle(point1, point2, point3)
            triangle2 = triangle.Triangle(point1, point4, point3)
        else:
            triangle1 = triangle.Triangle(point1, point2, point4)
            triangle2 = triangle.Triangle(point2, point4, point3)

        triangles.append(triangle1)
        triangles.append(triangle2)

        if orientation=="normal":
            oppositekey="inverted"
        else:
            oppositekey="normal"

        if key=="up":
            createNewEquilateralTriangles(point4.x, point4.y, "up", oppositekey)
        
        if key=="right":
            createNewEquilateralTriangles(point2.x, point2.y, "right", orientation)

        if key=="all":
            createNewEquilateralTriangles(point2.x, point2.y, "right", orientation)
            createNewEquilateralTriangles(point3.x, point3.y, "all", oppositekey)
            createNewEquilateralTriangles(point4.x, point4.y, "up", oppositekey)


def createNewIscocelesTriangles(curX, curY, key, orientation):

    if curX <screenWidth and curY<screenHeight:
        
        point1 = point.Point(curX, curY)
        point2 = point.Point(curX+triangleSideLength, curY)
        point3 = point.Point(curX+triangleSideLength, curY+triangleSideLength)
        point4 = point.Point(curX, curY+triangleSideLength)

        vertices.append(point1)
        vertices.append(point2)
        vertices.append(point3)
        vertices.append(point4)

        if orientation =="normal":
            triangle1 = triangle.Triangle(point1, point2, point3)
            triangle2 = triangle.Triangle(point1, point4, point3)
        else:
            triangle1 = triangle.Triangle(point1, point2, point4)
            triangle2 = triangle.Triangle(point2, point4, point3)

        triangles.append(triangle1)
        triangles.append(triangle2)

        if orientation=="normal":
            oppositekey="inverted"
        else:
            oppositekey="normal"

        if key=="up":
            createNewIscocelesTriangles(point4.x, point4.y, "up", oppositekey)
        
        if key=="right":
            createNewIscocelesTriangles(point2.x, point2.y, "right", oppositekey)

        if key=="all":
            createNewIscocelesTriangles(point2.x, point2.y, "right", oppositekey)
            createNewIscocelesTriangles(point3.x, point3.y, "all", "normal")
            createNewIscocelesTriangles(point4.x, point4.y, "up", oppositekey)
    return

def drawTriangle(tri: triangle.Triangle):
    glBegin(GL_QUADS)
    glVertex2f(tri.point1.x, tri.point1.y) # Coordinates for the bottom left point
    glVertex2f(tri.point1.x, tri.point1.y) # Coordinates for the bottom right point
    glVertex2f(tri.point2.x, tri.point2.y) # Coordinates for the top left point
    glVertex2f(tri.point3.x, tri.point3.y) # Coordinates for the top left point
    glEnd()

def drawTriangles():
    for tri in trianglesToConsider:
        colorkey1 = decimal.Decimal(random.randrange(0, 100))/100
        colorkey2 = decimal.Decimal(random.randrange(0, 100))/100
        colorkey3 = decimal.Decimal(random.randrange(0, 100))/100
        glColor3f(colorkey1, colorkey2, colorkey3)
        drawTriangle(tri)

def distanceFromCircle(x, y):
    length = math.sqrt((x-250)*(x-250) + (y-250)*(y-250))
    return length - circleRadius

def distanceFromBox(x, y):
    newX = x - 250
    newY = y - 250

    boxWidth = 200
    boxHeight = 200

    px = abs(newX) - boxWidth
    py = abs(newY) - boxHeight

    toSquareX = px
    toSquareY = py

    if ((px==0 and py<0) or (py==0 and px < 0)):
        return 0
    elif (px < 0 and py < 0):
        return max(px, py)
    elif px < 0:
        return py
    elif py < 0:
        return px
    else:
        return math.sqrt(toSquareX*toSquareX + toSquareY*toSquareY)

def distanceFromEquilateralTriangle(x, y):
    k = math.sqrt(2)

    newX = abs(x-250) - 250
    newY = (y-250) + 250/k

    if (newX + k*newY > 0):
        newX = (newX - k*newY) / 500
        newY = (-k*newX - newY) / 500
    
    newX = newX - min(max( newX , -500 ), 0 )

    length = math.sqrt(newX*newX + newY*newY)

    if newY>=0:
        return -length
    elif newY==0:
        return 0
    else:
        return length



def isVertexInsideIsosurface(x, y):
    if (distanceFromIsoSurface(x, y)==0):
        return 0
    elif distanceFromIsoSurface(x, y)>0:
        return -1
    else:
        return 1


def drawIsosurface():
    threshold = 0.5
    for i in range(1, 500):
        for j in range(1, 500):
            if (distanceFromIsoSurface(i, j)>-threshold and distanceFromIsoSurface(i, j)<threshold):
                glBegin(GL_QUADS)
                glVertex2f(i, j) # Coordinates for the bottom left point
                glVertex2f(i+1, j) # Coordinates for the bottom left point
                glVertex2f(i+1, j+1) # Coordinates for the bottom left point
                glVertex2f(i, j+1) # Coordinates for the bottom left point
                
                glEnd()

def filterTriangles():
    for triangle in triangles:
        isInside1 = isVertexInsideIsosurface(triangle.point1.x, triangle.point1.y)
        isInside2 = isVertexInsideIsosurface(triangle.point2.x, triangle.point2.y)
        isInside3 = isVertexInsideIsosurface(triangle.point3.x, triangle.point3.y)
        if isInside1==1 or isInside2==1 or isInside3==1:
            trianglesToConsider.append(triangle)
            if isInside1==-1 or isInside2==-1 or isInside3==-1:
                perimeterTriangles.append(triangle)

def findCutPointAlongLine(posVertex: point.Point, negVertex: point.Point):
    retValX = 0
    retValY = 0

    x1 = negVertex.x
    x2 = posVertex.x
    y1 = negVertex.y
    y2 = posVertex.y

    dx = x2 - x1
    dy = y2 - y1

    a = abs(distanceFromIsoSurface(x1, y1))
    b = abs(distanceFromIsoSurface(x2, y2))
    cutPointPercentage = a / (a + b)

    retValX = x1 + cutPointPercentage*dx
    retValY = y1 + cutPointPercentage*dy

    return point.Point(retValX, retValY)



def findCutPoints():
    for tri in perimeterTriangles:
        isInside1 = isVertexInsideIsosurface(tri.point1.x, tri.point1.y)
        isInside2 = isVertexInsideIsosurface(tri.point2.x, tri.point2.y)
        isInside3 = isVertexInsideIsosurface(tri.point3.x, tri.point3.y)

        negativeVertices = []
        positiveVertices = []
        if isInside1==-1:
            negativeVertices.append(tri.point1)
        if isInside1==1:
            positiveVertices.append(tri.point1)
        if isInside2==-1:
            negativeVertices.append(tri.point2)
        if isInside2==1:
            positiveVertices.append(tri.point2)
        if isInside3==-1:
            negativeVertices.append(tri.point3)
        if isInside3==1:
            positiveVertices.append(tri.point3)

        for posVertex in positiveVertices:
            for negVertex in negativeVertices:
                newCutPoint = findCutPointAlongLine(posVertex, negVertex)
                newCutPointObj = Cutpoint(newCutPoint.x, newCutPoint.y, posVertex, negVertex)
                tri.cutpoints.append(newCutPointObj)

                # cutpoints.append(newCutPointObj)

def plotCutPoints():
    for triangle in perimeterTriangles:
        cutpoints.extend(triangle.cutpoints)

    for cutpoint in cutpoints:
        xToPlot = cutpoint.x
        yToPlot = cutpoint.y
        glBegin(GL_QUADS)
        glVertex2f(xToPlot-2, yToPlot-2) # Coordinates for the bottom left point
        glVertex2f(xToPlot+2, yToPlot-2) # Coordinates for the bottom left point
        glVertex2f(xToPlot+2, yToPlot+2) # Coordinates for the bottom left point
        glVertex2f(xToPlot-2, yToPlot+2) # Coordinates for the bottom left point
        glEnd()

def distanceBetweenTwoPoints(point1: point.Point, point2: point.Point):
    return math.sqrt((point2.x - point1.x)*(point2.x - point1.x) + (point2.y - point1.y)*(point2.y - point1.y))

def warpCutPoints():
    for triangle in perimeterTriangles:
        points = [triangle.point1, triangle.point2, triangle.point3]
        for curPoint in points:
            if (isVertexInsideIsosurface(curPoint.x, curPoint.y)==-1):
                trianglesSharingVertex = []
                for tri in perimeterTriangles:
                    if tri.doesContainVertex(curPoint):
                        trianglesSharingVertex.append(tri)
                cutPointsToConsider = []
                for tri in trianglesSharingVertex:
                    potentialCutpoints = tri.cutpoints
                    for potentialCutpoint in potentialCutpoints:
                        if (potentialCutpoint.isContainedByVertex(curPoint)):
                            cutPointsToConsider.append(potentialCutpoint)
                
                lowestDistance = inf 
                lowestDistanceIndex = -1
                for i in range(0, len(cutPointsToConsider)):
                    if (distanceBetweenTwoPoints(curPoint, point.Point(cutPointsToConsider[i].x, cutPointsToConsider[i].y)) < lowestDistance):
                        lowestDistanceIndex = i
                        lowestDistance = distanceBetweenTwoPoints(curPoint, point.Point(cutPointsToConsider[i].x, cutPointsToConsider[i].y))
                if lowestDistanceIndex!=-1 and lowestDistance < alpha:
                    # print(lowestDistance)
                    cutPointToWarpTo = cutPointsToConsider[lowestDistanceIndex]
                    # print("Wrapping to ", cutPointToWarpTo.x, cutPointToWarpTo.y)

                    for tri in trianglesSharingVertex:
                        tri.wrapVertexToCutpoint(curPoint.x, curPoint.y, cutPointToWarpTo)

                    for cutPointToRemove in cutPointsToConsider:
                        for tritri in perimeterTriangles:
                            if tritri.doesContainCutpoint(cutPointToRemove):
                                tritri.removeCutpoint(cutPointToRemove)
    
def clipPerimeterTriangles():
    newPerimeterTriangles = []
    for tri in trianglesToConsider:
        isInside1 = isVertexInsideIsosurface(tri.point1.x, tri.point1.y)
        isInside2 = isVertexInsideIsosurface(tri.point2.x, tri.point2.y)
        isInside3 = isVertexInsideIsosurface(tri.point3.x, tri.point3.y)

        if isInside1 < 0 or isInside2 < 0 or isInside3 < 0:
            newPerimeterTriangles.append(tri)

    perimeterTriangles.clear()
    perimeterTriangles.extend(newPerimeterTriangles)

    for tri in perimeterTriangles:
        isInside1 = isVertexInsideIsosurface(tri.point1.x, tri.point1.y)
        isInside2 = isVertexInsideIsosurface(tri.point2.x, tri.point2.y)
        isInside3 = isVertexInsideIsosurface(tri.point3.x, tri.point3.y)

        negativeVertices = []
        positiveVertices = []
        if isInside1 < 0:
            negativeVertices.append(tri.point1)
        else:
            positiveVertices.append(tri.point1)

        if isInside2 < 0:
            negativeVertices.append(tri.point2)
        else:
            positiveVertices.append(tri.point2)

        if isInside3 < 0:
            negativeVertices.append(tri.point3)
        else:
            positiveVertices.append(tri.point3)

    
        if len(negativeVertices)>=1:
            if len(negativeVertices)==2:
                cutPoint1 = findCutPointAlongLine(negativeVertices[0], positiveVertices[0])
                cutPoint2 = findCutPointAlongLine(negativeVertices[1], positiveVertices[0])
                tri.removeCutpoints()
                trianglesToConsider.remove(tri)
                # perimeterTriangles.remove(tri)
                triangles.remove(tri)

                newTriangle = triangle.Triangle(cutPoint1, cutPoint2, positiveVertices[0])
                triangles.append(newTriangle)
                trianglesToConsider.append(newTriangle)
            elif len(negativeVertices)==1:
                cutPoint1 = findCutPointAlongLine(negativeVertices[0], positiveVertices[0])
                cutPoint2 = findCutPointAlongLine(negativeVertices[0], positiveVertices[1])
                tri.removeCutpoints()
                trianglesToConsider.remove(tri)
                # perimeterTriangles.remove(tri)
                triangles.remove(tri)

                newTriangle1 = triangle.Triangle(cutPoint1, positiveVertices[1], positiveVertices[0])
                newTriangle2 = triangle.Triangle(cutPoint2, positiveVertices[1], cutPoint1)
                triangles.append(newTriangle1)
                trianglesToConsider.append(newTriangle1)
                triangles.append(newTriangle2)
                trianglesToConsider.append(newTriangle2)

def findAngles():
    for tri in trianglesToConsider:
        dx1 = (tri.point1.x)-(tri.point2.x)
        dy1 = (tri.point1.y)-(tri.point2.y)
        a = math.sqrt(dx1*dx1 + dy1*dy1)

        dx2 = (tri.point2.x)-(tri.point3.x)
        dy2 = (tri.point2.y)-(tri.point3.y)
        b = math.sqrt(dx2*dx2 + dy2*dy2)

        dx3 = (tri.point3.x)-(tri.point1.x)
        dy3 = (tri.point3.y)-(tri.point1.y)
        c = math.sqrt(dx3*dx3 + dy3*dy3)

        angle1 = math.acos((b*b + c*c - a*a) / (2*b*c))
        angle1 = angle1*180 / math.pi
        angle2 = math.acos((b*b + a*a - c*c) / (2*b*a))
        angle2 = angle2*180 / math.pi
        angle3 = math.acos((c*c + a*a - b*b) / (2*c*a))
        angle3 = angle3*180 / math.pi

        if round(angle1) in anglesFrequencies.keys():
            anglesFrequencies[round(angle1)] += 1
        else:
            anglesFrequencies[round(angle1)] = 1
    
    # for key in anglesFrequencies.keys():
    #     print(key, anglesFrequencies[key])

def plotGraph():
    glBegin(GL_QUADS)
    glVertex2f(525, 20) # Coordinates for the bottom left point
    glVertex2f(530, 20) # Coordinates for the bottom left point
    glVertex2f(530, 480) # Coordinates for the bottom left point
    glVertex2f(525, 480) # Coordinates for the bottom left point
    glEnd()

    glBegin(GL_QUADS)
    glVertex2f(525, 20) # Coordinates for the bottom left point
    glVertex2f(975, 20) # Coordinates for the bottom left point
    glVertex2f(975, 25) # Coordinates for the bottom left point
    glVertex2f(525, 25) # Coordinates for the bottom left point
    glEnd()

    groupedFrequencies = {}

    total = 0

    for angle in range(1, 180):
        curKey = math.ceil(angle / 5)
        if angle in anglesFrequencies.keys():
            if curKey in groupedFrequencies.keys():
                groupedFrequencies[curKey] += anglesFrequencies[angle]
            else:
                groupedFrequencies[curKey] = anglesFrequencies[angle]

            total += anglesFrequencies[angle]
    
    maxGroupedVal = -1
    for key in groupedFrequencies.keys():
        if groupedFrequencies[key] > maxGroupedVal:
            maxGroupedVal = groupedFrequencies[key]

    graphWidth = 450
    graphHeight = 455
    widthOfOneBar = graphWidth / 36

    valueOfOneVerticalPixel = graphHeight / maxGroupedVal

    for key in groupedFrequencies.keys():
        curVal = groupedFrequencies[key]

        startPointOfBar = 530 + widthOfOneBar*(key-1)
        heightOfBar = valueOfOneVerticalPixel*curVal
        colorkey1 = decimal.Decimal(random.randrange(0, 100))/100
        colorkey2 = decimal.Decimal(random.randrange(0, 100))/100
        colorkey3 = decimal.Decimal(random.randrange(0, 100))/100
        glColor3f(colorkey1, colorkey2, colorkey3)
        glBegin(GL_QUADS)
        glVertex2f(startPointOfBar, 25) # Coordinates for the bottom left point
        glVertex2f(startPointOfBar+(widthOfOneBar-5), 25) # Coordinates for the bottom left point
        glVertex2f(startPointOfBar+(widthOfOneBar-5), 25+heightOfBar) # Coordinates for the bottom left point
        glVertex2f(startPointOfBar, 25+heightOfBar) # Coordinates for the bottom left point
        glEnd()

    face = freetype.Face("arial.ttf")
    face.set_char_size( 48*64 )
    face.load_char('S')
    bitmap = face.glyph.bitmap
    print(bitmap.buffer)



def iterate():
    glViewport(0, 0, 1000, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 1000, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    findCutPoints()
    warpCutPoints()
    clipPerimeterTriangles()
    drawTriangles()
    glColor3f(1.0, 0, 3.0)
    drawIsosurface()
    glColor3f(3.0, 3.0, 1.0)
    plotCutPoints()
    findAngles()
    glColor3f(3.0, 3.0, 1.0)
    plotGraph()

    glutSwapBuffers()

glutInit()
setupTriangles()
filterTriangles()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(1000, 500)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow("OpenGL Coding Practice")
glutDisplayFunc(showScreen)
# glutIdleFunc()
glutMainLoop()