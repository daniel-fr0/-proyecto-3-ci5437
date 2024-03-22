from src.JSON_to_SAT import getTournamentInfo, generateCNF
from src.SAT_to_calendar import solve, getCalendar

info = getTournamentInfo("torneo.json")
generateCNF(info, "torneo.cnf")
sol = solve("glucose", "torneo.cnf")
if not sol:
	print("No hay solución")
	exit()

calendario = getCalendar(info, sol)

print(f'{calendario.name}:')
for event in sorted(list(calendario.events), key=lambda x: x.begin):
	print(f'{event.name}\t{event.begin.strftime("%d/%m/%y")}\t{event.begin.strftime("%H")}:00 - {event.end.strftime("%H")}:00')

with open("torneo.ics", "w") as f:
	f.write(calendario.serialize())