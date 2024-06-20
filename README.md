# Bypass RPCBind  

## Overview

This project provides a solution for bypassing a filtered port 111 (portmapper/rpcbind) on a remote server. By creating a local portmap dump and setting up a proxy, you can connect to the RPC services offered by the remote server, even when the portmapper service is inaccessible. This README file provides detailed information on why and when this project is used, usage cases, functionality, and instructions on how to use it.

## Why Use This Project?

In scenarios where the portmapper (rpcbind) service on port 111 is filtered or blocked, clients cannot query the RPC service mappings. However, other RPC services (like NFS, status, nlockmgr, mountd) might still be accessible. This project allows you to bypass the filtered portmapper by using a local proxy that forwards RPC requests to the appropriate ports on the remote server, based on a manually created portmap dump.

## Usage Cases

- **Penetration Testing:** During security assessments, you may encounter RPC services with a filtered portmapper. This tool helps you access those services.
- **Network Troubleshooting:** When diagnosing network issues, being able to bypass a filtered port 111 can be crucial for accessing and testing RPC services.
- **Research and Development:** For developers working with RPC services, this tool provides a method to test and interact with services without needing direct access to portmapper.

## Features

- **Local Portmap Dump:** Create a local file containing RPC service mappings.
- **Proxy Requests:** Forward RPC requests to the remote server using the information from the local portmap dump.
- **Customizable:** Easily modify the portmap dump and proxy configuration to fit different environments.

## How to Use

### Prerequisites

- Python 3.x
- Basic knowledge of networking and RPC services

### Setup

1. **Clone the Repository:**
   ```sh
     git clone https://github.com/yourusername/rpcdump.git
     cd rpcdump
   ```
2.**Create a file named portmap.dump with the following content (modify as needed):**
 ```sh
    100000  2    tcp  111  portmapper
    100005  1    udp  32769  mountd
    100005  1    tcp  32770  mountd
    100003  2    udp   2049  nfs
    100003  3    udp   2049  nfs
    100003  4    tcp   2049  nfs
   ```
  3.**Run the Proxy Script:**
  ```sh
     python3 rpcdump.py

   ```
