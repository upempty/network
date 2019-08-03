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
