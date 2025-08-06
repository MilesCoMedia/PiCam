<p align="center">
  <img width="150" src="https://github.com/MilesCoMedia/PiCam/blob/7dc0de8d4f252ec6a511e90d2810d0ff1cf49be2/GITSmall/PiCam%20Connect%20APPICON-iOS-Dark-1024x1024%402x.png" alt="PiCamConnect Logo">
</p> 

<h1 align="center">PiCam + PiCam Connect</h1>

> 

<div align="center">
  <a href="https://www.buymeacoffee.com/tysonm" target="_blank">
    <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;">
  </a>
  <a href="https://github.com/MilesCoMedia/PiCam/wiki" target="_blank">
    <img src="https://github.com/MilesCoMedia/PiCam/blob/fbe640fc1a126e3e2510d982d8a982fefeb84d3e/View-6.png" alt="PiCam Wiki Link" style="height: 60px !important;width: 217px !important;">
  </a>
</div>

## **Introduction**

PiCam is a fully open-source and budget-friendly dashcam system designed for seamless integration into any vehicle.  Unlike proprietary dashcam solutions, PiCam leverages the power and flexibility of the Raspberry Pi, making it an accessible and customizable option for drivers seeking reliable video recording and potentially other advanced features.  Because it's open source, users have complete control over the software and hardware, allowing them to tailor the system to their specific needs and contribute to its ongoing development.  The affordability of PiCam stems from its use of readily available components and the absence of licensing fees typically associated with commercial dashcam products.  This combination of open-source nature, affordability, and ease of integration makes PiCam an attractive alternative for those looking for a versatile and cost-effective dashcam solution.

 >### Note ###
> The "PiCam Connect iOS app and Hardware" is still under development. So, if you find any bugs or have any suggestion, feel free to post an issue or a pull request. [Post An Issue](https://github.com/MilesComedia/PiCam/issues/new)


> 

## **Getting Started**

Firstly, PiCam requires a **Raspberry Pi Zero**, A **Camera Module that supports PiCamera**, and a Minimum of **64GB Micro SD Card** as hardware.
PiCam will also need to have its **Micro SD Card** Flashed with the latest version of **Raspberry Pi OS Lite (Bullsye)**. You can use Raspberry Pi Imager for this: [Raspberry Pi Imager](https://www.raspberrypi.com/software/).

### Step 1
**1A**
Install Raspberry Pi OS Lite (Bullsye) Edition onto an Micro SD Card using Raspberry Pi Imager. [Windows Download](https://downloads.raspberrypi.org/imager/imager_latest.exe) [MacOS Download](https://downloads.raspberrypi.org/imager/imager_latest.dmg)
1. Click 'Choose OS' and find select 'Raspberry Pi OS (Other)'.
2. Find and select 'Raspberry Pi OS Lite (32 BIT)' or 'Raspberry Pi OS Lite (64 BIT)'
3. Insert your SD Card and select 'Choose Storage' then select your MicroSD Card.
4. Click 'NEXT' and an Options Menu will show, set the 'Hostname' to 'PiCam', and set both the 'Username' and 'Password' to 'picam' (all lowercase)
5. Then configure your Wi-Fi Network's SSID and Password.
6. Then click 'SAVE' and click 'Write'. The Imager will begin to write the OS to the Micro SD card.
> [!WARNING]
> **DO NOT UNPLUG THE SD CARD OR CLOSE THE IMAGER UNTIL IT INDICATES THE WRITE IS COMPLETE, Doing so could corrupt the SD Card.**

> [!NOTE]
> You may need to use a MicroSD card adapter to insert the SD Card into your Computer.

> [!IMPORTANT]
> Your Micro SD Card may display as 'Generic Media Device (CAPACITY e.g 64GB)'. To ensure you are selecting the right storage device, compare the storage capacity on the SD Card to what is displayed.

**1B**
> You may need to use a MicroSD card adapter to insert the SD Card into your Computer
Once you have installed Raspberry Pi OS Lite onto the SD Card, insert the MicroSD into the MicroSD card slot on a Raspberry Pi (Zero, Zero W, or 3A+ or newer) and attach a compatible Raspberry Pi Camera [List of Compatible Cameras](enter link).
Then plug in a Micro USB cable to the Raspberry Pi's **POWER or PWR** Port, then power it on.

### Step 2

**2A**
Ensure your Raspberry Pi booted correctly plug a HDMI cable into your Raspberry Pi, if the Raspberry Pi displays 
> You may need to use a Mini HDMI to HDMI adapter 
**Install required Packages and Dependencies*

Firs
```bash

```
```bash



# Navigate to the project directory
cd my-awesome-project

# Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

