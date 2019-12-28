## data foward
```
1. Init EAL:
ret = rte_eal_init(argc, argv)

2. Allocate mempool for tx/rx queues
mbuf_pool = rte_pktmbuf_pool_create("MBUF_POOL", NUM_MBUFS * nb_ports,
        MBUF_CACHE_SIZE, 0, RTE_MBUF_DEFAULT_BUF_SIZE, rte_socket_id())
3. init ports
for (portid = 0; portid < nb_ports; portid++) {
    if (port_init(portid, mbuf_pool) != 0)
        rte_exit(EXIT_FAILURE, "Cannot init port %"PRIu8 "\n", portid);
}
3.1 get eth count
3.2 configure port
3.3 setup tx/rx queues for the port
3.4 enable the port
3.5 set port mode

4. lcore_main()
4.1 read packet from the port
4.2 send packet to the port
    for (;;) {
        for (port = 0; port < nb_ports; port++) {
            struct rte_mbuf *bufs[BURST_SIZE];
 
            const uint16_t nb_rx = rte_eth_rx_burst(port, 0, bufs, BURST_SIZE);
            if (unlikely(nb_rx == 0))  
                continue;
 
            const uint16_t nb_tx = rte_eth_tx_burst(port ^ 1, 0, bufs, nb_rx);
            if (unlikely(nb_tx < nb_rx)) {  // to release mbuf if no successed to be sent.
                uint16_t buf;
                for (buf = nb_tx; buf < nb_rx; buf++)
                    rte_pktmbuf_free(bufs[buf]);
            }
       

```
