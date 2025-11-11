import random
import zmq

# Establish Server TCP connection on port 5555
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://localhost:5555")

# Establish loop to receive incoming requests
while True:
    try:
        # Error handling for empty JSON requests
        message = socket.recv_json()
        if len(message) == 0:
            reply = {'Error': 'Requests for random number must have content'}

        # Process for shutting down the server
        elif len(message) > 0 and message[0] == "Q":
            reply = {"Status": "Shutting Down"}
            socket.send_json(reply)
            break

        # Process for sending back a float inclusively between 1 and 100
        elif len(message) == 1:
            reply = random.uniform(1, 100)

        # Process for sending back a float inclusively between a min and max
        elif len(message) == 2 and all(isinstance(x, (int, float)) for x in message) and message[0] < message[1]:
            reply = random.uniform(message[0], message[1])
        else:
            try:

                # Process for returning a random item from a sequence
                reply = random.choice(message)

    # Error Handling
            except (IndexError, TypeError):
                reply = {'Error': 'Requests for random number must be valid JSON'}
    except ValueError:
        reply = {'Error': 'Requests for random number must be valid JSON'}

    # Sending the reply
    socket.send_json(reply)
