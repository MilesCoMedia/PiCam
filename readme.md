# ANNOUNCMENT!
### We need YOUR help, to continue developing PiCam and PiCam Connect, we have to get Apple Developer Program Certification to be able to push PiCam Connect to the App Store! This costs $99USD and our budget has been spent developing PiCam to the level it is at today. 
## Just a small donation ($2USD) is enough to help us reach our goal. [Donate Here](https://square.link/u/odWVVRI8)


# PiCam and PiCam Connect

![Alt text](https://github.com/Tys0nat0r01/PiCam/blob/main/CONNECT.png)

PiCam is an affordable dashcam system that can be run on any Raspberry Pi 
and Raspberry Pi compatible camera and can be easliy integrated into any vehicle. 

## **Introduction**

PiCam is a fully open-source and budget-friendly dashcam system designed for seamless integration into any vehicle.  Unlike proprietary dashcam solutions, PiCam leverages the power and flexibility of the Raspberry Pi, making it an accessible and customizable option for drivers seeking reliable video recording and potentially other advanced features.  Because it's open source, users have complete control over the software and hardware, allowing them to tailor the system to their specific needs and contribute to its ongoing development.  The affordability of PiCam stems from its use of readily available components and the absence of licensing fees typically associated with commercial dashcam products.  This combination of open-source nature, affordability, and ease of integration makes PiCam an attractive alternative for those looking for a versatile and cost-effective dashcam solution.

 >### Note ###
> The "PiCam Connect iOS app and Hardware" is still under development. So, if you find any bugs or have any suggestion, feel free to post an issue or a pull request. [Post An Issue](https://github.com/Tys0nat0r01/PiCam/issues/new)


> 

## **Getting Started**

Firstly, PiCam requires a **Raspberry Pi Zero**, A **Camera Module that supports PiCamera**, and a Minimum of **64GB Micro SD Card** as hardware.
PiCam will also need to have its **Micro SD Card** Flashed with the latest version of **Raspberry Pi OS Lite (Bullsye)**. You can use Raspberry Pi Imager for this: [Raspberry Pi Imager](https://www.raspberrypi.com/software/).

### Step 1
## 1A
Install Raspberry Pi OS Lite (Bullsye) Edition onto an Micro SD Card using Raspberry Pi Imager, [Windows Download](https://downloads.raspberrypi.org/imager/imager_latest.exe) [MacOS Download](https://downloads.raspberrypi.org/imager/imager_latest.dmg)
![Image of installing PiOs lite onto sd card](https://github.com/Tys0nat0r01/PiCam/blob/main/Raspberry%20Pi%20Zero.png)
## 1B
> You may need to use a MicroSD card adapter to insert the SD Card into your Computer
Once you have installed Raspberry Pi OS Lite onto the SD Card, insert the MicroSD into the MicroSD card slot on a Raspberry Pi (Zero, Zero W, or 3A+ or newer). 


```bash



# Navigate to the project directory
cd my-awesome-project

# Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
