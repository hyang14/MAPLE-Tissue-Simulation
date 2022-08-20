# ReadMe for soft tissue simulation

# What is included

this git repo contains a simple script that creates a simulation of a ball dropping on a silicone phantom. Running the script requires the user to install the SOFA framework and relevant sofa plugins (i.e. sofapython3). **SOFA installation on Linux is recommended.**

![Display Image](/image.png)
---

# Installation

## SOFA Installation

SOFA can be installed by running prepared binaries or building from source code. Resources and instructions are on [SOFA website](https://www.sofa-framework.org/download/).  You can choose the binaries installation or build from source code. **Your choice here will impact how the Sofapython3 plugin is installed. Please Read the Sofapython3 installation before installing anything.** 

## Sofapython3 Installation

Since the script is written in python, the sofapython3 plugin must be installed and configured for the SOFA framework for it to work. Relevant information can be found [here](https://sofapython3.readthedocs.io/en/latest/menu/SofaPlugin.html).

**Two ways** to install Sofapython3 plugin: **in-tree build** vs **out-of-tree-build** 

- **In-Tree**: If you are building SOFA from source code, the sofapython3 plugin can be installed during the build process of SOFA.
- **Out-of-Tree**: If SOFA is installed via binaries version or SOFA is already built on the computer, choose the Out-of-Tree method to configure sofapython3 correctly.

# Run example script

Once SOFA and Sofapython3 plugins are installed and configured correctly. Clone the code on this repo onto your local computer. Then, you can check if SOFA and Sofapython3 are working by running the following code in the directory where you cloned the repo.

`runSofa simulation.py`

# Coding for Sofa

- Quick Intro based on my experience (best way to learn sofa is to read the documentation and example python or XML scripts. The examples are included in the SOFA and Sofapython3 installation) [Example files](https://github.com/sofa-framework/SofaPython3/tree/master/examples)
    - Think sofapython3 script as a tree, and the scene is the root node. In the root node it contains the objects you want to simulate and other functional components
        - for each object in the simulation scene, it contains different representations of the object. For example, a liver can contain a collision model that addresses the liver collision with other things, a forcefield model that deals with deformation, and a visual model that deals with how the liver is rendered.
        - The mapping component is used to link all of the models
- SOFA script could have many unexpected errors, here are a few errors I have encountered.
    - if the mesh is fine enough, a collision between objects may not be detected event when two objects have intersected each other.
    - Poisson's ratio of an object should never be set at 0.5 or above. It will trigger division by zero and break the scene.
    - when multiple components are using the same mesh (i.e. collision node and visual node), identity mapping should be used.

# helpful resources

- examples from the sofapython3 plugin and XML examples that came with SOFA are helpful reference guides.
- [sofapython3](https://sofapython3.readthedocs.io/en/latest/menu/SofaPlugin.html)
- [SOFA documentation](https://www.sofa-framework.org/community/doc/)
- [SOFA API documentation](https://www.sofa-framework.org/api/master/sofa/html/index.html) (look up components and see what parameters they take)
- [SOFA Forum](https://github.com/sofa-framework/sofa/discussions)

# Obtain Mesh

- gmsh
    - volumetric mesh can be obtained from [gmsh](https://gmsh.info/).
