# ImageGeneration BlenderProc
 Generating realistic RGBD images of objects (designed for YUMI platform)
 
## Git Pull

pull with

```
git clone --recursive https://github.com/JiangBowen0008/ImageGeneration-BlenderProc.git
```

## Get Started

### 1. Follow BlenderProc Setup

https://github.com/DLR-RM/BlenderProc

### 2. Install Prerequisite for bop_toolkit

For detailed instructions, check

https://github.com/thodan/bop_toolkit

```
pip3 install -r bop_toolkit/requirements.txt
apt-get install freetype
apt-get install libglfw3
```

### 3. Run Image Generation

```
cd BlenderProc && ./generateImages.sh
```

