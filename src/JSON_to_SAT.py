import json, datetime

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

	# cantidad de variables
	N = n * (n-1) * p * q

	# restricciones
	# 1. Todos los participantes deben jugar con todos los demas 2 veces (ida y vuelta)
	# 2. Un participante no puede jugar consigo mismo
	# 3. Dos juegos no pueden ocurrir al mismo tiempo
	# 4. Un participante no puede jugar dos veces en un mismo dia
	# 5. Un participante no puede jugar dos veces seguidas como local o visitante
	clauses = []

	for i in range(n):
		for j in range(i+1,n):
			# existe por lo menos un partido entre cada par de participantes
			posible_local = []
			posible_visit = []	

			for k in range(p):
				for l in range(q):
					# para un i y j dados, se propone un partido local y uno visitante
					local = i * n * p * q + j * p * q + k * q + l + 1	# i-j-k-l
					visit = j * n * p * q + i * p * q + k * q + l + 1   # j-i-k-l

					# para un i y j dados, tiene que haber un partido local y uno visitante
					posible_local.append(local)
					posible_visit.append(visit)

					# pero no pueden ser al mismo tiempo, alguno debe ser false
					clauses.append([-local, -visit, 0])

					# el dia siguiente no pueden jugar de nuevo como local o visitante
					if k < p-1:
						# local
						clauses.append([-local, -(local + q), 0])	# i-j-k-l -> i-j-k+1-l
						# visitante
						clauses.append([-visit, -(visit + q), 0])	# j-i-k-l -> j-i-k+1-l

					for l2 in range(l+1,q):
						# no se puede repetir a otra hora el mismo dia
						local2 = i * n * p * q + j * p * q + k * q + l2 + 1	# i-j-k-l2
						visit2 = j * n * p * q + i * p * q + k * q + l2 + 1	# j-i-k-l2

						clauses.append([-local, -local2, 0])	# i-j-k-l -> i-j-k-l2
						clauses.append([-visit, -visit2, 0])	# j-i-k-l -> j-i-k-l2

					for k2 in range(k+1,p):
						for l2 in range(q):
							# no se puede repetir en otro dia a cualquier hora
							local2 = i * n * p * q + j * p * q + k2 * q + l2 + 1	# i-j-k2-l2
							visit2 = j * n * p * q + i * p * q + k2 * q + l2 + 1	# j-i-k2-l2

							clauses.append([-local, -local2, 0])	# i-j-k-l -> i-j-k2-l2
							clauses.append([-visit, -visit2, 0])	# j-i-k-l -> j-i-k2-l2

			# al menos un partido como local y uno como visitante
			clauses.append(posible_local + [0])
			clauses.append(posible_visit + [0])

	for k in range(p):
		for l in range(q):
			# no pueden haber dos partidos al mismo tiempo
			for i1 in range(n):
				for j1 in range(n):
					if i1 == j1: continue  # un equipo no puede jugar contra sí mismo
					for i2 in range(n):
						for j2 in range(n):
							if i2 == j2: continue  # un equipo no puede jugar contra sí mismo
							if i1 == i2 and j1 == j2: continue  # el mismo partido no puede ser comparado consigo mismo
							# partido 1
							partido1 = i1 * n * p * q + j1 * p * q + k * q + l + 1
							# partido 2
							partido2 = i2 * n * p * q + j2 * p * q + k * q + l + 1
							# no pueden haber dos partidos al mismo tiempo
							clauses.append([-partido1, -partido2, 0])

	# archivo con el CNF en formato DIMACS
	with open(outputFile, 'w') as f:
		f.write(f'p cnf {N} {len(clauses)}\n')
		for clause in clauses:
			f.write(' '.join(map(str, clause)) + '\n')