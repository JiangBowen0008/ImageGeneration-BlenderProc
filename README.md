# ImageGeneration BlenderProc
 Generating realistic RGBD images of objects (designed for YUMI platform) using [BlenderProc](https://github.com/DLR-RM/BlenderProc). The code is modified based on [bop_object_physics_positioning](https://github.com/DLR-RM/BlenderProc/tree/master/examples/bop_object_physics_positioning). 
 
 ![demo](/doc/demo.png)
 
## Git Pull

pull with

```
git clone --recursive https://github.com/JiangBowen0008/ImageGeneration-BlenderProc.git
```



## Get Started


### 1. Prerequisite

Notice: For detailed instructions, check

https://github.com/thodan/bop_toolkit

```
pip3 install pyyaml
pip3 install cython
pip3 install -r bop_toolkit/requirements.txt
sudo apt install freetype
sudo apt install libglfw3
```
**Note: If freetype cannot be installed, try install it with the following command:**
```
sudo apt update && sudo apt install freetype2-demos
```

Install any other missing dependency if prompted.


### 2. Run Image Generation

```
cd BlenderProc && sh ./generateImages.sh 1
```
The command generates 1 image with randomly chosen amount (1-15) of objects. Replace 1 with custom numbers of images to generate.

To change the range of the number of spawned objects, modify **generateImages.sh**.

## Customization

### Camera Position
Camera position is set inside **BlenderProc/ImageGenConfig/camera_positions**.

### Object Models
Currently the project is using the LM-O (Linemod-Occluded) dataset (can be found on [BOP dataset](https://bop.felk.cvut.cz/datasets/)). To change the dataset, simply replace **lmo** inside **generateImages.sh** with the name of the dataset to replace.

### Scene
The scene used by default is the **scene.blend** file located inside **BlenderProc/ImageGenConfig**. To customzie your own scene, replace it with your own blender file.

**Notice: Concave objects need to be properly segmented before used. Physics simulations will be miscalculated otherwise.**
