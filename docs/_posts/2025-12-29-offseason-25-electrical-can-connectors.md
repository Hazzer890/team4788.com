---
title: "Offseason `25 | Electrical CAN Connectors"
date: 2025-12-29
image: /assets/img/blog/offseason-25-electrical-can-connectors.jpg
image_alt: "Desk containing our CAN pcbs in progress"
---

Going into the new season we identified that one area we wanted to improve on for our 2026 robots was our electrical robustness as we had multiple issues between competitions and during build season with electrical that slowed us down greatly.

### Solution Overview

One of these issues was an inability to quickly identify and diagnose CANBus issues as all connections were soldered, to fix this issue we will use 5 custom PCB designs to route both our RIO and CANivore CANBuses, as well as 12V and DIO lines (for RIO network only) over standard RJ45 (ethernet) cabling, allowing for quick disconnection and rerouting of CAN signals, whilst **retaining a robust connection**

### Designs

## Rio Hub

![Render of a CAN breakout PCB](/assets/img/blog/offseason-25-electrical-can-connectors-1.png)

The Rio Hub acts as a connection between the RoboRio's CANBus output and the RJ45 Bus that connects to it. The board also provides reverse polarity protection and voltage regulation (if the regulator is installed) for 12v supply, 4 DIO lines over RJ45 and 8 through Molex SL connectors, 2 PWM lines for servos over Molex SL connectors and the board mounts to the MXP port of a RoboRIO

## Rio Module

![Render of a CAN-over-RJ45 PCB](/assets/img/blog/offseason-25-electrical-can-connectors-2.png)

The Rio modules act as nodes to connect one or more CAN devices to the network, they also provide DIO access and 12v output, they can be soldered to terminate the bus.

## Swerve Hub

![Render of a small power PCB](/assets/img/blog/offseason-25-electrical-can-connectors-3.png)

Functions similarly to the Rio Hub, without DIO lines, PWM or voltage regulation, has mounting holes that line up with the CANivore mounting holes

## Swerve Module

![Render of a CAN-over-RJ45 PCB](/assets/img/blog/offseason-25-electrical-can-connectors-4.png)

Functions similarly to the Rio Modules but without DIO access, it is compatible with Rio modules and Hubs, but won't pass through the DIO lines (to be fixed in the next iteration)

## Rio Hub Regulator

![Render of a blue PCB](/assets/img/blog/offseason-25-electrical-can-connectors-5.png)

A simple 8V-22V to 12V regulator that can be plugged into the Rio Hub and held down with the mounting hole (not lined up correctly in current version)

### Downloads

[GitHub - Files](https://github.com/CurtinFRC/CAN-over-RJ45)

[GitHub - Releases](https://github.com/CurtinFRC/CAN-over-RJ45/releases/)
