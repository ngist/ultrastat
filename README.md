# Github Custom for Home Assistant

[![Build][build_badge]][actions]
[![License][license_shield]](LICENSE)
[![hacs][hacs_badge]][hacs]

[license_shield]: https://img.shields.io/github/license/ngist/ultrastat?style=for-the-badge
[hacs]: https://github.com/custom-components/hacs
[hacs_badge]: https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge
[actions]: https://github.com/ngist/ultrastat/actions
[build_badge]: https://img.shields.io/github/actions/workflow/status/ngist/ultrastat/pythonpackage.yaml?branch=main&style=for-the-badge


> [!WARNING]
> This integration is in the very early statges of active development, it's not ready for use do not install!. See [Development Progress](#development-progress)

## About

This repo contains a custom component for [Home Assistant](https://www.home-assistant.io) that provides a unified thermostat control for your home.
It brings together all of your temp sensors and temperature control appliances for your house and can seamlessly control between them. The goal of this project is simplicity of setup and use.

It also allows you to select between several different modes:

1.  Comfort: minimizes temperature fluctuations but may use more energy
2.  Eco: minimizes carbon footprint
3.  Budget: minimizes energy expenditure (if you only have one type of heating or cooling system this is the same as eco mode)

## Motivation

Why bother making another thermostat integration? 

- HA natively has thermostat helpers can't this all be done natively without a custom integration?

  Well yes it can, and in fact that's what I started with, well at least that's what I tried to do, but the complexity became unmanagable for my needs, too many entities, and too many automatations to keep track of properly, and very error prone and repetitious to make small changes. If you have a relatively simple heating/cooling setup this may be the best option for you.
  
- Why not use [Versatile Thermostat](https://github.com/jmcollin78/versatile_thermostat) or [Better Thermostat](https://github.com/KartoffelToby/better_thermostat) or [HASmartThermostat](https://github.com/ScratMan/HASmartThermostat)?

  Well actually you may want to go check them out, and look at the [Features](#features) below to compare.

  Better and HASmartThermostat are both designed for working with a single room at a time, I want something that will manage multiple rooms elegantly especially when a heat or cooling call may cover more than one room at a time. Versatile has some functionality for managing multiple rooms but I don't think it handles multiple rooms on the same zone very well yet, additionally I don't think it can handle multiple heating appliances in the same room, I'll admit though there's alot of documentation and it wasn't entirely clear to me what it could and couldn't do. Versatile and HASmartThermostat also require manual tuning of the control loops, this was something I wanted to avoid, especially given the interaction between rooms in my house it seemed like this would be a sisyphian task.

  I'll use my house as an example to make concrete the use case. I have a multizone boiler setup with open/closed zone valves but one zone is always on if any boiler zone is called(this prevents to possiblility of the circulator pump driving into a closed system), I also have mini-split heatpumps in several rooms. I wanted a thermostat that would wisely choose between boiler heating and heatpump heating for any given room and ambient conditions, and also switch the heatpumps to cooling mode automatically when appropriate. At higher ambient temperatures the heatpumps are very efficient compared with the boiler but at much lower temperatures the heatumps either can't keep up in some rooms or are more costly to operate than the boiler, the goal is that this will use one or both heatsources as appropriate to maximize comfort and efficiency. Another problem I wanted to overcome is that basic on/off control of my boiler zones resulted in several degrees of overshoot so I wanted more optimal control.

- What about xyz thermostat integration?

  At the time I started the project the above were the only ones I saw I didn't look at others.

## Should I use this?
If you have a single HVAC zone for heating/cooling as many houses in the US do this is not the integration for you there are better options with fewer features, and less configuration.

If you're in the situation where you have any of the following then this integration may be for you:

- You have a multi-zone heating or cooling system(s) where more than one area/temp sensor is in each zone.
- Partially overlapping heating/cooling zones, ie your heating zones aren't the same as your cooling zones.
- You have multiple heating or cooling systems for the same area. Maybe you have an HVAC system and a supplemental window AC unit, or you have a boiler/radiator system but you also have minisplit heat-pumps.

Supported control outputs:
 - switch (for simple on/off heating/cooling/humidification/dehumidification calls)
 - numeric (for TRVs or things that take a 0-100% value)
 - climate (for appliances that are already integrated into HA that have a climate interface)

## Features

### Planned
 - [ ] Handle rooms with multiple heating/cooling appliances.
 - [ ] Handle multiple rooms that are on the same heating or cooling zone 
 - [ ] Automatic tuning - no user configuration of control loop parameters everything is learned by mathemagic(or AI if you want to call it that).
 - [ ] Implement presets
 - [ ] Implement schedules
 - [ ] Smart Start - activates heating or cooling early so temp is acheived by the scheduled time.
 - [ ] Use external temperature to optimize control
 - [ ] Use boiler inlet/outlet temperatures to optimize control
 - [ ] Use external wind speed and direction to optimize control
 - [ ] Use solar irradiance to optimize control
 - [ ] Implement stale sensor detection
 - [ ] Implement freeze protection
 - [ ] Implement inferred temperature for stale sensors
 - [ ] Implement room adjacency for better control
 - [ ] Handle Grouped Mini-split heatpumps

### Not Planned
[Versatile Thermostat](https://github.com/jmcollin78/versatile_thermostat) offers many of these features but they are intentionally not planned to avoid added complexity 
 - Automatic room control based on occupancy (this can be setup externally if desired)
 - Automatic room control based on opening or closing a door or window (can be setup externally if desired)
 - Power shedding

## Prerequisites

1. Setup [Areas](https://www.home-assistant.io/docs/organizing/areas/) for any room in your house you want this integration to control.
2. Have at least one temperature sensor in each Area you're interested in controlling, it doesn't need to be associated with the area in HA(though you probably should associate it), it just needs to be physically located there.
3. Have at least one climate control device controllable by HA, either switch, climate, or numeric type.

## Installation

The simplest way to install this integration is with the Home Assistant Community Store (HACS). This is not (yet) part of the default store and will need to be added as a custom repository.

## Configuration

The configuration flow requires some explanation as many things are possible and supported that may not be obvious.

### Outdoor sensors

These are entirely optional, but populating at least outside temperature is recommended, for most people the other sensors will have minimal impact.

If you have a weather station you can use entities from this to populate outdoor sensors, if you don't have a weather station you can use a weather integration to provide these entities.

Rough order of importance of outside sensors:
1. Temperature (this matters for everyone)
2. Wind Speed (this will matter more for older drafty homes)
3. Wind Direction (this will matter more for older drafty homes)
4. Solar Irradiance (probably doesn't matter that much)

### Boiler settings

If you have a hydronic(aka water) boiler then you'll want to specify the heat call switch or switches if you have a multizone system. It's important for the system to know which controls are associated with the hydronic boiler as they have much longer time constants than HVAC/Heatpump/electric type systems.

> [!Note]
> This integration assumes a hydronic boiler system with one or more heat call switches for one/off type zone valves(all valves are assumed to be normally closed, if you have a normally open valve invert it before passing it in), or flow regulating valves(TRVs). If you have an always circulating system with reset controller or some other exotic boiler system. These aren't supported right now. If you are interested in adding support open a pr or [issue](https://github.com/ngist/ultrastat/issues)

### Room settings

You must specify what home assistant "area" these settings are for any entities that this integration makes will be added to these areas.

You must specify a temperature sensor for the area, you can specify more than one if you like but you shouldn't need more than one if it's well placed. If you do specify more than one then the average reading is used for control. **Temperature sensors must be unique to each area, sharing temperature sensors across multiple areas is not allowed**

You can optionally specify a humidity sesnor for the area, if you also want to control a humidity appliance.
**Humidity sensors must be unique to each area, sharing temperature sensors across multiple areas is not allowed**

In general because a heating or cooling appliance or zone may cover more than one room, it is allowed and even recommended to reuse these entities across multiple rooms to capture their association with those rooms. 

Examples:
Scenario 1: The first floor is on a single boiler zone(switch.boiler_zone1) but you have three rooms with one temp sensors in each room. There are several options on how this could be configured. 1. (Preferred) You can setup 3 different areas each with it's own temp sensor, and use the same switch.boiler_zone1 for the heat call in all three. 2. (Not Recommended) You can setup a single area in UltraStat and add all three temp sensors to it.  
 3. (Not Recommended) You only really care about one room, so you only setup a single area in UltraStat and only supply the associated temp sensor for the room you care about.

        2 is not recommended as it provides less granular control, maybe you want to control to a different room at different times of day, option 2 doesn't allow for this. 3 omits information from UltraStat, which once adjacency information is added can help improve temperature control in the room you care about, you can just disable control in the rooms you aren't interested in after you setup UltraStat.
