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
	root.gravity = [0,-9.81,0]
	root.dt = 0.0001
        
	root.addObject('DefaultVisualManagerLoop')
	root.addObject('DefaultAnimationLoop')

	root.addObject('VisualStyle', displayFlags="hideCollisionModels showForceFields showMappings")
	root.addObject('RequiredPlugin', pluginName="SofaImplicitOdeSolver SofaLoader SofaOpenglVisual SofaBoundaryCondition SofaGeneralLoader SofaGeneralSimpleFem SofaMeshCollision SofaEngine SofaConstraint SofaRigid")
	root.addObject('DefaultPipeline', name="CollisionPipeline")
	root.addObject('BruteForceDetection', name="N2")
	root.addObject('DefaultContactManager', name="CollisionResponse", response="PenalityContactForceField")
	root.addObject('NewProximityIntersection', name="Proximity", alarmDistance=0.00001, contactDistance=0.000005)
	root.addObject('DiscreteIntersection')
	
	confignode = root.addChild("Config")
	confignode.addObject('OglSceneFrame', style="Arrows", alignment="TopRight")
    	
	phantom = root.addChild('Phantom')
	phantom.addObject('EulerImplicitSolver', name="cg_odesolver", rayleighStiffness=0.1, rayleighMass=0.1)
	phantom.addObject('CGLinearSolver', name="linear_solver", iterations=25, tolerance=1e-15, threshold=1e-20)
    	
	phantom.addObject('MeshGmshLoader', name="meshLoader", filename="./phantom.msh")
	phantom.addObject('MeshTopology', src="@meshLoader")
	phantom.addObject('TetrahedronSetTopologyContainer', name="topo", src="@meshLoader")
	phantom.addObject('MechanicalObject', name="dofs", src="@meshLoader")
	#phantom.addObject('TetrahedronSetTopologyModifier' name="Modifier")
	phantom.addObject('TetrahedronSetGeometryAlgorithms', template="Vec3d", name="GeomAlgo")
	phantom.addObject('UniformMass', name="Mass", totalMass="0.22")
    	#human breast has poisson ratio of 0.5 according to  https://www.eng.tau.ac.il/~msbm/resources/55.PDF
    	#young's modulos = 200 kPa by assumption
	phantom.addObject('TetrahedralCorotationalFEMForceField', template="Vec3d", name="FEM", method="large", poissonRatio=0.45, youngModulus=3000, computeGlobalMatrix=False)
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
	
	ball = root.addChild("Sphere")
	ball.addObject('MechanicalObject', name="mstate", template="Rigid3", position=[0.05, 0.045, 0.05, 0, 0, 0, 1])
	ball.addObject('UniformMass', totalMass=0.01)
	ball.addObject('UncoupledConstraintCorrection')
	
	ball.addObject('EulerImplicitSolver', name='odesolver')
	ball.addObject('CGLinearSolver', name='Solver', iterations=25, tolerance=1e-15, threshold=1e-20)
	
	ballCollision = ball.addChild('collision')
	ballCollision.addObject('MeshOBJLoader', name="loader", filename="mesh/ball.obj", triangulate="true", scale=0.01)
	
	ballCollision.addObject('MeshTopology', src="@loader")
	ballCollision.addObject('MechanicalObject')
	
	ballCollision.addObject('TriangleCollisionModel')
	ballCollision.addObject('LineCollisionModel')
	ballCollision.addObject('PointCollisionModel')
	
	ballCollision.addObject('RigidMapping')
	
	return root
  
        
if __name__ == '__main__':
    main()
