VisiStrom
======

Open Energy Data Hackdays project.

# Design Challenge
How might we visualize peaks, valleys and provenance of electric power,
so that end consumers know when consumption and production is most ecological and/or cheapest.

# Business Goals
Minimize the necessity to buy expensive, "dirty" electricity (produced from oil and coal).

- reduce peaks (peak shaving)
- reduce unplanned differences in consumption and production

# Functionality
## Home Screen
The Home Screen is split in half. In the upper part, an icon is shown as a quick and easy-to-understand indicator for the user - a call to action. The icon shows one of three states:

- the lightbulb is turned on, which means that the club produces more energy than expected and the user is welcomed to increase his or her energy consumption (invest more energy)
- the lightbulb is turned of, which means that the club consumes more energy than expected and the user is welcomed to decrease his or her energy consumption (save some energy for later)
- the lightbulb is cut in half showing a balance of a turned on and turned off light, which means that the club is on track and the user does not need to change anything.

A click on the icon will show the user a forecast of the lightbulb so he or she can plan their energy consumption ahead.

On the second half of the Home Screen are other options the user can choose. These are
- Forecast
- Club
- History
- Options

## Lightbulb Forecast
The Lightbulb Forecast shows a series of lightbulbs from top to bottom. Each lightbulb belongs to a specific time period (e.g. 1 hour, 1 pm - 2pm). Similar to the lightbulb on the Home Screen, the lightbulbs indicate whether the specific period is more likely to be a period to spend or save energy. A click on one of the lightbulbs gives the user the option to set a reminder (e.g. for vacuum cleaning, not yet implemented).

## Forecast Screen
coming soon

## Club Screen
coming soon

## History Screen
coming soon

## Options Screen
In the first versions of the Options Screen, a list of typical electrical appliances will be shown. The list should help the user to decide which devices can be turned on or turned off, depending on the current situation. In later versions, these options can be improved by
- showing only appliances the user actually has
- highlighting appliances that can actually be turned on or turned off (e.g. not showing a boiler that is already beeing running)
- sorting the list in a smart way (taking the power consumption, ramp up time, saving potential, etc. into account)
