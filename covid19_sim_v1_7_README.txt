COVID-19 simulator v1.7 README:  by Caleb Owens
updated 12/16/2020

This python program uses MatPlotLib and NumPy to plot a graph of the data points that are generated in this program. For the program to function, please have these libraries in your selected environment.
Matplotlib version 3.3.3
NumPy version 1.19.4

This simulation creates a semi-random generated population that is customized based on user selected parameters. the generated population is then subjected to encounter situations with an infected sub-population.

Each 'Person' has attributes unique to that person.

	Risk factor: lower/higher chance of dying if infected
	Condition: whether infected/uninfected/immune
	Activity: how many encounters a person has each day
	Safety: if a person uses safety precautions such as less activity and masks/distancing
and other attributes explained in commentation of the program source

the simulation runs a selected amount of days, and each day runs multiple encounters based on user activity level

This is a diagram showing the general idea of 'Encounters'
each '0' represents a person, and each 'x' represents an infected person.

[ x , 0 , 0, 0, 0, 0, x, 0, 0, 0, 0, 0, 0]
each x has a chance to infect the adjacent people in the encounter. when an encounter ends, all active people are shuffled around. let's assume the next encounter is this.

[0, x, 0, 0, 0, x, 0, 0, x, 0, 0 | 0, 0]
the bar on the right represents people who are 'at home'. they will no longer infect anyone or be infected for that day. as the day progresses, more people will move into the 'at home' section.

[ 0, 0, 0, 0, x, 0, 0, x, |0, 0, x, 0, 0]
the encounters will continue until the most active person is done interacting for the day and the 'at home' bar is all the way to the left.

[|0, 0, 0, x, 0, x, 0, 0, 0, x, 0, 0, 0]

When the day ends, each infected person will have a chance of dying based on their health risk and customized user input settings. If a person who has been infected for 14 days is still alive by then, they will be considered 'immune' and can no longer be infected, die by the disease, or infect others.
Multiple days will be run this way until the program ends, and the data is graphed.
 




