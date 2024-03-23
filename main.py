from src.JSON_to_SAT import getTournamentInfo, generateCNF
from src.SAT_to_calendar import solve, getCalendar
from sys import argv

if len(argv) < 2:
	print("Uso: python main.py <torneo.json> [solver]")
	exit()

print("Generando archivo CNF...")

# Transformar el JSON a CNF
basename = argv[1].split(".")[0]
basename = basename.split("/")[-1]
info = getTournamentInfo(argv[1])
variables, clausulas = generateCNF(info, f"{basename}.cnf")

print(f"Se generó el archivo {basename}.cnf")

print(f"{len(info['participantes'])} participantes")
print(f"{len(info['dias'])} días")
print(f"{len(info['horas'])} horas")

print(f"Resolviendo SAT de {variables} variables y {clausulas} cláusulas...")

# Resolver el problema de SAT
solver = 'glucose' if len(argv) < 3 else argv[2]
sol = solve(solver, f"{basename}.cnf")

print('SATISFACIBLE' if sol else 'UNSATISFACIBLE')
if not sol:
	print("No hay solución")
	exit()

print("Generando calendario...")

calendario = getCalendar(info, sol)

print()
print('#' * 80)
print()
print(f'\t{calendario.name}\n')
print('#' * 80)
print()
print('\tJuego(local vs visitante)\tFecha\t\tHora\n')

for event in sorted(list(calendario.events), key=lambda x: x.begin):
	print(f'\t{event.name}\t\t\t{event.begin.strftime("%d/%m/%y")}\t{event.begin.strftime("%H")}:00 - {event.end.strftime("%H")}:00')
print()

with open(f"ICS/{basename}.ics", "w") as f:
	f.write(calendario.serialize())

print(f"Se generó el archivo {basename}.ics con el calendario del torneo '{calendario.name}'")