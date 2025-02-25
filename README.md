# Mininet-and-RYU-Applications (Firewall and Routing).

**Requirements**

  **--Mininet**: http://mininet.org/download/

  **--RYU controller**: https://github.com/osrg/ryu.git

  **--Python**: https://www.python.org/

  **--Two RYU applications**: Firewall and Routing(Together)

**You can see Topology used in Topo.png**

**It is expected** to develop a system that will allow the SDN network more efficient control and allowing greater flexibility using the 2 planned implementations.

**Firewall**: Effective blocking of unwanted packets, increasing security.

**Routing**: Forwarding packets using IPv4 and having routing and path redundancy.

**These scripts create a simulated network environment with routers, switches, and a firewall to control traffic flows between hosts, with a RYU Controller.**

**Topologia.py**: This script defines a network topology using Mininet, a network emulator. It creates **four Linux-based routers** (r1, r2, r3, r4), **four Open vSwitch switches** (s1, s2, s3, s4), a**nd four hosts** (h1, h2, h3, h4). The script sets up IP forwarding, configures static routing to enable communication between different subnets, and includes an iptables rule **on h4 to block traffic from h1**.

**FirewallRYU.py**: This script implements a **software-defined network (SDN)** firewall using the **Ryu controller**. It blocks specific traffic flows between certain hosts based on predefined rules. The firewall operates on **OpenFlow 1.3**, handling switch feature configurations and dynamically adding flow rules to either block or allow traffic. The default rule permits all other communication.


**CONCLUSION:**

								--In this work, Mininet practice was carried out together with the RYU controller to simulate a network composed of routers and an SDN firewall. The objective was to demonstrate how routing and network security can be dynamically managed in a virtualized environment. 

Routing was implemented so that communication between different subnets was guaranteed using the configured routers. The firewall, on the other hand, acted as a filter, blocking unwanted packets based on defined rules, preventing specific communications between hosts.

The work shows how the use of SDN (Software-Defined Networking) allows centralized and programmable control of the network infrastructure. The integration of Mininet with RYU made it possible to create a simulated network for routing and security tests without the need for physical hardware, being an efficient solution for studies, development and experimentation in software-defined networks.

