#### mbuf simple explanation 1



m_data pointing to packet/frames from ethernet (ethernet L2, IP L3, UDP/TCP L4, payload)

m_head pointer updating from layer to layer.



```c
struct mbuf;

/* Header present at the beginning of every mbuf */
struct m_hdr {
	struct mbuf *mh_next;
	uint8_t     *mh_head;
	uint8_t     *mh_tail;
};

struct mbuf {
	struct m_hdr m_hdr;
	uint8_t      m_data[MLEN];
};

#define m_next m_hdr.mh_next
#define m_head m_hdr.mh_head
#define m_tail m_hdr.mh_tail

#define MB_IP_ALIGN 2

/*
 * Following ascii diagram illustrates the layout of mbuf data structure.
 *
 *           +--+-------------+
 *   m_hdr   |  |             |
 *           |  |             |
 *           +--------------------> &m_data[0]
 *           |  |             |
 *           |  |             |
 *           |  |             +---> m_head
 *           |  |             |
 *           +  |             |
 * m_data[MLEN] |             |
 *           +  |             |
 *           |  |             |
 *           |  |             |
 *           |  |             +---> m_tail
 *           |  |             |
 *           +--+-------------+---> &m_data[MLEN]
 */
```

