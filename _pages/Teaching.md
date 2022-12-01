---
title: "Teaching"
permalink: /Teaching/
header:

---

<!-- # **Optimization-based trajectory planning for legged robots**

#### **IIT/Dibris, University of Genova, 2021 (Genova, Italy)**

This course will introduce modern methods for robotics movement generation based on numerical optimal control. An introduction to approximated models is also given (Linear Inverted Pendulum and Centroidal Dynamics). It will also contain hands-on exercises for real robotic applications such as walking on flat terrain. The student will be able to generate a locomotion trajectory for the robot via optimization and track it with the controller implemented in the previous course  of “Control of legged robots”.

# **Introduction To Robotics**

#### **Industrial Engineering Department,  2021, University of Trento (Trento, Italy)**

﻿The course offers a bird-eye view on the most important topics related to modern robotics, highlighting the main problems that need to be faced in order to make the robots operate correctly in the environment. Specifically, the course will cover the following topics: taxonomy of the different types of robots, physical modelling of robots (direct and inverse kinematics and dynamics), simulation of models, sensing and actuation solutions for perception and action. Using the developed models, the most famous methodologies to control robot motion and interaction, will be presented. These methods will be first studied in theory, and then implemented in simulation (with the Python language) to gain practical experience. Attention will be also paid to illustrate the most common non idealities and issues that are present when controlling robots. The course will adopt a combination of simulation models and lab experiences to consolidate the knowledge transmitted during the theoretical lessons. After completing the course, students will be able to:

\- select the most suitable sensors and actuators for a given robotic application

\- model the kinematics and dynamics any kind of robot

\- understand the working principles of several control algorithms for robotic systems

\- choose the appropriate approach(es) to control a specific system for a given target application

\- implement, tune, and test control algorithms with the Python language

### Prerequisites

This course will assume an intuitive grasp of concepts from linear algebra, a good understanding of linear ordinary differential equations, and a moderate level of mathematical maturity in linear systems. If the student is unsure to meet this criteria, below are a few representative prerequisite topics that we will draw upon:

- Mechanics: basic Newtonian dynamics in 3D, work, kinetic potential energy
- Electrics: voltage, current, ohms law.
- Linear algebra: eigenvalues, eigenvectors, rank, null space, positive definite matrices
- Multivariable differential calculus: gradient, Jacobian, Taylor series, chain rule
- Linear dynamical systems: linear systems, state space, transfer function, poles/zeros.
- Programming: object-oriented programming (if-else, for loops, classes, objects, inheritance)

[Here](https://www.dropbox.com/sh/6mrnlze5vo8cyb1/AABbNjY4bkSgKmivA-t3LOgaa?dl=0) you can find videos and [here](https://www.dropbox.com/sh/if2lq3s6c0zayxl/AADr7SYiQU1Zn96tLKv7NnXwa?dl=0) slides of all the lectures of the first academic  year (20 /21)

You can also find [here](https://www.dropbox.com/sh/5trh0s5y1xzdjds/AACchznJb7606MbQKb6-fUiUa) a virtual machine (password:  student) containing the Python software needed for the lab sessions (for the Matlab lab code send me an email).

### **Syllabus**



#### **Introduction**

**- Introduction to robotics**: What is a robot? Robots History. Robot classification. Evolution toward Industrial robots. Other kind of robots: service robots, exoskeletons. Under-actuated robots: underwater robots, space robots, drones, legged robots, humanoids, quadrupeds.

\- **Robot’s functional units:** Mechanical Structure: joints, links, end-effector, workspace, robot classification based on joint arrangement. Overview of functional units of a robot: sensors, actuators, etc. Overview of the main robotics topics: control, perception, estimation, planning.



#### **Sensors**

**- Introduction to measurement:** properties of a measurement system (accuracy, repeatability, uncertainty), sensors characteristics (sensitivity, range, resolution, dynamic response), type of measurements errors (systematic, random). Non idealities in sensors: non-linearity, offset, scaling, dead-band, hysteresis.

**- Proprioceptive sensors:** Types of (propio-ceptive) sensors. Position sensors (potentiometers, relative/absolute encoders) quantization noise, contact switches, LDR, inertial sensors (accelerometers, gyros).

**- Exteroceptive sensors:** Types of extero-ceptive sensors. Force sensors (strain gauges, reading/mounting of strain gauges, wheatstone bridge, F/T 6 axis force sensors). Vision sensors. Passive cameras, stereo camera, triangulation in stereo-vision. Camera modeling (pinhole model), camera calibration. Active sensors: LiDAR, Structured light sensors, basic image processing, visual odometry, state estimation, point cloud. Proxy-sensors.

**- Signal processing:** Analog/discrete signals. Sampling, quantization and reconstruction (A/D, D/A converters). Problems in digital implementation: quantization errors, delays, aliasing (Nyquist theorem). Low-pass filter (discrete implementation). Basic signal processing: average, moving average, weighted average.



#### **Actuators**

**- Typer of actuators:** types of actuators in robotics:  pneumatic, hydraulic actuators, EHAs, electric motors, Series elastic actuators.

**- Electrical actuators:** Review of some useful notions of physics. Synchronous/ Asynchronous AC Motor, brushed/brushless DC Motor, efficiency, model of a DC motor steady state response. Motor control : voltage / current.

**- Transmissions**: types of transmissions, modeling transmission, gearbox,  Optimal choice of reduction ratio, modeling elasticity in transmission.

**- Non idealities:** Non idealities in actuators: modeling friction, back-lash, dead-band

**- Simulation of actuators:** Simulation of actuators: state space dynamics of a DC motor, discrete equivalent model, integration of dynamics, time responses.



#### **Control basics**

**- Introduction to control:** open loop control, feed-back concept, bang-bang controller, transient/steady-state response, static/dynamic control specifications, design of a controller.

**- PID:** P, PD, PID control, current control, anti-windup technique

**- Implementation of PID:**  realizability issue of PID, Digital PID, tuning techniques for PID.



#### **Kinematics:**

**- Kinematics of a rigid body** Position and orientation of a rigid body. Reference frames. Rotation matrices (properties, composition, and interpretations). Derivative of a rotation matrix. Minimal representations of orientation. Skew-symmetric matrices. Exponential maps and the Rodríguez formula. Euler angles. Relation between Euler rates and angular velocity. Unit quaternions.

\- **Manipulator direct kinematics:** Definition of forward and inverse kinematics. Joint, task and actuation spaces. Generalized coordinates. Forward kinematics of robot manipulators. Homogeneous transformations (properties, composition and interpretations). Inverse of a homogeneous transformation matrix. Frame placement. Direct kinematics of a kinematic chain.

**- Inverse Kinematics:** Definition of inverse kinematics. Solvability and workspace. Closed form (analytical) solutions. Examples.  

**- Direct Differential Kinematics:** Linear and angular velocity of a rigid body. Linear and velocity of a manipulator link driven from prismatic or revolute joints. Contribution of prismatic and revolute joints to end-effector velocity. The Geometric Jacobian. The Analytical Jacobian. Relationship between Geometric and Analytical Jacobian.

**- Numerical Inverse Kinematics:** Gauss-Newton iterative approach. Pathological cases . Line search. Discussion on multiple solutions.

**- Redundancy and Singularities:** Definition of redundancy. Redundant manipulators. Primer on linear algebra sub-spaces. Redundancy and vector null space. The pseudo-inverse. Geometric interpretation of inverse kinematics mapping. Singular values. Definition of singularity. Types of singularities. Inverse differential kinematics and singularities. Damped least-squares method. Higher order differential inversion. 



#### **Dynamics:**

**- Statics:** statics vs. dynamics. Principle of virtual works. Kineto-static duality and analysis of sub-spaces. Velocity and force transformations.

\- **Dynamic of a rigid body:** Kinetic energy of a rigid body. Examples of moments of inertia. Potential gravitational energy.  Euler-Lagrange method. Contribution of non consevative forces. Linearity of the model in the dynamic parameters. Analysis of inertial couplings, Coriolis and centrifugal effects. Recursive Newton-Euler method. Examples. 

**- Interaction dynamics:** Rigid and compliant contact models. Constrained robot dynamics. Simulation with a compliant contact model.

\- **Under-actuation:** Definition and examples of under-actuated robots. Modeling of floating base robots. Structure of the floating base dynamics. 



#### **Joint Space control** 

**-** **PID for manipulators:** Overview of control problems in robotics. The concept of stability. PD, PD + gravity compensation, PID control.

**- Inverse dynamics.** Decentralized vs. centralized control. Feedback linearization in robotics. Joint space Inverse dynamics (Computed torque).



#### **Task Space Control**

**- Cartesian space control:** inverse kinematics control, direct Cartesian space control. Cartesian PD, PD+ gravity compensation. Inverse dynamics in Cartesian space (non-redundant and redundant case). 

**- Orientation Control:** orientation control with different parametrization of orientation (rotation matrix, angle-axis, Euler angle, quaternions).

**- Interaction Control:** Applications. passive/ active methods. Direct force control. Cartesian space impedance control, concept of inertia shaping. Superimposition of impedances. Simplified formulations. Compliance control. Selection of impedance parameters. Torsional impedance. Admittance control. Visual servoing.

### **Lab sessions**

**- Lab Python: i**ntroductory lecture to python programming and to the usage of the *numpy* library

**- Lab Control:** simulation and control of a DC motor, PID design and tuning (Matlab).

**-** **Lab** **Kinematics/Dynamics:** learn to build a robot model using the Unified Robot Description Format (URDF), compute the direct/inverse kinematics of a 4-DoF serial manipulator. Design a reference trajectory with polynomials. Implement the numerical inverse kinematics.  Compute and analyze the forward/inverse dynamics of a 4-DoF serial manipulator using the Recursive Newton-Euler Algorithm (RNEA). 

**- Lab Joint Space Control:** design motion controllers (of increasing complexity) in the joint space for a manipulator in free-motion. Implement a centralized approach (i.e. inverse dynamics). Implement the interaction with the environment with a compliant contact model.

**-** **Lab** **Task Space Control:** design a motion controllers (of increasing complexity) in the task space for a manipulator in free-motion. Implement a centralized approach (i.e. inverse dynamics). Implement the control of the orientation using the angle-axis representation.



# Course on Control of Legged Robots

#### **IIT/Dibris, University of Genova, 2020 (Genova, Italy)**

The course is meant to provide to post-graduate students a broad overview on the most common control strategies for fixed-based robots (position, force, impedance, admittance control and inverse dynamics).Modeling of actuators, gear-box, friction and contact models is also briefly discussed. Cartesian space control is presented as well as the extension to floating-base (e.g. legged) robots. The problem of ensuring locomotion stability for a legged robot is tackled both from a projection-based and an optimization-based perspective (Convex Quadratic Programming).  Python templates will be provided to the students to implement in practice what was presented in the theory. The goal of the course is to allow students to design controllers and  make them aware of pros and cons of the different state-of-the art approaches. 

### **Prerequisites:**

A basic knowledge on articulated body dynamics and kinematics is required such as can be obtained from a first course in dynamics at undergraduate level. A basic knowledge of linear systems and linear algebra is also required.

Interested people can find:

- the recordings of the Lectures  [here](https://www.youtube.com/playlist?list=PLpppns-JGSyKFwngvh-DYRBpH9NUdqH4J) 

- the pdf of the slides  [here](https://www.dropbox.com/sh/etxpgbsoxqgoyco/AAAXDiL7nLiHMLSftgZ4A1d5a ) 

- the framework used for the LAB sessions is Locosim: https://github.com/mfocchi/locosim 

  Note that the branch compatible with the video lectures is an old branch called   **controlOfLeggedRobots**  -->

