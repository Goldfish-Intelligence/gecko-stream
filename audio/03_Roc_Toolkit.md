# Roc-Toolit

> Roc is a toolkit for real-time audio streaming over the network.
> (GitHub)[https://github.com/roc-streaming/roc-toolkit]
> (Documentation)[https://roc-streaming.org/toolkit/docs/]

The command line tools and pulseaudio are installed on the mixing pc and are
available in path and the pulseaudio modules are discoverable by pulseaudio.

## What this does

Roc is able to send uncompressed audio via an unreliable network (such as wifi).
It does this by sending not only the audio but also a lot of Redundancy
information for error correction. This way a receiver can reconstruct missing
audio data without requesting retransmissions. If you hear audio glitches, this
probably means, that error correction was not possible because too much data
was lost.

## Flow of data

When a sender wants to send data, the following happens. The sender is
configured with two ports. An audio port (Default: 10001) that transmits the
audio (we use type `rtp+rs8m`) and an error correction port for the
redundancy information (Default: 10002, Type: `rs8m`).

Transmission is done via UDP and stateless. The sender does not realize if a
receiver is present and listening. You can also shutdown a transmitter and start
it up again without touching the receiver.

Multiple transmitter can send audio to the same receiver by being configured
with identical ports. This reduces complexity but at the loss of the ability
to control latency, loudness or other effects further down in the audio
pipeline.

## Command line tools

There are more tools available. We will explain the two most important ones.
Refer to roc-toolkit documentation.

### roc-recv

Receives audio and can send it to pulseaudio, save data to a file or pipe to
arbitrary commands. Very useful for debugging. Can be configured to beep on
data loss. See `roc-recv --help` for more flags.

#### Examples

Playback audio:

> roc-recv -s rtp+rs8m::10001 -r rs8m::10002

Save audio to .wav:

> roc-recv -s rtp+rs8m::10001 -r rs8m::10002 --driver=wav --output=out.wav

### roc-send

Sends audio to a receiver. Useful if you want to send audio to a phone or if
you want to test the local receiver setup. Almost identical to roc-recv.

Send wav file:

> roc-send -s rtp+rs8m:192.168.0.3:10001 -r rs8m:192.168.0.3:10002 -i ./file.wav

Capture sound from a specific PulseAudio device:

> roc-send -s rtp+rs8m:192.168.0.3:10001 -r rs8m:192.168.0.3:10002 -d pulseaudio -i <device>


## Pulseaudio modules

### Receiver

For the receiving side, Roc provides module-roc-sink-input PulseAudio module. It
creates a PulseAudio sink input that receives samples from Roc sender and passes
them to the sink it is connected to. You can then connect it to any audio
device.

Roc sink input supports several options:

|option               |required|default       |description                                                 |
|---------------------|--------|--------------|------------------------------------------------------------|
|sink                 |no      |<default sink>|the name of the sink to connect the new sink input to       |
|sink_input_properties|no      |empty         |additional sink input properties                            |
|resampler_profile    |no      |medium        |resampler mode, supported values: disable, high, medium, low|
|sess_latency_msec    |no      |200           |target session latency in milliseconds                      |
|io_latency_msec      |no      |40            |target playback latency in milliseconds                     |
|local_ip             |no      |0.0.0.0       |local address to bind to                                    |
|local_source_port    |no      |10001         |local port for source (audio) packets                       |
|local_repair_port    |no      |10002         |local port for repair (FEC) packets                         |

Here is how you can create a Roc sink input from command line:

> pactl load-module module-roc-sink-input

Alternatively, you can add this line to /etc/pulse/default.pa to create a Roc sink input automatically at PulseAudio start:

> load-module module-roc-sink-input

You can then connect the Roc sink input to an audio device (i.e. a sink) via command line:

> # determine Roc sink-input number
> $ pactl list sink-inputs
>
> # connect Roc sink-input to a sink
> $ pactl move-sink-input <roc_sink_input_number> <sink>

### Sender

For the sending side, Roc provides module-roc-sink PulseAudio module. It creates
a PulseAudio sink that sends samples written to it to a preconfigured receiver
address. You can then connect an audio stream of any running application to that
sink, or make it the default sink.

Roc sink supports several options:

|option            |required|default   |description                                    |
|------------------|--------|----------|-----------------------------------------------|
|sink_name         |no      |roc_sender|the name of the new sink                       |
|sink_properties   |no      |empty     |additional sink properties                     |
|local_ip          |no      |0.0.0.0   |local sender address to bind to                |
|remote_ip         |yes     |no        |remote receiver address                        |
|remote_source_port|no      |10001     |remote receiver port for source (audio) packets|
|remote_repair_port|no      |10002     |remote receiver port for repair (FEC) packets  |

Here is how you can create a Roc sink from command line:

> pactl load-module module-roc-sink remote_ip=<receiver_ip>

Alternatively, you can add this line to /etc/pulse/default.pa to create a Roc sink automatically at PulseAudio start:

> load-module module-roc-sink remote_ip=<receiver_ip>

You can then connect an audio stream (i.e. a sink input) to the Roc sink via command line:

> pactl move-sink-input <sink_input_number> roc_sender

