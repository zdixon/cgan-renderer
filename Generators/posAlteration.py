import maya.mel as mel
import maya.cmds as cmds
import random

def initRandom():
	pointLights = cmds.ls("point")
	for light in pointLights:
		x = random.uniform(-1.0, 1.0) * 10
		y = random.random() * 20
		z = random.uniform(-1.0, 1.0) * 10
		cmds.setAttr('%s.%s' % (light, 'translateX'), x)
		cmds.setAttr('%s.%s' % (light, 'translateY'), y)
		cmds.setAttr('%s.%s' % (light, 'translateZ'), z)
	return [x,y,z]

def setLight(pos):
	pointLights = cmds.ls("point")
	for light in pointLights:
		cmds.setAttr('%s.%s' % (light, 'translateX'), pos[0])
		cmds.setAttr('%s.%s' % (light, 'translateY'), pos[1])
		cmds.setAttr('%s.%s' % (light, 'translateZ'), pos[2])

def randomizePointLight(initPosition):
	lightInfoFile = "/Users/Max/Dropbox (Brown)/CS2951/Training Data/PositionAlterationTest/lightInfo/lightInfo.txt"
	pointLights = cmds.ls("point")
	camera = cmds.ls('camera1')[0]
	# print camera
	cameraX = cmds.getAttr('%s.%s' % (camera, 'translateX'))
	cameraY = cmds.getAttr('%s.%s' % (camera, 'translateY'))
	cameraZ = cmds.getAttr('%s.%s' % (camera, 'translateZ'))
	for light in pointLights:
		x = random.uniform(-1.0, 1.0) * 10
		y = random.random() * 20
		z = random.uniform(-1.0, 1.0) * 10
		cmds.setAttr('%s.%s' % (light, 'translateX'), x)
		cmds.setAttr('%s.%s' % (light, 'translateY'), y)
		cmds.setAttr('%s.%s' % (light, 'translateZ'), z)
		lightString = "%f,%f,%f\n" % (x-initPosition[0],y-initPosition[1],z-initPosition[2])
		# lightString = "%f,%f,%f\n" % (x-cameraX,y-cameraY,z-cameraZ)
		with open(lightInfoFile, "a") as file:
			file.write(lightString)

def generateSamples(sceneNum, lightNum):
	lightInfoFile = "/Users/Max/Dropbox (Brown)/CS2951/Training Data/PositionAlterationTest/lightInfo/lightInfo.txt"
	open(lightInfoFile, 'w').close()
	sceneShapes = cmds.ls(tr=True)
	sceneShapes = sceneShapes[7:]
	sceneShapes = sceneShapes[:-2]
	for sceneArrangements in range(0, sceneNum):
		for shape in sceneShapes:
			x = random.uniform(-1.0, 1.0) * 5
			y = random.random() * 10
			z = random.uniform(-1.0, 1.0) * 5
			cmds.setAttr('%s.%s' % (shape, 'translateX'), x)
			cmds.setAttr('%s.%s' % (shape, 'translateY'), y)
			cmds.setAttr('%s.%s' % (shape, 'translateZ'), z)
		initPosition = initRandom()
		for lightArrangements in range(0, lightNum):
			print sceneArrangements * lightNum + lightArrangements
			baselineName = "\"/Users/Max/Dropbox (Brown)/CS2951/Training Data/PositionAlterationTest/baseline/baseline." + '%04d' % (sceneArrangements * lightNum + lightArrangements) + '.exr\"'
			beautyName = "\"/Users/Max/Dropbox (Brown)/CS2951/Training Data/PositionAlterationTest/beauty/beauty." + '%04d' % (sceneArrangements * lightNum + lightArrangements) + '.exr\"'
			nName = "\"/Users/Max/Dropbox (Brown)/CS2951/Training Data/PositionAlterationTest/N/N." + '%04d' % (sceneArrangements * lightNum + lightArrangements) + '.exr\"'
			zName = "\"/Users/Max/Dropbox (Brown)/CS2951/Training Data/PositionAlterationTest/Z/Z." + '%04d' % (sceneArrangements * lightNum + lightArrangements) + '.exr\"'
			setLight(initPosition)
			cmds.showHidden("point")
			cmds.hide("baseline")
			mel.eval("setAttr defaultArnoldRenderOptions.displayAOV -type \"string\"  \"beauty\"")
			mel.eval("arnoldRender -cam \"camera1\"")
			mel.eval("renderWindowSaveImageCallback \"renderView\" %s \"EXR\"" % baselineName)

			cmds.showHidden("point")
			cmds.hide("baseline")
			randomizePointLight(initPosition)
			mel.eval("setAttr defaultArnoldRenderOptions.displayAOV -type \"string\"  \"beauty\"")
			mel.eval("arnoldRender -cam \"camera1\"")
			mel.eval("renderWindowSaveImageCallback \"renderView\" %s \"EXR\"" % beautyName)

			mel.eval("setAttr defaultArnoldRenderOptions.displayAOV -type \"string\"  \"N\"")
			mel.eval("arnoldRender -cam \"camera1\"")
			mel.eval("renderWindowSaveImageCallback \"renderView\" %s \"EXR\"" % nName)

			mel.eval("setAttr defaultArnoldRenderOptions.displayAOV -type \"string\"  \"Z\"")
			mel.eval("arnoldRender -cam \"camera1\"")
			mel.eval("renderWindowSaveImageCallback \"renderView\" %s \"EXR\"" % zName)

generateSamples(50,1)