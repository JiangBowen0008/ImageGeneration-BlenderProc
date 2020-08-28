# ImageGeneration BlenderProc
 Generating realistic RGBD images of objects (designed for YUMI platform)
 
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
The command generates 10 images with randomly chosen amount (1-15) of objects.

To change the range of the number of spawned objects, change the range inside **generateImages.sh**.
