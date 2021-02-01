# wsrabbit
Local webservice to rabbitmq

This python code runs with flask and will listening on 127.0.0.1:5000

It provides a send function and a poll function.

The send will publish a message into minetest exchange of the rabbitmq broker.

The poll will retrive all the message waiting into a RAM queue into python process. These messages come from the minetest_server rabbitmq queue.

It is a very stupid non secure interface from local DMZ to a rabbitmq more secured server. It allows the minetest server to communicate with other applications using msg_bridge mod.
