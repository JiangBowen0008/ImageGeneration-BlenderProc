# ImageGeneration BlenderProc
 Generating realistic RGBD images of objects (designed for YUMI platform) using [BlenderProc](https://github.com/DLR-RM/BlenderProc). The code is modified based on [bop_object_physics_positioning](https://github.com/DLR-RM/BlenderProc/tree/master/examples/bop_object_physics_positioning). 
 
 ![demo](/doc/demo.png)
 
## Git Pull

pull with

```
git clone --recursive https://github.com/JiangBowen0008/ImageGeneration-BlenderProc.git
```



## Get Started


### 1. Install Prerequisite for bop_toolkit

Notice: For detailed instructions, check

https://github.com/thodan/bop_toolkit

```
pip3 install pyyaml
pip3 install cython
pip3 install -r bop_toolkit/requirements.txt
sudo apt-get install freetype
sudo apt-get install libglfw3
```

Install any missing dependency if prompted.

### 3. Run Image Generation

```
cd BlenderProc && ./generateImages.sh 10
```
The command generates 10 images with randomly chosen amount (1-15) of objects. Replace 10 with custom numbers.

To change the range of the number of spawned objects, modify **generateImages.sh**.

## Customization

### Camera Position
Camera position is set inside **BlenderProc/ImageGenConfig/camera_positions**

### Object Models
Currently the project is using the LM-O (Linemod-Occluded) dataset (can be found on [BOP dataset](https://bop.felk.cvut.cz/datasets/)). To change the dataset, simply replace **lmo** inside **generateImages.sh** with the name of the replacement dataset.
