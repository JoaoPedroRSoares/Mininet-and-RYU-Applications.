# Mininet-and-RYU-Applications (Firewall and Routing).

**Requirements**
**Mininet**: http://mininet.org/download/
**RYU controller**: https://github.com/osrg/ryu.git
**Python**: https://www.python.org/
**Two RYU applications**: Firewall and Routing(Together)

**These scripts create a simulated network environment with routers, switches, and a firewall to control traffic flows between hosts, with a RYU Controller.**

**Topologia.py**: This script defines a network topology using Mininet, a network emulator. It creates **four Linux-based routers** (r1, r2, r3, r4), **four Open vSwitch switches** (s1, s2, s3, s4), a**nd four hosts** (h1, h2, h3, h4). The script sets up IP forwarding, configures static routing to enable communication between different subnets, and includes an iptables rule **on h4 to block traffic from h1**.

**FirewallRYU.py**: This script implements a **software-defined network (SDN)** firewall using the **Ryu controller**. It blocks specific traffic flows between certain hosts based on predefined rules. The firewall operates on **OpenFlow 1.3**, handling switch feature configurations and dynamically adding flow rules to either block or allow traffic. The default rule permits all other communication.

