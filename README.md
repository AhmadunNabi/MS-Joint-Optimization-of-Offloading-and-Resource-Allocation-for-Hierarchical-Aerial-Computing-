# User Association Between Ground Users (GUs) and UAVs, and GUs' Offloading Decision
This repository contains a Matching Game Theory-based approach for user association between ground users (GUs) and unmanned aerial vehicles (UAVs), along with the binary offloading decision of GUs. It is part of my master's thesis, "Joint Optimization of Offloading and Resource Allocation for Hierarchical Aerial Computing Systems for IoT."

**The extended version of this work is currently under the trird-round revision in IEEE Transactions on Mobile Computing**. After publication, we will publicly share the pseudocode. For now, I am sharing the code for the Matching Game-based user association and the GUs' offloading decision.

* We have considered GUs which generates tasks randomly and make offloading decision as well as asociate with most preferred UAV using Matching game based algorithm
* Afther this UAV make partial offloading decision to HAP, then UAV and HAP allocate their computation resource using enhanced soft actor critic algorithm
* We have created one class for GU using file GU.py wehre GUs generate the tasks with task information and other related information
* We have created another class for UAV using file UAV.py where UAVs generate their corresponding information
* Then the main_GU_UAV_association.py file contains the code of User association and GUs offloading decision
* Another file plot.py - give us the figure of the system model

