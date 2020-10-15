Audio Infrastructure
====================

The audio pipeline is responsible for collecting audio streams, processing them
and finally feeding audio samples to OBS. Processing includes muxing multiple
streams and applying effects and filters on them at different stages. The
pipeline lives inside (Pulseaudio)[02_Pulseaudio.md].

To get audio inside the pipeline we use (roc-toolkit)[03_Roc_Toolkit.md].

To produce audio we use an (Android App)[04_Android_Audio_App.md] created by
Rafael that is compatible with roc-toolkit.