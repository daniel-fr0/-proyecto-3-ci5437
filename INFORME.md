# Actividad 1
Para traducir el problema a formato CNF, se definen las variables como los posibles juegos que pueden ocurrir en el torneo. Cada juego es una tupla de 4 elementos:
- El primer elemento es el participante local.
- El segundo elemento es el participante visitante.
- El tercer elemento es la fecha del juego.
- El cuarto elemento es la hora del juego.

Por lo tanto la variable $x_{i,j,k,l}$ representa el juego entre el participante `i` y el participante `j` en la fecha `k` y la hora `l`.

Para cumplir con las restricciones de los dias y los horarios en los que pueden ocurrir los juegos, se calculan los horarios por indice, empezando desde la primera hora posible y contando cuantos juegos de 2 horas se pueden realizar en el rango de horas especificado. Luego se calculan los dias por indice, empezando desde la fecha de inicio y contando cuantos dias hay entre la fecha de inicio y la fecha de fin.

Para cumplir con la restriccion de que no puede haber un juego entre el mismo jugador, es decir que no puede haber un juego entre el participante `i` y el participante `i`, no se agregan las variables $x_{i,i,k,l}$ al conjunto de variables. Por lo que el numero de variables es $n*(n-1)*d*h$ donde $n$ es el numero de participantes, $d$ es el numero de dias y $h$ es el numero de horas posibles.

Una vez con las variables y las clausulas definidas, se procede a escribir el archivo DIMACS CNF. 

# Actividad 2
Una vez con el problema en formato DIMACS CNF, se procede a resolverlo con el SAT solver Glucose. Para ello se crea un programa en Python que se encarga de llamar a Glucose y obtener la asignacion de las variables. Las variables con valores positivos representan una asignacion verdadera, por lo que estos representan los juegos que se van a realizar.

Se traduce la asignacion de las variables a un archivo con extension `.ics` en formato de iCalendar. Para ello se crea un objeto `Calendar` de la libreria `icalendar` y se agregan los eventos correspondientes a la asignacion de los juegos.
Los eventos tienen su hora asignada, la fecha del juego, el participante local y el participante visitante. El nombre que reciben es `{local} vs {visitante}`, la hora de inicio es la hora asignada y la de fin es la hora asignada mas 2 horas.