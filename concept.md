## 1 MTU in switch  
[MTU in L2 and L3(IP)] (https://ccieblog.co.uk/uncategorized/mtu-values-and-ping-on-cisco-products)

## 2 SOCK_RAW
```python
sockfd = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)--ip packet---AF_INET

sockfd = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))--ethernet packet
#define ETH_P_ALL       0x0003          /* Every packet (be careful!!!) */
#define ETH_P_IP        0x0800          /* Internet Protocol packet     */
```
## 3 comm
```
FullMsg, MsgPayload---pack/unpack
Msghandler emit/recv via conn. Connection via dedicated one type connector e.g tcp channel.
TaskSchedule
```

## 4 socket / file descripter
```
socket associated local IP@ and port
file descripter associated 5 elements : source IP@/source port/des IP@/dest port/protocol
```
## 5 data transfer
```
PC_A-->dest IP@-->PC_B:
==
PC_A->dest IP@--->ARP--->switch--->Router: return mac@ of router, then data transfer to Router;
check the dest IP@, Router--->switch....->PC_B.
==
==
Action: if no dest mac@ in ARP table, ARP broadcast.
          if target PC_B responsed, then get mac@, construct ip layer/ethernet layer to send.
          if router(default gw) find dest mac@ is in another network, response with route mac@, 
                            then get mac@, contruct ip/ethernet layer to send to router.
             router will continue check go to Action.
```
## broadcast vs flooding
```
A switch never broadcasts frames;
A switch can only flood a frame
ARP is example for barodcast for finding IP@'s mac
Flooding is for that unknown destination mac comes into switch:
  Since it doesn't know where the destination MAC address is, it floods the frame out all ports.
   simply duplicate the frame and send it out all ports
```
