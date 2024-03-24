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

# Actividad 3
El cliente implementado en `main.py` recibe un JSON con el formato de entrada, ejecuta el programa que lo transforma en CNF, se guarda en un archivo con el mismo nombre pero extension `.cnf` en el directorio `CNF`. Luego el programa resuelve el problema con Glucose y se asegura de que se cree el archivo con el mismo nombre y extension `.ics` con la respuesta, o falle en caso de ser UNSAT.

Se incluyen archivos de prueba en el directorio `casosDePrueba` con los cuales se puede probar el programa.

## Conclusiones
Los resultados de los casos de prueba se pueden encontrar en `resultados`.
De los resultados obtenidos podemos ver en practica que el uso de heuristicas y algoritmos de busqueda de conflictos como los estudiados en clase e implementados en Glucose, permiten resolver problemas de satisfaccion de restricciones de manera eficiente y rapida. Esto porque en los casos donde se obtiene una solucion son mucho mas rapidos que los casos donde no se obtiene una solucion, lo que indica que el algoritmo es capaz de mejorar la busqueda usando las heuristicas y busqueda de conflictos para encontrar la solucion con el menor numero de backtracks posibles.

## Modo de uso
Para instalar las dependencias, se debe correr el siguiente comando:
```bash
pip install -r requirements.txt
```

Para ejecutar el programa, se debe correr el siguiente comando:
```bash
python main.py <archivo_entrada>.json [solver]
```
Se puede especificar el solver a utilizar, por defecto se utiliza Glucose. Para utilizar glucose-syrup se debe especificar `solver` como `syrup`.

El archivo `.cnf` se guardara en el directorio `CNF` y el archivo `.ics` se guardara en el directorio `ICS`.