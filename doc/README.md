# README

## Installation

- Download the 8 VMs (the 8 .ova files)
- Import them in VirtualBox by double-clicking on the .ova file and then click on the import button
- Start the 8 VMs and wait one minute the time all components boot.

## Network

Our project has 3 different networks:

- internalNetwork: The internal Network shared by `Core_Server`, `CA_Server`, `Backup`, `MySQL_Server` and `Firewall`. 10.0.20.0/24
- DMZ: The network directly accessible from internet shared by `Webserver`, `VPN`, `Firewall` and `Client`. It is the network you have to connect to if you want to test our system from the point of view of an external attacker. 192.168.1.0/24
- internalDMZ: The network allowing the `Webserver` to speak to the `Core_Server`. It is shared by the `Firewall` and the `Core_Server`. 10.0.10.0/24

## VMs

| Name       | IPs                                          | Credential                                                   |
| ---------- | -------------------------------------------- | ------------------------------------------------------------ |
| Client     | 192.168.1.10                                 | ubuntu:ubuntu                                                |
| Web Server | 192.168.1.20                                 | ubuntu:GBciDw_fkMO<x3KQ@!<br />backup_user:C?NMuPu77c4sHfa3  |
| VPN        | 192.168.1.30                                 | ubuntu:IloveASL<br />backup_user: ?c_bEpuN-ssCJ4Y3           |
| Firewall   | 192.168.40,<br />10.0.10.40,<br />10.0.20.40 | ubuntu:0=?w-x_X(OC3X&iW5z<br />backup_user:rS^9cN?E?jxTj@4K  |
| Core       | 10.0.10.10,<br />10.0.20.10                  | ubuntu:YA&pd>I01>*h)6vjFT<br />backup_user:7zM2YCHky=SQ?e3n  |
| CA         | 10.0.20.20                                   | ubuntu:y9!x/En6pJ?uvFP(Q%<br />backup_user:WR=JdhtW4R_qV4b9  |
| MySQL      | 10.0.20.30                                   | ubuntu:l6C)XRhH!P9iuFvTVa<br />backup_user:4-c/hT?CsHTg$b&<Xt |
| Backup     | 10.0.20.50                                   | ubuntu:6-jR=)aDGavj-exU39                                    |

The backup_user is used by `Backup` to backup periodically the components and ubuntu is used for administration.

## REST

| Path                              | Response                      |
| --------------------------------- | ----------------------------- |
| https://webserver/                | Home page                     |
| https://webserver/revocation_list | Download .crl revocation list |

The admin certificate is already setup inside Firefox. All PKCS#12 files are protected by the password `asl`.

## Administration via SSH

If you want to administrate any system's components, you can use this command from the Client: `ssh ubuntu@{webserver, vpn, firewall, core, ca, mysql, backup}`. You will be logged in automatically as the user ubuntu. For the corresponding password, please refer to section `VMs`.