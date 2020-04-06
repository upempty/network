### publish subscriber

#### publish store the 'message' to channel's msg...

connecting to server.

each clients for this channel to store the msg.

  adding the events. trigger event of poll

via poll to send msg to existing subscribers.



#### subscriber now...

connecting to server.

store the msg of this channel. trigger event of poll.

via poll to send msg to new added subscribers.



**0 aync_ps main:**

1->2 1->3

1 aync_ps_server(start()) : 

​    accept_cb, read_cb, write_cb, parse_request, register_client, channels(map), clients(map), event.

2 event_daemon(loop) : event_register_fd, get_connection, update_event,  set_read_op(accept, read), set_write_op

3 async_ps_channel: subscribe, publish

4 async_client

5 networking









