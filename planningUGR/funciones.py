from datetime import datetime,date,time
from datetime import time
from dateutil import tz
from datetime import date
from datetime import datetime
import calendar
import bd_bot
import os # para borrar graficas
import glob  # para borrar graficas


def borrar_graficas():
	files = glob.glob('graficas/*.png')
	for f in files:
		os.remove(f)


def dia_prox():
	now = datetime.now()
	anio = now.year   # Año.
	mes = now.month  # Mes.
	dia = now.day
	ultimodiames = calendar.monthrange(anio, mes)[1]
	if ultimodiames == dia:
		dia = 0
		mes = mes + 1
		if(mes == 12):
			mes = 1
			anio = anio + 1
	dia = dia+1
	fecha = "{}-{}-{}".format(dia,mes,anio)
	# print('fecha mañana ',fecha)
	return fecha

def calcular_semana_prox():
	#fecha_hoy = datetime.strptime('3-2-2020', "%d-%m-%Y")# para pruebas test NO BORRAR
	fecha_hoy = date.today() # obtiene la fecha actual
	dia_hoy = fecha_hoy.day
	mes = fecha_hoy.month
	anio = fecha_hoy.year
	ultimodiames = calendar.monthrange(anio, mes)[1] # obtiene el ultimo dia del mes
	# print('ultimodiames', ultimodiames)
	# print('fecha de hoy', fecha_hoy)
	dia_semana = date.today().weekday() # Devuelve el día de la semana como un entero, donde el lunes es 0 y el domingo es 6.
	#dia_semana = fecha_hoy.weekday() # para pruebas test NO BORRAR
	# print('diahoy',dia_hoy)
	if dia_semana == 0: # si es lunes
		dia_hoy += 7
		if dia_hoy > ultimodiames:
			dia_hoy = dia_hoy - ultimodiames
			mes = mes+1
			if(mes == 13):
				mes = 1
				anio = anio+1
	elif dia_semana == 1:
		dia_hoy += 6
		if dia_hoy > ultimodiames:
			dia_hoy = dia_hoy - ultimodiames
			mes = mes+1
			if(mes == 13):
				mes = 1
				anio = anio+1
	elif dia_semana == 2:
		dia_hoy += 5
		if dia_hoy > ultimodiames:
			dia_hoy = dia_hoy - ultimodiames
			mes = mes+1
			if(mes == 13):
				mes = 1
				anio = anio+1
	elif dia_semana == 3:
		dia_hoy += 4
		if dia_hoy > ultimodiames:
			dia_hoy = dia_hoy - ultimodiames
			mes = mes+1
			if(mes == 13):
				mes = 1
				anio = anio+1
	elif dia_semana == 4:
		dia_hoy += 3
		if dia_hoy > ultimodiames:
			dia_hoy = dia_hoy - ultimodiames
			mes = mes+1
			if(mes == 13):
				mes = 1
				anio = anio+1
	elif dia_semana == 5:
		dia_hoy += 2
		if dia_hoy > ultimodiames:
			dia_hoy = dia_hoy - ultimodiames
			mes = mes+1
			if(mes == 13):
				mes = 1
				anio = anio+1
	elif dia_semana == 6:
		dia_hoy += 1
		if dia_hoy > ultimodiames:
			dia_hoy = dia_hoy - ultimodiames
			mes = mes+1
			if(mes == 13):
				mes = 1
				anio = anio+1


	# print('dia semana siguiente',dia_hoy)
	fecha = "{}-{}-{}".format(dia_hoy,mes,anio)
	# print('fecha final devuelta',str(fecha))

	return fecha

# Funciones para las tareas pendientes por prioridad

def tareaspendientes_prioridad(id_usuario):
	msg = ''
	datos1 = bd_bot.leer_tareas_prioridad1(id_usuario)
	datos2 = bd_bot.leer_tareas_prioridad2(id_usuario)
	datos3 = bd_bot.leer_tareas_prioridad3(id_usuario)

	if datos1:
		msg +="\n<b>➖ Prioridad alta</b>\n"
		for x in datos1:
			msg += "🛑 {}\n".format(x[2])
	if datos2:
		msg +="\n<b>➖ Prioridad media</b>\n"
		for x in datos2:
			msg += "✴️ {}\n".format(x[2])
	if datos3:
		msg +="\n<b>➖ Prioridad baja</b>\n"
		for x in datos3:
			msg += "❇️ {}\n".format(x[2])

	return msg


def premios_rutina(id):
	msg = ''
	datos = bd_bot.leer_rutinas(id)
	texto = 'Has conseguido: '
	puntuacion = ''
	if(datos):
		for data in datos:
			# print('puntos',str(data[0]))
			if(int(data[7]) >= 15 and int(data[7]) < 30 ):
				premio = '🏅'
			elif(int(data[7]) >= 30 and int(data[7]) < 45 ):
				premio = '🏅🏅'
			elif(int(data[7]) >= 45 and int(data[7]) < 60 ):
				premio = '🏅🏅🏅'
			elif(int(data[7]) >= 60 and int(data[7]) < 75 ):
				premio = '🏅🏅🏅🏅'
			elif(int(data[7]) >= 75):
				premio = '🏅🏅🏅🏅🏅'
			else:
				# premio ="Por ahora no has conseguido ninguna estrella, realizada rutinas. Si eres constante con tus rutinas, obtendrás mejores premios"
				premio = "❌"
			puntuacion += "🔹 {}".format(data[2]) + ": " + str(premio) + "\n"
		return puntuacion
	else:
		puntuacion = 'No podemos obtener su puntuación si no realiza sus rutinas'
		return puntuacion

def premios_tarea(id):
	msg = ''
	datos = bd_bot.leer_tareas_suma(id)
	datos2 = bd_bot.leer_tareas_completadas(id)
	puntuacion = '0'
	texto = 'Has conseguido: '
	print('dats',datos)
	if(datos2):
		for data in datos:
			# print('puntos',str(data[0]))
			if(int(data[0]) >= 100):
				puntuacion = '⭐'

			elif(int(data[0]) >= 150):
				puntuacion = '⭐⭐'

			elif(int(data[0]) >= 200):
				puntuacion = '⭐⭐⭐'

			elif(int(data[0]) >= 250):
				puntuacion = '⭐⭐⭐⭐'
			elif(int(data[0]) >= 300):
				puntuacion = '⭐⭐⭐⭐⭐'
			elif(int(data[0]) < 100):
				puntuacion = '0 estrellas, completa más tareas y conseguirás tu primera ⭐'
			else:
				puntuacion ="Por ahora no has conseguido ninguna estrella, realizada tareas. Al completar tareas de mayor prioridad podrás obtener más estrellas.",
		puntuacion = texto + puntuacion
		return puntuacion
	else:
		puntuacion = 'No podemos obtener su puntuación si no completa tareas'
		return puntuacion

def tareascompletadas(id):
	msg = ''
	datos = bd_bot.leer_tareas_completadas(id)
	if datos:
		for x in datos:
			msg += " 🔹 {}\n".format(x[2])
	else:
		msg += "No has completado ninguna tarea \n"
	return msg

def obtener_categorias(id_usuario):
	datos = bd_bot.leer_categorias_rutina(id_usuario)
	datos2 = bd_bot.contar_categorias_usuario(id_usuario)
	msg = ''

	for data in datos:
				if(data[2] == 'Ocio' and data[1] == id_usuario):
					datos2 = bd_bot.leer_categorias_rutina_usuario(id_usuario)
					for data2 in datos2:
						msg += "🔹 {}".format(data[2] + "\n")
				else:
					msg += "🔹 {} ".format(data[2] + "\n")

	return msg

def rutinaspendientes(id_usuario):
	msg = ''

	datos = bd_bot.leer_rutinas(id_usuario)
	if datos:
		i = 1
		msg += "➖➖➖➖➖➖➖➖\n"
		for x in datos:
			msg += "🔹 {}\n".format(x[2])
	else:
		msg += "No tienes rutinas pendientes\n"
	return msg

# Funciones para las tareas pendientes por fecha


def tareaspendientes_fecha(id_usuario):
	msg = ''
	datos1 = bd_bot.leer_tareas(id_usuario)
	#mañana
	now = datetime.now()
	fecha_hoy = now.day
	fecha_ma = now.day+1
	hay = False
	if datos1:
		msg +="\n<b>➡ Pendientes hoy </b>\n"
		for x in datos1:
			fecha = datetime.strptime(x[4], "%d-%m-%Y")
			#
			if(fecha.day == fecha_hoy and fecha.month == now.month and fecha.year == now.year):
				msg += "🔹 {} - ".format(x[4]) + "{}\n".format(x[2])
		if(fecha.day != fecha_hoy and fecha.month != now.month and fecha.year != now.year):
			msg += "No tienes tareas pendientes para hoy\n"

		msg +="\n<b>➡ Próximas </b>\n"
		for x in datos1:
			fecha = datetime.strptime(x[4], "%d-%m-%Y")
			if(fecha.day != fecha_hoy):
				hay = True
				msg += "🔹 {} - ".format(x[4]) + "{}\n".format(x[2])
		if not hay:
			msg += "No tiene tareas pendientes próximamente"

	return msg

# Función para fecha cuando no queremos una fecha incorrecta ni pasada
def valida_fecha(fecha):
	try:
		fecha_hoy = date.today()
		dee = datetime.strptime(fecha, '%d-%m-%Y')
		anio = dee.year
		mes = dee.month
		dia = dee.day
		fecha_int = date(anio,mes,dia)
		if(date):
			if( fecha_int < fecha_hoy):
				return False
			else:
				return True
	except ValueError:
		return False

#Función para validar fecha incluyendo fechas pasadas para la búsqueda por fecha en tareas
def valida_fecha_busqueda(fecha):
	try:
		fecha_hoy = date.today()
		dee = datetime.strptime(fecha, '%d-%m-%Y')
		anio = dee.year
		mes = dee.month
		dia = dee.day
		fecha_int = date(anio,mes,dia)
		if(date):
			return True
	except ValueError:
		return False


def valida_hora(hora):
	try:
		datetime.strptime(hora, "%H:%M")
		return True
	except ValueError:
		return False

def valida_entero(numero):
	try:
		if(int(numero) > 0):
			return True
		elif(float(numero)):
			print('hola soy float')
	except ValueError:
		return False


def valida_float(numero):
	try:
		if(float(numero) > 0):
			return True
	except ValueError:
		return False

def obtener_fecha_actual():
	now = datetime.now()
	anio = now.year   # Año.
	mes = now.month  # Mes.
	dia = now.day
	fecha = "{}-{}-{}".format(dia,mes,anio)
	# print('fecha actual',str(fecha))
	return fecha
