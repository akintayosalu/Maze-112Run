from cmu_112_graphics_openCV import *
import math
import random
import copy

# Name, andrew_id : Akintayo Salu, asalu
# TP3
testMap = [[1,1,1,1,1,1,1,1,1,1,1,1,1],
           [1,1,1,1,1,1,1,1,1,0,0,0,1],
           [1,1,1,1,0,0,0,0,0,0,0,0,1],
           [1,1,1,1,0,0,0,0,0,0,0,0,1],
           [1,1,1,1,0,0,0,0,0,0,0,0,1],
           [1,1,1,1,0,0,0,1,1,1,1,1,1],
           [1,1,1,1,0,0,0,1,1,1,1,1,1],
           [1,1,1,1,0,0,0,1,1,1,1,1,1],
           [1,1,1,1,0,0,0,1,1,1,1,1,1],
           [1,1,1,0,0,0,0,1,1,1,1,1,1],
           [1,1,1,0,0,0,0,1,1,1,1,1,1],
           [1,1,1,0,0,0,0,1,1,1,1,1,1],
           [1,1,1,1,1,1,1,1,1,1,1,1,1]]

rightMap = [[1,1,1,1,1,1,1,1,1,1,1,1,1],
           [1,1,1,1,1,1,1,1,1,0,0,0,1],
           [1,1,1,1,0,0,0,0,0,0,0,0,1],
           [1,1,1,1,0,0,0,0,0,0,0,0,1],
           [1,1,1,1,"L","M","R",0,0,0,0,0,1],
           [1,1,1,1,0,0,0,1,1,1,1,1,1],
           [1,1,1,1,0,0,0,1,1,1,1,1,1],
           [1,1,1,1,0,0,0,1,1,1,1,1,1],
           [1,1,1,1,0,0,0,1,1,1,1,1,1],
           [1,1,1,0,0,0,0,1,1,1,1,1,1],
           [1,1,1,0,0,0,0,1,1,1,1,1,1],
           [1,1,1,0,0,0,0,1,1,1,1,1,1],
           [1,1,1,1,1,1,1,1,1,1,1,1,1]]

leftMap = [[1,1,1,1,1,1,1,1,1,1,1,1,1],
           [1,0,0,0,1,1,1,1,1,1,1,1,1],
           [1,0,0,0,0,0,0,0,0,1,1,1,1],
           [1,0,0,0,0,0,0,0,0,1,1,1,1],
           [1,0,0,0,0,0,"L","M","R",1,1,1,1],
           [1,1,1,1,1,1,0,0,0,1,1,1,1],
           [1,1,1,1,1,1,0,0,0,1,1,1,1],
           [1,1,1,1,1,1,0,0,0,1,1,1,1],
           [1,1,1,1,1,1,0,0,0,1,1,1,1],
           [1,1,1,1,1,1,0,0,0,0,1,1,1],
           [1,1,1,1,1,1,0,0,0,0,1,1,1],
           [1,1,1,1,1,1,0,0,0,0,1,1,1],
           [1,1,1,1,1,1,1,1,1,1,1,1,1]]



class Map:
    #This is module function that initializes the constant variables of 
    #the class Map. Some of the values for the constant variables were 
    #inspired by a Raycasting tutorial:
    # https://www.youtube.com/watch?v=Rt5rEW0jQjw
    # https://www.youtube.com/watch?v=AjPPhx8-lXg&t=97s
    # https://www.youtube.com/watch?v=SnexnrINBB0&t=747s
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.mapSize = 13
        self.map = [[1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,0,0,0,1,1,1,1,1,1,1,1,1],
                    [1,0,0,0,0,0,0,0,0,1,1,1,1],
                    [1,0,0,0,0,0,0,0,0,1,1,1,1],
                    [1,0,0,0,0,0,"L","M","R",1,1,1,1],
                    [1,1,1,1,1,1,0,0,0,1,1,1,1],
                    [1,1,1,1,1,1,0,0,0,1,1,1,1],
                    [1,1,1,1,1,1,0,0,0,1,1,1,1],
                    [1,1,1,1,1,1,0,0,0,1,1,1,1],
                    [1,1,1,1,1,1,0,0,0,1,1,1,1],
                    [1,1,1,1,1,1,0,0,0,1,1,1,1],
                    [1,1,1,1,1,1,0,0,0,1,1,1,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1]]
    
        self.map = self.addObstacles(self.map)

        self.gridSizeX = int((self.width/2)/self.mapSize)
        self.gridSizeY = int((self.height)/self.mapSize)
        self.maxDepth = int(self.mapSize * max(self.gridSizeX,self.gridSizeY))

        self.fov = math.pi/3
        self.halfFov = self.fov/2
        self.castedRayNum = self.width//2
        self.stepAngle = self.fov/self.castedRayNum
        self.scale = (self.height)/self.castedRayNum

        self.lineLength = 50

    #Information from a tutorial was used in HELPING make the following functions:
    #
    # drawMap(self,canvas,playObj)
    # castRays(self,canvas,playObj)
    # drawWall(self,canvas,row,col,rayX,rayY,ray,startAngle,depth,playObj)
    # drawObstacle(self,canvas,row,col,rayX,rayY,ray,startAngle,depth,playObj)
    # blankGrid(self,canvas)
    # blank3D(self,canvas)
    #
    #Citation: https://www.youtube.com/watch?v=Rt5rEW0jQjw
    # https://www.youtube.com/watch?v=AjPPhx8-lXg&t=97s
    # https://www.youtube.com/watch?v=SnexnrINBB0&t=747s
    # Note: All functions are carried out using 112 GRAPHICS, and not PYGAME.

    #This view function displays the 2D grid that the raycasting will be 
    #visualized with using canvas.create functions, nested for loops and 
    #conditionals.  
    def drawMap(self,canvas,playObj):
        for row in range(len(self.map)):
            for col in range(len(self.map[0])):
                if self.map[row][col] == 1:
                    color = rgbString(200,200,200)
                else:
                    color = rgbString(100,100,100)

                x0 = col*self.gridSizeX
                y0 = row*self.gridSizeY
                x1 = x0 + self.gridSizeX - 1
                y1 = y0 + self.gridSizeY - 1
            
                canvas.create_rectangle(x0,y0,x1,y1,
                                fill=color, outline='black', width=1)
        
        r = 10
        x0 = int(playObj.playerX) - r
        y0 = int(playObj.playerY) - r
        x1 = x0 + 2*r
        y1 = y0 + 2*r
        canvas.create_oval(x0,y0,x1,y1,fill= "red")
  
        x0 = playObj.playerX
        y0 = playObj.playerY
        x1 = playObj.playerX - math.sin(playObj.playerAngle) * self.lineLength
        y1 = playObj.playerY + math.cos(playObj.playerAngle) *self.lineLength
        canvas.create_line(x0,y0,x1,y1,
                            fill="green", width=3)

        leftmostAngle = playObj.playerAngle - self.halfFov
        x0 = playObj.playerX
        y0 = playObj.playerY
        x1 = playObj.playerX - math.sin(leftmostAngle) * self.lineLength
        y1 = playObj.playerY + math.cos(leftmostAngle) * self.lineLength
        canvas.create_line(x0,y0,x1,y1,
                            fill="green", width=3)

        rightmostAngle = playObj.playerAngle + self.halfFov
        x0 = playObj.playerX
        y0 = playObj.playerY
        x1 = playObj.playerX - math.sin(rightmostAngle) * self.lineLength
        y1 = playObj.playerY + math.cos(rightmostAngle) * self.lineLength
        canvas.create_line(playObj.playerX,playObj.playerY,x1,y1,
                            fill="green", width=3)
    
    #This view functions draws the rays on the 2D grid to visualize the 
    #raycasting process for walls using canvas.create functions and IF 
    #conditionals. 
    def castRays(self,canvas,playObj):
        startAngle = playObj.playerAngle - self.halfFov

        for ray in range(self.castedRayNum):
            for depth in range(self.maxDepth):

                rayX = playObj.playerX - math.sin(startAngle) * depth
                rayY = playObj.playerY + math.cos(startAngle) * depth

                row = int(rayY//self.gridSizeX)
                col = int(rayX//self.gridSizeY) 

                if self.map[row][col] == 1:
                    self.drawWall(canvas,row,col,rayX,rayY,ray,startAngle,depth,playObj)
                    break
                elif self.map[row][col] == 2:
                    self.drawObstacle(canvas,row,col,rayX,rayY,ray,startAngle,depth,playObj)
                    break

            startAngle += self.stepAngle
    
    #This view functions draws the rays on the 2D grid to visualize the 
    #raycasting for the "walls" using canvas.create functions 
    #and IF conditionals
    def drawWall(self,canvas,row,col,rayX,rayY,ray,startAngle,depth,playObj):
        x0 = col*self.gridSizeX
        y0 = row*self.gridSizeY
        x1 = x0 + self.gridSizeX - 1
        y1 = y0 + self.gridSizeY - 1
        color = "green"

        #canvas.create_rectangle(x0,y0,x1,y1, fill=color, outline='black', width=1)

        x0 = playObj.playerX
        y0 = playObj.playerY
        x1 = rayX
        y1 = rayY
        #canvas.create_line(x0,y0,x1,y1,fill=rgbString(255,255,0))
                
        color = 255/(1 + depth*depth*0.0001) # + 1 to avoid zeroDivisionError

        depth *= math.cos(playObj.playerAngle - startAngle)

        wallHeight = 20000/(depth + 1)

        if wallHeight > self.height: 
            wallHeight = self.height
            
        wallColor = rgbString(color,color,color)
        x0 = self.height + (ray * self.scale)
        y0 = (self.height/2) - wallHeight/2 
        x1 = x0 + self.scale
        y1 = y0 + wallHeight

        canvas.create_rectangle(x0,y0,x1,y1, fill=wallColor,outline=wallColor)
    
    #This view functions draws the rays on the 2D grid to visualize the 
    #raycasting for the "obstacles" using canvas.create functions 
    #and IF conditionals
    def drawObstacle(self,canvas,row,col,rayX,rayY,ray,startAngle,depth,playObj):
        x0 = col*self.gridSizeX
        y0 = row*self.gridSizeY
        x1 = x0 + self.gridSizeX - 1
        y1 = y0 + self.gridSizeY - 1
        color = "red"

        #canvas.create_rectangle(x0,y0,x1,y1, fill=color, outline='black', width=1)

        x0 = playObj.playerX
        y0 = playObj.playerY
        x1 = rayX
        y1 = rayY
        #canvas.create_line(x0,y0,x1,y1,fill=rgbString(255,0,0))
            
        color = 255/(1 + depth*depth*0.0001) # + 1 to avoid zeroDivisionError

        depth *= math.cos(playObj.playerAngle - startAngle)

        obstacleHeight = 20000/(depth + 1)

        if obstacleHeight > self.height: 
            obstacleHeight = self.height
        
        obsColor = rgbString(color,0,0)
        x0 = self.height + (ray * self.scale)
        y0 = (self.height/2) - obstacleHeight/2 
        x1 = x0 + self.scale
        y1 = y0 + obstacleHeight

        canvas.create_rectangle(x0,y0,x1,y1,fill=obsColor,outline=obsColor)
    
    #This is helper function that checks whether a row in the map can have obstacles
    #using conditionals.
    def isLegalRow(self,rows):
        if (rows >= 9):
            return False
        elif (rows == 5 or rows == 8):
            return True
        else:
            return False

    #This is a helper function that adds obstacles to certain rows by using nested
    #for loops, connditionals, recursive functions and random.randint. 
    def addObstacleToRow(self,L,changedRows):
        copyL = copy.deepcopy(L)
        mainObsList = []
        for rows in changedRows:
            obsList = []
            for cols in range(len(copyL)):
                if (copyL[rows][cols] == 0):
                    obstacleNum = random.randint(0,1)
                    obsList.append(obstacleNum)
                    if (obstacleNum == 1):
                        copyL[rows][cols] = 2
            mainObsList.append(obsList)

        for lists in mainObsList:
            if (lists.count(1) == 3 or lists.count(0) == 3):
                return self.addObstacleToRow(L,changedRows)

        L = copyL
        return L

    #This fucntion adds obstacles to the map by changing the values within the 
    #2D list.
    def addObstacles(self,L):
        changedRows = []
        for rows in range(len(L)):
            if (self.isLegalRow(rows)):
                changedRows.append(rows)
        
        newL = self.addObstacleToRow(L,changedRows)
        return newL
    
    #This helper function determines when a player has reached a certain checkpoint
    #in order to move them to a new map using if conditionals and random.randint.
    def newBoard(self,row,col,playObj):
        if (self.map[row][col] == "L" or 
            self.map[row][col] == "M" or 
            self.map[row][col] == "R"):
            mapNum = random.randint(0,1)

            if (mapNum == 1):
                print("RightMap")
                playObj.playerX = (self.width)/4 - self.gridSizeX*3
                playObj.playerAngle += math.pi/2
                self.map = rightMap
                self.map = self.addObstacles(self.map)
            else: #mapNum ==  0
                print("LefttMap")
                playObj.playerX = (self.width)/4 + self.gridSizeX*3
                playObj.playerAngle -= math.pi/2
                self.map = leftMap
                self.map = self.addObstacles(self.map)
                
            if (self.map[row][col] == "L"):
                playObj.playerY = ((self.mapSize-4)/self.mapSize)*((self.height))
            elif (self.map[row][col] == "R"):
                offset = self.gridSizeY//2
                playObj.playerY = ((self.mapSize-2)/self.mapSize)*((self.height)) + offset
            else: # app.map[row][col] == "M"
                playObj.playerY = ((self.mapSize-3)/self.mapSize)*((self.height))

    #This is a view function that makes the 2D grid blank using canvas.create 
    #functions.
    def blankGrid(self,canvas):
        color = rgbString(0,0,0)
        x0 = 0
        y0 = 0
        x1 = self.height
        y1 = self.height
        canvas.create_rectangle(x0,y0,x1,y1, fill=color)

    #This is a view function that makes the "3D" world blank using canvas.create 
    #functions.
    def blank3D(self,canvas):
        x0 = self.width/2
        y0 = self.height/2
        x1 = self.width
        y1 = self.height
        x2 = self.width/2
        y2 = 0
        x3 = self.width
        y3 = self.height/2
        color1 = rgbString(100,100,100)
        color2 = rgbString(200,200,200)
        canvas.create_rectangle(x0,y0,x1,y1, fill=color1)
        canvas.create_rectangle(x2,y2,x3,y3, fill=color2)


class Player:
    #This is module function that initializes the constant variables of 
    #the class Map.
    def __init__(self,mapObj):
        self.forward = True
        self.playerX = (mapObj.width)/4 + mapObj.gridSizeX
        self.playerY = ((mapObj.mapSize-2)/(mapObj.mapSize))*((mapObj.height))
        self.playerAngle = math.pi

        self.speed = 0
        self.score = 0

#This is module function that initializes the constant variables of 
#the program. Some of the values for the constant variables were 
#inspired by a faceTracking tutorial:
# https://towardsdatascience.com/face-detection-in-2-minutes-using-opencv-python-90f89d7c0f81
# Logo from: https://www.pixilart.com/draw?gclid=Cj0KCQjw06OTBhC_ARIsAAU1yOWLbu6cD-xtSW
# 0JPC83zrjqm_jYLbplQfWNF1KUhsLiBeco7bNcOs4aAk_mEALw_wcB
# Background Image: https://www.google.com/search?q=cool+maze+designs+black+and+white
# +non+stock&tbm=isch&ved=2ahUKEwiKp4ur87T3AhUWGc0KHeH1A24Q2-cCegQIABAA&oq=cool+maze+desi
# gns+black+and+white+non+stock&gs_lcp=CgNpbWcQA1D0BFiaJmDALGgAcAB4AIABiwGIAaYJkgEDMy44mAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=
# img&ei=NI9pYoq9HpaytAbh64_wBg&bih=764&biw=1440&rlz=1C5CHFA_enNG934NG935#imgrc=hCiy-nWajGfOLM
def appStarted(app):
    app.mainMap = Map(app.width,app.height)
    app.mainPlayer = Player(app.mainMap)

    app.notStarted = True
    app.showMap = False
    app.gameOver = False

    app.backgroundImg = app.loadImage("mazepics.jpeg")
    app.imgWidth,app.imgHeight = app.backgroundImg.size 
    app.imageScale = min(app.imgWidth,app.imgHeight)
    app.backgroundImg = app.scaleImage(app.backgroundImg,app.height/app.imageScale)
    
    app.gameName = app.loadImage("pixil-frame-0.png")
    app.gameNameHome = app.scaleImage(app.gameName,2)
    app.gameName = app.scaleImage(app.gameName,1/2)

    app.timePassed = 0

    app.frame = None
    app.faceTupleList = []
    app.cascPath=os.path.dirname(cv2.__file__)+"/data/haarcascade_frontalface_default.xml"
    app.faceCascade = cv2.CascadeClassifier(app.cascPath)

    app.xMid = None
    app.direction = ""

#This view function draws the images captured by the camera using canvas and
# and tkinter functions. 
def drawCamera(app, canvas):
    if (not app.gameOver):
        if app.frame is None: return
        tkImage = app.opencvToTk()
        canvas.create_image(app.width / 2, app.height / 2, image=tkImage)

#This is a view function that draws a rectangle around the face captured
#by the camera using canvas functions. 
def drawFaces(app,canvas):
    for faces in app.faceTupleList:
        x0,y0,x1,y1 = faces
        canvas.create_rectangle(x0,y0,x1,y1,outline="black",width=5)

#This is a controller function that uses event functions to uses key presses
#to change aspects of variables in the program. 
def keyPressed(app,event):
    #if event.key == 'c':
        #app.cameraOpen = True
    if (not app.gameOver): 
        if (event.key == "Left"): 
            app.mainPlayer.playerAngle -= 0.1
        if (event.key == "Right"): 
            app.mainPlayer.playerAngle += 0.1
        if (event.key == "Up"):
            app.mainPlayer.forward = True
            app.mainPlayer.playerX += -math.sin(app.mainPlayer.playerAngle) * 5 *2
            app.mainPlayer.playerY += math.cos(app.mainPlayer.playerAngle) * 5*2
        if (event.key == "Down"):
            app.mainPlayer.forward = False
            app.mainPlayer.playerX -= -math.sin(app.mainPlayer.playerAngle) * 5*2
            app.mainPlayer.playerY -= math.cos(app.mainPlayer.playerAngle) * 5*2
        
        if (event.key == "m"):
            app.showMap = True
        if (event.key == "n"):
            app.showMap = False

    if (event.key == "s"):
        app.notStarted = False

    if event.key == "q":
        App._theRoot.app.quit()
    if event.key == "r":
        appStarted(app)

#Citation: 
# https://stackoverflow.com/questions/5661725/format-ints-into-string-of-hex
#This is a helper function that turns values into a hexadecimal value 
#formatted as a string.
def rgbString(r, g, b):
    return "#" + ''.join(f'{i:02x}' for i in [int(r), int(g), int(b)])

#This controller function changes the playerAngle using conditionals.
def changeAngle(app):
    for faces in app.faceTupleList:
        x0,_,x1,_ = faces
        app.xMid = (x0+x1)/2
        print(app.xMid)
        if (app.xMid  <= 400):
            app.direction = "Turning left"
            app.mainPlayer.playerAngle -= 0.05
        elif (app.xMid >= 800):
            app.direction = "Turning right"
            app.mainPlayer.playerAngle += 0.05
        else:
            app.direction = "Moving forward"

#This is a helper function that makes sure we do not go outside the grid
#or through the obstacles using list indexing and IF conditionals.
def collisionCheck(app,row,col):
    if (app.mainMap.map[row][col] == 1 or app.mainMap.map[row][col] == 2):
        app.gameOver = True

#This function uses functions from cv2 module to track an individuals face.
#Forst half of code is from:
#https://towardsdatascience.com/face-detection-in-2-minutes-using-opencv-python-90f89d7c0f81
def faceTrack(app):
    frameRGB = cv2.cvtColor(app.frame, cv2.COLOR_BGR2GRAY)
    faces = app.faceCascade.detectMultiScale(
            frameRGB,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
            )
    for (x0,y0,width,height) in faces:
        x1 = x0 + width
        y1 = y0 + height
        if (width>= 150):
            app.faceTupleList = [(x0,y0,x1,y1)]

#This is a controller function that fires the laptop's camera to capture image 
#frames. 
def cameraFired(app):
    _, app.frame = app.camera.read()
    app.frame = cv2.flip(app.frame, 1)
    faceTrack(app)

#This is a controller function that uses app.timerDelay.
def timerFired(app):
    if (not app.notStarted):
        if (not app.gameOver):
            changeAngle(app)

            app.timePassed += app.timerDelay
            app.speed = 1 + app.timePassed/100
            app.mainPlayer.score = app.timePassed

            if (app.timePassed%(50) == 0):
                app.mainPlayer.playerX += -math.sin(app.mainPlayer.playerAngle) * 5 * app.speed
                app.mainPlayer.playerY += math.cos(app.mainPlayer.playerAngle) * 5 * app.speed

            row = int(app.mainPlayer.playerY//app.mainMap.gridSizeY)
            col = int(app.mainPlayer.playerX//app.mainMap.gridSizeX) 

            collisionCheck(app,row,col)
            app.mainMap.newBoard(row,col,app.mainPlayer)


#This view function displays the game score using canvas functions.
def displayScoreboard(app,canvas):
    x0 = 1000
    y0 = 0
    x1 = 1200
    y1 = 50
    canvas.create_rectangle(x0,y0,x1,y1,fill="black")

    xText = x0+10
    yText = (y0+y1)/2
    textSize = 15

    canvas.create_text(xText, yText, 
                        text= f'Current Score: {app.mainPlayer.score}',
                        font=f'Arial {textSize}', fill='white',anchor='w')

#This view function displays the direction of movement using canvas functions.
def showDirection(app,canvas):
    x0 = 1000
    y0 = 50
    x1 = 1200
    y1 = 100
    canvas.create_rectangle(x0,y0,x1,y1,fill="black")

    xText = x0+10
    yText = (y0+y1)/2
    textSize = 15

    canvas.create_text(xText, yText, 
                        text= f'Direction: {app.direction}',
                        font=f'Arial {textSize}', fill='white',anchor='w')

#This view function displays the gameOver page using canvas functions.
def drawGameOverBoard(app,canvas):
    x0 = 0
    y0 = 0
    x1 = app.width
    y1 = app.height
    canvas.create_rectangle(x0,y0,x1,y1,fill="black")

    xText = (x0+x1)/2
    yText = (y0+y1)/2
    textSize = 50   

    canvas.create_text(xText, yText, 
                        text= f'The Game is Over! Your Score was: {app.mainPlayer.score}.',
                        font=f'Arial {textSize}', fill='white')
    
    canvas.create_text(app.width/2, 3*app.height/4, 
                    text= f'Press the "r" key to restart the game',
                    font=f'Arial {30}', fill='white',anchor="n")

#This is a view function that draws the innstruction page during the 
#game using canvas.create functions.
def drawInstructions(app,canvas):
    canvas.create_image(app.width/4,app.height/2,
                        image=ImageTk.PhotoImage(app.backgroundImg))

    canvas.create_rectangle((1/4)*app.width/2,0,
                            (3/4)*app.width/2,app.height,fill="black")
    
    
    canvas.create_image(app.width/4,app.height/2,
                        image=ImageTk.PhotoImage(app.gameName),anchor="s")
    
    canvas.create_text(app.width/4,3*app.height/4,
                text="""
                INSTRUCTIONS:
                1. Move your head to the left side
                of the screen to turn left. 
                2. Move your head to the right side 
                of the screen to turn right.
                3. Keep your head in the center to 
                move forward.
                4. If you hit any walls or obstacles, 
                it is GAME OVER. 

                5. Press the "q" key to quit the 
                canvas.
                6. Press the key "m" to show the 
                map.
                7. Press the key "n" to go back to 
                instructions. 
                """
                ,anchor="s",font=f'Arial {12}', fill='white')

#This is a view function that draws the home screen at the beginning of the 
#game using canvas.create functions.
def homeScreen(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill="black")
    canvas.create_image(app.width/2,app.height/2,
                        image=ImageTk.PhotoImage(app.gameNameHome))

    canvas.create_text(app.width/2, 3*app.height/4, 
                    text= f'Press the "s" key to start the game',
                    font=f'Arial {30}', fill='white',anchor="n")

#This is a view function that creates the canvas for the program. 
def redrawAll(app, canvas):
    if (app.notStarted):
        homeScreen(app,canvas)
    else:
        if (not app.gameOver):
            row = int(app.mainPlayer.playerY//app.mainMap.gridSizeY)
            col = int(app.mainPlayer.playerX//app.mainMap.gridSizeX) 

            if (not app.showMap):
                drawInstructions(app,canvas)
                #app.mainMap.blankGrid(canvas)
                app.mainMap.blank3D(canvas)
                #app.mainMap.drawMap(canvas,app.mainPlayer)
                app.mainMap.castRays(canvas,app.mainPlayer)
            else:
                #drawInstructions(app,canvas)
                app.mainMap.blankGrid(canvas)
                app.mainMap.blank3D(canvas)
                app.mainMap.drawMap(canvas,app.mainPlayer)
                app.mainMap.castRays(canvas,app.mainPlayer)
        
            displayScoreboard(app,canvas)
            showDirection(app,canvas)
            
        else:
            drawGameOverBoard(app,canvas)

        # app.drawCamera(canvas)
        # drawFaces(app,canvas)

runApp(width=1200,height=600)
