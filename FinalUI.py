import maya.cmds as cmds
import math

class M_Window(object):
    def __init__(self):
        self.window = "M_Window"  # nombre de la clase
        self.title = "Boss Animation Plugin"  # nombre de la ventana
        self.size = (300, 400)
        self.amountJoints = 0
        self.yGap = 5
        self.height = 0
        self.positions = self.initialPosition()

        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window, window=True)

        self.window = cmds.window(self.window, title=self.title, widthHeight=self.size)
        cmds.columnLayout()

        self.valueJoints = cmds.text(l="Number of Joints")
        self.valJoints = cmds.intField(minValue=0, maxValue=100, value=0)
        cmds.rowLayout(numberOfColumns=2, columnWidth2=(100, 100), columnOffset2=(10, 10))
        self.CreateJoints = cmds.button(l="Generate Joints", c=self.createJoints)
        self.GenerateMaya = cmds.button(l="Generate Maya", c=self.createMaya)
        cmds.setParent('..')

        # ATTACK ANIMATION ################################################################################
        cmds.separator(height=10, style='none')
        cmds.rowLayout(numberOfColumns=2, columnWidth2=(100, 100), columnOffset2=(10, 10))
        self.attackFrames = cmds.text(l="Initial Frame")
        self.attackFrames = cmds.text(l="Last Frame")
        cmds.setParent('..')
        cmds.rowLayout(numberOfColumns=2, columnWidth2=(100, 100), columnOffset2=(10, 10))
        self.attackInitialFrame = cmds.intField(minValue=0, maxValue=500, value=0)
        self.attackLastFrame = cmds.intField(minValue=0, maxValue=500, value=0)
        cmds.setParent('..')
        self.createAttackAnimation = cmds.button(l="Generate Attack Animation", c=self.createAttackAnimation)
        # IDLE ANIMATION ################################################################################
        cmds.separator(height=10, style='none')
        cmds.rowLayout(numberOfColumns=2, columnWidth2=(100, 100), columnOffset2=(10, 10))
        self.idleFrames = cmds.text(l="Initial Frame")
        self.idleFrames = cmds.text(l="Last Frame")
        cmds.setParent('..')
        cmds.rowLayout(numberOfColumns=2, columnWidth2=(100, 100), columnOffset2=(10, 10))
        self.idleInitialFrame = cmds.intField(minValue=0, maxValue=500, value=0)
        self.idleLastFrame = cmds.intField(minValue=0, maxValue=500, value=0)
        cmds.setParent('..')
        self.createIdleAnimation = cmds.button(l="Generate Idle Animation", c=self.createIdleAnimation)
        # FIGHT ANIMATION ################################################################################
        cmds.separator(height=10, style='none')
        cmds.rowLayout(numberOfColumns=2, columnWidth2=(100, 100), columnOffset2=(10, 10))
        self.fightFrames = cmds.text(l="Initial Frame")
        self.fightFrames = cmds.text(l="Last Frame")
        cmds.setParent('..')
        cmds.rowLayout(numberOfColumns=2, columnWidth2=(100, 100), columnOffset2=(10, 10))
        self.fightInitialFrame = cmds.intField(minValue=0, maxValue=500, value=0)
        self.fightLastFrame = cmds.intField(minValue=0, maxValue=500, value=0)
        cmds.setParent('..')
        self.createFightAnimation = cmds.button(l="Generate Fight Animation", c=self.createFightAnimation)
        # DEFENSE ANIMATION ################################################################################
        cmds.separator(height=10, style='none')
        cmds.rowLayout(numberOfColumns=2, columnWidth2=(100, 100), columnOffset2=(10, 10))
        self.defenseFrames = cmds.text(l="Initial Frame")
        self.defenseFrames = cmds.text(l="Last Frame")
        cmds.setParent('..')
        cmds.rowLayout(numberOfColumns=2, columnWidth2=(100, 100), columnOffset2=(10, 10))
        self.defenseInitialFrame = cmds.intField(minValue=0, maxValue=500, value=0)
        self.defenseLastFrame = cmds.intField(minValue=0, maxValue=500, value=0)
        cmds.setParent('..')
        self.createDefenseAnimation = cmds.button(l="Generate Defense Animation", c=self.createDefenseAnimation)

        cmds.separator(height=10, style='none')
        self.DeleteAll = cmds.button(l="Delete All", c=self.deleteAll)
        cmds.showWindow()  # muestra la ventana

    def createJoints(self, *args):
        self.amountJoints = cmds.intField(self.valJoints, query=True, value=True)
        self.height = self.yGap * (self.amountJoints - 1)
        for i in range(self.amountJoints):
            cmds.joint(p=(self.positions[0], self.positions[1] + -i * self.yGap, self.positions[2]))

    def createMaya(self, *args):
        cylinder = cmds.polyCone(n="cill", sx=self.amountJoints, sy=self.amountJoints, sz=self.amountJoints, h=self.height)[0]
        cmds.rotate('180deg', 0, 0, cylinder)
        
        x_coord = self.positions[0]
        y_coord = self.positions[1] + self.height / -2.0
        z_coord = self.positions[2]
        
        cmds.move(x_coord, y_coord, z_coord, cylinder)
        cmds.move(0, 0, 0, "cill.scalePivot", "cill.rotatePivot", absolute=False)
        cmds.skinCluster("joint1", "cill")
        
        self.joints_map = {}
        for joint in range(self.amountJoints):
            xPos = self.getJointPosition("joint" + str(joint + 1), 0)
            yPos = self.getJointPosition("joint" + str(joint + 1), 1)
            zPos = self.getJointPosition("joint" + str(joint + 1), 2)
            self.joints_map[joint] = [xPos, yPos, zPos]
        print(self.joints_map)

    def createAttackAnimation(self, *args):
        initialFrame = cmds.intField(self.attackInitialFrame, query=True, value=True)
        lastFrame = cmds.intField(self.attackLastFrame, query=True, value=True)
        
        self.resetJoints()
        cmds.rotate('90deg', 0, 0, "joint1", relative=True)
        
        degreesStep = (2 * math.pi)
        for i in range(initialFrame, lastFrame):
            for j in range(self.amountJoints):
                if i == lastFrame - 1:
                    cmds.setKeyframe("joint" + str(j + 1), at="rz", v=0, t=i)
                else:
                    cmds.setKeyframe("joint" + str(j + 1), at="rz", v=(degreesStep + (i * 2)) / (j + 1), t=i)
        
        print("Attack animation applied")
        # Beta version ready, recommended range = 70 frames
        
    def createIdleAnimation(self, *args):
        initialFrame = cmds.intField(self.idleInitialFrame, query=True, value=True)
        lastFrame = cmds.intField(self.idleLastFrame, query=True, value=True)
        
        self.resetJoints()
        
        cmds.rotate('90deg', 0, 0, "joint1", relative=True)
        
        for i in range(initialFrame, lastFrame):
            for j in range(1, self.amountJoints):
                x_position = self.getJointPosition("joint" + str(j + 1), 0)
                newPosition = math.sin((2 * math.pi * i) / (lastFrame - initialFrame) + j)
                cmds.setKeyframe("joint" + str(j + 1), at="translateX", v=x_position + newPosition, t=i)
        
        print("Idle animation applied")
        
    def createFightAnimation(self, *args):
        initialFrame = cmds.intField(self.fightInitialFrame, query=True, value=True)
        lastFrame = cmds.intField(self.fightLastFrame, query=True, value=True)
        
        self.resetJoints()
        
        cmds.rotate('90deg', 0, 0, "joint1", relative=True)
        
        for i in range(initialFrame, lastFrame):
            for j in range(1, self.amountJoints):
                x_position = self.getJointPosition("joint" + str(j + 1), 0)
                newPosition = math.cos((8 * math.pi * i) / (lastFrame - initialFrame) + j) * 0.5
                cmds.setKeyframe("joint" + str(j + 1), at="translateZ", v=(x_position + newPosition) * i / 10, t=i)

        print("Fight animation applied")

    def createDefenseAnimation(self, *args):
        initialFrame = cmds.intField(self.defenseInitialFrame, query=True, value=True)
        lastFrame = cmds.intField(self.defenseLastFrame, query=True, value=True)

        self.resetJoints()
        
        cmds.rotate('90deg', 0, 0, "joint1", relative=True)
        
        for i in range(initialFrame, lastFrame):
            for j in range(1, self.amountJoints):
                curl_amount = (math.pi * i * 3/4)  / self.amountJoints
                shake_amount = math.sin((8 * math.pi * i) / (lastFrame - initialFrame) + j)  
                cmds.setKeyframe("joint" + str(j + 1), at="rotateX", v=curl_amount, t=i/5)
                cmds.setKeyframe("joint" + str(j + 1), at="translateX", v=shake_amount, t=i)

        print("Defense animation applied")

    def deleteAll(self, *args):
        cmds.delete(cmds.ls(type='joint'))
        cmds.delete(cmds.ls(type='transform'))

    def initialPosition(self, *args):
        nombre = cmds.ls(sl=True)
        print(nombre[0])
        position = cmds.xform(nombre[0], query=True, translation=True)
        radius = cmds.xform(nombre[0], query=True, scale=True)
        radius = radius[0]
        positionX = position[0]
        positionY = position[1]
        positionZ = position[2]
        doubleRadius = 2 * radius
        return positionX, positionY, positionZ

    def getJointPosition(self, jointName, axis):
        position = cmds.xform(jointName, query=True, translation=True)
        return position[axis]

    def resetJoints(self):
        for joint in range(self.amountJoints):
            cmds.xform("joint" + str(joint + 1), translation=(self.joints_map[joint][0], self.joints_map[joint][1], self.joints_map[joint][2]), absolute=True)

myWindow = M_Window()
