## General

Today we are going to get started with the ESP-01 for wiring and further information please watch this Video.

## Code Explanations

!It is important to sent all MQTT messages to the script with the retained flag set to true!

This is a general script. Where to send and recive MQTT messages and code examples are in the comments of the script. If you have any questions feel free to comment in the Video.

To test the script send this message: {"property":true} or {"property":false} (!Retained Flag true e.g MQTT.fx top right) to the channel you subscribed to.

This also works with the ESP32. Change the first line from ```#include "ESP8266WiFi.h"``` to ```#include <WiFi.h>```