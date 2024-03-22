from src.JSON_to_SAT import getTournamentInfo, generateCNF
from src.SAT_to_calendar import solve, getCalendar

info = getTournamentInfo("torneo.json")
generateCNF(info, "torneo.cnf")
sol = solve("glucose", "torneo.cnf")
calendario = getCalendar(info, sol)

for event in sorted(list(calendario.events), key=lambda x: x.begin):
	print(f'{event.name}\t\t{event.begin.strftime("%d/%m")}\t\tdesde las {event.begin.strftime("%H")} hasta las {event.end.strftime("%H")}')

with open("torneo.ics", "w") as f:
	f.write(calendario.serialize())