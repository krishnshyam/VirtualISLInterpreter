# Working with the actual animations on Unity

Note: To use the animations with expression, LipSyncPro is required to be installed, ass described in the *Assets* section below

The steps required to get started with the project on Unity:

* Animation file created in blender software as .fbx files are imported into Unity project .
* All the fbx files must be changed from genric (default) to humanoid in animation type This makes the animation on one model to be retargetted to different model
*To do that:
  * Upload/import the fbx file inside a folder in  project(tab)
  * Select the fbx file and go to the inspector(tab)
  * Select rig(tab) under inspector and change the animation type to humanoid  and select apply .
      
      ![alt text](img/1.jpg?raw=true "1")
  * Select animation(tab) under inspector and scroll down to find root transform rotation option.
      
      ![alt text](img/2.jpg?raw=true "2")
  * Select the check box for bake into pose for all 3 root transform options and 
  * Change the root motion node from <none> to <root transform> under motion as shown in the below picture 
      
      ![alt text](img/3.jpg?raw=true "3")
  * Now select the animation file in the project(tab) and left click the file and drag and drop the file inside animator(tab) and a new animation state will be create, Which will be used to play the animation which is controlled by the animator controller
      
      ![alt text](img/4.jpg?raw=true "4")
  * To create animator controller , right click inside the project(tab) -> create ->animator controller as shown in the picture below
      
      ![alt text](img/5.jpg?raw=true "5")


# assets 
1. Lipsync-pro
• Application uses Lipsync-pro (animation tool) to create facial expression data (Lipsync-pro data) thanks to this asset we are able to retarget facial expression between different model. 
• Application also uses Eye controller component which is an add-on included when you purchase Lipsync-pro , Eye controller component is used to blink eyes with predetermined intervals and duration of the blink animation.



https://assetstore.unity.com/packages/tools/animation/lipsync-pro-32117
