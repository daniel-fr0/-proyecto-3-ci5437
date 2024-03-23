from src.JSON_to_SAT import getTournamentInfo, generateCNF
from src.SAT_to_calendar import solve, getCalendar
from sys import argv

if len(argv) != 2:
	print("Uso: python main.py <torneo.json>")
	exit()

basename = argv[1].split(".")[0]
info = getTournamentInfo(argv[1])
generateCNF(info, f"{basename}.cnf")
sol = solve("glucose", f"{basename}.cnf")
if not sol:
	print("No hay solución")
	exit()

calendario = getCalendar(info, sol)

print(f'{calendario.name}:')
for event in sorted(list(calendario.events), key=lambda x: x.begin):
	print(f'{event.name}\t{event.begin.strftime("%d/%m/%y")}\t{event.begin.strftime("%H")}:00 - {event.end.strftime("%H")}:00')

with open(f"{basename}.ics", "w") as f:
	f.write(calendario.serialize())