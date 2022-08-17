# Python program to illustrate the concept
# of Ricatta_Agarwala Distributed mutual exclusion
# importing the threading module
import threading
import sys


no_of_sites=3 #defualt value =3 ,should be atleast 2
requests = [] #requests buffer
replys = [] #replys buffer
SPACE = 10 #space alignment for printing output
keep_alive = []# marker to keep running other sites until every one finishes

#function to request critical section
def request_crit_section(sitenum,time_stamp):
    spacing =  (" " * ((sitenum-1)*SPACE))#space alignment for printing output
    for i in range(no_of_sites):
        if i != sitenum-1: #send requests all sites other than self
            requests[i].append((time_stamp,sitenum)) # format of request (event_timestamp, site_id)
            print(spacing+"site %s : requested CS to site %s with (ts,pi)= (%s,%s)\n"
                  %(sitenum,i+1,time_stamp,sitenum))
            
            
#function to send replys
def send_replys(sitenum,time_stamp,CS_status,Request_Deferred,LastReq):
    spacing =  (" " * ((sitenum-1)*SPACE)) #space alignment for printing output
    while requests[sitenum -1]: # for requests requests received by current site
        req = requests[sitenum -1].pop(0) # pop out the first entry since FIFO channel is assumed
        requester_timestamp = req[0]
        requester_site_id = req[1]
        time_stamp = max(time_stamp,requester_timestamp)# update own timestamp when a request is received
        
        if (((CS_status == 0) or (requester_timestamp < LastReq) 
                or ((requester_timestamp == LastReq) and (requester_site_id < sitenum)))
            and (CS_status != 2)):
        #sends a REPLY message to site Si if site Sj is neither requesting nor executing the CS
        #or if timestamp is smaller 
            
            replys[requester_site_id -1].append((time_stamp,sitenum))
            print(spacing+"site %s : replied to site %s with timestamp %s for request(%s,%s)->(%s,%s)\n"
                %(sitenum,requester_site_id,time_stamp,req[0],req[1],time_stamp,sitenum))
        else:
            #the reply is deferred and Sj sets RDj [i] = 1  
            print(spacing+"site %s : reply to site %s is deferred\n"
              %(sitenum,requester_site_id))
            Request_Deferred[requester_site_id-1]=1
    return time_stamp
  
#function to check for replys when waiting for critical section
def check_replys(sitenum,time_stamp):
    spacing =  (" " * ((sitenum-1)*SPACE))
    reply_count = 0
    for i in range(1,no_of_sites+1):
        for rep in replys[sitenum -1]:# for every reply received by the current site
            if rep[1] == i: #check if a reply is recived from ith site
                reply_count = reply_count+1 # if yes set flag and break
                    #print(spacing+"site %s : reply received from site %s -> (%s,%s)\n"
                        #%(sitenum,i,rep[0],rep[1]))  
                    #break
    #print(spacing+"site %s :reply_count : %s" %(sitenum,reply_count))
    
    if reply_count >= (no_of_sites-1):
        print(spacing+"site %s : event with (ts,pi)=(%s,%s)received all replys\n" %(sitenum,time_stamp,sitenum))
        replys[sitenum -1] = [] ## clean up once the reply is processed from all sites
    return reply_count >= (no_of_sites-1)

#function to send replys to requests which were deferred
def send_deffered_replys(sitenum,time_stamp,Request_Deferred):
    #When site Si exits the CS, it sends all the deferred REPLY messages: 
    
    spacing =  (" " * ((sitenum-1)*SPACE))
    print(spacing+"site %s : Request_Deferred : %s \n" %(sitenum,Request_Deferred))
    for j in range(len(Request_Deferred)):
        if Request_Deferred[j] == 1:
            replys[j].append((time_stamp,sitenum))
            Request_Deferred[j] == 0
            print(spacing+"site %s : replied to deferred req from site %s with timestamp %s ->(%s,%s)\n"
                %(sitenum,j+1,time_stamp,time_stamp,sitenum))
            
#function to represent one site.This can be run in multiple threads to simulate multiple sites        
def Site_process(sitenum, events, critical_events):
    """
    function which handles site process
    """
    Request_Deferred =[0] * no_of_sites
    spacing =  (" " * ((sitenum-1)*SPACE))
    print(spacing + "site %s started\n" %sitenum)
    time_stamp = 0
    LastReq = 65536 # Time stamp of last CS request is initialized with MAXINT
    
    for i in range(1,events+1):
        wait_for_CS = 0
        CS_in_progress =0
        time_stamp = time_stamp +1
        print(spacing+"site %s : event %s start with (ts,pi)=(%s,%s)\n" %(sitenum,i,time_stamp,sitenum))
        if i in critical_events:
            print(spacing+"site %s : event %s with (ts,pi)=(%s,%s)need CS entry\n" %(sitenum,i,time_stamp,sitenum))
            #call request critical section
            wait_for_CS = 1;
            request_crit_section(sitenum,time_stamp)
            LastReq = time_stamp
            while wait_for_CS == 1:
                if check_replys(sitenum,time_stamp):
                    wait_for_CS = 0
                    CS_in_progress = 1
                else:
                    time_stamp = send_replys(sitenum,time_stamp,wait_for_CS,Request_Deferred,LastReq)
        #run a loop of large number of iterations to simulate some processing.    
        for j in range(100000):
            time_stamp = send_replys(sitenum,time_stamp,CS_in_progress*2,Request_Deferred,LastReq) 
            
            if j==0:
                if CS_in_progress == 1:
                    print(spacing+"site %s : event %s ___critical section__ start\n" %(sitenum,i))
            if j == 99999:
                if CS_in_progress == 1:
                    print(spacing+"site %s : event %s ___critical section__ end\n" %(sitenum,i))
                    CS_in_progress =0
                    send_deffered_replys(sitenum,time_stamp,Request_Deferred)
                print(spacing+"site %s : event %s completed with (ts,pi)=(%s,%s)\n" %(sitenum,i,time_stamp,sitenum))
        
    
    keep_alive.pop() # mark completion of current site
    print(spacing+"site %s is waiting for other sites to finish\n" %sitenum)
	#send replys to other sites if anyone other site is alive
    while keep_alive:
        send_replys(sitenum,time_stamp,wait_for_CS,Request_Deferred,LastReq)
    print(spacing+"site %s is stopping...\n" %sitenum)   
  
if __name__ == "__main__":
    
	#Introducing a version check of python
    if sys.version_info[0] < 3:
        print("WARNING :: Old version of python(<3) found ")
	
	#initialization	
    site_threads = []
    CS_events = []
	
	#collect input parameters
    print("Enter 0 for working with default values")
    no_of_sites = int(input("Enter the number of sites :"))
    if no_of_sites == 0: #default values for simulation
        no_of_sites = 3
        no_of_events = 5
        for i in range (no_of_sites):
            CS_events.append([2])#mark event 2 as critical event
    else:
        no_of_sites = max(2,no_of_sites)
        no_of_events = max(2,int(input("Enter the number events in each site :")))
        for i in range(no_of_sites):
            CS_events.append([])#add a an empty request for every site
            print("Enter the index of critical events in site %s seperated by space"%(i+1))
            if sys.version_info[0] < 3:
                user_input = raw_input()
            else:
                user_input = input()
            for event in user_input.split():
                CS_events[i].append(int(event))

        
    #print simulation parameters
    print ("number of sites :%s"%(no_of_sites))
    print ("number events in each site :%s"%(no_of_events))
    print (" critical events in each site :")
    print (CS_events)
	#create a marker in keep_alive to signal each site
    keep_alive = [1] * no_of_sites
    # creating thread for each site
    for i in range (no_of_sites):
        
        requests.append([])#add a an empty request for every site
        replys.append([])#add a an empty reply for every site
        site_threads = site_threads + [threading.Thread(target=Site_process, args=(i+1,no_of_events,CS_events[i],))]
        
    #start thread for each site
    for sites in site_threads:
        sites.start()
        
    #wait till all sites are completed
    for sites in site_threads:
        sites.join()
  
    # All threads completely executed
    print("Done!")
