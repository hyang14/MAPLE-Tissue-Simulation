#required import for python
import Sofa
import math

USE_GUI = True


def main():
	import SofaRuntime
	import Sofa.Gui
	SofaRuntime.importPlugin("SofaOpenglVisual")
	SofaRuntime.importPlugin("SofaImplicitOdeSolver")
	
	root = Sofa.Core.Node("root")
	createScene(root)
	
	Sofa.Simulation.init(root)
	
	if not USE_GUI:
		for iteration in range(10):
			Sofa.Simulation.animate(root, root.dt.value)
	else:
		Sofa.Gui.GUIManager.Init("myscene", "qglviewer")
		Sofa.Gui.GUIManager.createGUI(root, __file__)
		Sofa.Gui.GUIManager.SetDimension(1080, 1080)
		Sofa.Gui.GUIManager.MainLoop(root)
		Sofa.Gui.GUIManager.closeGUI()


def createScene(root):
	root.gravity = [0,-1,0]
	root.dt = 0.02
        
	root.addObject('DefaultVisualManagerLoop')
	root.addObject('DefaultAnimationLoop')

	root.addObject('VisualStyle', displayFlags="showCollisionModels showForceFields showMappings")
	root.addObject('RequiredPlugin', pluginName="SofaImplicitOdeSolver SofaLoader SofaOpenglVisual SofaBoundaryCondition SofaGeneralLoader SofaGeneralSimpleFem SofaMeshCollision SofaEngine")
	root.addObject('DefaultPipeline', name="CollisionPipeline")
	root.addObject('BruteForceDetection', name="N2")
	root.addObject('DefaultContactManager', name="CollisionResponse", response="PenalityContactForceField")
	root.addObject('NewProximityIntersection', name="Proximity", alarmDistance=0.5, contactDistance=0.25)
	root.addObject('DiscreteIntersection')
	
	confignode = root.addChild("Config")
	confignode.addObject('OglSceneFrame', style="Arrows", alignment="TopRight")
    	
	phantom = root.addChild('Phantom')
	phantom.addObject('EulerImplicitSolver', name="cg_odesolver", rayleighStiffness=0.1, rayleighMass=0.1)
	phantom.addObject('CGLinearSolver', name="linear_solver", iterations=25, tolerance=1e-09, threshold=1e-09)
    	
	phantom.addObject('MeshGmshLoader', name="meshLoader", filename="./phantom.msh")
	phantom.addObject('MeshTopology', src="@meshLoader")
	phantom.addObject('TetrahedronSetTopologyContainer', name="topo", src="@meshLoader")
	phantom.addObject('MechanicalObject', name="dofs", src="@meshLoader")
	#phantom.addObject('TetrahedronSetTopologyModifier' name="Modifier")
	phantom.addObject('TetrahedronSetGeometryAlgorithms', template="Vec3d", name="GeomAlgo")
	phantom.addObject('UniformMass', name="Mass", totalMass="0.22")
    	#human breast has poisson ratio of 0.5 according to  https://www.eng.tau.ac.il/~msbm/resources/55.PDF
    	#young's modulos = 200 kPa by assumption
	phantom.addObject('TetrahedralCorotationalFEMForceField', template="Vec3d", name="FEM", method="large", poissonRatio=0.49, youngModulus=200000, computeGlobalMatrix=False)
	phantom.addObject('BoxROI', template="Vec3d", box="-0.01 -0.00001 -0.01 0.1 0.00001 0.1", name="FixedROI", drawBoxes="1", drawSize="1")
	phantom.addObject('FixedConstraint', name="fixROIindices", indices="@FixedROI.indices", showObject="True", drawSize="1")

	
    
    #add collision node for the phantom
	collision = phantom.addChild('Collision')
	rotation=[0,0,0]
	collision.addObject('MeshGmshLoader', name="collMeshLoader", filename="./phantom.msh",rotation=rotation)
	collision.addObject('MechanicalObject', name="collMesh", src="@collMeshLoader", template='Vec3d', listening=1)
	collision.addObject('MeshTopology', src='@collMeshLoader')
	collision.addObject('TriangleCollisionModel')
	collision.addObject('LineCollisionModel')
	collision.addObject('PointCollisionModel')
	collision.addObject('BarycentricMapping',name="CollisionMapping", input="@../dofs", output="@collMesh")
	
	# add a floor to hold the droped object
	
	root.addObject(KeyPressedController(name = "SphereCreator"))
	
	return root
        
class KeyPressedController(Sofa.Core.Controller):
	"""monitor and control sphere dropping
	"""     
	def __init__(self, *args, **kwargs):
	    Sofa.Core.Controller.__init__(self, *args, **kwargs)
	    self.iteration = 0
	    print("\n\n\n KeyPressedController added \n\n\n")
	    
	def onKeypressedEvent(self, event):
		if event['key']=='L':
			self.createNewSphere()
            
	def createNewSphere(self):
		root = self.getContext()
		newSphere = root.addChild('FallingSphere-'+str(self.iteration))
		newSphere.addObject('EulerImplicitSolver')
		newSphere.addObject('CGLinearSolver', threshold='1e-09', tolerance='1e-09', iterations='200')
		#not sure what the rest of position is (quarternion?)
		MO = newSphere.addObject('MechanicalObject', showObject=True, position=[0.05, 0.05, 0.05, 0, 0, 0, 1], name=f'Partical-{self.iteration}', template='Rigid3d') 
		Mass = newSphere.addObject('UniformMass', totalMass=0.001)
		Force = newSphere.addObject('ConstantForceField', name='CFF', totalForce=[0,0,0,0,0,0])
		Sphere = newSphere.addObject('SphereCollisionModel', name="SCM", radius=0.02)
        
		newSphere.init()
		self.iteration = self.iteration+1
        
if __name__ == '__main__':
    main()
