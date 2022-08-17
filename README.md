# Distributed_Mutex
Program to implement the Ricart-Agrawala algorithm for distributed mutual exclusion in python

## System Requirements:
### 1. Operating System: Windows 10 or later
### 2. Python should be installed in your PC
  #### a. Open Command Prompt > Type Python, Hit Enter If Python Is Installed it will show the version Details
  #### b. Python 2 or Python 3 should be installed.
  #### c. ‘threading’ and ‘sys’ packages should be part of your python installation. Generally, it comes by default.
  
  
## Instructions to execute the code:
### 1. Download the contents to a local folder.
### 2. To start the execution, you have have 2 options:
#### a. Rename “RA_run.txt” to “RA_run.bat” and Execute the file named as “RA_run.bat” by double clicking on it.
#### b. Or execute the command “python RA_algo.py” in a Command Prompt at the location where these files are stored.
#### 3. Then you will be asked to enter the number of sites which need to be simulated.

<p>You can enter 0, if you would like to simulate with default values in code. Then, and simulation will start printing
the logs from each site, please jump to step 6.
For each site a separate thread will be created. Minimum of 2 sites will be used in code. </p>

#### 4. Then you will be asked to enter the number of events in each site.
To make the data entry easy, it is assumed that the number of events are same in each site. So it is recommended
to enter the number of events as the maximum events in one site.
#### 5. Then you will be asked to enter the critical events in each site, one be one
#### 6. Once the data entry is completed, the simulation parameters are printed and output starts printing the logs from all sites.
