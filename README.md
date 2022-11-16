# Simple TCP Echo Program

Development of a simple chat program using threaded TCP echo server and client 

### Table of Contents

0. [Required Techniques](#required-techniques)
1. [About the Program](#about-the-program)
2. [Implementation Decisions](#implementation-decisions)

### Required Technologies

> 1. **Mininet** </br>
> Mininet is an emulator of a network. It is used to instantly create a virtual network for us to visualize the infrastructure of the network as well as its connections and transmissions.

> 2. **Virtual Machine** </br>
> Mininet requires to be run on a VM. In the project, VirtualBox was used for creating, managing and using VMs.

### About the Program

This program uses the Transmission Control Protocol, as the underlying protocol to connect servers and clients. I will be developing two python files, one for the server, and another for the clients. The goal is to be able to successfully create threaded connections, which creates threads for every connection between a client and a server for managing multiple connections simultaneously. When one client sends a bundle of TCP packet containing a message, the server should send it to all other clients. Both program files will be developed in the VM which runs mininet. 


### Implementation Decisions

