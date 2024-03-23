import json, datetime
import numpy as np
from itertools import product

def getTournamentInfo(inputFile):
	with open(inputFile) as f:
		data = json.load(f)

	campeonato = data['tournament_name']
	participantes = data['participants']
	
	# calculo cuantos dias hay en el torneo a partir de la fecha de inicio y fin
	start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d')
	end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d')
	duracion = (end_date - start_date).days + 1

	dias = []
	for i in range(duracion):
		dias.append(start_date + datetime.timedelta(days=i))

	# calculo cuantos partidos se pueden jugar en un dia, los partidos duran 2 horas
	start_time = datetime.datetime.strptime(data['start_time'], '%H:%M:%S')
	end_time = datetime.datetime.strptime(data['end_time'], '%H:%M:%S')

	# las horas deben ser en punto
	if start_time.minute != 0 or start_time.second != 0:
		start_time = start_time.replace(minute=0, second=0)
		start_time += datetime.timedelta(hours=1)

	if end_time.minute != 0 or end_time.second != 0:
		end_time = end_time.replace(minute=0, second=0)

	partidos = (end_time - start_time).seconds // 3600 // 2

	horas = []
	for i in range(partidos):
		horas.append(start_time + datetime.timedelta(hours=i*2))
		
	return {
		'campeonato': campeonato,
		'participantes': participantes,
		'dias': dias,
		'horas': horas
	}

def generateCNF(info, outputFile):
	participantes = info['participantes']
	dias = info['dias']
	horas = info['horas']

	# las variables son de tipo "local-visitante-dia-hora"
	# la cantidad es participantes * (participantes-1) * dias * horas
	n = len(participantes)
	p = len(dias)
	q = len(horas)

	class Match:
		def __init__(self, local, visit, dia, hora):
			self.i = local
			self.j = visit
			self.dia = dia
			self.hora = hora
			self.idx = local * (n * p * q) + visit * (p * q) + dia * q + hora + 1

	# cantidad de variables
	N = n * (n-1) * p * q

	# restricciones
	# 1. Todos los participantes deben jugar con todos los demas 2 veces (ida y vuelta)
	# 2. Un participante no puede jugar consigo mismo
	# 3. Dos juegos no pueden ocurrir al mismo tiempo
	# 4. Un participante no puede jugar dos veces en un mismo dia
	# 5. Un participante no puede jugar dos veces seguidas como local o visitante
	clauses = []


	# 1. Todos los participantes deben jugar con todos los demas 2 veces (ida y vuelta)
	# 2. Un participante no puede jugar consigo mismo
	for i, j in product(range(n), range(n)):
		if i == j: continue
		local = [Match(i, j, d, h) for d, h in product(range(p), range(q))]
		visit = [Match(j, i, d, h) for d, h in product(range(p), range(q))]

		clauses.append([m.idx for m in local] + [0])
		clauses.append([m.idx for m in visit] + [0])

		# solo un juego i vs j
		for m1, m2 in product(local, local):
			if m1.dia != m2.dia or m1.hora != m2.hora:
				clauses.append([-m1.idx, -m2.idx, 0])

		for m1, m2 in product(visit, visit):
			if m1.dia != m2.dia or m1.hora != m2.hora:
				clauses.append([-m1.idx, -m2.idx, 0])

	# 3. Dos juegos no pueden ocurrir al mismo tiempo
	for d, h in product(range(p), range(q)):
		horarios = [Match(i, j, d, h) for i, j in product(range(n), range(n)) if i != j]

		for m1, m2 in product(horarios, horarios):
			if m1.i != m2.i or m1.j != m2.j:
				clauses.append([-m1.idx, -m2.idx, 0])

	# 4. Un participante no puede jugar dos veces en un mismo dia
	for i, d in product(range(n), range(p)):
		partidosLocal = [Match(i, j, d, h) for j, h in product(range(n), range(q)) if i != j]
		partidosVisit = [Match(j, i, d, h) for j, h in product(range(n), range(q)) if i != j]

		for m1, m2 in product(partidosLocal, partidosLocal):
			if m1.j != m2.j or m1.hora != m2.hora:
				clauses.append([-m1.idx, -m2.idx, 0])

		for m1, m2 in product(partidosVisit, partidosVisit):
			if m1.i != m2.i or m1.hora != m2.hora:
				clauses.append([-m1.idx, -m2.idx, 0])

		for m1, m2 in product(partidosLocal, partidosVisit):
			if m1.hora != m2.hora:
				clauses.append([-m1.idx, -m2.idx, 0])

	
	# 5. Un participante no puede jugar dos dias seguidos como local o visitante
	for i, d in product(range(n), range(p-1)):
		partidosLocal = [Match(i, j, d, h) for j, h in product(range(n), range(q)) if i != j]
		partidosVisit = [Match(j, i, d, h) for j, h in product(range(n), range(q)) if i != j]

		partidosLocalNext = [Match(i, j, d+1, h) for j, h in product(range(n), range(q)) if i != j]
		partidosVisitNext = [Match(j, i, d+1, h) for j, h in product(range(n), range(q)) if i != j]

		for m1, m2 in product(partidosLocal, partidosLocalNext):
			clauses.append([-m1.idx, -m2.idx, 0])

		for m1, m2 in product(partidosVisit, partidosVisitNext):
			clauses.append([-m1.idx, -m2.idx, 0])

	# archivo con el CNF en formato DIMACS
	with open(outputFile, 'w') as f:
		f.write(f'p cnf {N} {len(clauses)}\n')
		for clause in clauses:
			f.write(' '.join(map(str, clause)) + '\n')

	# retorna la cantidad de variables y restricciones
	return N, len(clauses)