# ImageGeneration BlenderProc
 Generating realistic RGBD images of objects (designed for YUMI platform) using [BlenderProc](https://github.com/DLR-RM/BlenderProc). The code is modified based on [bop_object_physics_positioning](https://github.com/DLR-RM/BlenderProc/tree/master/examples/bop_object_physics_positioning). 
 
 ![demo](/doc/demo.png)

## Supported Platforms
- Linux 16.04 (Tested)
- Linux 18.04 (Tested)
- Linux 20.04 (Tested)
- Mac (Not Tested)
- Windows (Not supported because BlenderProc is currently not supported on Windows. However, BOP toolkit supports direct rendering using its own renderers.)

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
pip install pyyaml
pip install cython
pip install -r bop_toolkit/requirements.txt
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

### Object Scale
By default all objects are scaled by 0.5. To use custom scale, change the value at [the corresponding value at the config.yaml file](https://github.com/JiangBowen0008/BlenderProc/blob/c87a6662e21bab60cd3f55b1f5adcf0516ce8e6b/ImageGenConfig/config.yaml#L73) together with the one at [config.py file](https://github.com/JiangBowen0008/bop_toolkit/blob/7eb6c12974ba31cd6f6a3ad2932e9205b45172d5/scripts/bop_toolkit_lib/config.py#L21).



### Scene
The scene used by default is the **scene.blend** file located inside **BlenderProc/ImageGenConfig**. To customzie your own scene, replace it with your own blender file.

**Notice: Concave objects need to be properly segmented before used. Physics simulations will be miscalculated otherwise.**
