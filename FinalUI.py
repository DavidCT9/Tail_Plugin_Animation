import maya.cmds as cmds
import math

class M_Window(object):
    def __init__(self):
        self.window = "M_Window"
        self.title = "Boss Animation Plugin"
        self.size = (350, 500)
        self.amountJoints = 0
        self.yGap = 5
        self.height = 0
        self.positions = self.initialPosition()
        self.joints_map = {}
        self.tails = []
        self.angle = 50
        self.image_path = r"C:\Users\david\Documents\DAVID\UP\4_Semestre\DesarroloPlugins\monster\textures\Final_low_Mostro_mat_BaseColor.1001.png"

        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window, window=True)

        self.window = cmds.window(self.window, title=self.title, widthHeight=self.size)
        self.form = cmds.formLayout()
        self.scroll = cmds.scrollLayout(horizontalScrollBarThickness=16, verticalScrollBarThickness=16)
        self.column = cmds.columnLayout(adjustableColumn=True, parent=self.scroll)

        # JOINTS CONFIGURATION
        cmds.text(label="Joint Settings", align='center', font='boldLabelFont')
        self.valueTails = cmds.text(l="Number of Tails", align='center')
        self.valTails = cmds.intSlider(min=1, max=5, value=1, step=1, dragCommand=self.updateTailsText)
        self.numTailsText = cmds.text(label="1", align='center')

        self.valueJoints = cmds.text(l="Number of Joints", align='center')
        self.valJoints = cmds.intField(minValue=0, maxValue=100, value=0, step=1)

        cmds.rowLayout(numberOfColumns=2, adjustableColumn=2, columnAlign=(1, 'center'), columnAttach=[(1, 'both', 5), (2, 'both', 5)])
        self.CreateJoints = cmds.button(l="Generate Joints", c=self.createJoints, bgc=(0.6, 0.8, 0.6))
        self.GenerateMaya = cmds.button(l="Generate Maya", c=self.createMaya, bgc=(0.6, 0.8, 0.6))
        cmds.setParent('..')

        cmds.separator(height=20, style='double')

        # ATTACK ANIMATION
        cmds.text(label="Attack Animation", align='center', font='boldLabelFont')
        cmds.rowLayout(numberOfColumns=2, adjustableColumn=2, columnAlign=(1, 'center'), columnAttach=[(1, 'both', 5), (2, 'both', 5)])
        self.attackFrames = cmds.text(l="Initial Frame", align='center')
        self.attackInitialFrame = cmds.intField(minValue=0, maxValue=500, value=0, step=1)
        cmds.setParent('..')
        cmds.rowLayout(numberOfColumns=2, adjustableColumn=2, columnAlign=(1, 'center'), columnAttach=[(1, 'both', 5), (2, 'both', 5)])
        self.attackFrames = cmds.text(l="Last Frame", align='center')
        self.attackLastFrame = cmds.intField(minValue=0, maxValue=500, value=0, step=1)
        cmds.setParent('..')
        self.createAttackAnimation = cmds.button(l="Generate Attack Animation", c=self.createAttackAnimation, bgc=(0.8, 0.6, 0.6))

        cmds.separator(height=20, style='double')

        # IDLE ANIMATION
        cmds.text(label="Idle Animation", align='center', font='boldLabelFont')
        cmds.rowLayout(numberOfColumns=2, adjustableColumn=2, columnAlign=(1, 'center'), columnAttach=[(1, 'both', 5), (2, 'both', 5)])
        self.idleFrames = cmds.text(l="Initial Frame", align='center')
        self.idleInitialFrame = cmds.intField(minValue=0, maxValue=500, value=0, step=1)
        cmds.setParent('..')
        cmds.rowLayout(numberOfColumns=2, adjustableColumn=2, columnAlign=(1, 'center'), columnAttach=[(1, 'both', 5), (2, 'both', 5)])
        self.idleFrames = cmds.text(l="Last Frame", align='center')
        self.idleLastFrame = cmds.intField(minValue=0, maxValue=500, value=0, step=1)
        cmds.setParent('..')
        self.createIdleAnimation = cmds.button(l="Generate Idle Animation", c=self.createIdleAnimation, bgc=(0.6, 0.6, 0.8))

        cmds.separator(height=20, style='double')

        # FIGHT ANIMATION
        cmds.text(label="Fight Animation", align='center', font='boldLabelFont')
        cmds.rowLayout(numberOfColumns=2, adjustableColumn=2, columnAlign=(1, 'center'), columnAttach=[(1, 'both', 5), (2, 'both', 5)])
        self.fightFrames = cmds.text(l="Initial Frame", align='center')
        self.fightInitialFrame = cmds.intField(minValue=0, maxValue=500, value=0, step=1)
        cmds.setParent('..')
        cmds.rowLayout(numberOfColumns=2, adjustableColumn=2, columnAlign=(1, 'center'), columnAttach=[(1, 'both', 5), (2, 'both', 5)])
        self.fightFrames = cmds.text(l="Last Frame", align='center')
        self.fightLastFrame = cmds.intField(minValue=0, maxValue=500, value=0, step=1)
        cmds.setParent('..')
        self.createFightAnimation = cmds.button(l="Generate Fight Animation", c=self.createFightAnimation, bgc=(0.8, 0.8, 0.6))

        cmds.separator(height=20, style='double')

        # DEFENSE ANIMATION
        cmds.text(label="Defense Animation", align='center', font='boldLabelFont')
        cmds.rowLayout(numberOfColumns=2, adjustableColumn=2, columnAlign=(1, 'center'), columnAttach=[(1, 'both', 5), (2, 'both', 5)])
        self.defenseFrames = cmds.text(l="Initial Frame", align='center')
        self.defenseInitialFrame = cmds.intField(minValue=0, maxValue=500, value=0, step=1)
        cmds.setParent('..')
        cmds.rowLayout(numberOfColumns=2, adjustableColumn=2, columnAlign=(1, 'center'), columnAttach=[(1, 'both', 5), (2, 'both', 5)])
        self.defenseFrames = cmds.text(l="Last Frame", align='center')
        self.defenseLastFrame = cmds.intField(minValue=0, maxValue=500, value=0, step=1)
        cmds.setParent('..')
        self.createDefenseAnimation = cmds.button(l="Generate Defense Animation", c=self.createDefenseAnimation, bgc=(0.6, 0.8, 0.8))

        cmds.separator(height=20, style='double')

        self.DeleteAll = cmds.button(l="Delete All", c=self.deleteAll, bgc=(0.9, 0.4, 0.4))

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.formLayout(self.form, edit=True, attachForm=[(self.scroll, 'top', 0), (self.scroll, 'bottom', 0), (self.scroll, 'left', 0), (self.scroll, 'right', 0)])

        cmds.showWindow()  # show the window

    def updateTailsText(self, value):
        cmds.text(self.numTailsText, edit=True, label=str(value))

    def createJoints(self, *args):
        self.amountJoints = cmds.intField(self.valJoints, query=True, value=True)
        self.numTails = cmds.intSlider(self.valTails, query=True, value=True)
        self.height = self.yGap * (self.amountJoints - 1)
        for t in range(self.numTails):
            cmds.select(clear=True)
            tail_joints = []
            for i in range(self.amountJoints):
                x = self.positions[0]
                y = self.positions[1] + -i * self.yGap
                z = self.positions[2]
                joint = cmds.joint(p=(x, y, z), name=f"tail{t+1}_joint{i+1}")
                tail_joints.append(joint)
            self.joints_map[f"tail{t+1}"] = tail_joints

    def createMaya(self, *args):
        self.numTails = cmds.intSlider(self.valTails, query=True, value=True)
        self.amountJoints = cmds.intField(self.valJoints, query=True, value=True)
        self.height = self.yGap * (self.amountJoints - 1)

        for t in range(self.numTails):
            # Create the cylinder for the current tail
            tail = cmds.polyCone(n=f"cyl{t+1}", sx=self.amountJoints, sy=self.amountJoints, sz=self.amountJoints, h=self.height)[0]
            self.tails.append(tail)
            cmds.rotate('180deg', 0, 0, self.tails[t])

            # Position the cylinder
            x_coord = self.positions[0]
            y_coord = self.positions[1] + self.height / -2.0
            z_coord = self.positions[2]
            cmds.move(x_coord, y_coord, z_coord, self.tails[t])
            cmds.move(0, 0, 0, f"cyl{t+1}.scalePivot", f"cyl{t+1}.rotatePivot", absolute=False)

            # Skin the cylinder to the joints of the current tail
            tail_joints = self.joints_map.get(f"tail{t+1}")
            if tail_joints:
                cmds.skinCluster(tail_joints, f"cyl{t+1}")

            self.apply_texture(f"cyl{t+1}", self.image_path)


        # Print joint map for debugging
        for t in range(self.numTails):
            self.joints_map[f"tail{t+1}"] = []
            for joint in range(self.amountJoints):
                xPos = self.getJointPosition(f"tail{t+1}_joint{joint + 1}", 0)
                yPos = self.getJointPosition(f"tail{t+1}_joint{joint + 1}", 1)
                zPos = self.getJointPosition(f"tail{t+1}_joint{joint + 1}", 2)
                self.joints_map[f"tail{t+1}"].append((xPos, yPos, zPos))
        print(self.joints_map)
        

    def createAttackAnimation(self, *args):
        initialFrame = cmds.intField(self.attackInitialFrame, query=True, value=True)
        lastFrame = cmds.intField(self.attackLastFrame, query=True, value=True)
        
        degreesStep = (5 * math.pow(math.pi, 2))
        
        for t in range(self.numTails):
            cmds.rotate('90deg', f'{self.angle*t}deg', 0, f"tail{t+1}_joint{1}", relative=True)
            for i in range(initialFrame, lastFrame):
                for j in range(self.amountJoints):
                    joint_name = f"tail{t+1}_joint{j+1}"
                    if i == lastFrame - 1:
                        cmds.setKeyframe(joint_name, at="rx", v=0, t=i)
                    else:
                        cmds.setKeyframe(joint_name, at="rx", v=(degreesStep + (i * 2)) / (j + 1), t=i)
            
        print("Attack animation applied")

    def createIdleAnimation(self, *args):
        initialFrame = cmds.intField(self.idleInitialFrame, query=True, value=True)
        lastFrame = cmds.intField(self.idleLastFrame, query=True, value=True)

        for t in range(self.numTails):
            self.resetJoints(t)
            cmds.rotate('90deg', f'{self.angle*t}deg', 0, f"tail{t+1}_joint{1}", relative=True)
            for i in range(initialFrame, lastFrame):
                for j in range(1, self.amountJoints):
                    joint_name = f"tail{t+1}_joint{j+1}"
                    x_position = self.getJointPosition(joint_name, 0)
                    newPosition = math.sin((2 * math.pi * i) / (lastFrame - initialFrame) + j)
                    cmds.setKeyframe(joint_name, at="translateX", v=x_position + newPosition, t=i)
        
        print("Idle animation applied")

    def createFightAnimation(self, *args):
        initialFrame = cmds.intField(self.fightInitialFrame, query=True, value=True)
        lastFrame = cmds.intField(self.fightLastFrame, query=True, value=True)

        for t in range(self.numTails):
            self.resetJoints(t)
            cmds.rotate('90deg', f'{self.angle*t}deg', 0, f"tail{t+1}_joint{1}", relative=True)
            for i in range(initialFrame, lastFrame):
                for j in range(1, self.amountJoints):
                    joint_name = f"tail{t+1}_joint{j+1}"
                    x_position = self.getJointPosition(joint_name, 0)
                    newPosition = math.cos((8 * math.pi * i) / (lastFrame - initialFrame) + j) * 0.5
                    cmds.setKeyframe(joint_name, at="translateZ", v=(x_position + newPosition) * i / 10, t=i)

        print("Fight animation applied")

    def createDefenseAnimation(self, *args):
        initialFrame = cmds.intField(self.defenseInitialFrame, query=True, value=True)
        lastFrame = cmds.intField(self.defenseLastFrame, query=True, value=True)

        for t in range(self.numTails):
            self.resetJoints(t)
            cmds.rotate('90deg', f'{self.angle*t}deg', 0, f"tail{t+1}_joint{1}", relative=True)
            for i in range(initialFrame, lastFrame):
                for j in range(1, self.amountJoints):
                    joint_name = f"tail{t+1}_joint{j+1}"
                    curl_amount = (math.pi * i * 3 / 4) / self.amountJoints
                    shake_amount = math.sin((8 * math.pi * i) / (lastFrame - initialFrame) + j)
                    cmds.setKeyframe(joint_name, at="rotateX", v=curl_amount, t=i / 5)
                    cmds.setKeyframe(joint_name, at="translateX", v=shake_amount, t=i)

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

    def resetJoints(self, tail_index, *args):
        for joint in range(self.amountJoints):
            joint_name = f"tail{tail_index+1}_joint{joint+1}"
            x, y, z = self.joints_map[f"tail{tail_index+1}"][joint]
            cmds.xform(joint_name, translation=(x, y, z), absolute=True)
            
    def apply_texture(self, object_name, image_file):
        # Create a Lambert shader
        shader_name = cmds.shadingNode('lambert', asShader=True, name='lambert_shader')
        
        # Create a shading group
        shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=shader_name + 'SG')
        
        # Connect the shader to the shading group
        cmds.connectAttr(shader_name + '.outColor', shading_group + '.surfaceShader', force=True)
        
        # Create a file node
        file_node = cmds.shadingNode('file', asTexture=True, isColorManaged=True, name='file_texture')
        cmds.setAttr(file_node + '.fileTextureName', image_file, type='string')
        
        # Connect the file node to the Lambert shader's color attribute
        cmds.connectAttr(file_node + '.outColor', shader_name + '.color', force=True)
        
        # Assign the shader to the object
        cmds.select(object_name)
        cmds.hyperShade(assign=shader_name)
        
        # Ensure textures are visible in the viewport
        cmds.modelEditor('modelPanel4', edit=True, displayTextures=True)
        cmds.modelEditor('modelPanel4', edit=True, displayAppearance='smoothShaded')

myWindow = M_Window()
