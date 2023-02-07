import sys, pygame

class play(object):
    def __init__(self):
        
        pygame.init()
        
        self._size = self._width, self._height = 700, 700
        self._black = 0, 0, 0
        
        self._screen = pygame.display.set_mode(self._size)

        #Player & Bullet Drawing
        self._playerview = pygame.image.load("ship.jpg")
        self._bulletview = pygame.image.load("bullet.png")
        
        #Enemy Drawing
        self._enemyview = pygame.image.load("enemy.png")
        self._enemyview0 = pygame.image.load("enemy.png")
        self._enemyview1 = pygame.image.load("enemy.png")
        self._enemyview2 = pygame.image.load("enemy.png")

        #Creating Player & Bullet Model
        self._playermodel = Player(20, 660, self._width, 0.5)
        self._bulletmodel = Bullet(20,640,2)
        #Creating all 4 Enemys
        self._enemymodel = Enemy(20, 20, self._width, 0.3,50)
        self._enemymodel0 = Enemy(120, 20, self._width, 0.3,5)
        self._enemymodel1 = Enemy(220, 20, self._width, 0.3,5)
        self._enemymodel2 = Enemy(320, 20, self._width, 0.3,5)

    #Main run function
    def rungame(self):
        globalxchange = 1
        ydif = 0
        cnt = 0
        c = 0
        #While to continously run the game
        while c == 0:
            #Exit game
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()
            #Move your Player
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self._playermodel.handleMoveLeft()
            if keys[pygame.K_RIGHT]:
                self._playermodel.handleMoveRight()


            #Enemy Moving
            globalxchange, ydif = self._enemymodel.move(globalxchange,ydif)
            self._enemymodel0.move(globalxchange,ydif)
            self._enemymodel1.move(globalxchange,ydif)
            self._enemymodel2.move(globalxchange,ydif)


            #Bullet Shooting
            self._bulletmodel.shoot(self._playermodel.getXPos())

            
            #Display Sprites
            self._screen.fill(self._black)
            self._screen.blit(self._playerview, (self._playermodel.getXPos()-33, self._playermodel.getYPos()))
            self._screen.blit(self._bulletview, (self._bulletmodel.getXPos(), self._bulletmodel.getYPos()))
            #All Enemys
            self._screen.blit(self._enemyview, (self._enemymodel.getXPos(), self._enemymodel.getYPos()+ydif))
            self._screen.blit(self._enemyview0, (self._enemymodel0.getXPos(), self._enemymodel0.getYPos()+ydif))
            self._screen.blit(self._enemyview1, (self._enemymodel1.getXPos(), self._enemymodel1.getYPos()+ydif))
            self._screen.blit(self._enemyview2, (self._enemymodel2.getXPos(), self._enemymodel2.getYPos()+ydif))


            #Detect a Collision
            cnt,self._enemyview = self._enemymodel.collision(self._bulletmodel.getXPos(),self._bulletmodel.getYPos(),cnt,globalxchange,self._enemyview)
            cnt,self._enemyview0 = self._enemymodel0.collision(self._bulletmodel.getXPos(),self._bulletmodel.getYPos(),cnt,globalxchange,self._enemyview0)
            cnt,self._enemyview1 = self._enemymodel1.collision(self._bulletmodel.getXPos(),self._bulletmodel.getYPos(),cnt,globalxchange,self._enemyview1)
            cnt,self._enemyview2 = self._enemymodel2.collision(self._bulletmodel.getXPos(),self._bulletmodel.getYPos(),cnt,globalxchange,self._enemyview2)

            #print(cnt)
            #When the enemys reach you
            self._enemymodel.lose(ydif)
            self._enemymodel0.lose(ydif)
            self._enemymodel1.lose(ydif)
            self._enemymodel2.lose(ydif)

            #Score Calculation
            self._screen.blit(self._playermodel.score(cnt), (5, 10))
            
            # Win scenario
            if cnt == 8:
                c = 1
                print("You Win!!")
                sys.exit()
            pygame.display.flip()

            

            

class Player(object):
    def __init__(self, xpos, ypos, maxxpos, change):
        self._x = xpos
        self._y = ypos
        self._maxXPos = maxxpos
        self._playerchange = change

    def getXPos(self):
        return self._x

    def getYPos(self):
        return self._y

    def handleMoveLeft(self):
        if self._x > 0:
            self._x -= self._playerchange

    def handleMoveRight(self):
        if self._x < self._maxXPos - 10:
            self._x += self._playerchange

    #Returns Score for display
    def score(self,cnt):
        myfont = pygame.font.SysFont("monospace", 25)
        scoretext = myfont.render("Score = "+str(cnt*1050), 1, (255,255,255))
        return scoretext



class Enemy(object):
    def __init__(self, xpos, ypos, maxxpos,xchange,ychange):
        self._x = xpos
        self._y = ypos
        self._maxXPos = maxxpos
        self._xchange = xchange
        self._ychange = ychange
        

    def getXPos(self):
        return self._x

    def getYPos(self):
        return self._y

    #This is the method used to control the movemnt of the enemies
    def move(self,globalxchange,ydif):
        if self._x <= 50:
            globalxchange = 1

        if globalxchange == 1:
            self._x += self._xchange
        elif globalxchange == -1:
            self._x -= self._xchange

        if self._x >= self._maxXPos - 400:
            return -1, ydif + self._ychange
        return globalxchange, ydif

    #This is my collsision detection of for the enemies and bullet. I did not use rectangles so my collision isnt as accurate as it would have been with rectangles
    def collision(self,bulletx,bullety,cnt, globalxchange,look):
        if bullety - 10 < self._y < bullety + 10:
            if bulletx - 25  < self._x < bulletx + 25:
                #If the enmey is in its last life
                if self._y % 5 != 0:
                    self._y = 2000
                    #print(bulletx + 20*globalxchange," - ", bulletx + 40 +  20*globalxchange, "Bullet:", bulletx, "Enemy: ",self._x, "Global: ", 20*globalxchange)
                #Change enemy to its second life
                self._y += 23
                cnt += 1
                look = pygame.image.load("enemy2.png")
        return cnt, look

    #Lose Method
    def lose(self,ydif):
        if 800 >= ydif >= 560:
            print("You Lose :(")
            sys.exit()
                

class Bullet(object):
    def __init__(self,xpos,ypos,change):
        self._x = xpos
        self._y = ypos
        self._bulletchange = change 
        self._shooting = False

    def getXPos(self):
        return self._x

    def getYPos(self):
        return self._y

    #This is the method used to shoot the bullet
    def shoot(self,x1pos):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self._shooting = True
            self._x = x1pos
            self._y = 640

        if self._y < 0:
            self._shooting = False
            self._x = 1000
            self._y = 1000

        if self._shooting == True:
            self._y -= self._bulletchange


#Main calling of rungame method
if __name__ == "__main__":
    mygame = play()
    mygame.rungame()