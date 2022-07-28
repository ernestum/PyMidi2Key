# PyMidi2Key
A simple tool to convert midi events to key presses

## Installation Notes

To make the midi module of pygame work I had to do:

```bash
sudo mkdir /usr/lib/alsa-lib/
sudo ln /usr/lib/x86_64-linux-gnu/alsa-lib/libasound_module_conf_pulse.so /usr/lib/alsa-lib/libasound_module_conf_pulse.so
```

Read more about it here: https://stackoverflow.com/questions/64638256/pygame-midi-libasound-module-conf-pulse-so-error-unable-to-open-slave

