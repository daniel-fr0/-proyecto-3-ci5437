import subprocess, datetime
from ics import Calendar, Event

def solve(solver, inputFile):
	# Comando a ejecutar - reemplaza esto con el comando real
	comando = [f"./{solver}", inputFile]

	# Ejecuta el comando y captura su salida
	resultado = subprocess.run(comando, capture_output=True, text=True)

	# Obtiene la salida de stdout
	salida = resultado.stdout.split("\n")[-2].split(" ")

	# Si es UNSAT, devuelve una lista vacía
	if salida[1] == "UNSATISFIABLE":
		return []

	# Devuelve los valores como una lista de enteros
	valores = list(map(int, salida[1:]))
	return valores

def getCalendar(info, solucion):
	campeonato = info['campeonato']
	participantes = info['participantes']
	dias = info['dias']
	horas = info['horas']

	# Crea un diccionario para almacenar los partidos
	partidos = {}

	n = len(participantes)
	p = len(dias)
	q = len(horas)

	calendario = Calendar()
	calendario.name = campeonato

	# Itera sobre la solución
	for idx in solucion:
		if idx < 0:
			continue
		# Resta 1 de idx para convertirlo a base 0
		idx0 = idx - 1

		# Calcula los índices
		i = idx0 // (n * p * q)
		j = (idx0 % (n * p * q)) // (p * q)
		k = ((idx0 % (n * p * q)) % (p * q)) // q
		l = ((idx0 % (n * p * q)) % (p * q)) % q

		# Obtiene los nombres de los participantes y las fechas
		participante1 = participantes[i]
		participante2 = participantes[j]
		fecha = dias[k]
		hora = horas[l]

		# Crea nuevo evento para el calendario
		partido = Event()
		partido.name = f'{participante1} vs {participante2}'
		partido.begin = f'{fecha.date()} {hora.time()}'
		partido.end = f'{fecha.date()} {(hora + datetime.timedelta(hours=2)).time()}'

		# Agrega el evento al calendario
		calendario.events.add(partido)

	return calendario