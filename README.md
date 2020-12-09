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


## Task 2 

Problem: Niska waga urodzeniowa

Szef oddziału pediatrycznego w szpitalu miejskim w X stwierdził, że niska waga urodzeniowa (lbw – ang. low birth weight) może mieć negatywny wpływ na szanse przeżycia dziecka pierwszego roku. Rozważa rozpoczęcie programu, która pomoże kobietom w ciąży lepiej dbać o własne zdrowie, dzięki czemu zwiększa się szansa, aby ich dzieci rodziły się z prawidłową wagą urodzeniową. Przed przystąpieniem do realizacji programu, który wymaga znaczących nakładów finansowych, doktor chce się upewnić, że niska masa urodzeniowa rzeczywiście ma wpływ na zdrowie niemowląt, a zwłaszcza na ich szanse na przeżycie. Jego pytanie brzmi:

    „Czy niska waga urodzeniowa naprawdę zmniejsza szanse na przeżycie dziecka powyżej jego pierwszych urodzin?”

Do realizacji zadań dysponujesz danymi lbw (pliki singletons – ciąże pojedyncze oraz twins – ciąże bliźniacze, opis w pliku lbv.csv). Jest to publicznie dostępny zbiór danych powiązanych z danymi dotyczącymi narodzin i zgonów niemowląt. Każda linia pliku dotyczy jednego przypadku niemowlęcia i zawiera dane o dacie urodzenia oraz śmierci niemowlęcia, jeśli zmarł w ciągu roku. Zawiera również informacje o matce i ojcu. 

Przyjmujemy, że niska masa urodzeniowa oznacza dbirwt < 2700 gram (wówczas należy przyjąć lbw=1, w przeciwnym przypadku lbw=0), zaś zmienną wyjściową (outcome) jest śmiertelność (mortality, mort=1 / mort=0)

### Zadanie 2.1 (ocena 3)

2.1.1 Poprzedni asystent sugerował zbadanie wpływu niskiej masy urodzeniowej na populację bliźniaków. Na podstawie analizy danych wyjaśnij lekarzowi, z czego mogło wynikać skupienie się na bliźniakach? Użyj danych lbw, aby oszacować średni wpływ niskiej masy urodzeniowej na śmiertelność w ciągu roku dla populacji bliźniaków. Aby to zrobić skutecznie, przeanalizuj przypadki bliźniaków, w których tylko jeden z nich znajduje się poniżej progu wagowego. 

2.1.2 Czy ten średni wpływ można uogólnić na całą populację, w tym niemowlęta z ciąży pojedynczych? Czyli: Czy możemy założyć, że średni wpływ lbw w populacji niemowląt z ciąży pojedynczych jest taki sam, jak z ciąży bliźniaczych?

> Wskazówka: oblicz współczynniki śmiertelności wśród bliźniaków i populacji niemowląt z ciąży pojedynczych.

### Zadanie 2.2 (ocena 4)

Szef oddziału pediatrycznego stwierdził, że chciałby nieco rozszerzyć swoje pytanie. Wyjaśnia, że ​​jego program byłby bezpośrednio ukierunkowany na rzucenie palenia wśród kobiet w ciąży, ponieważ wykazano, że dzieci urodzone przez kobiety, które palą podczas ciąży, są bardziej narażone na lbw. Jeśli palenie u matki naprawdę powoduje, że dzieci rodzą się z mniejszą wagą, program doktora byłby przydatny. Do analizy użyj danych dotyczących niemowląt z ciąż pojedynczych.

Przeprowadź analizę współzależności (np. metodą regresji), aby ocenić wpływ palenia u matki na masę urodzeniową dziecka. 

### Zadanie 2.3 (ocena 5)

Zweryfikuj, jakie inne czynniki spośród badanych parametrów, mogą mieć wpływ na niską masę urodzeniową. Oprócz raportu z analizy przygotuj wyjaśnienie, jakich metod z zakresu statystycznej analizy danych i metod uczenia maszynowego mógłbyś użyć, jakie w rezultacie zostały wybrane i dlaczego.