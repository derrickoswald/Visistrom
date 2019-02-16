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

# Data analytics
For this project, we used different sets of available data (open data).
- [Aggregated load profiles of apartment blocks](https://github.com/schoolofdata-ch/energy-data/issues/3)
- [Project VEiN](https://github.com/schoolofdata-ch/energy-data/issues/4)

[ ] todo: add all the data being used / calculated

# Functionality
## Home Screen
The Home Screen is split in half. In the upper part, an icon is shown as a quick and easy-to-understand indicator for the user - a call to action. The icon shows one of three states:

- the lightbulb is turned on, which means that the club produces more energy than expected and the user is welcomed to increase his or her energy consumption (invest more energy)
- the lightbulb is turned of, which means that the club consumes more energy than expected and the user is welcomed to decrease his or her energy consumption (save some energy for later)
- the lightbulb is cut in half showing a balance of a turned on and turned off light, which means that the club is on track and the user does not need to change anything.

A click on the icon will show the user a forecast of the lightbulb so he or she can plan their energy consumption ahead.

On the second half of the Home Screen are other options the user can choose. These are
- My Realm
- My Club
- My History
- Compare Appliances
- What can I do

## Lightbulb Forecast Screen
The Lightbulb Forecast shows a series of lightbulbs from top to bottom. Each lightbulb belongs to a specific time period (e.g. 1 hour, 1 pm - 2pm). Similar to the lightbulb on the Home Screen, the lightbulbs indicate whether the specific period is more likely to be a period to spend or save energy. A click on one of the lightbulbs gives the user the option to set a reminder (e.g. for vacuum cleaning, not yet implemented).

## My Realm Screen (not yet implemented, coming soon)
The My Realm Screen shows the energy consumption of the user's home or flat using a simple graph. The data is limited to the last 24 hours. If possible, different energy consumers will be shown separately as well as aggregated. As an example, the bas load (typical household appliances), the usage of the battery, the pv production as well as the consumption of the heatpump could be shown. The user can switch between the aggregated view, showing only "what flows into / out of the house" or the detailed view.

## My Club Screen (not yet implemented, coming soon)
*Club is the term for a group of customers connected to the same network node*
Similar to the My Realm Screen, the My Club Screen shows a simplified overview of the electricity network area the user is connected to (automatically determined, login required). On the one hand, the graph shows the performance of the network within the last 24 hours. On the other hand, the graph shows the number of participants or rather their aggregated energy consumption and production in order to highlight the ratio and improve that.

## My History Screen (not yet implemented, coming soon)
The My History Screen provides a filter mechanism to specify a period of interest. As an example, the user can select from last day, last week, specific week, last month, specific month, last season, specific season, last year and custom from/to dates. The specified period is then being displayed as a graph whereas the scaling is determined by the period itself. Additionally, the user can add a second period of the same kind in order to start comparing time series. As an example, the user could compare the last week with the same week a year ago.

## Compare Appliances Screen (not yet implemented, coming soon)
The Compare Appliances Screen is meant to support the user in acquisition decisions. It focuses on the operational costs based on electricity consumption of the specified appliances. In the first version, the user can input 5 values into the form:
- electricity consumption when turned on in Watt
- hours of operation per year in hours
- electricity consumption when in stand by in Watt
- hours in stand by per year in hours
- electricity cost (default value provided by operator)

After putting the values in, the estimated electricity costs of that appliance is being shown. The user can add multiple appliances in order to compare them.

Additionally, a list of typical values is being shown, as for example the number of hours a tv es being operated in general (as a rule of thumb).

## What can I do Screen (not yet implemented, coming soon)
In the first versions of the What can I do Screen, a list of typical electrical appliances will be shown. The list should help the user to decide which devices can be turned on or turned off, depending on the current situation. In later versions, these options can be improved by
- showing only appliances the user actually has
- highlighting appliances that can actually be turned on or turned off (e.g. not showing a boiler that is already beeing running)
- sorting the list in a smart way (taking the power consumption, ramp up time, saving potential, etc. into account)

## Supportive Messages (not yet implemented, coming soon)
The system motivates the user by displaying a supportive message every now and then. A message can be displayed when the user simply opens the app/website (e.g. 'It's nice to see you here', 'Welcome back!'). More importantly, a message should be shown if the user has seen a call to action (e.g. lightbulb is turned on) and the system notices that the energy consumption of the user actually dropped (e.g. 'Thank you for your support, you helped the Club!').
