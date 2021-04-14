import time
import MPPT_Classes
import TCPClient
TRUE = 1
FALSE = 0

if __name__ == '__main__':
    print("main")
    #Initialize GPIO and Pi
    initialize = MPPT_Classes.Initialize()
    #Create Algorithm Class and run Algorithm
    algorithm = MPPT_Classes.Algorithm()
    algorithm.RunAlgorithm(TRUE)
    #Create Algorithm Class and run Algorithm
    EmergencyShutdown = MPPT_Classes.EmergencyShutdown()
    EmergencyShutdown.EShutDown(TRUE)
    
    #Run TCP Server
    server = TCPServer.TCPServer()
    #If server already running, run Pi as client
    if(server.alreadyrunning == 1):
        client = TCPClient.TCPClient()