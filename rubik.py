import maya.cmds as cmds
import maya.mel as mel
import os
import random

# Variable for time on slider

FRAME = 10

# Functions

def buildCubeModel():
    # Clear the scene to start
    cmds.select(all=True)
    cmds.delete()

    # Generates the entire cube model
    cmds.polyCube(w=1, h=1, d=1, sx=1, sy=1, sz=1, ax=(0,1,0), cuv=4, ch=1)
    cmds.polyBevel("pCube1", com=0, fraction=0.15, offsetAsFraction=1, autoFit=1, segments=5, 
        worldSpace=1, uvAssignment=0, smoothingAngle=30, fillNgons=1, mergeVertices=1,
        mergeVertexTolerance=0.0001, miteringAngle=180, angleTolerance=180, ch=1)
    cmds.select("pCube1", replace=True)
    cmds.duplicate(rr=True)
    cmds.move(1, 0, 0, r=True)
    for i in range(1):
        cmds.duplicate(rr=True, st=True)
    cmds.select("pCube1", "pCube2", "pCube3", replace=True)
    cmds.duplicate(rr=True)
    cmds.move(0, 0, -1, r=True)
    for i in range(1):
        cmds.duplicate(rr=True, st=True)
    cmds.select("pCube1", "pCube2", "pCube3",
        "pCube4", "pCube5", "pCube6",
        "pCube7", "pCube8", "pCube9")
    cmds.duplicate(rr=True)
    cmds.move(0, 1, 0, r=True)
    for i in range(1):
        cmds.duplicate(rr=True, st=True)
    textureCube()
    initSetup()
    cmds.autoKeyframe(state=True)
    cmds.select(clear=True)
    #cmds.scriptEditorInfo(sw=True)
    #setPos()
    setInitialKeys()
    
def textureCube():
    # Texture the entire cube initially black
    cubeBaseColorBlinn = cmds.shadingNode("blinn", asShader=True)
    cmds.setAttr(cubeBaseColorBlinn + '.color', 0, 0, 0) # Black
    cmds.select("pCube1", "pCube2", "pCube3", "pCube4", "pCube5", "pCube6", 
        "pCube7", "pCube8", "pCube9", "pCube10", "pCube11", "pCube12", "pCube13", "pCube14",
        "pCube15", "pCube16", "pCube17", "pCube18", "pCube19", "pCube20", "pCube21", 
        "pCube22", "pCube23", "pCube24", "pCube25", "pCube26", "pCube27")
    cmds.hyperShade(assign=cubeBaseColorBlinn)
    
    # Texture the individual faces with apropriate colors
    
    # White face
    whiteBlinn = cmds.shadingNode("blinn", asShader=True)
    cmds.setAttr(whiteBlinn + '.color', 1, 1, 1) 
    cmds.select("pCube1.f[1]", "pCube2.f[1]", "pCube3.f[1]",
        "pCube10.f[1]", "pCube11.f[1]", "pCube12.f[1]",
        "pCube19.f[1]", "pCube20.f[1]", "pCube21.f[1]")
    cmds.hyperShade(assign=whiteBlinn)
    
    # Blue face
    blueBlinn = cmds.shadingNode("blinn", asShader=True)
    cmds.setAttr(blueBlinn + '.color', 0, 0, 1) 
    cmds.select("pCube19.f[4]", "pCube20.f[4]", "pCube21.f[4]",
        "pCube22.f[4]", "pCube23.f[4]", "pCube24.f[4]",
        "pCube25.f[4]", "pCube26.f[4]", "pCube27.f[4]")
    cmds.hyperShade(assign=blueBlinn)
    
    # Red face
    redBlinn = cmds.shadingNode("blinn", asShader=True)
    cmds.setAttr(redBlinn + '.color', 1, 0, 0)
    cmds.select("pCube3.f[3]", "pCube6.f[3]", "pCube9.f[3]",
        "pCube12.f[3]", "pCube15.f[3]", "pCube18.f[3]",
        "pCube21.f[3]", "pCube24.f[3]", "pCube27.f[3]")
    cmds.hyperShade(assign=redBlinn)
    
    # Yellow face
    yellowBlinn = cmds.shadingNode("blinn", asShader=True)
    cmds.setAttr(yellowBlinn + '.color', 1, 1, 0)
    cmds.select("pCube7.f[5]", "pCube8.f[5]", "pCube9.f[5]",
        "pCube16.f[5]", "pCube17.f[5]", "pCube18.f[5]",
        "pCube25.f[5]", "pCube26.f[5]", "pCube27.f[5]")
    cmds.hyperShade(assign=yellowBlinn)
    
    # Green face
    greenBlinn = cmds.shadingNode("blinn", asShader=True)
    cmds.setAttr(greenBlinn + '.color', 0, 1, 0)
    cmds.select("pCube1.f[0]", "pCube2.f[0]", "pCube3.f[0]",
        "pCube4.f[0]", "pCube5.f[0]", "pCube6.f[0]",
        "pCube7.f[0]", "pCube8.f[0]", "pCube9.f[0]")
    cmds.hyperShade(assign=greenBlinn)
    
    # Orange face
    orangeBlinn = cmds.shadingNode("blinn", asShader=True)
    cmds.setAttr(orangeBlinn + '.color', 1, 0.5, 0)
    cmds.select("pCube1.f[2]", "pCube4.f[2]", "pCube7.f[2]",
        "pCube10.f[2]", "pCube13.f[2]", "pCube16.f[2]",
        "pCube19.f[2]", "pCube22.f[2]", "pCube25.f[2]")
    cmds.hyperShade(assign=orangeBlinn)


def setPos():
    # Sets the default position of the cube
    # This is the trick that allows me easier rotations
    cmds.select(allDagObjects=True)
    cmds.makeIdentity(apply=True, t=0, r=1, s=0, n=0, pn=1)    

'''All turns are in referce to white face as the front and blue face on top'''
'''If inverse is not specified, a clockwise turn will be made, otherwise, counterclkwise'''

# Front face rotation
def F(inverse=None):
    if inverse is None:
        inverse = -1
    else:
        inverse = 1    
    center = ''       
    selectAllCubes()
    selected = cmds.ls(selection=True)
    for cube in selected:
        y = cmds.getAttr(cube+'.translateY')
        x = cmds.getAttr(cube+'.translateX')
        if cmds.getAttr(cube+'.translateZ') < 0.9:
            cmds.select(cube, deselect=True) 
        elif y < 0.1 and y > -0.1 and x < 0.1 and x > -0.1:
            center = cube
    cmds.select(center, deselect=True)
    cmds.select(center, add=True)
    cmds.parent()
    cmds.select(center, r=True)
    #cmds.setAttr("pCube11.rotateZ", -90)
    cmds.rotate(0, 0, inverse*90, relative=True)
    selectAllCubes()
    cmds.parent(w=True)
    cmds.select(clear=True)

# Top/Upper Face Rotations    
def U(inverse=None): 
    if inverse is None:
        inverse = -1
    else:
        inverse = 1
    center = ''
    selectAllCubes()
    selected = cmds.ls(selection=True)
    for cube in selected:
        z = cmds.getAttr(cube+'.translateZ')
        x = cmds.getAttr(cube+'.translateX')
        if cmds.getAttr(cube+'.translateY') < 0.9:
            cmds.select(cube, deselect=True)
        elif z < 0.1 and z > -0.1 and x < 0.1 and x > -0.1:
            center = cube
    cmds.select(center, deselect=True)
    cmds.select(center, tgl=True)
    cmds.parent()
    cmds.select(center, r=True)
    #cmds.setAttr("pCube23.rotateY", -a90)
    cmds.rotate(0, inverse*90, 0, relative=True)
    selectAllCubes()
    cmds.parent(w=True)
    cmds.select(clear=True)

# Right side face rotations   
def R(inverse=None): 
    if inverse is None:
        inverse = -1
    else:
        inverse = 1
    center = ''
    selectAllCubes()
    selected = cmds.ls(selection=True)
    for cube in selected:
        z = cmds.getAttr(cube+'.translateZ')
        y = cmds.getAttr(cube+'.translateY')
        if cmds.getAttr(cube+'.translateX') < 0.9:
            cmds.select(cube, deselect=True) 
        elif z < 0.1 and z > -0.1 and y < 0.1 and y > -0.1:
            center = cube
    cmds.select(center, deselect=True)
    cmds.select(center, tgl=True)
    cmds.parent()
    cmds.select(center, r=True)
    cmds.rotate(inverse*90, 0, 0, relative=True)
    selectAllCubes()
    cmds.parent(w=True)
    cmds.select(clear=True)

# Left side face rotations    
def L(inverse=None):
    if inverse is None:
        inverse = 1
    else:
        inverse = -1
    center = ''
    selectAllCubes()
    selected = cmds.ls(selection=True)
    for cube in selected:
        z = cmds.getAttr(cube+'.translateZ')
        y = cmds.getAttr(cube+'.translateY')
        if cmds.getAttr(cube+'.translateX') > -0.9:
            cmds.select(cube, deselect=True) 
        elif z < 0.1 and z > -0.1 and y < 0.1 and y > -0.1:
            center = cube
    cmds.select(center, deselect=True)
    cmds.select(center, tgl=True)
    cmds.parent()
    cmds.select(center, r=True)
    cmds.rotate(inverse*90, 0, 0, relative=True)
    selectAllCubes()
    cmds.parent(w=True)
    cmds.select(clear=True)

# Bottom/Down face rotations    
def D(inverse=None):
    if inverse is None:
        inverse = 1
    else:
        inverse = -1
    center = ''
    selectAllCubes()
    selected = cmds.ls(selection=True)
    for cube in selected:
        z = cmds.getAttr(cube+'.translateZ')
        x = cmds.getAttr(cube+'.translateX')
        if cmds.getAttr(cube+'.translateY') > -0.9:
            cmds.select(cube, deselect=True) 
        elif z < 0.1 and z > -0.1 and x < 0.1 and x > -0.1:
            center = cube
    cmds.select(center, deselect=True)
    cmds.select(center, tgl=True)
    cmds.parent()
    cmds.select(center, r=True)
    cmds.rotate(0, inverse*90, 0, relative=True)
    selectAllCubes()
    cmds.parent(w=True)
    cmds.select(clear=True)

# Back face rotations
def B(inverse=None):
    if inverse is None:
        inverse = 1
    else:
        inverse = -1 
    center = ''    
    selectAllCubes()
    selected = cmds.ls(selection=True)
    for cube in selected:
        y = cmds.getAttr(cube+'.translateY')
        x = cmds.getAttr(cube+'.translateX')
        if cmds.getAttr(cube+'.translateZ') > -0.9:
            cmds.select(cube, deselect=True) 
        elif y < 0.1 and y > -0.1 and x < 0.1 and x > -0.1:
            center = cube
    cmds.select(center, deselect=True)
    cmds.select(center, add=True)
    cmds.parent()
    cmds.select(center, r=True)
    cmds.rotate(0, 0, inverse*90, relative=True)
    selectAllCubes()
    cmds.parent(w=True)
    cmds.select(clear=True)

# Middle slice rotations (up and down)    
def M(inverse=None):
    if inverse is None:
        inverse = 1
    else:
        inverse = -1
    selectAllCubes()
    selected = cmds.ls(selection=True)
    for cube in selected:
        x = cmds.getAttr(cube+'.translateX')
        if x > 0.1 or x < -0.1:
            cmds.select(cube, deselect=True) 
    cmds.select("pCube14", deselect=True)
    cmds.select("pCube14", tgl=True)
    cmds.parent()
    cmds.select("pCube14", r=True)
    cmds.rotate(inverse*90, 0, 0, relative=True)
    selectAllCubes()
    cmds.parent(w=True)
    cmds.select(clear=True)

# Middle slice rotations (left and right)
def E(inverse=None):
    if inverse is None:
        inverse = 1
    else:
        inverse = -1
    selectAllCubes()
    selected = cmds.ls(selection=True)
    for cube in selected:
        y = cmds.getAttr(cube+'.translateY')
        if y > 0.1 or y < -0.1:
            cmds.select(cube, deselect=True) 
    cmds.select("pCube14", deselect=True)
    cmds.select("pCube14", tgl=True)
    cmds.parent()
    cmds.select("pCube14", r=True)
    cmds.rotate(0, inverse*90, 0, relative=True)
    selectAllCubes()
    cmds.parent(w=True)
    cmds.select(clear=True)

# Side slice rotations (up and down)    
def S(inverse=None):
    if inverse is None:
        inverse = -1
    else:
        inverse = 1
    selectAllCubes()
    selected = cmds.ls(selection=True)
    for cube in selected:
        z = cmds.getAttr(cube+'.translateZ')
        if z > 0.1 or z < -0.1:
            cmds.select(cube, deselect=True) 
    cmds.select("pCube14", deselect=True)
    cmds.select("pCube14", tgl=True)
    cmds.parent()
    cmds.select("pCube14", r=True)
    cmds.rotate(0, 0, inverse*90, relative=True)
    selectAllCubes()
    cmds.parent(w=True)
    cmds.select(clear=True)

'''Double layer turns: based on single layer turns'''

# Top two layers rotations    
def u(inverse=None):
    if inverse is None:
        U()
        E(1)
    else:
        U(1)
        E()

# Left two layers rotations                
def l(inverse=None):
    if inverse is None:
        L()
        M()
    else:
        L(1)
        M(1)

# Front two layers rotations                
def f(inverse=None):
    if inverse is None:
        F()
        S()
    else:
        F(1)
        S(1)
        
# Right two layers rotations                
def r(inverse=None):
    if inverse is None:
        R()
        M(1)
    else:
        R(1)
        M()

# Back two layers rotations                
def b(inverse=None):
    if inverse is None:
        B()
        S(1)
    else:
        B(1)
        S()
        
# Bottom two layers rotations                
def d(inverse=None):
    if inverse is None:
        D()
        E()
    else:
        D(1)
        E(1)
    
def rotCubeRight():
    # Rotate the entire cube to the right
    cmds.select("pCube1", "pCube2", "pCube3", "pCube4", "pCube5", "pCube6", 
        "pCube7", "pCube8", "pCube9", "pCube10", "pCube11", "pCube12", "pCube13", "pCube14",
        "pCube15", "pCube16", "pCube17", "pCube18", "pCube19", "pCube20", "pCube21", 
        "pCube22", "pCube23", "pCube24", "pCube25", "pCube26", "pCube27", replace=True)
    
    cmds.rotate(0, '90deg', 0, relative=True)
    
def rotCubeLeft():
    # Rotate the entire cube to the left
    cmds.select("pCube1", "pCube2", "pCube3", "pCube4", "pCube5", "pCube6", 
        "pCube7", "pCube8", "pCube9", "pCube10", "pCube11", "pCube12", "pCube13", "pCube14", 
        "pCube15", "pCube16", "pCube17", "pCube18", "pCube19", "pCube20", "pCube21", 
        "pCube22", "pCube23", "pCube24", "pCube25", "pCube26", "pCube27", replace=True)
    
    cmds.rotate(0, '-90deg', 0, relative=True)    

def setInitialKeys():
    selectAllCubes()
    cmds.setKeyframe(attribute='rotateX', t=1)
    cmds.setKeyframe(attribute='rotateY', t=1)
    cmds.setKeyframe(attribute='rotateZ', t=1)
    cmds.select(clear=True)

def animate():
    global FRAME
    cmds.currentTime(FRAME)
    selectAllCubes()
    cmds.setKeyframe(attribute='rotateX', t=FRAME)
    cmds.setKeyframe(attribute='rotateY', t=FRAME)
    cmds.setKeyframe(attribute='rotateZ', t=FRAME)
    cmds.select(clear=True)
    FRAME = FRAME + 10

def initSetup():
    # Move the cube to the center of the scene
    cmds.select(allDagObjects=True)
    cmds.move(-1,-1,1,relative=True)

    # Move all of the pivots to the origin
    cmds.move(0,0,0,"pCube1.scalePivot","pCube1.rotatePivot")
    cmds.move(0,0,0,"pCube2.scalePivot","pCube2.rotatePivot")
    cmds.move(0,0,0,"pCube3.scalePivot","pCube3.rotatePivot")
    cmds.move(0,0,0,"pCube4.scalePivot","pCube4.rotatePivot")
    cmds.move(0,0,0,"pCube5.scalePivot","pCube5.rotatePivot")
    cmds.move(0,0,0,"pCube6.scalePivot","pCube6.rotatePivot")
    cmds.move(0,0,0,"pCube7.scalePivot","pCube7.rotatePivot")
    cmds.move(0,0,0,"pCube8.scalePivot","pCube8.rotatePivot")
    cmds.move(0,0,0,"pCube9.scalePivot","pCube9.rotatePivot")
    cmds.move(0,0,0,"pCube10.scalePivot","pCube10.rotatePivot")
    cmds.move(0,0,0,"pCube11.scalePivot","pCube11.rotatePivot")
    cmds.move(0,0,0,"pCube12.scalePivot","pCube12.rotatePivot")
    cmds.move(0,0,0,"pCube13.scalePivot","pCube13.rotatePivot")
    cmds.move(0,0,0,"pCube14.scalePivot","pCube14.rotatePivot")
    cmds.move(0,0,0,"pCube15.scalePivot","pCube15.rotatePivot")
    cmds.move(0,0,0,"pCube16.scalePivot","pCube16.rotatePivot")
    cmds.move(0,0,0,"pCube17.scalePivot","pCube17.rotatePivot")
    cmds.move(0,0,0,"pCube18.scalePivot","pCube18.rotatePivot")
    cmds.move(0,0,0,"pCube19.scalePivot","pCube19.rotatePivot")
    cmds.move(0,0,0,"pCube20.scalePivot","pCube20.rotatePivot")
    cmds.move(0,0,0,"pCube21.scalePivot","pCube21.rotatePivot")
    cmds.move(0,0,0,"pCube22.scalePivot","pCube22.rotatePivot")
    cmds.move(0,0,0,"pCube23.scalePivot","pCube23.rotatePivot")
    cmds.move(0,0,0,"pCube24.scalePivot","pCube24.rotatePivot")
    cmds.move(0,0,0,"pCube25.scalePivot","pCube25.rotatePivot")
    cmds.move(0,0,0,"pCube26.scalePivot","pCube26.rotatePivot")
    cmds.move(0,0,0,"pCube27.scalePivot","pCube27.rotatePivot")
    
    # Set the time slider range
    cmds.playbackOptions(maxTime='60sec')

def flower():
    M(); S(); M(1); S(1);
    
def checkerboard():
    M(); M(); E(); E(); S(); S();
    
def tetris():
    L(); R(); F(); B(); U(1); D(1); L(1); R(1);
    
def cubeInACube():
    F(); L(); F(); U(1); R(); U(); F(); F(); L(); L(); U(1);
    L(1); B(); D(1); B(1); L(); L(); U();
    
def selectAllCubes():
    # Select all of the cubes
    cmds.select("pCube1", "pCube2", "pCube3", "pCube4", "pCube5", "pCube6", 
        "pCube7", "pCube8", "pCube9", "pCube10", "pCube11", "pCube12", "pCube13", "pCube14",
        "pCube15", "pCube16", "pCube17", "pCube18", "pCube19", "pCube20", "pCube21", 
        "pCube22", "pCube23", "pCube24", "pCube25", "pCube26", "pCube27", replace=True)
        
def getPos(cube):
    coords = cmds.xform(cube, query=True, wd=True, translation=True)
    return coords     

def scramble(n):
    # Use randomly generated numbers to scrable the cube with n turns
    random.seed()
    for i in range(n):
        randNum = random.randint(1,12)
        animate()
        if randNum == 1:
            U()
        elif randNum == 2:
            U(1)
        elif randNum == 3:
            L()
        elif randNum == 4:
            L(1)
        elif randNum == 5:
            F()
        elif randNum == 6:
            F(1)
        elif randNum == 7:
            R()
        elif randNum == 8:
            R(1)
        elif randNum == 9:
            B()
        elif randNum == 10:
            B(1)    
        elif randNum == 11:
            D()
        elif randNum == 12:
            D(1)

def reset():
    buildCubeModel()
       
def createUI():
    # Create the GUI
    WINDOW_NAME = "Rubik's Cube Controls"
      
    myWindow = 'myWindowID'  
      
    if cmds.window(myWindow, exists=True):
        cmds.deleteUI(myWindow)
    if cmds.window(myWindow, exists=True):
        cmds.windowPref(myWindow, remove=True)

    cmds.window(myWindow, title=WINDOW_NAME, resizeToFitChildren=True)
    
    cmds.rowColumnLayout(numberOfColumns=7, columnWidth=[(1,200),(2,75),(3,75),(4,75),(5,75),(6,75),(7,75)]) 
    
    # Build and reset
    cmds.text(label="Main Functions:"); cmds.separator(); cmds.separator(); cmds.separator() 
    cmds.separator(); cmds.separator(); cmds.separator(); cmds.separator(style='none',width=5)
    cmds.button('Build_Btn', label="Build", command="buildCubeModel()")
    cmds.button('Reset_Btn', label="Reset", command="reset()")
    cmds.button('Flower_Btn', label="Flower", command="flower()")
    cmds.button('Checkerboard_Btn', label="Checkerboard", command="checkerboard()")
    cmds.button('Tetris_Btn', label="Tetris", command="tetris()")
    cmds.button('CubeInACube_Btn', label="Cube in a cube", command="cubeInACube()")
 
    # Clockwise face rotations
    cmds.text(label="Clockwise face rotations:"); cmds.separator(); cmds.separator(); cmds.separator() 
    cmds.separator(); cmds.separator(); cmds.separator(); cmds.separator(style='none',width=5)
    cmds.button('U_Btn', label="U", command="animate(); U()")   
    cmds.button('F_Btn', label="F", command="animate(); F()")
    cmds.button('R_Btn', label="R", command="animate(); R()")
    cmds.button('L_Btn', label="L", command="animate(); L()")
    cmds.button('D_Btn', label="D", command="animate(); D()")
    cmds.button('B_Btn', label="B", command="animate(); B()")
    
    # Counter clockwise face rotations
    cmds.text(label="Coutner-clockwise face rotations:"); cmds.separator(); cmds.separator(); cmds.separator()
    cmds.separator(); cmds.separator(); cmds.separator(); cmds.separator(style='none',width=5)
    cmds.button('UPrime_Btn', label="U'", command="animate(); U(1)")
    cmds.button('FPrime_Btn', label="F'", command="animate(); F(1)")
    cmds.button('RPrime_Btn', label="R'", command="animate(); R(1)")
    cmds.button('LPrime_Btn', label="L'", command="animate(); L(1)")
    cmds.button('DPrime_Btn', label="D'", command="animate(); D(1)")
    cmds.button('BPrime_Btn', label="B'", command="animate(); B(1)")
    
    # Slice turns
    cmds.text(label="Slice rotations:"); cmds.separator(); cmds.separator(); cmds.separator()
    cmds.separator(); cmds.separator(); cmds.separator(); cmds.separator(style='none',width=5)
    cmds.button('M_Btn', label="M", command="animate(); M()")   
    cmds.button('MPrime_Btn', label="M'", command="animate(); M(1)")
    cmds.button('E_Btn', label="E", command="animate(); E()")
    cmds.button('EPrime_Btn', label="E'", command="animate(); E(1)")
    cmds.button('S_Btn', label="S", command="animate(); S()")
    cmds.button('SPrime_Btn', label="S'", command="animate(); S(1)")
    
    # Double layer turns
    cmds.text(label="Double layer rotations:"); cmds.separator(); cmds.separator(); cmds.separator()
    cmds.separator(); cmds.separator(); cmds.separator(); cmds.separator(style='none',width=5)
    cmds.button('u_Btn', label="u", command="animate(); u()")   
    cmds.button('f_Btn', label="f", command="animate(); f()")
    cmds.button('r_Btn', label="r", command="animate(); r()")
    cmds.button('l_Btn', label="l", command="animate(); l()")
    cmds.button('d_Btn', label="d", command="animate(); d()")
    cmds.button('b_Btn', label="b", command="animate(); b()")
    
    # Inverse double layer turns
    cmds.text(label="Inverse double layer rotations:"); cmds.separator(); cmds.separator(); cmds.separator();
    cmds.separator(); cmds.separator(); cmds.separator(); cmds.separator(style='none',width=5)
    cmds.button('uPrime_Btn', label="u'", command="animate(); u(1)")
    cmds.button('fPrime_Btn', label="f'", command="animate(); f(1)")
    cmds.button('rPrime_Btn', label="r'", command="animate(); r(1)")
    cmds.button('lPrime_Btn', label="l'", command="animate(); l(1)")
    cmds.button('dPrime_Btn', label="d'", command="animate(); d(1)")
    cmds.button('bPrime_Btn', label="b'", command="animate(); b(1)")
     
    # Scrable Options
    cmds.text( label="Scramble Turns:")
    cmds.separator(); cmds.separator(); cmds.separator(); cmds.separator(); cmds.separator(); cmds.separator();
    cmds.intSliderGrp('nScrambleTurns', field=True, minValue=1, maxValue=50, value=25)
    cmds.button('scramle_Btn', label='Scramble', command="scramble(cmds.intSliderGrp('nScrambleTurns', query=True, value=True))") 
     
    cmds.showWindow(myWindow)
  
# Main Execution 

createUI()
