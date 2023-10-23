import asyncio

#load pygame
import pygame as game
import random as r
game.mixer.pre_init(44100, -16, 2, 2048)
game.mixer.init()
game.init()
game.display.set_caption("Blobbed")

# Wrap whole program
async def main():
    screen = game.display.set_mode([832,640])

    #colors
    dblue=game.color.Color('#003387')
    blue=game.color.Color('#3d86ff')
    colora=blue
    colorb=dblue
    colorc=dblue

    #sprites
    pimg=game.image.load('Sprites/player.png')
    eimg0=game.image.load('Sprites/enemy0.png')
    eimg1=game.image.load('Sprites/enemy1.png')
    eimg2=game.image.load('Sprites/enemy2.png')
    eimg3=game.image.load('Sprites/enemy3.png')
    eimg4=game.image.load('Sprites/enemy4.png')
    eimg=eimg0
    lockimg=game.image.load('Sprites/lock.png')
    wall=game.image.load('Sprites/wall.png')
    wallimg=game.transform.scale(wall,(32,32))
    keyimg=game.image.load('Sprites/key.png')
    portalimg0=game.image.load('Sprites/portal0.png')
    portalimg1=game.image.load('Sprites/portal1.png')
    portalimg=portalimg0
    bossimg0=game.image.load('Sprites/boss0.png')
    bossimg1=game.image.load('Sprites/boss1.png')
    bossimg2=game.image.load('Sprites/boss2.png')
    bossimg3=game.image.load('Sprites/boss3.png')
    bossimg=bossimg0
    bg=game.image.load('Sprites/floor.png')
    title=game.image.load('Sprites/title.png')

    #sounds and music
    sdeath=game.mixer.Sound('Sounds/death.ogg')
    sportal=game.mixer.Sound('Sounds/portal.ogg')
    skey=game.mixer.Sound('Sounds/key.ogg')
    select=game.mixer.Sound('Sounds/select.ogg')
    sgameover=game.mixer.Sound('Sounds/gameover.ogg')
    gamemusic='Sounds/music.ogg'
    bossmusic='Sounds/boss.ogg'
    titlemusic='Sounds/titlemusic.ogg'

    #fonts and text
    fnt=game.font.Font(None,30)
    gofnt=game.font.Font(None,150)
    selectfnt=game.font.Font(None,50)
    gotxt=gofnt.render('GAME OVER!',0,(200,0,0))
    wintxt=gofnt.render('YOU WIN!',0,(0,230,0))

    #variables
    #player varibales
    xx=64
    yy=64
    spd=4
    lives=3

    #enemy variables
    enemyimgcount=0
    enemyleft=False
    enemyright=True

    #portal variables
    portalimgcount=0
    pleft=True
    pright=False
    px=128
    py=128

    #boss variables
    bossimgcount=0
    bosshp=20
    bspd=4

    #game variables
    level=1
    unlocked=False
    collision=False
    enemycollision=False
    prevkey=""
    enemies=[]
    walls=[]
    boss=[]
    espawn=False
    wspawn=False
    bspawn=False
    reset=False
    death=False

    #loops
    titlescreen=True
    gameon=False
    gameover=False
    win=False

    #selection vars
    kup=True
    kdown=False

    #FUNCTIONS
    #ENEMY ANIMATTION
    def enemyAnimation():
        nonlocal enemyimgcount,eimg,eimg0,eimg1,eimg2,eimg3,eimg4
        #check for image change
        enemyimgcount+=1
        if enemyimgcount==4:
            eimg=eimg1
        elif enemyimgcount==8:
            eimg=eimg2
        elif enemyimgcount==12:
            eimg=eimg3
        elif enemyimgcount==16:
            eimg=eimg4
        elif enemyimgcount==20:
            eimg=eimg0
            enemyimgcount=0

    #ENEMY MOVEMENT HORIZONTAL
    def enemyMove():
        nonlocal enemyright,enemyleft
        #check for direction
        if enemyleft==True:
            if e[0]>32:
                e[0]-=spd
            else:
                enemyright=True
                enemyleft=False
        elif enemyright==True:
            if e[0]<736:
                e[0]+=spd
            else:
                enemyleft=True
                enemyright=False

    #enemy collision check
    def enemyCollision(playerx,playery):
        nonlocal lives,xx,yy,enemycollision
        if enemycollision==True:
            lives-=1
            sdeath.play()
            xx=playerx
            yy=playery
            enemycollision=False

    #BOSS MOVEMENT HORIZONTAL
    def bossMove():
        nonlocal enemyright,enemyleft
        #check for direction
        if enemyleft==True:
            if b[0]>32:
                b[0]-=bspd
            else:
                enemyright=True
                enemyleft=False
        elif enemyright==True:
            if b[0]<700:
                b[0]+=bspd
            else:
                enemyleft=True
                enemyright=False

    #BOSS MOVEMENT HORIZONTAL
    def portalMove():
        nonlocal pright,pleft,px,py
        #check for direction
        if pleft==True:
            if px>32:
                px-=bspd
            else:
                pright=True
                pleft=False
        elif pright==True:
            if px<700:
                px+=bspd
            else:
                pleft=True
                pright=False

    #PORTAL ANIMATION
    def portalAnimation():
        nonlocal portalimgcount,portalimg0,portalimg1,portalimg
        #check for image change
        portalimgcount+=1
        if portalimgcount==3:
            portalimg=portalimg1
        elif portalimgcount==6:
            portalimg=portalimg0
            portalimgcount=0

    #BOSS ANIMATION
    def bossAnimation():
        nonlocal bossimgcount,bossimg0,bossimg1,bossimg
        #check for image change
        bossimgcount+=1
        if bossimgcount==3:
            bossimg=bossimg1
        if bossimgcount==6:
            bossimg=bossimg2
        if bossimgcount==9:
            bossimg=bossimg3
        elif bossimgcount==12:
            bossimg=bossimg0
            bossimgcount=0

    #DRAW BACKGROUND
    def drawFloor():
        #draw x and y
        for xloc in range(0,13):
            for yloc in range(0,10):
                screen.blit(bg,(64*xloc,64*yloc))

    #BORDER WALLS
    def drawEdgeWalls():
        #draw x and y
        for wx in range(0,26):
            screen.blit(wallimg,(32*wx,0))
            screen.blit(wallimg,(32*wx,608))
        for wy in range(1,19):
            screen.blit(wallimg,(0,32*wy))
            screen.blit(wallimg,(800,32*wy))

    #DRAW PORTAL AND COLLISION
    def portal(px,py,playerx,playery):
        nonlocal level,xx,yy,reset,bosshp
        #draw
        screen.blit(portalimg,(px,py))
        #collision
        portalbox=game.Rect(px,py,64,64)
        if portalbox.colliderect(pbox):
            if level==5:
                sgameover.play()
                xx=416
                yy=532
                bosshp-=1
            else:
                sportal.play()
                xx=playerx
                yy=playery
                level+=1
                reset=True

    #KEY AND LOCK DRAW AND COLLISION
    def keyLock(lx,ly,kx,ky):
        nonlocal unlocked,collision,pbox
        #DRAW
        if unlocked==False:
            screen.blit(lockimg,(lx,ly))
            screen.blit(keyimg,(kx,ky))
            lockbox=game.Rect(lx,ly,64,64)
            keybox=game.Rect(kx,ky,64,14)
        else:
            lockbox=game.Rect(0,0,0,0)
            keybox=game.Rect(0,0,0,0)
        #COLLISION
        if keybox.colliderect(pbox):
            if unlocked==False:
                skey.play()
                unlocked=True
        if lockbox.colliderect(pbox):
            collision=True
        else:
            collision=False

    #DRAW GAME TEXT
    def drawText():
        #RENDER AND DRAW
        livestxt=fnt.render('Lives: '+str(lives),0,(255,255,0))
        leveltxt=fnt.render('Level '+str(level),0,(255,255,0))
        screen.blit(leveltxt,(32,8))
        screen.blit(livestxt,(720,616))

    #gameover check
    def deathCheck():
        nonlocal lives,level,reset,lives,death
        if lives<=0:
            level=1
            lives=3
            game.time.wait(500)
            sgameover.play()
            reset=True
            death=True
            game.mixer.music.stop()
            
    #DRAW X WALL
    def drawXWall(amount,startx,ypos):
        for wx in range(0,amount):
            walls.append([(wx*32)+32*startx,32*ypos])

    #DRAW Y WALL
    def drawYWall(amount,xpos,starty):
        for wy in range(0,amount):
            walls.append([32*xpos,(wy*32)+32*starty])

    #RESET VARIABLES
    def resetVars(key):
        nonlocal enemyimgcount,enemyleft,enemyright,unlocked,collision,enemycollision,prevkey,enemies,walls,espawn,wspawn,bspawn,boss,bspd,bosshp,pleft,pright,px,py
        enemyimgcount=0
        enemyleft=False
        enemyright=True
        unlocked=key
        collision=False
        enemycollision=False
        prevkey=""
        enemies=[]
        walls=[]
        boss=[]
        espawn=False
        wspawn=False
        bspawn=False
        bspd=4
        bosshp=20
        pleft=True
        pright=False
        px=128
        py=128

    while True:
        #TITLE SCREEN LOOP
        kup=True
        game.mixer.music.stop()
        game.mixer.music.load(titlemusic)
        game.mixer.music.play(-1)
        while titlescreen:
            #DRAW BACKGROUND
            drawFloor()
            drawEdgeWalls()

            #TITLE DRAW
            screen.blit(title,(165,0))
            
            #DRAW SELECTION TEXT
            playtxt=selectfnt.render('Play',0,(colora))
            exittxt=selectfnt.render('Exit',0,(colorb))
            creditz=fnt.render('By Maxim Brochin',0,(0,0,0))
            screen.blit(creditz,(615,580))
            screen.blit(playtxt,(375,300))
            screen.blit(exittxt,(375,500))

            #EVENTS AND KEYS
            event=game.event.poll()
            if event.type==game.QUIT:
                game.quit()
            key=game.key.get_pressed()

            #SELECTION
            if key[game.K_UP]:
                colora=blue
                colorb=dblue
                kup=True
                kdown=False
            elif key[game.K_DOWN]:
                colora=dblue
                colorb=blue
                kup=False
                kdown=True
            #SELECTION
            if kup==True:
                if key[game.K_RETURN]:
                    select.play()
                    titlescreen=False
                    break
            elif kdown==True:
                if key[game.K_RETURN]:
                    game.quit()
            #REFRESH
            game.display.flip()
            await asyncio.sleep(0)  # Let other tasks run
        #MAIN LOOP OF THE GAME
        gameon=True
        game.mixer.music.stop()
        game.mixer.music.load(gamemusic)
        game.mixer.music.play(-1)
        while gameon:
            #DRAW
            #DRAW FLOOR TILES
            drawFloor()
            
            #DRAW WALLS
            drawEdgeWalls()
            
            #DRAW SPRITES
            screen.blit(pimg,(xx,yy))

            #DRAW TEXT
            drawText()

            #HITBOXES
            pbox=game.Rect(xx,yy,64,64)
            
            #EVENTS
            event=game.event.poll()
            if event.type==game.QUIT:
                game.quit()
            key=game.key.get_pressed()

            #ENEMY MOVEMENT AND DRAW
            for e in enemies:
                enemyMove()
            for e in enemies:
                screen.blit(eimg,(e[0],e[1]))
                enemybox=game.Rect(eimg.get_rect())
                enemybox.x=e[0]
                enemybox.y=e[1]
                if enemybox.colliderect(pbox):
                    enemycollision=True
                    
            #BOSS MOVEMENT AND DRAW
            for b in boss:
                bossMove()
            for b in boss:
                screen.blit(bossimg,(b[0],b[1]))
                bossbox=game.Rect(bossimg.get_rect())
                bossbox.x=b[0]
                bossbox.y=b[1]
                if bossbox.colliderect(pbox):
                    enemycollision=True

            #LEVELS 1-5
            #LEVEL 1
            if level==1:
                if reset==True:
                    resetVars(True)
                    xx=64
                    yy=64
                    reset=False

                #COLLISION WITH ENEMY
                enemyCollision(64,64)
                
                #PORTAL FUNCTION
                portal(200,350,700,64)
                
                #SPAWNS FOR WALL AND ENEMY
                if wspawn==False:
                    wspawn=True
                    drawXWall(21,1,4)
                    drawYWall(11,21,5)
                    drawXWall(17,4,15)
                    drawYWall(7,4,8)
                    drawXWall(11,5,8)
                if espawn==False:
                    espawn=True       
                    enemies.append([100,375])
                    enemies.append([100,175])
            #LEVEL 2
            elif level==2:
                if reset==True:
                    resetVars(True)
                    reset=False
                    
                #COLLISION WITH ENEMY
                enemyCollision(700,64)
                
                #PORTAL FUNCTION
                portal(64,532,400,64)
                
                #SPAWNS FOR WALL AND ENEMY
                if wspawn==False:
                    wspawn=True
                    drawXWall(21,4,4)
                    drawXWall(21,1,15)
                if espawn==False:
                    espawn=True       
                    enemies.append([100,175])
                    enemies.append([250,175])
                    enemies.append([400,175])
                    enemies.append([400,250])
                    enemies.append([100,325])
                    enemies.append([400,400])
                    enemies.append([250,400])
                    enemies.append([100,400])
            #LEVEL 3
            elif level==3:
                if reset==True:
                    resetVars(False)
                    reset=False
                    
                #COLLISION WITH ENEMY
                enemyCollision(400,64)
                
                #PORTAL FUNCTION
                portal(384,532,64,500)

                #KEY AND LOCK
                keyLock(384,448,700,100)
                
                #SPAWNS FOR WALL AND ENEMY
                if wspawn==False:
                    wspawn=True
                    drawYWall(6,10,5)
                    drawXWall(5,10,4)
                    drawYWall(10,15,1)
                    drawYWall(5,10,14)
                    drawYWall(5,15,14)
                if espawn==False:
                    espawn=True
                    enemies.append([601,40])
                    enemies.append([600,200])
                    enemies.append([600,390])
                    enemies.append([600,515])
                    enemies.append([99,175])
                    enemies.append([100,375])
                    enemies.append([100,500])
            #LEVEL 4
            elif level==4:
                if reset==True:
                    resetVars(False)
                    reset=False
                    
                #COLLISION WITH ENEMY
                enemyCollision(64,532)
                
                #PORTAL FUNCTION
                portal(384,532,400,532)

                #KEY AND LOCK
                keyLock(175,532,716,564)
                
                #SPAWNS FOR WALL AND ENEMY
                if wspawn==False:
                    wspawn=True
                    drawYWall(12,5,4)
                    drawXWall(14,6,7)
                    drawYWall(15,20,4)
                    
                if espawn==False:
                    espawn=True
                    enemies.append([100,425])
                    enemies.append([100,46])
                    enemies.append([100,270])
                    enemies.append([400,425])
                    enemies.append([400,46])
                    enemies.append([400,270])
            #LEVEL 5
            elif level==5:
                if reset==True:
                    resetVars(True)
                    reset=False

                #PORTAL
                portal(px,py,416,532)
                portalMove()
                
                #COLLISION WITH BOSS
                enemyCollision(416,532)

                #SPAWN FOR BOSS
                if bspawn==False:
                    game.mixer.music.stop()
                    game.mixer.music.load(bossmusic)
                    game.mixer.music.play(-1)
                    bspawn=True
                    boss.append([120,120])

                #HP TEXT
                hptxt=selectfnt.render('BOSS HP: '+str(bosshp),0,(255,0,0))
                screen.blit(hptxt,(300,32))

            #BOSS SPEED
            if bosshp==15:
                bspd=6
            elif bosshp==10:
                bspd=8
            elif bosshp==10:
                bspd=10

            #BOSS DEATH
            if bosshp<=0:
                game.time.wait(500)
                gameon=False
                win=True
                break
            
            #WALL DRAW
            for w in walls:
                screen.blit(wallimg,(w[0],w[1]))
                wallbox=game.Rect(wallimg.get_rect())
                wallbox.x=w[0]
                wallbox.y=w[1]
                if wallbox.colliderect(pbox):
                    collision=True
            
            #MOVEMENT WITH COLLISION CHECK
            if collision==False:
                if key[game.K_RIGHT] and xx<734:
                    prevkey="right"
                    if key[game.K_DOWN]:
                        prevkey="rightdown"
                    if key[game.K_UP]:
                        prevkey="rightup"
                    if collision==False:
                        xx+=spd
                if key[game.K_LEFT] and xx>32:
                    prevkey="left"
                    if key[game.K_DOWN]:
                        prevkey="leftdown"
                    if key[game.K_UP]:
                        prevkey="leftup"
                    if collision==False:
                        xx-=spd
                if key[game.K_DOWN] and yy<542:
                    prevkey="down"
                    if key[game.K_LEFT]:
                        prevkey="leftdown"
                    if key[game.K_RIGHT]:
                        prevkey="rightdown"
                    if collision==False:
                        yy+=spd
                if key[game.K_UP] and yy>32:
                    prevkey="up"
                    if key[game.K_LEFT]:
                        prevkey="leftup"
                    if key[game.K_RIGHT]:
                        prevkey="rightup"
                    if collision==False:
                        yy-=spd

            #BARRIER COLLISION
            if event.type==game.KEYUP:
                if collision==True:
                    if prevkey=="left":
                        xx+=5
                    if prevkey=="right":
                        xx-=5
                    if prevkey=="down":
                        yy-=5
                    if prevkey=="up":
                        yy+=5
                    if prevkey=="rightup":
                        yy+=5
                        xx-=5
                    if prevkey=="rightdown":
                        yy-=5
                        xx-=5
                    if prevkey=="leftdown":
                        yy-=5
                        xx+=5
                    if prevkey=="leftup":
                        yy+=5
                        xx+=5
                    collision=False

            #CHECK FOR GAMEOVER
            deathCheck()
            
            #GAME OVER
            if death==True:
                death=False
                titlescreen=False
                gameon=False
                gameover=True
                win=False
                xx=64
                yy=64
                break
                
            #ANIMATIONS
            enemyAnimation()
            portalAnimation()
            bossAnimation()
            
            #refresh draw
            game.display.flip()
            await asyncio.sleep(0)  # Let other tasks run

        #GAME OVER LOOP
        kup=True
        while gameover:
            #DRAW
            drawFloor()
            drawEdgeWalls()

            #TEXT AND SELECTION COLOR
            tatxt=selectfnt.render('Try Again',0,colora)
            exittxt=selectfnt.render('Exit',0,colorb)
            screen.blit(gotxt,(82,100))
            screen.blit(tatxt,(330,400))
            screen.blit(exittxt,(375,500))

            #EVENTS AND KEYS
            event=game.event.poll()
            if event.type == game.QUIT:
                game.quit()
            key=game.key.get_pressed()
            if key[game.K_UP]:
                colora=blue
                colorb=dblue
                kup=True
                kdown=False
            elif key[game.K_DOWN]:
                colora=dblue
                colorb=blue
                kup=False
                kdown=True

            #SELECTION
            if kup==True:
                if key[game.K_RETURN]:
                    gameon=True
                    gameover=False
                    select.play()
                    break
            elif kdown==True:
                if key[game.K_RETURN]:
                    game.quit()

            #REFRESH
            game.display.flip()
            await asyncio.sleep(0)  # Let other tasks run

        #WIN LOOP
        if win: # (2023) Fix to prevent: https://developer.chrome.com/blog/play-request-was-interrupted/
            game.mixer.music.stop()
            game.mixer.music.load(titlemusic)
            game.mixer.music.play(-1)
        while win:
            #DRAW
            drawFloor()
            drawEdgeWalls()

            #TEXT AND SELECTION COLOR
            tatxt=selectfnt.render('Play Again',0,colora)
            exittxt=selectfnt.render('Exit',0,colorb)
            screen.blit(wintxt,(150,100))
            screen.blit(tatxt,(330,400))
            screen.blit(exittxt,(375,500))

            #EVENTS AND KEYS
            event=game.event.poll()
            if event.type == game.QUIT:
                game.quit()
            key=game.key.get_pressed()
            if key[game.K_UP]:
                colora=blue
                colorb=dblue
                kup=True
                kdown=False
            elif key[game.K_DOWN]:
                colora=dblue
                colorb=blue
                kup=False
                kdown=True

            #Selection
            if kup==True:
                if key[game.K_RETURN]:
                    gameon=True
                    win=False
                    select.play()
                    reset=True
                    level=1
                    xx=64
                    yy=64
                    break
            elif kdown==True:
                if key[game.K_RETURN]:
                    game.quit()

            #REFRESH
            game.display.flip()
            await asyncio.sleep(0)  # Let other tasks run

# This is the program entry point
asyncio.run(main())
