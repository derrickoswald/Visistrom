VisiStrom
======

Visistrom helps individuals to plan using electricity at a good time in order to use sustainable energy as much as possible. 
In turn, this behaviour helps utility companies to reduce energy purchases from expensive sources like coal and oil plants. 

## Energy Hack Days 

This project emerged from the following Open Energy Hack Days challenge: [Visistrom challenge](https://hack.opendata.ch/project/289).


**16.02.2019, 08:00 - Second Update:**
A basic version of the prototype is running.

**15.02.2019, 18:00 - First Update:**
We realized that it is not just about consuming as little as you can - it is also important that when you consume the electricity, you want to avoid coal-produced electricity. Some solar energy is being produced, sometimes it is good to use electricity when the sun is shining. We are trying to come up with a good visualization to tell this message. There are three recommendations for the end user: now is a good time to use electricity, now you should save, or just keep going. We are quite advanced with visualization, we have some nice data we can use, but the challenge is how to decide when to recommend using electricity.

## Design Challenge
How might we visualize peaks, valleys and provenance of electric power,
so that end consumers know when consumption and production is most ecological and/or cheapest?

## Business Goals
Minimize the necessity to buy expensive, "dirty" electricity (produced from oil and coal).

- reduce peaks (peak shaving)
- reduce unplanned differences in consumption and production

## Data Analytics
To make a recommendation of when to use electricity or not, we need to try to avoid peaks in consumption, at the individual household level, and at the area level. 


### 1. Consumption for a given household
Predict consumption peaks and valleys for a given time based on the household's past consumption:
- for a given hour during the day (e.g. from 3pm to 4pm)
- on a given day of the week (e.g. Saturday)
- in a given month of the year (e.g. July)
--> not using that at the moment yet

At the moment, the front-end app prototype uses the non-processed usage data from last year as a proxy prediction. 

**Data source:** 

[Aggregated load profiles of apartment blocks](https://github.com/schoolofdata-ch/energy-data/issues/3)
01. Aug 2017 - 31. Aug 2018

*These are Smartmeter measurments in 15-minute intervalls by blocks of flats (usually about 3-8). It's not by individual households, but this is a good enough apporximation for now.*

### 2. Consumption for Kanton of Aargau, SwissGrid
As a proxy for prediction data from the utility provider
[Energieübersicht 2018, Swissgrid (Kanton Aargau)](https://www.swissgrid.ch/de/home/operation/grid-data/generation.html#endverbrauchte-energie)
Scaled down to match 
01.01.2018-31.12.2018


### 3. Consumption for a given area (TO DO)
Predict consumption peaks and valleys for a given time based on the area's past consumption:
- for a given hour during the day (e.g. from 3pm to 4pm)
- on a given day of the week (e.g. Saturday)
- in a given month of the year (e.g. July)

**Data source:**
- [Aggregated load profiles of apartment blocks](https://github.com/schoolofdata-ch/energy-data/issues/3) (summed up)
- Or alternatively: load profiles from Trafo stations (not openly available)



### 4. Solar panel production for a given household
Predict production peaks and valleys for a given time based on sunlight and on the household' past solar panel production:
- for a given hour during the day (e.g. from 3pm to 4pm)
- on a given day of the week (e.g. Saturday)
- in a given month of the year (e.g. July)

**Data sources:** 
[Solarenergie Prognose from NETSTRANSPERNENZ](https://www.netztransparenz.de/Weitere-Veroeffentlichungen/Solarenergie-Prognose)

Optional data to refine the prediction at household level: Past production of solar electricity for this household


## Functionality 

The functionality purpose for the consumers is:
- to adapt their behaviors to have cleaner energy usage
- to see their progression in energy consumption over time

To adapt their behaviors, accessible data of factors impacting energy production will be shown to the user. Such include prevision of solar intensity for the upcoming week, coupled with other data such as past average consumption habits of the Club. Data can also integrate predictable special events susceptible to induce consequent perturbation in the general consumption (e.g. World Cup Football).

The integrated data is presented to the user in the form of a table showing predicted energy conditions for the upcoming week, for every hour. The table will highlight the day and hours when clean energy will be the more available among the week. This will enable users to plan their energy most consuming tasks (usually cooking and housekeeping) according to external energy availabiity conditions.
![Mockup of solar panel production](data/best%20moment%20prediction_ink.png?raw=true)

The user will be able to click on the case of the table to access to more details explaining the reasons why he/she should stay to his current task planification or move it to anothe time:
- sunlight availability
- saturation of Club
- etc.

To see their progression over time, consumers will have access to the profile curve of their past days, weeks and months consumptions. They will also be able to see the difference between their actual daily consumption of a specific weekday with average of past consumption for the same weekday.

![Demo of a household's consumption for 1 day](/data/demo.png)


### Home Screen
The Home Screen is split in half. In the upper part, an icon is shown as a quick and easy-to-understand indicator for the user - a call to action. The icon shows one of three states:

- the lightbulb is turned on, which means that the club produces more energy than expected and the user is welcomed to increase his or her energy consumption (invest more energy)
- the lightbulb is turned of, which means that the club consumes more energy than expected and the user is welcomed to decrease his or her energy consumption (save some energy for later)
- the lightbulb is cut in half showing a balance of a turned on and turned off light, which means that the club is on track and the user does not need to change anything.

A click on the icon will show the user a forecast of the lightbulb so he or she can plan their energy consumption ahead.

### Forecast Screen
As an end consumer, I want to know when is the best time to use electricity in the coming hours and days, so that I can plan energy-intensive tasks accordingly (e.g. doing the laundry, charging my electric car,...)

**Implementation:** The Lightbulb Forecast Screen shows a series of lightbulbs from top to bottom. Each lightbulb belongs to a specific time period (e.g. 1 hour, 1 pm - 2pm). Similar to the lightbulb on the Home Screen, the lightbulbs indicate whether the specific period is more likely to be a period to spend or save energy. 

![Algorithm for the usage recommendation](images/2019_02_16%2014_36%20Office%20Lens.jpg)


## Backlog (not implemented yet)

### Notification / Reminder: 
**User Story:** As an end consumer, I want to get notified of the best time to use electricity, so I don't have to check the app actively. 

**Implementation:** On the "Forecast" screen, a click on one of the lightbulbs (= time period) gives the user the option to set a reminder (e.g. to vacuum clean).


### Drill-Down
As an end consumer, I want to see the forecasted consumption and production for a particular time period (e.g. today 3-4pm), so that I understand why I get a recommendation to use or save electricity at that time. 


### My Realm Screen (not yet implemented, coming soon)
The My Realm Screen shows the energy consumption of the user's home or flat using a simple graph. The data is limited to the last 24 hours. If possible, different energy consumers will be shown separately as well as aggregated. As an example, the bas load (typical household appliances), the usage of the battery, the pv production as well as the consumption of the heatpump could be shown. The user can switch between the aggregated view, showing only "what flows into / out of the house" or the detailed view.

### My Club Screen (not yet implemented, coming soon)
*Club is the term for a group of customers connected to the same network node*
Similar to the My Realm Screen, the My Club Screen shows a simplified overview of the electricity network area the user is connected to (automatically determined, login required). On the one hand, the graph shows the performance of the network within the last 24 hours. On the other hand, the graph shows the number of participants or rather their aggregated energy consumption and production in order to highlight the ratio and improve that.

### My History Screen (not yet implemented, coming soon)
The My History Screen provides a filter mechanism to specify a period of interest. As an example, the user can select from last day, last week, specific week, last month, specific month, last season, specific season, last year and custom from/to dates. The specified period is then being displayed as a graph whereas the scaling is determined by the period itself. Additionally, the user can add a second period of the same kind in order to start comparing time series. As an example, the user could compare the last week with the same week a year ago.

### Compare Appliances Screen (not yet implemented, coming soon)
The Compare Appliances Screen is meant to support the user in acquisition decisions. It focuses on the operational costs based on electricity consumption of the specified appliances. In the first version, the user can input 5 values into the form:
- electricity consumption when turned on in Watt
- hours of operation per year in hours
- electricity consumption when in stand by in Watt
- hours in stand by per year in hours
- electricity cost (default value provided by operator)

After putting the values in, the estimated electricity costs of that appliance is being shown. The user can add multiple appliances in order to compare them.

Additionally, a list of typical values is being shown, as for example the number of hours a tv is being operated in general (as a rule of thumb).

### What can I do Screen (not yet implemented, coming soon)
In the first versions of the What can I do Screen, a list of typical electrical appliances will be shown. The list should help the user to decide which devices can be turned on or turned off, depending on the current situation. In later versions, these options can be improved by
- showing only appliances the user actually has
- highlighting appliances that can actually be turned on or turned off (e.g. not showing a boiler that is already beeing running)
- sorting the list in a smart way (taking the power consumption, ramp up time, saving potential, etc. into account)

### Supportive Messages (not yet implemented, coming soon)
The system motivates the user by displaying a supportive message every now and then. A message can be displayed when the user simply opens the app/website (e.g. 'It's nice to see you here', 'Welcome back!'). More importantly, a message should be shown if the user has seen a call to action (e.g. lightbulb is turned on) and the system notices that the energy consumption of the user actually dropped (e.g. 'Thank you for your support, you helped the Club!').
