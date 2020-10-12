# ZIMed

<img src="https://static.dwcdn.net/css/flag-icons/flags/4x3/pl.svg" height="10" width="20"> Laboratoria z **Zastsowania Informatyki w Medycynie** na Politechnice Łódzkiej (PŁ). Więcej informacji o przedmiocie: [karta przedmiotu](https://programy.p.lodz.pl/ectslabel-web/przedmiot_3.jsp?l=pl&idPrzedmiotu=172846&pkId=1149&s=2&t=1&j=0&w=informatyka%20stosowana).

<img src="https://static.dwcdn.net/css/flag-icons/flags/4x3/gb.svg" height="10" width="20"> **Computer Applications in Medicine** classes at Lodz University of Technology (TUL).

---

## Task 1

Problems and Tasks:

1. Use the us_contagious_disease.csv to create an object that stores only the Measles data, includes a per 100,000 people rate, and removes Alaska and Hawaii since they only became states in the late 50s. Note that there is a weeks_reporting column. Take that into account when computing the rate.

2. Plot the Measles disease rate per year for California. Find out when the Measles vaccine was introduced and add a vertical line to the plot to show this year. Seaborn for Python is recommended for plots

3. Note these rates start off as counts. For larger counts we can expect more variability. There are statistical explanations for this which we don't discuss here. But transforming the data might help stabilize the variability such that it is closer across levels. For 1950, 1960, and 1970, plot the histogram of the data across states with and without the square root transformation. Which seems to have more similar variability across years? Make sure to pick binwidths that result in informative plots.

4. Plot the Measles disease rate per year for California. Use the square root transformation. Find out when the Measles vaccine was introduced and add a vertical line to the plot to show this year. Does the pattern hold for other states? Use boxplots to get an idea of the distribution of rates for each year and see if the pattern holds across states. One problem with the boxplot is that it does not let us see state-specific trends. Make a plot showing the trends for all states. Add the US average to the plot.

    > Note 1: Note there are missing values in the data.

    > Note 2: Experiment with different plots  to distinguish states from each other and to make the whole plot more readable.

5. Prove hypotheses on effectiveness of vaccines for different diseases (at least 3 including the Measles disease). Use appropriate tests and provide statistical significance of your tests.
