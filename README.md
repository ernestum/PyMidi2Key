# PyMidi2Key
A simple tool to convert midi events to key presses.
It is inspired by [midi2input](https://gitlab.com/enetheru/midi2input/) but I hope to provide mostly the same functionality with a lot less LOC so it is ralistically long-term maintainable.

## Installation Notes

To make the midi module of pygame work I had to do:

```bash
sudo mkdir /usr/lib/alsa-lib/
sudo ln /usr/lib/x86_64-linux-gnu/alsa-lib/libasound_module_conf_pulse.so /usr/lib/alsa-lib/libasound_module_conf_pulse.so
```

Read more about it here: https://stackoverflow.com/questions/64638256/pygame-midi-libasound-module-conf-pulse-so-error-unable-to-open-slave

## Configuration

Just add your code to `handle_event()`.
For you convenience, each midi event is printed as a bool expression to match it, ready to copy-paste into `handle_event`.
