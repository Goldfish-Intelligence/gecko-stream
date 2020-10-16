# Audio-droid
## Purpose
The app can transmit audio from or to the device over the network with a fixed latency. Examples include wireless microphones.   

## Usage
### "Standalone"
The app can send rocstreaming packets to the specified address and ports. The roc-recv should be running to receive the audio.

### Server-controlled
Connected to the control-server to remotely manage the audio streams. The server can control the ports and mute/running status of the streams remotely. 
The user is still able to control this as well.

## Settings
### Connections
- Connect to control finds automatically a running control-server on the network.
- The ip is automatically set to the control-servers ip and can be overwritten.
- The ports for sending are the destination of the outgoing stream to the set ip. The roc-receiver should listen to this address.
- The receive ports are used to set up a roc-receive server on the local ip.

### audio transmission
- There are buttons to for each enable send/receive and mute/deaf audio.
- When enabling send/receive the roc-stream starts/listents on the currently specified ports

