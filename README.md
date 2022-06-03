# Making Intelligent Traffic

## Overview
Making Intelligent Traffic is a project that we developed at EPFL for the course "Making Intelligent Things" (CS-358) taught by Professor Christoph Koch. 

Since this was the first year this course has been running, it was open exclusively to 2nd and 3rd year students in the IC bachelor's section. Thus, our team consists of 5 EPFL BSc Computer Science students: Alexander Müller, Anirudhh Ramesh, Damian Kopp, Louis Domart, Luca Engel.

In order to read about what our project proposed, we suggest you read our project proposal here: **INSERT PROJECT PROPOSAL LINK**. 

Please note that due to time contraints and unforeseen challenges, there have been deviations from what we set out in this proposal. The main difference being that, in the end we have implemented a traffic simulation using multiple bluetooth-controlled hardware cars which, when clicking on a cell on our GUI, will create a "passenger" and designate a car (using the algorithm we have described further below) to include it to their planned trajectory in order to "pick-up" this passenger.

**INSERT PHOTOS AND YOUTUBE VIDEO DEMOS HERE**

## Quick start guide for Traffic simulation project
This is a quick rundown on how to get a version of our project launched and running yourself. It includes useful learning resources and examples as well as instructions to launch the codebase.

## Table of contents
- 3D design
  - Sketches
  - Bricklayer studio
  - Fusion 360
  - 3D Printing with Prusa
- Building the cars
  - Connecting the components
    - Soldering work
    - Wiring
  - Arduino
    - Communicate over bluetooth
    - Brush motor
    - Servo connection
- Software
  - Libraries
    - Bluetooth
    - AprilTags
    - OpenCV
  - Launching the codebase
    - Overview **DIAGRAM**
    - Launching different demos
  
## 3D Design
The first step in the project was designing the cars. To make a suitable car for our project, it took us two attempts;

On the first attempt we had a car with all the necessary components, but ended up with a turning radius to large for us to run in our camera's view. 

Hence, we had to redesign the cars from scratch with a focus on minimizing the wheelbase length (the distance between front wheel axle and back wheel axle) which in turn (no pun intended) will reduce the turning radius (so cars will have much tighter turns). 
We also took this opportunity to also use a differential in the second design, since it would prevent wheel slip (and make for more stable driving & turns). If you would like to know more about what a differential is and how it works, check out [this great explanation](https://www.youtube.com/watch?v=yYAw79386WI).

### Sketches
Designing a great, robust car is no easy task; you must place your components in an optimal way and ensure your parts are designed such that they can be 3D printed with minimal supports.

The best advice to begin with is to start with simple sketches. This will enable you to work much faster and visualise a design quickly and see what further ways you can improve the design. Don't hesitate to spend multiple days on this, and also speak to others to get new ideas.

For a better feel, you can also try working with lego and your arduino components to see how things could fit together.

Below are a few ideas/sketches that we had while designing our car and trying to minimize the wheel base:

**INSERT NOTES SKETCHES**

**EXPLAIN HERE HOW YOU TRIED TO SHORTEN THE WHEELBASE**

### Bricklayer studio
Once you have a clear final sketch of how you want to design your car, you can start with the implementations.

For us, since we would be using some lego components in our car (the gears, the differential, the lego axles and holes, the wheels) we first need to create a 3D model that we could then import into our Fusion 360 design. We have chosen to use these Lego components since they are much more durable than 3D printed PLA/PETG and hence will make our car more robust.

In order to create the 3D lego models, we use [Studio 2.0 from bricklink](https://www.bricklink.com/v3/studio/download.page). Their software is incredibly easy to use, we didn't have to follow any tutorials. We recommend just trying to drag in some lego parts and move them around and build something to learn quickly.

Once you have made your design, you can then export it to use in Fusion 360. Unfortunately, we were unable to directly export it into Fusion 360, we must instead:
- Within Studio 2.0, File>Export As> "Collada" (.dae)
- Use an online converter to convert the .dae into a .stl file type (we used [this](https://imagetostl.com/convert/file/dae/to/stl))
- Then import it into Fusion360. You'll notice it will be incredibly big and in the wrong orientation, to get the correct dimensions you will need to:
  - "Edit in place" your design, then scale down your lego model to a factor of exactly 0.04
  - Rotate the lego car model as needed

### Fusion 360
Unlike Studio, Fusion 360 has a very steep learning curve and getting started will be tough (and even with experience it is a very time-consuming process). This is why we really emphasise the importance of sketching out and planning your designs on paper first, you will save days if not weeks!

The best way to get started with Fusion 360 is to follow online tutorials, since there are many great tutorials. On top of the lectures that our professor made for us, here are some useful channels:
- Absolute beginning: https://www.youtube.com/watch?v=A5bc9c3S12g&ab_channel=LarsChristensen
- Tips to design faster and better: https://www.youtube.com/c/TylerBeckofTECHESPRESSO

There are many more resources so simply search up on Google or YouTube for these.


