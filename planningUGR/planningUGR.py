#!/usr/bin/python3.7
# -*- coding: utf-8 -*-

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup,Update
from telegram.ext import Updater, CommandHandler, MessageHandler,Filters,CallbackQueryHandler, ConversationHandler, CallbackContext
import logging
import sqlite3
import bd_bot # archivo bd
from matplotlib import pyplot  # gráficas
from datetime import datetime,date,time # fecha y hora
from dateutil import tz
import calendar #para obtener el dia de la semana
import re
import funciones
from config.auth import token

import calendar
################################### HABITLITAR LOG ####################################

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)

logger = logging.getLogger(__name__)


################################### ESTADOS ####################################

#utilizaron la función de rango para crear una lista

# ESTADOS & CALLBACK
# Función range para crear la lista

MENU_PRINCIPAL,MENU_LOGROS,MENU_BUSCADOR,GESTION_TAREAS,MENU_AYUDA, PREGUNTA2_TAREAS, \
PRIORIDADES_TAREA, PREGUNTA4_TAREAS,PREGUNTA_COMENT,PREGUNTA5_TAREAS,OBTIENE_ID_TAREA, \
EDICIONES_TAREA,EDITANOMBRE1,EDITAPRIORIDAD,EDITANOMBRE22,EDITANOMBRE3,ALARM_MHORA,\
ALARM_PHORA,ALARM_ELIGEH,ALARM_ELIGEG,RUTINAS_GESTION,PREGUNTA11_RUTINAS,PREGUNTA2_RUTINAS,\
PREGUNTA3_RUTINAS,PREGUNTA4_RUTINAS,HORAS_RUTINA,PREGUNTA5_RUTINAS,OBTIENE_ID_RUTINA, \
GUARDAR_CATEGORIA,EDICIONES_RUTINA,EDICIONES_RUTINA_HORAS,EDITANOMBRE1R,EDITANOMBRE2R,EDITANOMBRE3R,EDITANOMBRE4R,\
GESTION_AYUDA,ELIMINACION_RUTINA,OPCIONES_GUIA_RAPIDA,ENVIAR_MENSAJE,GESTION_LOGROS, \
GESTION_BUSCADOR,VISUALIZAR_CATEGORIAS,RESULTADO_BNOMBRE,TAREAS,MENU_TAREAS,EDICION_TAREAS,TAREAS_PORFECHA,VOLVER_MENU_PRINCIPAL,VOLVER_MENU_TAREAS_P, \
VOLVER_MENU_TAREAS_F,FINALIZAR,PRIORIDAD_ALTA,PRIORIDAD_MEDIA,PRIORIDAD_BAJA,COMENT_TAREA_SI, \
COMENT_TAREA_NO,EDICION,EDICION2,EDICION22,EDICION3,ESTADO_TAREA,VOLVER_MENU_TAREAS_P, \
RECORDATORIO_TAREA,RECORDATORIO_TAREA,ELIMINAR_TAREA_ACTUAL, \
ALARMA_MANIANA,ALARMA_SEMANAPROX,ALARMA_ELEGIRFECHA,MENU_RUTINAS,RUTINAS,CATEGORIAS_RUTINA, \
NUEVA_CATEGORIA,EDICION_RUTINAS,VOLVER_MENU_PRINCIPAL,VOLVER_MENU_RUTINAS,CATEGORIAS_USUARIOG,\
PREGUNTA6_RUTINAS,EDICIONR,EDICION2R,EDICION3R,EDICION4R,EDICION5R,PREGUNTA3_RUTINAS,PREGUNTA4_RUTINAS_HORAS, \
VOLVER_MENU_RUTINAS,ELIMINAR_RUTINA,PREMIOS,ELIMINAR_RUTINAS,CONSEJOS,GUIA_RAPIDA,CONTACTO,\
ACERCA_DE,VOLVER_MENU_GUIARAPIDA,VOLVER_MENU_AYUDA,VOLVER_MENU_PRINCIPAL,RUTINAS_AYUDA,\
TAREAS_AYUDA,LOGROS_AYUDA,BUSCADOR_AYUDA,GRAFICAS,GRAFICAMES,VOLVER,ENCONSTRUCCION, \
CATEGORIAS_RUTINAS,ENCONSTRUCCION,VOLVER_MENU_PRINCIPAL,VOLVER,EDITANOMBRE5R,GUARDA_DIAS, \
BUSQUEDA_NOMBRE,RECORDATORIO_RUTINA,GUARDA_DIAS_RECORD,EDITADIAS_RECORD,HORA_RECORDATORIOR, \
HORA_RECORDATORIO2,OBTIENE_ID_CATEGORIA, CATEGORIAS_GESTION,EDICION_CATEGORIAS, \
VOLVER_MENU_CATEGORIAS, ELIMINAR_CATEGORIA,EDITA_NOMBREC,EDITA_CATEGORIA,PREGUNTA6_RUTINAS_R, \
PREGUNTA6_RUTINAS_HORA,RESULTADO_FECHA,BUSQUEDA_FECHA, VOLVER_MENU_BUSCADOR,BUSQUEDA_CATEGORIA, \
BUSQUEDA_NOMBRE_R, RESULTADO_BNOMBRE_R,BUSQUEDA_RUTINA,BUSQUEDA_TAREA,MARCAR_RUTINA = range (133)


################################### MENU INICIAL ####################################

# Teclado menú principal

teclado_menu_principal = [
				[InlineKeyboardButton(text='📋 Rutinas ', callback_data=str(MENU_RUTINAS)),
				 InlineKeyboardButton(text='📝 Tareas ', callback_data=str(MENU_TAREAS))],
				[InlineKeyboardButton(text='🎖 Logros ', callback_data=str(MENU_LOGROS)),
				InlineKeyboardButton(text='🔎 Buscador ', callback_data=str(MENU_BUSCADOR))],
				[InlineKeyboardButton(text='❓ Ayuda ', callback_data=str(MENU_AYUDA)),
				InlineKeyboardButton(text='🔚 Salir ', callback_data=str(FINALIZAR))],
			  ]

def start(update: Update, context: CallbackContext):
	#variables del usuario

	datos_user = update.message.from_user
	nombre_usuario = datos_user.first_name
	id_usuario = datos_user.id
	context.user_data["nombre_usuario"] = nombre_usuario
	context.user_data["id_usuario"] = id_usuario
	alias_usuario = datos_user.username
	# Se comprueba si existe el usuario, si no se crea
	existe = bd_bot.comprueba_usuario(str(id_usuario))
	if existe:
		logger.info("El usuario %s ha iniciado el bot", context.user_data["nombre_usuario"])
	else:
		bd_bot.crear_usuario(id_usuario,nombre_usuario)
		id_usuario = context.user_data["id_usuario"]
		logger.info("El usuario %s ha sido creado y ha iniciado el bot", nombre_usuario)

	reply_markup  = InlineKeyboardMarkup(teclado_menu_principal)
	update.message.reply_text(
		text="<b>➖➖ PlanningUGR ➖➖</b>\n Bienvenid@ "+ nombre_usuario+ "👋",
		parse_mode=telegram.ParseMode.HTML,
		reply_markup=reply_markup
	)
	return MENU_PRINCIPAL


################################### VOLVER MENU INICIAL ####################################

def menu_principal(update: Update, context: CallbackContext):
	logger.info("El usuario %s ha vuelto al menú inicial", context.user_data["nombre_usuario"])
	query = update.callback_query
	reply_markup  = InlineKeyboardMarkup(teclado_menu_principal)
	context.bot.send_message(
		text="<b>➖➖ PlanningUGR ➖➖</b>",
		chat_id = query.message.chat_id,
		parse_mode=telegram.ParseMode.HTML,
		reply_markup=reply_markup
	)
	return MENU_PRINCIPAL

################################### FUNCIONES DE TAREAS ####################################


#Teclados para reusar de tareas

teclado_menu_tareas = [
			[InlineKeyboardButton("➕ Añadir tareas",  callback_data=str(TAREAS)),
			InlineKeyboardButton("✏️ Edición tareas", callback_data=str(EDICION_TAREAS)),
			],
			[
			InlineKeyboardButton("👁 Visualización por fecha", callback_data=str(TAREAS_PORFECHA)),
			],
			[InlineKeyboardButton(text="🔙 Volver al menú principal", callback_data=str(VOLVER_MENU_PRINCIPAL))]
			]

teclado_menu_tareas_fecha = [
			[InlineKeyboardButton("➕ Añadir tareas",  callback_data=str(TAREAS)),
			InlineKeyboardButton("✏️ Edición de tareas", callback_data=str(EDICION_TAREAS)),
			],
			[
			InlineKeyboardButton("📌 Visualización por prioridad", callback_data=str(MENU_TAREAS)),
			],
			[InlineKeyboardButton(text="🔙 Volver al menú principal", callback_data=str(VOLVER_MENU_PRINCIPAL))]
			]

teclado_menu_tareas_nd = [
			[InlineKeyboardButton("➕ Añadir tareas",  callback_data=str(TAREAS)),
			],
			[InlineKeyboardButton(text="🔙 Volver al menú principal", callback_data=str(VOLVER_MENU_PRINCIPAL))]
			]


teclado_volver_tareas = [
				[InlineKeyboardButton(text='🔙 Volver al menú tareas', callback_data=str(VOLVER_MENU_TAREAS_P))]
				]


# menu principal de tareas (visualización por defecto por prioridad)

def menu_tareas(update: Update, context: CallbackContext):
	logger.info("El usuario %s está en el menú tareas", context.user_data["nombre_usuario"])
	query = update.callback_query
	id_usuario = str(context.user_data["id_usuario"])
	context.user_data["visualizacion_prioridad"] = True
	reply_markup = InlineKeyboardMarkup(teclado_menu_tareas)
	reply_markup2 = InlineKeyboardMarkup(teclado_menu_tareas_nd)
	text = funciones.tareaspendientes_prioridad(id_usuario)
	datos = bd_bot.contar_tareas_pendientes(str(context.user_data["id_usuario"]))
	# Se comprueba que haya tareas, si no hay tareas se muestra el teclado sin modo edición
	if datos[0] != 0:
			context.bot.send_message(
			text="<b> 📝 Menú tareas 📝 </b>\n\nPuedes añadir una tarea nueva, cambiar de visualización o entrar en el menú de edición para modificar datos de tu tarea, eliminarla o marcarla como realizada.",
			chat_id = query.message.chat_id,
			parse_mode=telegram.ParseMode.HTML,
			)
			context.bot.send_message(
			text="<b> 📌 Tareas pendientes 📌</b>\n" + text,
			chat_id = query.message.chat_id,
			parse_mode=telegram.ParseMode.HTML,
			reply_markup=reply_markup
			)
	else:
		context.bot.send_message(
			text="<b> 📝 Menú tareas 📝 </b>\n\nEmpieza creando tu primera tarea.\n",
			chat_id = query.message.chat_id,
			parse_mode=telegram.ParseMode.HTML,
			reply_markup=reply_markup2
		)


	return GESTION_TAREAS

# menu principal de tareas visualización por fecha

def menu_tareas_fecha(update: Update, context: CallbackContext):
	logger.info("El usuario %s esta en el menú tareas modo visualización por fecha", context.user_data["nombre_usuario"])
	query = update.callback_query
	id_usuario = str(context.user_data["id_usuario"])
	context.user_data["visualizacion_prioridad"] = False
	reply_markup = InlineKeyboardMarkup(teclado_menu_tareas_fecha)
	reply_markup2 = InlineKeyboardMarkup(teclado_menu_tareas_nd)
	text = funciones.tareaspendientes_fecha(id_usuario)
	datos = bd_bot.contar_tareas_pendientes(str(context.user_data["id_usuario"]))

	if datos[0] != 0:
			context.bot.send_message(
			text="<b> 📝 Menú tareas 📝 </b>\n\n<b>📌 Tareas pendientes 📌</b>\n" + text,
			chat_id = query.message.chat_id,
			parse_mode=telegram.ParseMode.HTML,
			reply_markup=reply_markup
		)
	else:
		context.bot.send_message(
			text="<b> 📝 Menú tareas 📝 </b>\n\nEmpieza creando tu primera tarea.\n",
			chat_id = query.message.chat_id,
			parse_mode=telegram.ParseMode.HTML,
			reply_markup=reply_markup2
		)


	return GESTION_TAREAS



# Funciones para crear una nueva tarea

def pregunta1_tareas(update: Update, context: CallbackContext):
	logger.info("El usuario %s añade el nombre de la tarea", context.user_data["nombre_usuario"])
	query = update.callback_query
	context.bot.send_message(
							text="¿Cuál es el nombre de su tarea?",
							chat_id = query.message.chat_id,
							parse_mode=telegram.ParseMode.HTML
							)
	return PREGUNTA2_TAREAS


def pregunta2_tareas(update: Update, context: CallbackContext):
		logger.info("El usuario %s selecciona la prioridad de la tarea", context.user_data["nombre_usuario"])
		context.user_data['nombre_tarea'] = update.message.text
		if (str(context.user_data['nombre_tarea'].upper()) == '/salir'.upper()):
			update.message.reply_text(
				text="¡Hasta pronto!"
			)
			return ConversationHandler.END
		# comprueba si hay tareas pendientes con ese mismo nombre
		datos = bd_bot.leer_tareas(str(context.user_data['id_usuario']))
		for data in datos:
			if (str(data[2].upper()) == str(context.user_data['nombre_tarea'].upper())):
				update.message.reply_text(
				text = "💬 Ya existe una tarea con ese nombre. Vuelva a escribir el nombre de su tarea.",
				parse_mode=telegram.ParseMode.HTML
				)
				return PREGUNTA2_TAREAS

		teclado_prioridad = [
					[InlineKeyboardButton(" 🛑 Prioridad alta", callback_data=str(PRIORIDAD_ALTA))],
					[InlineKeyboardButton(" ✴️ Prioridad media", callback_data=str(PRIORIDAD_MEDIA))],
					[InlineKeyboardButton(" ❇️ Prioridad baja", callback_data=str(PRIORIDAD_BAJA))],
					]
		reply_markup = InlineKeyboardMarkup(teclado_prioridad)
		update.message.reply_text(
		text = '¿Cual será la prioridad de su tarea?',
		reply_markup=reply_markup
		)
		return PRIORIDADES_TAREA


def prioridadt_alta(update: Update, context: CallbackContext):
	logger.info("El usuario %s  ha seleccionado prioridad alta y escribe la fecha de vencimiento de la tarea", context.user_data["nombre_usuario"])
	query = update.callback_query
	context.user_data["prioridad"] = 1
	context.bot.send_message(
							text='Indique la fecha de vencimiento. Ej. ' + funciones.dia_prox(),
							chat_id = query.message.chat_id,
							parse_mode=telegram.ParseMode.HTML
							)
	return PREGUNTA4_TAREAS

def prioridadt_media(update: Update, context: CallbackContext):
	logger.info("El usuario %s ha seleccionado prioridad media y escribe la fecha de vencimiento de la tarea", context.user_data["nombre_usuario"])
	query = update.callback_query
	context.user_data["prioridad"] = 2
	context.bot.send_message(
							text='Indique la fecha de vencimiento. Ej. ' + funciones.dia_prox(),
							chat_id = query.message.chat_id,
							parse_mode=telegram.ParseMode.HTML
							)
	return PREGUNTA4_TAREAS

def prioridadt_baja(update: Update, context: CallbackContext):
	logger.info("El usuario %s ha seleccionado prioridad baja y añade la fecha de la tarea", context.user_data["nombre_usuario"])
	query = update.callback_query
	context.user_data["prioridad"] = 3
	context.bot.send_message(
							text='Indique la fecha de vencimiento. Ej. ' + funciones.dia_prox(),
							chat_id = query.message.chat_id,
							parse_mode=telegram.ParseMode.HTML
							)
	return PREGUNTA4_TAREAS


def pregunta4_tareas(update: Update, context: CallbackContext):
		logger.info("El usuario %s selecciona añadir o no un comentario a la tarea", context.user_data["nombre_usuario"])
		fecha_valida = funciones.valida_fecha(update.message.text)
		if (update.message.text.upper() == '/salir'.upper()):
				logger.info("El usuario %s usa el comando /salir para finalizar la conversación", context.user_data["nombre_usuario"])
				update.message.reply_text(
					text="¡Hasta pronto!"
				)
				return ConversationHandler.END
		if not fecha_valida:
			logger.info("El usuario %s ha escrito una fecha incorrecta", context.user_data["nombre_usuario"])
			update.message.reply_text(
									text="💬 Has introducido una fecha incorrecta ❌. Indique la fecha de vencimiento con el formato correcto y comprueba que no sea una fecha pasada. Ej. " + funciones.dia_prox(),
									parse_mode=telegram.ParseMode.HTML
									)
			return PREGUNTA4_TAREAS
		else:
			teclado_prioridad = [
							[InlineKeyboardButton("Si", callback_data=str(COMENT_TAREA_SI))],
							[InlineKeyboardButton("No", callback_data=str(COMENT_TAREA_NO))],
							]
			reply_markup = InlineKeyboardMarkup(teclado_prioridad)
			context.user_data["fecha_tarea"] = update.message.text
			update.message.reply_text(
			text='¿Quiere agregar un comentario sobre su tarea?',
			reply_markup=reply_markup
			)
			return PREGUNTA_COMENT

def coment_tarea_si(update: Update, context: CallbackContext):
	logger.info("El usuario %s ha elegido escribir un comentario sobre su tarea", context.user_data["nombre_usuario"])
	query = update.callback_query
	context.bot.send_message(
							text='Escriba el comentario de su tarea',
							chat_id = query.message.chat_id,
							parse_mode=telegram.ParseMode.HTML
							)
	return PREGUNTA5_TAREAS

def pregunta5_tareas_noc(update: Update, context: CallbackContext):
		logger.info("El usuario %s elige no escribir un comentario y se guarda su tarea", context.user_data["nombre_usuario"])
		query = update.callback_query
		reply_markup = InlineKeyboardMarkup(teclado_volver_tareas)
		id_usuario = str(context.user_data["id_usuario"])
		context.bot.send_message(
								text= "💬 Se han guardado los datos de su tarea 💾",
								chat_id = query.message.chat_id,
								parse_mode=telegram.ParseMode.HTML,
								reply_markup=reply_markup
								)
		id_usuario = context.user_data["id_usuario"]
		punt_inicial = 0
		bd_bot.insertar_tareas_nc(id_usuario,context.user_data["nombre_tarea"], context.user_data["prioridad"],context.user_data["fecha_tarea"],'NO',punt_inicial)

		return GESTION_TAREAS


def pregunta5_tareas(update: Update, context: CallbackContext):
		logger.info("El usuario %s ha guardado su tarea", context.user_data["nombre_usuario"])
		context.user_data["comentario"] = update.message.text
		reply_markup = InlineKeyboardMarkup(teclado_volver_tareas)
		id_usuario = str(context.user_data["id_usuario"])
		text = funciones.tareaspendientes_prioridad(id_usuario)
		if (update.message.text.upper() == '/salir'.upper()):
				update.message.reply_text(
					text="¡Hasta pronto!"
				)
				return ConversationHandler.END
		update.message.reply_text(
			text= '💬 Se han guardado los datos de su tarea. 💾',
			parse_mode=telegram.ParseMode.HTML,
			reply_markup=reply_markup
		)
		id_usuario = context.user_data["id_usuario"]
		punt_inicial = 0
		bd_bot.insertar_tareas(id_usuario,context.user_data["nombre_tarea"], context.user_data["prioridad"],context.user_data["fecha_tarea"], context.user_data["comentario"],'NO',punt_inicial)

		return GESTION_TAREAS

# Visualización de tareas por defecto (visualización por prioridad)

def visualizar_tareas(update: Update, context: CallbackContext):
	logger.info("El usuario %s está visualizando las tareas para editar modo prioridad", context.user_data["nombre_usuario"])
	query = update.callback_query
	id_usuario = str(context.user_data["id_usuario"])
	keyboard = []
	datos = bd_bot.leer_tareas(id_usuario)
	datos1 = bd_bot.leer_tareas_prioridad1(id_usuario)
	datos2 = bd_bot.leer_tareas_prioridad2(id_usuario)
	datos3 = bd_bot.leer_tareas_prioridad3(id_usuario)

	if datos:
		if datos1:
			for data in datos1:
					keyboard.append([InlineKeyboardButton('🛑 ' + str(data[2]),
									callback_data=data[0])])
		if datos2:
			for data in datos2:
				keyboard.append([InlineKeyboardButton('✴️ ' + str(data[2]),
								callback_data=data[0])])
		if datos3:
			for data in datos3:
				keyboard.append([InlineKeyboardButton('❇️ ' + str(data[2]),
								callback_data=data[0])])

		reply_markup = InlineKeyboardMarkup(keyboard)
		context.bot.send_message(
						text="<b> 📝 Selección de tarea 📝</b>\n\n Selecciona una tarea para entrar en edición ✏ \n",
						parse_mode=telegram.ParseMode.HTML,
						chat_id = query.message.chat_id,
						reply_markup=reply_markup
					)
		return OBTIENE_ID_TAREA


def recojo_id_ediciontarea(update: Update, context: CallbackContext):
	logger.info("El usuario %s entra en la edicion de campos de la tarea", context.user_data["nombre_usuario"])
	query = update.callback_query
	context.user_data['id_tarea'] = query.data
	id_tarea = context.user_data['id_tarea']
	keyboard = []
	datos = bd_bot.leerid_tarea(id_tarea)
	if datos:
		for data in datos:
				keyboard.append([InlineKeyboardButton('✏ Nombre: ' + str(data[2]),callback_data=str(EDICION))])
				# Comprueba que tipo de prioridad tiene asignada eb bd para mostrar al usuario
				if(str(data[3]) == '1'):
					keyboard.append([InlineKeyboardButton('✏ Prioridad: 🛑 Alta', callback_data=str(EDICION2))])
				elif(str(data[3]) == '2'):
					keyboard.append([InlineKeyboardButton('✏ Prioridad: ✴️ Media', callback_data=str(EDICION2))])
				elif(str(data[3]) == '3'):
					keyboard.append([InlineKeyboardButton('✏ Prioridad: ❇️ Baja', callback_data=str(EDICION2))])

				keyboard.append([InlineKeyboardButton('✏ Fecha vencimiento: ' + str(data[4]), callback_data=str(EDICION22))])
				#Comprueba si tiene comentario
				if(str(data[5]) == 'None'):
					keyboard.append([InlineKeyboardButton('✏ Comentario: ' + 'Pulsa para añadir uno', callback_data=str(EDICION3))])
				else:
					keyboard.append([InlineKeyboardButton('✏ Comentario: ' + str(data[5]), callback_data=str(EDICION3))])

				keyboard.append([InlineKeyboardButton(text='✅ Tarea realizada ', callback_data=str(ESTADO_TAREA)),
								InlineKeyboardButton(text='⏰ Recordatorio', callback_data=str(RECORDATORIO_TAREA))])
				keyboard.append([InlineKeyboardButton('❌ Eliminar tarea', callback_data=str(ELIMINAR_TAREA_ACTUAL))])
				# Compruebo en que tipo de visualización estaba para volver a la visualización correcta por prioridad o fecha
				if(context.user_data["visualizacion_prioridad"] == True):
					keyboard.append([InlineKeyboardButton(text='🔙 Volver al menú de tareas', callback_data=str(VOLVER_MENU_TAREAS_P))])
				else:
					keyboard.append([InlineKeyboardButton(text='🔙 Volver al menú de tareas', callback_data=str(VOLVER_MENU_TAREAS_F))])
				context.user_data['recordatorio_tarea'] = str(data[2])
				context.user_data['nombre_tarea'] = str(data[2])
				context.user_data['fecha_tarea'] = str(data[4])
				reply_markup = InlineKeyboardMarkup(keyboard)
				context.bot.send_message(
					text="<b>📝 Edición de tarea 📝</b>\n\nSelecciona el campo que quieras editar ✏. O bien puedes crear un recordatorio ⏰, marcar tu tarea como realizada ✅ o eliminar la tarea actual ❌.\n",
					parse_mode=telegram.ParseMode.HTML,
					chat_id = query.message.chat_id,
					reply_markup=reply_markup
				)

	return EDICIONES_TAREA


# Edición de la tarea seleccionada

def edicion_tarea1(update: Update, context: CallbackContext):
	logger.info("El usuario %s edita el nombre de la tarea", context.user_data["nombre_usuario"])
	query = update.callback_query
	context.bot.send_message(
			text="¿Cuál es el nuevo nombre de tu tarea?",
			chat_id = query.message.chat_id,
		)
	return EDITANOMBRE1

def editanombre_tarea(update: Update, context: CallbackContext):
	logger.info("El usuario %s actualiza el nombre de la tarea", context.user_data["nombre_usuario"])
	columna = 'nombre_tarea'
	valor = update.message.text
	id_tarea = context.user_data['id_tarea']
	datos = bd_bot.leer_tareas(str(context.user_data['id_usuario']))

	if (update.message.text.upper() == '/salir'.upper()):
			update.message.reply_text(
				text="¡Hasta pronto!"
			)
			return ConversationHandler.END

	# Compruebo en que tipo de visualización estaba para volver a la visualización correcta por prioridad o fecha
	if(context.user_data["visualizacion_prioridad"] == True):
		text = funciones.tareaspendientes_prioridad(str(context.user_data["id_usuario"]))
	else:
		text = funciones.tareaspendientes_fecha(str(context.user_data["id_usuario"]))
	reply_markup = InlineKeyboardMarkup(teclado_volver_tareas)

	for data in datos:
		if (str(update.message.text.upper()) == str(data[2].upper())):
			logger.info("El usuario %s ha escrito un nombre para la tarea existente", context.user_data["nombre_usuario"])
			update.message.reply_text(
			text = '💬 Ya existe una tarea con ese nombre. Vuelva a escribir el nombre de su tarea.',
			parse_mode=telegram.ParseMode.HTML

			)
			return EDITANOMBRE1

	bd_bot.actualizar_campot(columna,valor,id_tarea)
	update.message.reply_text(
		text="💬 Nombre de la tarea modificada con éxito ✍✅",
		parse_mode=telegram.ParseMode.HTML,
		reply_markup=reply_markup
	)

	return GESTION_TAREAS


def edicion_tarea2(update: Update, context: CallbackContext):
	logger.info("El usuario %s edita la prioridad de la tarea", context.user_data["nombre_usuario"])
	query = update.callback_query
	teclado_prioridad = [
				[InlineKeyboardButton("🛑 Prioridad alta", callback_data='1')],
				[InlineKeyboardButton(" ✴️ Prioridad media", callback_data='2')],
				[InlineKeyboardButton(" ❇️ Prioridad baja", callback_data='3')],
				]
	reply_markup = InlineKeyboardMarkup(teclado_prioridad)
	context.bot.send_message(
			text="¿Cuál es la nueva prioridad de su tarea?",
			chat_id = query.message.chat_id,
			reply_markup=reply_markup
		)
	return EDITAPRIORIDAD

def guardaprioridad_tarea(update: Update, context: CallbackContext):
	logger.info("El usuario %s actualiza la prioridad de la tarea", context.user_data["nombre_usuario"])
	query = update.callback_query
	valor_prioridad = query.data
	columna = 'prioridad_tarea'
	id_tarea = context.user_data['id_tarea']
	id_usuario = str(context.user_data["id_usuario"])
	bd_bot.actualizar_campot(columna,valor_prioridad,id_tarea)
	reply_markup = InlineKeyboardMarkup(teclado_menu_tareas)
	if(context.user_data["visualizacion_prioridad"] == True):
		text = funciones.tareaspendientes_prioridad(id_usuario)
	else:
		text = funciones.tareaspendientes_fecha(id_usuario)
	context.bot.send_message(
				text="💬 Prioridad de la tarea modificada con éxito ✍✅\n\n",
				parse_mode=telegram.ParseMode.HTML,
				chat_id = query.message.chat_id,
	)
	context.bot.send_message(
				text="<b> 📝 Menú tareas 📝 </b>\n\n<b> 📌 Tareas pendientes 📌</b>\n" + text,
				parse_mode=telegram.ParseMode.HTML,
				chat_id = query.message.chat_id,
				reply_markup=reply_markup
	)
	return GESTION_TAREAS


def edicion_tarea22(update: Update, context: CallbackContext):
	logger.info("El usuario %s edita la fecha de la tarea", context.user_data["nombre_usuario"])
	query = update.callback_query
	context.bot.send_message(
			text="¿Cuál es la nueva fecha de vencimiento de la tarea?",
			chat_id = query.message.chat_id,
		)
	return EDITANOMBRE22

def editafecha_tarea(update: Update, context: CallbackContext):
	logger.info("El usuario %s actualiza la fecha de vencimiento de la tarea", context.user_data["nombre_usuario"])
	columna = 'fecha_tarea'
	valor = update.message.text
	id_tarea = context.user_data['id_tarea']
	id_usuario = str(context.user_data["id_usuario"])
	fecha_valida = funciones.valida_fecha(update.message.text)
	if (update.message.text.upper() == '/salir'.upper()):
			update.message.reply_text(
				text="¡Hasta pronto!"
			)
			return ConversationHandler.END
	if not fecha_valida:
			update.message.reply_text(
									text="💬 Has introducido una fecha incorrecta ❌. Indique la fecha de vencimiento con el formato correcto y comprueba que no sea una fecha pasada. Ej. " + funciones.dia_prox(),
									parse_mode=telegram.ParseMode.HTML
									)
			return EDITANOMBRE22
	else:
		bd_bot.actualizar_campot(columna,valor,id_tarea)
		reply_markup = InlineKeyboardMarkup(teclado_menu_tareas)
		if(context.user_data["visualizacion_prioridad"] == True):
			text = funciones.tareaspendientes_prioridad(id_usuario)
		else:
			text = funciones.tareaspendientes_fecha(id_usuario)
		update.message.reply_text(
					text="💬 Fecha de vencimiento de la tarea modificada con éxito ✍✅\n\n",
					parse_mode=telegram.ParseMode.HTML,
		)
		update.message.reply_text(
					text="<b> 📝 Menú tareas 📝 </b>\n\n<b> 📌 Tareas pendientes 📌</b>\n" + text,
					parse_mode=telegram.ParseMode.HTML,
					reply_markup=reply_markup
		)
		return GESTION_TAREAS

def edicion_tarea3(update: Update, context: CallbackContext):
	logger.info("El usuario %s edita el comentario de la tarea", context.user_data["nombre_usuario"])
	query = update.callback_query
	context.bot.send_message(
			text="¿Cuál es el nuevo comentario de su tarea?",
			chat_id = query.message.chat_id,
		)
	return EDITANOMBRE3

def editacomentario_tarea(update: Update, context: CallbackContext):
	logger.info("El usuario %s actualiza el cometario de la tarea", context.user_data["nombre_usuario"])
	columna = 'comentario_tarea'
	valor = update.message.text
	id_tarea = context.user_data['id_tarea']
	id_usuario = str(context.user_data["id_usuario"])
	if (update.message.text.upper() == '/salir'.upper()):
			update.message.reply_text(
				text="¡Hasta pronto!"
			)
			return ConversationHandler.END
	bd_bot.actualizar_campot(columna,valor,id_tarea)
	if(context.user_data["visualizacion_prioridad"] == True):
		text = funciones.tareaspendientes_prioridad(id_usuario)
	else:
		text = funciones.tareaspendientes_fecha(id_usuario)
	reply_markup = InlineKeyboardMarkup(teclado_menu_tareas)
	update.message.reply_text(
		text="💬 Comentario de la tarea modificado con éxito ✍✅",
		parse_mode=telegram.ParseMode.HTML,
	)
	update.message.reply_text(
		text="<b> 📝 Menú tareas 📝 </b>\n\n<b> 📌 Tareas pendientes 📌</b>\n" + text,
		parse_mode=telegram.ParseMode.HTML,
		reply_markup=reply_markup
	)

	return GESTION_TAREAS

# Eliminar tarea

def eliminar_tarea(update: Update, context: CallbackContext):
	logger.info("El usuario %s ha eliminado la tarea", context.user_data["nombre_usuario"])
	query = update.callback_query
	id_tarea = context.user_data['id_tarea']
	id_usuario = str(context.user_data["id_usuario"])
	bd_bot.eliminar_tarea('bd_bot.db','tareas', 'id_tarea', id_tarea)
	reply_markup = InlineKeyboardMarkup(teclado_menu_tareas)
	reply_markup2 = InlineKeyboardMarkup(teclado_menu_tareas_nd)
	if(context.user_data["visualizacion_prioridad"] == True):
		text = funciones.tareaspendientes_prioridad(id_usuario)
	else:
		text = funciones.tareaspendientes_fecha(id_usuario)
	datos = bd_bot.contar_tareas_pendientes(str(context.user_data["id_usuario"]))

	if datos[0] != 0:
			context.bot.send_message(
				text="💬  Tarea eliminada con éxito ✅\n",
				chat_id = query.message.chat_id,
				parse_mode=telegram.ParseMode.HTML,
			)
			context.bot.send_message(
			text="<b> 📝 Menú tareas 📝 </b>\n\n<b> 📌 Tareas pendientes 📌</b>\n" + text,
			chat_id = query.message.chat_id,
			parse_mode=telegram.ParseMode.HTML,
			reply_markup=reply_markup
		)
	else:
		context.bot.send_message(
			text="<b>💬  Tarea eliminada con éxito ✅</b>\n",
			chat_id = query.message.chat_id,
			parse_mode=telegram.ParseMode.HTML,
			reply_markup=reply_markup2
		)

	return GESTION_TAREAS

# Marcar tarea como completada

def estado_tarea(update: Update, context: CallbackContext):
		logger.info("El usuario %s ha marcado como completada su tarea", context.user_data["nombre_usuario"])
		query = update.callback_query
		columna = 'estado_tarea'
		columna2 = 'premio_tarea'
		valor = 'SI'
		id_tarea =  context.user_data['id_tarea']
		bd_bot.actualizar_campot(columna,valor,id_tarea)
		datos = bd_bot.leerid_tarea(str(id_tarea))
		# Actualizo puntuación segun prioridad de la tarea
		for tarea in datos:
			if str(tarea[3]) == '1':
				bd_bot.actualizar_campot(columna2,30,id_tarea)
			elif str(tarea[3]) == '2':
				bd_bot.actualizar_campot(columna2,20,id_tarea)
			elif str(tarea[3]) == '3':
				bd_bot.actualizar_campot(columna2,10,id_tarea)
		if(context.user_data["visualizacion_prioridad"] == True):
			teclado_volver_tareas = [
						[InlineKeyboardButton("🔙 Volver al menú tareas", callback_data=str(VOLVER_MENU_TAREAS_P))],
						]
		else:
			teclado_volver_tareas = [
						[InlineKeyboardButton("🔙 Volver al menú tareas", callback_data=str(VOLVER_MENU_TAREAS_F))],
						]
		reply_markup = InlineKeyboardMarkup(teclado_volver_tareas)
		context.bot.send_message(
			text="\n\n 💬 Su tarea se ha marcado como realizada ✅",
			chat_id = query.message.chat_id,
			parse_mode=telegram.ParseMode.HTML,
			reply_markup=reply_markup
		)

		return GESTION_TAREAS

# Recordatorios para la tarea

def crear_recordatorios(update: Update, context: CallbackContext):
	logger.info("El usuario %s está creando un recordatorio", context.user_data["nombre_usuario"])
	query = update.callback_query
	chat_id= update.callback_query.message.chat_id
	id_tarea = context.user_data['id_tarea']
	nombre =context.user_data['recordatorio_tarea']

	teclado_recordatorios = [
				[InlineKeyboardButton("⏰ Para mañana", callback_data=str(ALARMA_MANIANA))],
				[InlineKeyboardButton("⏰ Próxima semana", callback_data=str(ALARMA_SEMANAPROX))],
				[InlineKeyboardButton("⏰ Elegir otra fecha", callback_data=str(ALARMA_ELEGIRFECHA))],
				]
	reply_markup = InlineKeyboardMarkup(teclado_recordatorios)
	context.bot.send_message(
				text="\n\n<b> ⏰ Estableciendo tu recordatorio para la tarea: </b> "+ nombre,
				chat_id = query.message.chat_id,
				parse_mode=telegram.ParseMode.HTML,
				reply_markup=reply_markup
	)

	return EDICIONES_TAREA

def alarma_maniana(update: Update, context: CallbackContext):
	nombre_recordatorio= context.user_data['recordatorio_tarea']
	logger.info("El usuario %s está establece hora para la alarma de mañana", context.user_data["nombre_usuario"])
	query = update.callback_query
	context.bot.send_message(
				text="\n ✍ Escribe la hora . Ej. 23:40",
				chat_id = query.message.chat_id,
				parse_mode=telegram.ParseMode.HTML,
	)

	return ALARM_MHORA


def alarm_mhora(update: Update, context: CallbackContext):
	logger.info("El usuario %s guarda su alarma para mañana", context.user_data["nombre_usuario"])
	valor = update.message.text
	chat_id= update.message.chat_id
	if (update.message.text.upper() == '/salir'.upper()):
			update.message.reply_text(
				text="¡Hasta pronto!"
			)
			return ConversationHandler.END
	if not funciones.valida_hora(valor):
		update.message.reply_text(
		text="💬 Has introducido la hora en un formato incorrecto ❌. Escríbelo con el formato hh:mm. Ej. 23:40 \n",
		)
		return ALARM_MHORA
	else:
		if(context.user_data["visualizacion_prioridad"] == True):
			teclado_volver_tareas = [
						[InlineKeyboardButton("🔙 Volver al menú tareas", callback_data=str(VOLVER_MENU_TAREAS_P))],
						]
		else:
			teclado_volver_tareas = [
						[InlineKeyboardButton("🔙 Volver al menú tareas", callback_data=str(VOLVER_MENU_TAREAS_F))],
						]

		reply_markup = InlineKeyboardMarkup(teclado_volver_tareas)
		#fecha actual
		now = datetime.now()
		anio = now.year   # Año.
		mes = now.month  # Mes.
		dia = now.day
		# hora recogida por teclado
		mi_hora= datetime.strptime(valor, "%H:%M")
		hora = mi_hora.hour
		minuto = mi_hora.minute

		# Se establece el recordatorio para mañana
		zona_horaria = tz.gettz('Europe/Madrid')
		ultimodiames = calendar.monthrange(anio, mes)[1]
		if ultimodiames == dia:
			dia = 0
			if(mes == 12):
				mes = 1
				anio = anio + 1
		dia = dia+1
		nombre_recordatorio= context.user_data['recordatorio_tarea']
		fecha = datetime(anio,mes,dia,hora,minuto,0, tzinfo=zona_horaria)
		context.job_queue.run_once(alarma_tarea, fecha, context=(chat_id,nombre_recordatorio), name=nombre_recordatorio)
		update.message.reply_text(
		text='💬 Su recordatorio para mañana se ha guardado 💾',
		reply_markup=reply_markup
		)

		return EDICIONES_TAREA


def alarma_tarea(context):
	job = context.job
	reply_markup = InlineKeyboardMarkup(teclado_volver_tareas)
	context.bot.send_message(
	job.context[0],
	text="<b> ⏰ Te recuerdo que tienes pendiente la tarea: ⏰</b>\n ➡️ " + job.context[1],
	parse_mode=telegram.ParseMode.HTML,
	reply_markup=reply_markup
	)

def alarma_semanaprox(update: Update, context: CallbackContext):
	nombre_recordatorio= context.user_data['recordatorio_tarea']
	logger.info("El usuario %s está establece hora para su alarma de la proxima semana", context.user_data["nombre_usuario"])
	query = update.callback_query
	context.bot.send_message(
				text="\n\n✍ Escribe la hora. Ej. 22:40",
				chat_id = query.message.chat_id,
				parse_mode=telegram.ParseMode.HTML,
	)

	return ALARM_PHORA


def alarm_phora(update: Update, context: CallbackContext):
	logger.info("El usuario %s guarda su alarma para la proxima semana", context.user_data["nombre_usuario"])
	valor = update.message.text
	chat_id= update.message.chat_id
	if (update.message.text.upper() == '/salir'.upper()):
			update.message.reply_text(
				text="¡Hasta pronto!"
			)
			return ConversationHandler.END
	if not funciones.valida_hora(valor):
		update.message.reply_text(
		text="💬 Has introducido la hora en un formato incorrecto ❌. Escríbelo con el formato hh:mm. Ej. 23:40 \n",
		)
		return ALARM_PHORA
	else:
		# print('visualizacion',context.user_data["visualizacion_prioridad"])
		if(context.user_data["visualizacion_prioridad"] == True):
			teclado_volver_tareas = [
						[InlineKeyboardButton("🔙 Volver al menú tareas", callback_data=str(VOLVER_MENU_TAREAS_P))],
						]
		else:
			teclado_volver_tareas = [
						[InlineKeyboardButton("🔙 Volver al menú tareas", callback_data=str(VOLVER_MENU_TAREAS_F))],
						]

		reply_markup = InlineKeyboardMarkup(teclado_volver_tareas)

		fecha_c = funciones.calcular_semana_prox()
		fecha_sp = datetime.strptime(fecha_c, "%d-%m-%Y")
		dia = fecha_sp.day
		mes = fecha_sp.month
		anio = fecha_sp.year
		mi_hora= datetime.strptime(valor, "%H:%M")
		hora = mi_hora.hour
		minuto = mi_hora.minute
		zona_horaria = tz.gettz('Europe/Madrid')
		fecha = datetime(anio,mes,dia,hora,minuto,0, tzinfo=zona_horaria)
		nombre_recordatorio = context.user_data['recordatorio_tarea']
		context.job_queue.run_once(alarma_tarea,fecha, context=(chat_id,nombre_recordatorio), name=nombre_recordatorio)
		update.message.reply_text(
		text='💬 Su recordatorio para la próxima semana se ha guardado 💾',
		reply_markup=reply_markup
		)

		return EDICIONES_TAREA


def alarma_elegirfecha(update: Update, context: CallbackContext):
	nombre_recordatorio= context.user_data['recordatorio_tarea']
	logger.info("El usuario %s está estableciendo una alarma eligiendo fecha", context.user_data["nombre_usuario"])
	query = update.callback_query
	context.bot.send_message(
				text="\n\n✍ Escribe la fecha. Ej. " + funciones.dia_prox(),
				chat_id = query.message.chat_id,
				parse_mode=telegram.ParseMode.HTML,
	)

	return ALARM_ELIGEH

def alarm_eligeh(update: Update, context: CallbackContext):
		logger.info("El usuario %s establece hora para su alarma", context.user_data["nombre_usuario"])
		valor = update.message.text
		context.user_data['fecha_recordatorio'] = valor
		if (update.message.text.upper() == '/salir'.upper()):
				update.message.reply_text(
					text="¡Hasta pronto!"
				)
				return ConversationHandler.END
		fecha_valida = funciones.valida_fecha(update.message.text)
		if not fecha_valida:
			# print('fecha no valida')
			update.message.reply_text(
					text='💬 Has introducido una fecha incorrecta ❌. Indique la fecha de vencimiento con el formato correcto y comprueba que no sea una fecha pasada. Ej. ' + funciones.dia_prox(),
					parse_mode=telegram.ParseMode.HTML
			)
			return ALARM_ELIGEH
		else:
			update.message.reply_text(
				text="\n\n✍ Escribe la hora. Ejemplo 22:40",
				parse_mode=telegram.ParseMode.HTML,
			)

			return ALARM_ELIGEG

def alarm_eligeg(update: Update, context: CallbackContext):
	logger.info("El usuario %s guarda su alarma para la fecha y hora elegida", context.user_data["nombre_usuario"])
	valor = update.message.text
	context.user_data['hora_recordatorio'] = valor
	chat_id= update.message.chat_id
	if not funciones.valida_hora(valor):
		update.message.reply_text(
		text="💬 Has introducido la hora en un formato incorrecto ❌. Escríbelo con el formato hh:mm. Ej. 23:40 \n",
		)
		return ALARM_ELIGEG
	else:

		# Se obtiene la fecha y hora introducida por teclado
		now = datetime.strptime(context.user_data['fecha_recordatorio'], "%d-%m-%Y")
		anio = now.year   # Año.
		mes = now.month  # Mes.
		dia = now.day
		mi_hora = datetime.strptime(context.user_data['hora_recordatorio'], "%H:%M")
		hora = mi_hora.hour
		minuto = mi_hora.minute
		if(context.user_data["visualizacion_prioridad"] == True):
			teclado_volver_tareas = [
						[InlineKeyboardButton("🔙 Volver al menú tareas", callback_data=str(VOLVER_MENU_TAREAS_P))],
						]
		else:
			teclado_volver_tareas = [
						[InlineKeyboardButton("🔙 Volver al menú tareas", callback_data=str(VOLVER_MENU_TAREAS_F))],
						]

		reply_markup = InlineKeyboardMarkup(teclado_volver_tareas)
		zona_horaria = tz.gettz('Europe/Madrid')
		dt = datetime(anio,mes,dia,hora,minuto,0, tzinfo=zona_horaria)
		nombre_recordatorio= context.user_data['recordatorio_tarea']
		context.job_queue.run_once(alarma_tarea,dt, context=(chat_id,nombre_recordatorio), name=nombre_recordatorio)
		update.message.reply_text(
		text='💬 Su recordatorio se ha guardado 💾\n',
		parse_mode=telegram.ParseMode.HTML,
		)
		update.message.reply_text(
		text='Se ha establecido para la fecha: ' + str(context.user_data['fecha_recordatorio']) \
		+ ' a las ' + str(context.user_data['hora_recordatorio']),
		parse_mode=telegram.ParseMode.HTML,
		reply_markup=reply_markup
		)

		return EDICIONES_TAREA

################################### FUNCIONES DE RUTINAS ####################################


# Teclados de rutinas para reusar

teclado_menu_rutinas = [

	[InlineKeyboardButton("➕ Añadir rutinas",  callback_data=str(RUTINAS))],
	[InlineKeyboardButton("💠 Categorias",  callback_data=str(CATEGORIAS_RUTINA)),
	InlineKeyboardButton("✏️ Edición rutinas", callback_data=str(EDICION_RUTINAS))],
	[InlineKeyboardButton("🔙 Volver al menú principal", callback_data=str(VOLVER_MENU_PRINCIPAL))]

	]

teclado_menu_rutinas_nd = [
	[InlineKeyboardButton("➕ Añadir rutinas",  callback_data=str(RUTINAS)),
	InlineKeyboardButton("💠 Categorias",  callback_data=str(CATEGORIAS_RUTINA))],
	[InlineKeyboardButton("🔙 Volver al menú principal", callback_data=str(VOLVER_MENU_PRINCIPAL))]]

teclado_mod_rutinas = [
		 [InlineKeyboardButton(text='✏️ Editar rutinas', callback_data=str(EDICION_RUTINAS))],
		 [InlineKeyboardButton(text=' 🔙 Volver al menú rutinas', callback_data=str(VOLVER_MENU_RUTINAS))],
	]

teclado_volver_categorias = [
		 [InlineKeyboardButton(text=' 🔙 Volver al menú categorías', callback_data=str(VOLVER_MENU_CATEGORIAS))],
	]
teclado_volver_rutinas = [
		 [InlineKeyboardButton(text=' 🔙 Volver al menú rutinas', callback_data=str(VOLVER_MENU_RUTINAS))],
	]

teclado_agrega_rutinas = [
				[InlineKeyboardButton(text='🔙 Volver al menú rutinas', callback_data=str(VOLVER_MENU_RUTINAS))]
				]


# Menu rutinas

def menu_rutinas(update: Update, context: CallbackContext):
	logger.info("El usuario %s ha entrado en el menú de rutinas", context.user_data["nombre_usuario"])
	query = update.callback_query
	reply_markup = InlineKeyboardMarkup(teclado_menu_rutinas)
	reply_markup2 = InlineKeyboardMarkup(teclado_menu_rutinas_nd)
	id_usuario = str(context.user_data["id_usuario"])
	datos = bd_bot.contar_rutinas_pendientes(str(context.user_data["id_usuario"]))
	if datos[0] != 0:
		context.bot.send_message(
			text="<b>📋 Menú rutinas 📋</b>\n\n En este menú puedes crear tus rutinas semanales y crear categorías para tu rutina. Además desde el menú edición puedes crear recordatorios diarios, editar datos de rutina y eliminar rutinas.",
			parse_mode=telegram.ParseMode.HTML,
			chat_id = query.message.chat_id,
		)
		context.bot.send_message(
			text="<b>Rutinas</b>\n"+ funciones.rutinaspendientes(id_usuario),
			parse_mode=telegram.ParseMode.HTML,
			chat_id = query.message.chat_id,
			reply_markup=reply_markup
		)
	else:
		context.bot.send_message(
			text="<b>📋 Menú rutinas 📋 </b>\n\nEmpieza creando tu primera rutina.\n",
			parse_mode=telegram.ParseMode.HTML,
			chat_id = query.message.chat_id,
			reply_markup=reply_markup2
		)

	return RUTINAS_GESTION


def categorias_rutina(update: Update, context: CallbackContext):
	logger.info("El usuario %s está visualizando las categorias disponibles para rutinas", context.user_data["nombre_usuario"])
	query = update.callback_query
	id_usuario = str(context.user_data["id_usuario"])
	keyboard = []
	datos = bd_bot.leer_categorias_rutina(id_usuario)
	datos2 = bd_bot.contar_categorias_usuario(str(context.user_data["id_usuario"]))
	text = funciones.obtener_categorias(id_usuario)
	if datos and datos2[0] == 0:
		keyboard.append([InlineKeyboardButton(text='➕ Añadir categorías', callback_data=str(NUEVA_CATEGORIA))])
		keyboard.append([InlineKeyboardButton(text='🔙 Volver al menú de rutinas', callback_data=str(VOLVER_MENU_RUTINAS))])
		reply_markup = InlineKeyboardMarkup(keyboard)
		context.bot.send_message(
				text="<b>💠 Categorías 💠 </b>\n\n"  + text,
				parse_mode=telegram.ParseMode.HTML,
				chat_id = query.message.chat_id,
				reply_markup=reply_markup
			)
	else:
		keyboard.append([InlineKeyboardButton(text='➕ añadir categoria', callback_data=str(NUEVA_CATEGORIA))])
		keyboard.append([InlineKeyboardButton(text='✏️ Edición categorías', callback_data=str(CATEGORIAS_GESTION))])
		keyboard.append([InlineKeyboardButton(text='🔙 Volver al menú rutinas ', callback_data=str(VOLVER_MENU_RUTINAS))])
		reply_markup = InlineKeyboardMarkup(keyboard)
		context.bot.send_message(
				text="<b> 💠 Categorías 💠 </b>\n\n" + text,
				parse_mode=telegram.ParseMode.HTML,
				chat_id = query.message.chat_id,
				reply_markup=reply_markup
			)
	return RUTINAS_GESTION

def categorias_gestion(update: Update, context: CallbackContext):
	logger.info("El usuario %s está visualizando las categorias de rutinas para su edición", context.user_data["nombre_usuario"])
	query = update.callback_query
	id_usuario = str(context.user_data["id_usuario"])
	keyboard = []
	datos = bd_bot.leer_categorias_rutina_usuario(id_usuario)
	if datos:
		for data in datos:
			keyboard.append([InlineKeyboardButton('🔹 ' + str(data[2]),callback_data=data[0])])
		reply_markup = InlineKeyboardMarkup(keyboard)
		context.bot.send_message(
				text="<b>💠 Selección de categorías 💠</b>\n Selecciona una para su edición\n",
				parse_mode=telegram.ParseMode.HTML,
				chat_id = query.message.chat_id,
				reply_markup=reply_markup
			)
		return OBTIENE_ID_CATEGORIA


def obtiene_id_categoria(update: Update, context: CallbackContext):
	 logger.info("El usuario %s visualiza su categoría para editar o eliminar", context.user_data["nombre_usuario"])
	 query = update.callback_query
	 context.user_data['id_categoria'] = query.data
	 id_categoria= str(context.user_data['id_categoria'])
	 datos = bd_bot.leerid_categoria(str(context.user_data['id_categoria']))
	 keyboard = []

	 if datos:
		 for data in datos:
			 context.user_data['nombre_categoria'] = str(data[2])
			 keyboard.append([InlineKeyboardButton(text='✏ Nombre: ' + str(data[2]),   callback_data=str(EDITA_NOMBREC))])

			 reply_markup = InlineKeyboardMarkup(keyboard)
		 keyboard.append([InlineKeyboardButton(text='❌ Eliminar categoría', callback_data=str(ELIMINAR_CATEGORIA))])
		 keyboard.append([InlineKeyboardButton(text='🔙 Volver al menú categorías', callback_data=str(VOLVER_MENU_CATEGORIAS))])
		 context.user_data['nombre_categoria'] = str(data[2])
		 context.bot.send_message(
							text="<b>💠 Edición de categorías</b> 💠 \n Puedes editar pulsando sobre su nombre o eliminar la categoría.\n",
							parse_mode=telegram.ParseMode.HTML,
							chat_id = query.message.chat_id,
							reply_markup=reply_markup
			)
	 return RUTINAS_GESTION


def edita_nombrec(update: Update, context: CallbackContext):
	logger.info("El usuario %s escribe el nuevo nombre de su categoría", context.user_data["nombre_usuario"])
	query = update.callback_query
	context.bot.send_message(
			text="¿Cuál es el nuevo nombre de su categoría?",
			chat_id = query.message.chat_id,
		)

	return EDITA_CATEGORIA

def edita_categoria(update: Update, context: CallbackContext):
	logger.info("El usuario %s actualiza el nombre de su categoría", context.user_data["nombre_usuario"])
	columna = 'nombre_categoria'
	valor = update.message.text
	id_categoria =  context.user_data['id_categoria']
	id_usuario = str(context.user_data["id_usuario"])
	datos = bd_bot.leer_categorias_rutina(id_usuario)
	for data in datos:
		if(str(data[2].upper()) == update.message.text.upper()):
			update.message.reply_text(
					text="💬 Ya existe una categoría con ese nombre. Vuelva a escribir el nombre para su categoría.",
					parse_mode=telegram.ParseMode.HTML,
			)
			return EDITA_CATEGORIA
	bd_bot.actualizar_campoc(columna,valor,id_categoria)
	update.message.reply_text('💬 Nombre de la categoría modificado con éxito ✍✅')
	reply_markup = InlineKeyboardMarkup(teclado_menu_rutinas)
	update.message.reply_text(
			text="<b>📋 Menú rutinas 📋</b>\n\n<b>Rutinas</b>\n\n"+ funciones.rutinaspendientes(str(context.user_data["id_usuario"])),
			parse_mode=telegram.ParseMode.HTML,
			reply_markup=reply_markup
	)

	return RUTINAS_GESTION

def nueva_categoria(update: Update, context: CallbackContext):
	logger.info("El usuario %s está añadiendo una nueva categoría", context.user_data["nombre_usuario"])
	query = update.callback_query
	context.bot.send_message(
		text='¿Cuál es el nombre de su nueva categoría?',
		parse_mode=telegram.ParseMode.HTML,
		chat_id = query.message.chat_id
	)
	return GUARDAR_CATEGORIA

def guardar_categoria(update: Update, context: CallbackContext):
	logger.info("El usuario %s guarda su categoria", context.user_data["nombre_usuario"])
	valor = update.message.text
	id_usuario = str(context.user_data["id_usuario"])
	datos = bd_bot.leer_categorias_rutina(id_usuario)
	if (update.message.text.upper() == '/salir'.upper()):
			update.message.reply_text(
				text="¡Hasta pronto!"
			)
			return ConversationHandler.END
	for data in datos:
		if(str(data[2].upper()) == update.message.text.upper()):
			update.message.reply_text(
					text="💬 Ya existe una categoría con ese nombre. Vuelva a escribir el nombre para su categoría.",
					parse_mode=telegram.ParseMode.HTML,
			)
			return GUARDAR_CATEGORIA

	bd_bot.insertar_categoria(id_usuario,valor)
	reply_markup = InlineKeyboardMarkup(teclado_volver_categorias)
	update.message.reply_text(
				text="💬 Categoría creada con éxito ✅",
				parse_mode=telegram.ParseMode.HTML,
				reply_markup=reply_markup
	)
	return RUTINAS_GESTION


def eliminar_categoria(update: Update, context: CallbackContext):
	logger.info("El usuario %s ha eliminado la categoria", context.user_data["nombre_usuario"])
	query = update.callback_query
	datos = bd_bot.leer_rutinas(str(context.user_data["id_usuario"]))
	reply_markup = InlineKeyboardMarkup(teclado_volver_categorias)
	context.user_data["encontrado"] = False
	for data in datos:
		if(str(data[3].upper()) == str(context.user_data['nombre_categoria'].upper())):
			context.user_data["encontrado"] = True
			context.bot.send_message(
					text="💬 No puede eliminar una categoría perteneciente a una rutina creada ❌. Primero elimine la rutina con esa categoria asignada. \n",
					parse_mode=telegram.ParseMode.HTML,
					chat_id = query.message.chat_id,
					reply_markup=reply_markup
			)

	if(context.user_data["encontrado"] == False):
		bd_bot.eliminar_rutina('bd_bot.db','categoria', 'id_categoria', str(context.user_data['id_categoria']))
		context.bot.send_message(
				text="💬  Categoría eliminada con éxito ✅\n\n",
				parse_mode=telegram.ParseMode.HTML,
				chat_id = query.message.chat_id,
				reply_markup=reply_markup
		)

		return RUTINAS_GESTION

# Funciones para recoger datos para crear una nueva rutina

def pregunta1_rutinas(update: Update, context: CallbackContext):
	logger.info("El usuario %s escribe el nombre de su rutina", context.user_data["nombre_usuario"])
	query = update.callback_query
	context.bot.send_message(
		text='¿Cuál es el nombre de su rutina?',
		parse_mode=telegram.ParseMode.HTML,
		chat_id = query.message.chat_id
	)
	return PREGUNTA11_RUTINAS

def pregunta11_rutinas(update: Update, context: CallbackContext):
		logger.info("El usuario %s selecciona la categoría de su rutina", context.user_data["nombre_usuario"])
		context.user_data['nombre_rutina'] = update.message.text
		if (update.message.text.upper() == '/salir'.upper()):
			update.message.reply_text(
				text="¡Hasta pronto!"
			)
			return ConversationHandler.END
		datos = bd_bot.leer_rutinas(str(context.user_data['id_usuario']))
		for data in datos:
			if(str(data[2].upper()) == str(context.user_data['nombre_rutina'].upper())):
				update.message.reply_text(
				text ='💬 Ya existe una rutina con ese nombre. Vuelve a escribir el nombre de su rutina.',
				parse_mode=telegram.ParseMode.HTML,

				)
				return PREGUNTA11_RUTINAS
		keyboard = []
		datos = bd_bot.leer_categorias_rutina_usuario2(str(context.user_data["id_usuario"]))
		if datos:
			for data in datos:
				keyboard.append([InlineKeyboardButton('🔹 ' + str(data[2]),
									callback_data=data[2])])
		reply_markup = InlineKeyboardMarkup(keyboard)
		update.message.reply_text(
		text ='Elige una categoría para su rutina.',
		parse_mode=telegram.ParseMode.HTML,
		reply_markup=reply_markup
		)

		return PREGUNTA2_RUTINAS


def pregunta2_rutinas(update: Update, context: CallbackContext):
		logger.info("El usuario %s establece la frecuencia de su rutina (veces por semana)", context.user_data["nombre_usuario"])
		query = update.callback_query
		context.user_data['categoria_rutina'] = query.data
		teclado_horassemana= [
					[InlineKeyboardButton("1 vez por semana",   callback_data='1')],
					[InlineKeyboardButton("2 veces por semana", callback_data='2')],
					[InlineKeyboardButton("3 veces por semana", callback_data='3')],
					[InlineKeyboardButton("4 veces por semana", callback_data='4')],
					[InlineKeyboardButton("5 veces por semana", callback_data='5')],
					[InlineKeyboardButton("6 veces por semana", callback_data='6')],
					[InlineKeyboardButton("7 veces por semana", callback_data='7')],
					]
		reply_markup = InlineKeyboardMarkup(teclado_horassemana)
		context.bot.send_message(
			text ='Elige la frecuencia que tendrá su rutina por semana.',
			parse_mode=telegram.ParseMode.HTML,
			chat_id = query.message.chat_id,
			reply_markup=reply_markup
		)

		return PREGUNTA3_RUTINAS


def pregunta3_rutinas(update: Update, context: CallbackContext):
		logger.info("El usuario %s selecciona cuantas horas le dedicara a su rutina", context.user_data["nombre_usuario"])
		query = update.callback_query
		context.user_data['repeticion_rutina'] = query.data
		context.user_data['veces_rutina'] = query.data
		teclado_horassemana= [
					[InlineKeyboardButton("1 hora",  callback_data='1')],
					[InlineKeyboardButton("2 horas", callback_data='2')],
					[InlineKeyboardButton("3 horas", callback_data='3')],
					[InlineKeyboardButton("4 horas", callback_data='4')],
					[InlineKeyboardButton("5 horas", callback_data='5')],
					[InlineKeyboardButton("Elegir horas", callback_data='6')],
					]
		reply_markup = InlineKeyboardMarkup(teclado_horassemana)
		context.bot.send_message(
			text ='¿Cuantas horas por día quieres dedicarle?',
			parse_mode=telegram.ParseMode.HTML,
			chat_id = query.message.chat_id,
			reply_markup=reply_markup
		)
		return PREGUNTA4_RUTINAS


def pregunta4_rutinas(update: Update, context: CallbackContext):
		logger.info("El usuario %s indica qué dias le dedicara a su rutina (L,M,X...)", context.user_data["nombre_usuario"])
		query = update.callback_query
		context.user_data['duracion_rutina'] = query.data
		print('numero de horas otra vez 2',context.user_data['duracion_rutina'])
		context.user_data['lunes'] = 7
		context.user_data['martes'] = 7
		context.user_data['miercoles'] = 7
		context.user_data['jueves'] = 7
		context.user_data['viernes'] = 7
		context.user_data['sabado'] = 7
		context.user_data['domingo'] = 7
		if(query.data == '6'):
			context.bot.send_message(
						text ='Escribe las horas',
						parse_mode=telegram.ParseMode.HTML,
						chat_id = query.message.chat_id,

			)
			return HORAS_RUTINA
		else:
			teclado_diassemana= [
								[InlineKeyboardButton("Lunes", callback_data='0')],
								[InlineKeyboardButton("Martes", callback_data='1')],
								[InlineKeyboardButton("Miercoles", callback_data='2')],
								[InlineKeyboardButton("Jueves", callback_data='3')],
								[InlineKeyboardButton("Viernes", callback_data='4')],
								[InlineKeyboardButton("Sabado", callback_data='5')],
								[InlineKeyboardButton("Domingo", callback_data='6')],
								]

			reply_markup = InlineKeyboardMarkup(teclado_diassemana)
			context.bot.send_message(
						text ='¿Qué días de la semana quieres que se repita?' ,
						parse_mode=telegram.ParseMode.HTML,
						chat_id = query.message.chat_id,
						reply_markup=reply_markup
			)

		return PREGUNTA5_RUTINAS


def pregunta4_rutinas_horas(update: Update, context: CallbackContext):
		logger.info("El usuario %s indica qué dias le dedicara a su rutina (L,M,X...)", context.user_data["nombre_usuario"])
		query = update.callback_query
		print('numero de horas eligiendo',context.user_data['duracion_rutina'])
		context.user_data['lunes'] = 7
		context.user_data['martes'] = 7
		context.user_data['miercoles'] = 7
		context.user_data['jueves'] = 7
		context.user_data['viernes'] = 7
		context.user_data['sabado'] = 7
		context.user_data['domingo'] = 7

		teclado_diassemana= [
							[InlineKeyboardButton("Lunes", callback_data='0')],
							[InlineKeyboardButton("Martes", callback_data='1')],
							[InlineKeyboardButton("Miercoles", callback_data='2')],
							[InlineKeyboardButton("Jueves", callback_data='3')],
							[InlineKeyboardButton("Viernes", callback_data='4')],
							[InlineKeyboardButton("Sabado", callback_data='5')],
							[InlineKeyboardButton("Domingo", callback_data='6')],
							]

		reply_markup = InlineKeyboardMarkup(teclado_diassemana)
		context.bot.send_message(
					text ='¿Qué días de la semana quieres que se repita?' ,
					parse_mode=telegram.ParseMode.HTML,
					chat_id = query.message.chat_id,
					reply_markup=reply_markup
		)

		return PREGUNTA5_RUTINAS


def horas_rutina(update: Update, context: CallbackContext):
		logger.info("El usuario %s escribe cuantas horas dedicara a su rutina", context.user_data["nombre_usuario"])
		context.user_data['duracion_rutina'] = update.message.text
		print('numero de horas que has escrito por teclado',context.user_data['duracion_rutina'])
		teclado_diassemana= [
							[InlineKeyboardButton("Continuar", callback_data=str(PREGUNTA4_RUTINAS_HORAS))],
							]

		if (update.message.text.upper() == '/salir'.upper()):
			update.message.reply_text(
				text="¡Hasta pronto!"
			)
			return ConversationHandler.END
		if not funciones.valida_float(str(context.user_data['duracion_rutina'])) and not funciones.valida_entero(str(context.user_data['duracion_rutina'])):
			update.message.reply_text(
			text="Error al escribir el número de horas ❌, solo se admiten números positivos.. Vuelva a escribir el número de horas.\n",
			parse_mode=telegram.ParseMode.HTML,
			)
			return HORAS_RUTINA
		else:
			reply_markup = InlineKeyboardMarkup(teclado_diassemana)
			update.message.reply_text(
			text="Pulsa continuar para seguir creando tu rutina.\n",
			parse_mode=telegram.ParseMode.HTML,
			reply_markup=reply_markup
			)
			return EDICIONES_RUTINA

def pregunta5_rutinas(update: Update, context: CallbackContext):
	logger.info("El usuario %s selecciona los días de su rutina (L,M,X)", context.user_data["nombre_usuario"])
	query = update.callback_query
	context.user_data['dias_rutina'] = query.data
	veces = int(context.user_data['repeticion_rutina'])
	context.user_data['repeticion_rutina'] =  int(context.user_data['repeticion_rutina'])-1
	int(context.user_data['repeticion_rutina'])
	# print('veces -- ',int(context.user_data['repeticion_rutina']))
	lunes = 'Lunes'
	martes = 'Martes'
	miercoles = 'Miercoles'
	jueves = 'Jueves'
	viernes = 'Viernes'
	sabado = 'Sabado'
	domingo = 'Domingo'

	if int(context.user_data['repeticion_rutina']) == 0:

		if int(query.data) == 0:
			context.user_data['lunes'] = 0
		elif int(query.data) == 1:
			context.user_data['martes'] = 1
		elif int(query.data) == 2:
				context.user_data['miercoles'] = 2
		elif int(query.data) == 3:
			context.user_data['jueves'] = 3
		elif int(query.data) == 4:
			context.user_data['viernes'] = 4
		elif int(query.data) == 5:
			context.user_data['sabado'] = 5
		elif int(query.data) == 6:
			context.user_data['domingo'] = 6

		context.user_data['dias'] = []
		if int(context.user_data['lunes']) == 0:
			lunes = 'Lunes ✅'
			context.user_data['dias'].append(0)
			# print('diasssssssssssss', str(context.user_data['dias']))
		if int(context.user_data['martes']) == 1:
			martes = 'Martes ✅'
			context.user_data['dias'].append(1)
			# print('diasssssssssssss', str(context.user_data['dias']))
		if int(context.user_data['miercoles']) == 2:
			miercoles = 'Miercoles ✅'
			context.user_data['dias'].append(2)
		if int(context.user_data['jueves'] ) == 3:
			jueves = 'Jueves ✅'
			context.user_data['dias'].append(3)
		if int(context.user_data['viernes']) == 4:
			viernes = 'Viernes ✅ '
			context.user_data['dias'].append(4)
		if int(context.user_data['sabado']) == 5:
			sabado = 'Sabado ✅'
			context.user_data['dias'].append(5)
		if int(context.user_data['domingo']) == 6:
			domingo = 'Domingo ✅'
			context.user_data['dias'].append(6)
		# print('duracion de la rutina',context.user_data['duracion_rutina'])
		text ='<b>Resumen:</b>\nRecordatorio de rutina establecida para los dias marcados:\n'+ \
		lunes + '\n'+ martes+ '\n'+  miercoles+ '\n'+  jueves+ '\n'+  viernes+ '\n'+ sabado+ '\n'+ domingo,
		context.bot.send_message(
			text='<b>Resumen de la rutina:</b>\n\n' \
			+ '🔷 <b>Nombre: </b>'+  str(context.user_data['nombre_rutina']) + '\n' \
			+ '🔷 <b>Categoría: </b>'+  str(context.user_data['categoria_rutina']) + '\n' \
			 + '🔷 <b>Duración: </b>' + context.user_data['duracion_rutina'] +  ' horas\n' \
			+ '🔷 <b>Repetición: </b>' + str(context.user_data['veces_rutina']) +  ' días a la semana' + '\n',
			parse_mode=telegram.ParseMode.HTML,
			chat_id = query.message.chat_id,
		)
		context.bot.send_message(
			text='🔷 <b>Se repite los días marcados</b>\n➖ ' + lunes + '\n➖ '+ martes+ '\n➖ '+  miercoles+ '\n➖ '+  jueves+ '\n➖ '+  viernes+ '\n➖ '+ sabado+ '\n➖ '+ domingo,
			parse_mode=telegram.ParseMode.HTML,
			chat_id = query.message.chat_id,
		)
		teclado_diassemana= [
							[InlineKeyboardButton("🔙 Cancelar", callback_data=str(VOLVER_MENU_RUTINAS))],
							[InlineKeyboardButton("💾 Guardar ", callback_data=str(PREGUNTA6_RUTINAS))],
							[InlineKeyboardButton("💾⏰ Guardar con recordatorio ", callback_data=str(PREGUNTA6_RUTINAS_HORA))],
							]

		reply_markup = InlineKeyboardMarkup(teclado_diassemana)
		context.bot.send_message(
				text="¿Guardar rutina?\n",
				parse_mode=telegram.ParseMode.HTML,
				chat_id = query.message.chat_id,
				reply_markup=reply_markup

			)

		return EDICIONES_RUTINA
	else:

		if int(query.data) == 0:
				context.user_data['lunes'] = 0
				teclado_diassemana= [
									[InlineKeyboardButton("Lunes ✅", callback_data='0')],
									[InlineKeyboardButton("Martes", callback_data='1')],
									[InlineKeyboardButton("Miercoles ", callback_data='2')],
									[InlineKeyboardButton("Jueves", callback_data='3')],
									[InlineKeyboardButton("Viernes", callback_data='4')],
									[InlineKeyboardButton("Sabado", callback_data='5')],
									[InlineKeyboardButton("Domingo", callback_data='6')],
									]

				reply_markup = InlineKeyboardMarkup(teclado_diassemana)
				context.bot.send_message(
							text ='¿Qué días de la semana quieres que se repita?',
							parse_mode=telegram.ParseMode.HTML,
							chat_id = query.message.chat_id,
							reply_markup=reply_markup
				)
				return PREGUNTA5_RUTINAS
		elif int(query.data) == 1 and str(context.user_data['martes']) == '7':
			context.user_data['martes'] = 1
			teclado_diassemana= [
								[InlineKeyboardButton("Lunes ", callback_data='0')],
								[InlineKeyboardButton("Martes ✅", callback_data='1')],
								[InlineKeyboardButton("Miercoles", callback_data='2')],
								[InlineKeyboardButton("Jueves", callback_data='3')],
								[InlineKeyboardButton("Viernes", callback_data='4')],
								[InlineKeyboardButton("Sabado", callback_data='5')],
								[InlineKeyboardButton("Domingo", callback_data='6')],
								]

			reply_markup = InlineKeyboardMarkup(teclado_diassemana)
			context.bot.send_message(
						text ='¿Qué días de la semana quieres que se repita?',
						parse_mode=telegram.ParseMode.HTML,
						chat_id = query.message.chat_id,
						reply_markup=reply_markup
			)
			return PREGUNTA5_RUTINAS
		elif int(query.data) == 2:
				context.user_data['miercoles'] = 2
				teclado_diassemana= [
									[InlineKeyboardButton("Lunes ", callback_data='0')],
									[InlineKeyboardButton("Martes", callback_data='1')],
									[InlineKeyboardButton("Miercoles ✅", callback_data='2')],
									[InlineKeyboardButton("Jueves", callback_data='3')],
									[InlineKeyboardButton("Viernes", callback_data='4')],
									[InlineKeyboardButton("Sabado", callback_data='5')],
									[InlineKeyboardButton("Domingo", callback_data='6')],
									]

				reply_markup = InlineKeyboardMarkup(teclado_diassemana)
				context.bot.send_message(
							text ='¿Qué días de la semana quieres que se repita?',
							parse_mode=telegram.ParseMode.HTML,
							chat_id = query.message.chat_id,
							reply_markup=reply_markup
				)
				return PREGUNTA5_RUTINAS
		elif int(query.data) == 3:
			context.user_data['jueves'] = 3
			teclado_diassemana= [
									[InlineKeyboardButton("Lunes ", callback_data='0')],
									[InlineKeyboardButton("Martes", callback_data='1')],
									[InlineKeyboardButton("Miercoles", callback_data='2')],
									[InlineKeyboardButton("Jueves ✅", callback_data='3')],
									[InlineKeyboardButton("Viernes", callback_data='4')],
									[InlineKeyboardButton("Sabado", callback_data='5')],
									[InlineKeyboardButton("Domingo", callback_data='6')],
									]

			reply_markup = InlineKeyboardMarkup(teclado_diassemana)
			context.bot.send_message(
							text ='¿Qué días de la semana quieres que se repita?',
							parse_mode=telegram.ParseMode.HTML,
							chat_id = query.message.chat_id,
							reply_markup=reply_markup
			)
			return PREGUNTA5_RUTINAS
		elif int(query.data) == 4:
			context.user_data['viernes'] = 4
			teclado_diassemana= [
									[InlineKeyboardButton("Lunes ", callback_data='0')],
									[InlineKeyboardButton("Martes", callback_data='1')],
									[InlineKeyboardButton("Miercoles", callback_data='2')],
									[InlineKeyboardButton("Jueves", callback_data='3')],
									[InlineKeyboardButton("Viernes ✅", callback_data='4')],
									[InlineKeyboardButton("Sabado", callback_data='5')],
									[InlineKeyboardButton("Domingo", callback_data='6')],
									]

			reply_markup = InlineKeyboardMarkup(teclado_diassemana)
			context.bot.send_message(
							text ='¿Qué días de la semana quieres que se repita?',
							parse_mode=telegram.ParseMode.HTML,
							chat_id = query.message.chat_id,
							reply_markup=reply_markup
				)
			return PREGUNTA5_RUTINAS
		elif int(query.data) == 5:
			context.user_data['sabado'] = 5
			teclado_diassemana= [
									[InlineKeyboardButton("Lunes ", callback_data='0')],
									[InlineKeyboardButton("Martes", callback_data='1')],
									[InlineKeyboardButton("Miercoles", callback_data='2')],
									[InlineKeyboardButton("Jueves", callback_data='3')],
									[InlineKeyboardButton("Viernes", callback_data='4')],
									[InlineKeyboardButton("Sabado ✅", callback_data='5')],
									[InlineKeyboardButton("Domingo", callback_data='6')],
									]

			reply_markup = InlineKeyboardMarkup(teclado_diassemana)
			context.bot.send_message(
							text ='¿Qué días de la semana quieres que se repita?',
							parse_mode=telegram.ParseMode.HTML,
							chat_id = query.message.chat_id,
							reply_markup=reply_markup
				)
			return PREGUNTA5_RUTINAS
		elif int(query.data) == 6:
			context.user_data['domingo'] = 6
			teclado_diassemana= [
									[InlineKeyboardButton("Lunes ", callback_data='0')],
									[InlineKeyboardButton("Martes", callback_data='1')],
									[InlineKeyboardButton("Miercoles", callback_data='2')],
									[InlineKeyboardButton("Jueves", callback_data='3')],
									[InlineKeyboardButton("Viernes", callback_data='4')],
									[InlineKeyboardButton("Sabado", callback_data='5')],
									[InlineKeyboardButton("Domingo ✅", callback_data='6')],
									]

			reply_markup = InlineKeyboardMarkup(teclado_diassemana)
			context.bot.send_message(
							text ='¿Qué días de la semana quieres que se repita?',
							parse_mode=telegram.ParseMode.HTML,
							chat_id = query.message.chat_id,
							reply_markup=reply_markup
				)


			return PREGUNTA5_RUTINAS

def pregunta6_rutinas(update: Update, context: CallbackContext):
	logger.info("El usuario %s guarda su rutina sin recordatorio", context.user_data["nombre_usuario"])
	query = update.callback_query
	lunes = 'Lunes'
	martes = 'Martes'
	miercoles = 'Miercoles'
	jueves = 'Jueves'
	viernes = 'Viernes'
	sabado = 'Sabado'
	domingo = 'Domingo'

	context.user_data['dias'] = []
	if int(context.user_data['lunes']) == 0:
		lunes = 'Lunes ✅'
		context.user_data['dias'].append(0)
		# print('diasssssssssssss', str(context.user_data['dias']))
	if int(context.user_data['martes']) == 1:
		martes = 'Martes ✅'
		context.user_data['dias'].append(1)
		# print('diasssssssssssss', str(context.user_data['dias']))
	if int(context.user_data['miercoles']) == 2:
		miercoles = 'Miercoles ✅'
		context.user_data['dias'].append(2)
	if int(context.user_data['jueves'] ) == 3:
		jueves = 'Jueves ✅'
		context.user_data['dias'].append(3)
	if int(context.user_data['viernes']) == 4:
		viernes = 'Viernes ✅ '
		context.user_data['dias'].append(4)
	if int(context.user_data['sabado']) == 5:
		sabado = 'Sabado ✅'
		context.user_data['dias'].append(5)
	if int(context.user_data['domingo']) == 6:
		domingo = 'Domingo ✅'
		context.user_data['dias'].append(6)

	now = datetime.now()
	anio = now.year   # Año.
	mes = now.month  # Mes.
	dia = now.day
	hora = now.hour
	minuto = now.minute
	id_usuario = context.user_data['id_usuario']
	nombre_rutina = context.user_data['nombre_rutina']
	categoria_rutina = context.user_data['categoria_rutina']
	repeticion_rutina = context.user_data['veces_rutina']
	duracion_rutina = context.user_data['duracion_rutina']
	valor = str(context.user_data['dias'])
	columna = 'dias_rutina'
	separator = ''
	context.user_data['dias_g'] = separator.join(valor) #

	bd_bot.insertar_rutina(id_usuario,nombre_rutina,categoria_rutina,repeticion_rutina,duracion_rutina,str(context.user_data['dias_g']),0)

	teclado_volver= [
							[InlineKeyboardButton("Volver a menú rutinas", callback_data=str(VOLVER_MENU_RUTINAS))],
						]

	reply_markup = InlineKeyboardMarkup(teclado_volver)
	context.bot.send_message(
					text="💬 Se ha guardado su rutina. 💾'\n",
					parse_mode=telegram.ParseMode.HTML,
					chat_id = query.message.chat_id,
					reply_markup=reply_markup
	)

	return EDICIONES_RUTINA


def pregunta6_rutinas_hora(update: Update, context: CallbackContext):
	logger.info("El usuario %s establece hora para su recordatorio", context.user_data["nombre_usuario"])
	query = update.callback_query
	context.bot.send_message(
				text="\n\nEscribe la hora. Ejemplo 23:40",
				chat_id = query.message.chat_id,
				parse_mode=telegram.ParseMode.HTML,
	)

	return PREGUNTA6_RUTINAS_R


def pregunta6_rutinas_r(update: Update, context: CallbackContext):
	logger.info("El usuario %s guarda su rutina con recordatorio", context.user_data["nombre_usuario"])
	context.user_data['hora_recordr'] = update.message.text
	if not funciones.valida_hora(context.user_data['hora_recordr']):
		update.message.reply_text(
		text="💬 Has introducido la hora en un formato incorrecto ❌. Escríbelo con el formato hh:mm. Ej. 23:40 \n",
		)
		return PREGUNTA6_RUTINAS_R
	else:
		lunes = 'Lunes'
		martes = 'Martes'
		miercoles = 'Miercoles'
		jueves = 'Jueves'
		viernes = 'Viernes'
		sabado = 'Sabado'
		domingo = 'Domingo'
		context.user_data['dias'] = []

		if int(context.user_data['lunes']) == 0:
			lunes = 'Lunes ✅'
			context.user_data['dias'].append(0)
			# print('diasssssssssssss', str(context.user_data['dias']))
		if int(context.user_data['martes']) == 1:
			martes = 'Martes ✅'
			context.user_data['dias'].append(1)
			# print('diasssssssssssss', str(context.user_data['dias']))
		if int(context.user_data['miercoles']) == 2:
			miercoles = 'Miercoles ✅'
			context.user_data['dias'].append(2)
		if int(context.user_data['jueves'] ) == 3:
			jueves = 'Jueves ✅'
			context.user_data['dias'].append(3)
		if int(context.user_data['viernes']) == 4:
			viernes = 'Viernes ✅ '
			context.user_data['dias'].append(4)
		if int(context.user_data['sabado']) == 5:
			sabado = 'Sabado ✅'
			context.user_data['dias'].append(5)
		if int(context.user_data['domingo']) == 6:
			domingo = 'Domingo ✅'
			context.user_data['dias'].append(6)


		now = datetime.now()
		anio = now.year   # Año.
		mes = now.month  # Mes.
		dia = now.day
		hora = now.hour
		minuto = now.minute
		id_usuario = context.user_data['id_usuario']
		nombre_rutina = context.user_data['nombre_rutina']
		categoria_rutina = context.user_data['categoria_rutina']
		repeticion_rutina = context.user_data['veces_rutina']
		duracion_rutina = context.user_data['duracion_rutina']

		valor = str(context.user_data['dias'])
		columna = 'dias_rutina'
		separator = ''
		context.user_data['dias_g'] = separator.join(valor) #
		print('Inserta rutina y recordatorio ')
		bd_bot.insertar_rutina(id_usuario,nombre_rutina,categoria_rutina,repeticion_rutina,duracion_rutina,str(context.user_data['dias_g']),0)

		id = str(context.user_data['id_usuario'])
		nombre_alarma = now.strftime(id +"-%d-%m-%Y-%H:%M:%S")
		chat_id= update.message.chat_id
		now = datetime.now()
		anio = now.year   # Año.
		mes = now.month  # Mes.
		dia = now.day
		mi_hora= datetime.strptime(context.user_data['hora_recordr'], "%H:%M")
		hora = mi_hora.hour
		minuto = mi_hora.minute
		# creción del recordatorio para la rutina
		zona_horaria = tz.gettz('Europe/Madrid')
		recor = context.user_data['nombre_rutina']
		context.job_queue.run_daily(alarma_rutina, time(hour=hora, minute=minuto, tzinfo=zona_horaria), days=(tuple(context.user_data['dias'])), context=(update.message.chat_id,recor,tuple(context.user_data['dias'])), name=nombre_alarma)
		teclado_volver= [
								[InlineKeyboardButton("Volver a menú rutinas", callback_data=str(VOLVER_MENU_RUTINAS))],
							]

		reply_markup = InlineKeyboardMarkup(teclado_volver)
		update.message.reply_text(
						text="💬 Se ha guardado el recordatorio de su rutina. 💾\n",
						parse_mode=telegram.ParseMode.HTML,


		)
		update.message.reply_text(
						text='<b>Resumen del recordatorio:</b>\n' \
						+ '🔷 <b>Nombre: </b>'+  str(context.user_data['nombre_rutina']) + '\n' \
						+ '🔷 <b>Sonará a las: </b>'+ str(context.user_data['hora_recordr']) + '\n' \
						+'🔷 <b>Los días marcados</b>\n➖ ' + lunes + '\n➖ '+ martes+ '\n➖ '+  miercoles+ '\n➖ '+  jueves+ '\n➖ '+  viernes+ '\n➖ '+ sabado+ '\n➖ '+ domingo,
						parse_mode=telegram.ParseMode.HTML,
						reply_markup=reply_markup
		)
		return EDICIONES_RUTINA


def recordatorio_rutina(update: Update, context: CallbackContext):
	logger.info("El usuario %s está establece hora", context.user_data["nombre_usuario"])
	query = update.callback_query
	context.bot.send_message(
				text="\n\nEscribe la hora. Ejemplo 23:40",
				chat_id = query.message.chat_id,
				parse_mode=telegram.ParseMode.HTML,
	)

	return HORA_RECORDATORIOR


def hora_recordatorior(update: Update, context: CallbackContext):
	logger.info("El usuario %s establece la hora para el recordatorio de su rutina", context.user_data["nombre_usuario"])
	context.user_data['hora_recordr'] = update.message.text
	id_rutina = context.user_data['id_rutina']
	datos= bd_bot.leerid_rutina(id_rutina)
	if (update.message.text.upper() == '/salir'.upper()):
		update.message.reply_text(
			text="¡Hasta pronto!"
		)
		return ConversationHandler.END
	if not funciones.valida_hora(context.user_data['hora_recordr']):
		update.message.reply_text(
		text="Datos o formato incorrecto. Escríbelo con el formato hh:mm. Ej. 23:40 \n",
		)
		return HORA_RECORDATORIOR

	else:
		for data in datos:
			context.user_data['repeticion_rutina'] = str(data[4])
		context.user_data['lunes'] = 7
		context.user_data['martes'] = 7
		context.user_data['miercoles'] = 7
		context.user_data['jueves'] = 7
		context.user_data['viernes'] = 7
		context.user_data['sabado'] = 7
		context.user_data['domingo'] = 7
		teclado_diassemana= [
							[InlineKeyboardButton("Lunes", callback_data='0')],
							[InlineKeyboardButton("Martes", callback_data='1')],
							[InlineKeyboardButton("Miercoles", callback_data='2')],
							[InlineKeyboardButton("Jueves", callback_data='3')],
							[InlineKeyboardButton("Viernes", callback_data='4')],
							[InlineKeyboardButton("Sabado", callback_data='5')],
							[InlineKeyboardButton("Domingo", callback_data='6')],
							]

		reply_markup = InlineKeyboardMarkup(teclado_diassemana)
		update.message.reply_text(
					text ='¿Qué días de la semana quieres que te recuerde la rutina?',
					parse_mode=telegram.ParseMode.HTML,
					reply_markup=reply_markup
		)

		return EDITADIAS_RECORD


def editadias_record(update: Update, context: CallbackContext):
	logger.info("El usuario %s edita los dias elegidos para su rutina", context.user_data["nombre_usuario"])
	query = update.callback_query
	veces = int(context.user_data['repeticion_rutina'])
	context.user_data['repeticion_rutina'] =  int(context.user_data['repeticion_rutina'])-1
	int(context.user_data['repeticion_rutina'])
	# print('veces -- ',int(context.user_data['repeticion_rutina']))

	if int(context.user_data['repeticion_rutina']) == 0:
		if int(query.data) == 0:
			context.user_data['lunes'] = 0
		elif int(query.data) == 1:
			context.user_data['martes'] = 1
		elif int(query.data) == 2:
				context.user_data['miercoles'] = 2
		elif int(query.data) == 3:
			context.user_data['jueves'] = 3
		elif int(query.data) == 4:
			context.user_data['viernes'] = 4
		elif int(query.data) == 5:
			context.user_data['sabado'] = 5
		elif int(query.data) == 6:
			context.user_data['domingo'] = 6

		teclado_diassemana= [
							[InlineKeyboardButton("🔙 Cancelar", callback_data=str(VOLVER_MENU_RUTINAS))],
							[InlineKeyboardButton("⏰💾 Guardar recordatorio ", callback_data=str(GUARDA_DIAS_RECORD))],
							]

		reply_markup = InlineKeyboardMarkup(teclado_diassemana)
		context.bot.send_message(
				text="<b>¿Guardar recordatorio?</b>\n",
				parse_mode=telegram.ParseMode.HTML,
				chat_id = query.message.chat_id,
				reply_markup=reply_markup

			)

		return EDICIONES_RUTINA
	else:

		if int(query.data) == 0:
			context.user_data['lunes'] = 0
			teclado_diassemana= [
								[InlineKeyboardButton("Lunes ✅", callback_data='0')],
								[InlineKeyboardButton("Martes", callback_data='1')],
								[InlineKeyboardButton("Miercoles", callback_data='2')],
								[InlineKeyboardButton("Jueves", callback_data='3')],
								[InlineKeyboardButton("Viernes", callback_data='4')],
								[InlineKeyboardButton("Sabado", callback_data='5')],
								[InlineKeyboardButton("Domingo", callback_data='6')],
								]

			reply_markup = InlineKeyboardMarkup(teclado_diassemana)
			context.bot.send_message(
						text ='¿Qué días de la semana quieres que se repita?',
						parse_mode=telegram.ParseMode.HTML,
						chat_id = query.message.chat_id,
						reply_markup=reply_markup
			)
			return EDITADIAS_RECORD
		elif int(query.data) == 1:
			context.user_data['martes'] = 1
			teclado_diassemana= [
								[InlineKeyboardButton("Lunes ", callback_data='0')],
								[InlineKeyboardButton("Martes ✅", callback_data='1')],
								[InlineKeyboardButton("Miercoles", callback_data='2')],
								[InlineKeyboardButton("Jueves", callback_data='3')],
								[InlineKeyboardButton("Viernes", callback_data='4')],
								[InlineKeyboardButton("Sabado", callback_data='5')],
								[InlineKeyboardButton("Domingo", callback_data='6')],
								]

			reply_markup = InlineKeyboardMarkup(teclado_diassemana)
			context.bot.send_message(
						text ='¿Qué días de la semana quieres que se repita?',
						parse_mode=telegram.ParseMode.HTML,
						chat_id = query.message.chat_id,
						reply_markup=reply_markup
			)
			return EDITADIAS_RECORD
		elif int(query.data) == 2:
				context.user_data['miercoles'] = 2
				teclado_diassemana= [
									[InlineKeyboardButton("Lunes ", callback_data='0')],
									[InlineKeyboardButton("Martes", callback_data='1')],
									[InlineKeyboardButton("Miercoles ✅", callback_data='2')],
									[InlineKeyboardButton("Jueves", callback_data='3')],
									[InlineKeyboardButton("Viernes", callback_data='4')],
									[InlineKeyboardButton("Sabado", callback_data='5')],
									[InlineKeyboardButton("Domingo", callback_data='6')],
									]

				reply_markup = InlineKeyboardMarkup(teclado_diassemana)
				context.bot.send_message(
							text ='¿Qué días de la semana quieres que se repita?',
							parse_mode=telegram.ParseMode.HTML,
							chat_id = query.message.chat_id,
							reply_markup=reply_markup
				)
				return EDITADIAS_RECORD
		elif int(query.data) == 3:
			context.user_data['jueves'] = 3
			teclado_diassemana= [
									[InlineKeyboardButton("Lunes ", callback_data='0')],
									[InlineKeyboardButton("Martes", callback_data='1')],
									[InlineKeyboardButton("Miercoles", callback_data='2')],
									[InlineKeyboardButton("Jueves ✅", callback_data='3')],
									[InlineKeyboardButton("Viernes", callback_data='4')],
									[InlineKeyboardButton("Sabado", callback_data='5')],
									[InlineKeyboardButton("Domingo", callback_data='6')],
									]

			reply_markup = InlineKeyboardMarkup(teclado_diassemana)
			context.bot.send_message(
							text ='¿Qué días de la semana quieres que se repita?',
							parse_mode=telegram.ParseMode.HTML,
							chat_id = query.message.chat_id,
							reply_markup=reply_markup
			)
			return EDITADIAS_RECORD
		elif int(query.data) == 4:
			context.user_data['viernes'] = 4
			teclado_diassemana= [
									[InlineKeyboardButton("Lunes ", callback_data='0')],
									[InlineKeyboardButton("Martes", callback_data='1')],
									[InlineKeyboardButton("Miercoles", callback_data='2')],
									[InlineKeyboardButton("Jueves", callback_data='3')],
									[InlineKeyboardButton("Viernes ✅", callback_data='4')],
									[InlineKeyboardButton("Sabado", callback_data='5')],
									[InlineKeyboardButton("Domingo", callback_data='6')],
									]

			reply_markup = InlineKeyboardMarkup(teclado_diassemana)
			context.bot.send_message(
							text ='¿Qué días de la semana quieres que se repita?',
							parse_mode=telegram.ParseMode.HTML,
							chat_id = query.message.chat_id,
							reply_markup=reply_markup
				)
			return EDITADIAS_RECORD
		elif int(query.data) == 5:
			context.user_data['sabado'] = 5
			teclado_diassemana= [
									[InlineKeyboardButton("Lunes ", callback_data='0')],
									[InlineKeyboardButton("Martes", callback_data='1')],
									[InlineKeyboardButton("Miercoles", callback_data='2')],
									[InlineKeyboardButton("Jueves", callback_data='3')],
									[InlineKeyboardButton("Viernes", callback_data='4')],
									[InlineKeyboardButton("Sabado ✅", callback_data='5')],
									[InlineKeyboardButton("Domingo", callback_data='6')],
									]

			reply_markup = InlineKeyboardMarkup(teclado_diassemana)
			context.bot.send_message(
							text ='¿Qué días de la semana quieres que se repita?',
							parse_mode=telegram.ParseMode.HTML,
							chat_id = query.message.chat_id,
							reply_markup=reply_markup
				)
			return EDITADIAS_RECORD
		elif int(query.data) == 6:
			context.user_data['domingo'] = 6
			teclado_diassemana= [
									[InlineKeyboardButton("Lunes ", callback_data='0')],
									[InlineKeyboardButton("Martes", callback_data='1')],
									[InlineKeyboardButton("Miercoles", callback_data='2')],
									[InlineKeyboardButton("Jueves", callback_data='3')],
									[InlineKeyboardButton("Viernes", callback_data='4')],
									[InlineKeyboardButton("Sabado", callback_data='5')],
									[InlineKeyboardButton("Domingo ✅", callback_data='6')],
									]

			reply_markup = InlineKeyboardMarkup(teclado_diassemana)
			context.bot.send_message(
							text ='¿Qué días de la semana quieres que se repita?',
							parse_mode=telegram.ParseMode.HTML,
							chat_id = query.message.chat_id,
							reply_markup=reply_markup
				)


			return EDITADIAS_RECORD

def guarda_dias_record(update: Update, context: CallbackContext):
	logger.info("El usuario %s guarda los dias de su rutina", context.user_data["nombre_usuario"])
	query = update.callback_query
	now = datetime.now()
	anio = now.year   # Año.
	mes = now.month  # Mes.
	dia = now.day
	lunes = 'Lunes'
	martes = 'Martes'
	miercoles = 'Miercoles'
	jueves = 'Jueves'
	viernes = 'Viernes'
	sabado = 'Sabado'
	domingo = 'Domingo'
	context.user_data['dias'] = []

	if int(context.user_data['lunes']) == 0:
		lunes = 'Lunes ✅'
		context.user_data['dias'].append(0)
		# print('diasssssssssssss', str(context.user_data['dias']))
	if int(context.user_data['martes']) == 1:
		martes = 'Martes ✅'
		context.user_data['dias'].append(1)
		# print('diasssssssssssss', str(context.user_data['dias']))
	if int(context.user_data['miercoles']) == 2:
		miercoles = 'Miercoles ✅'
		context.user_data['dias'].append(2)
	if int(context.user_data['jueves'] ) == 3:
		jueves = 'Jueves ✅'
		context.user_data['dias'].append(3)
	if int(context.user_data['viernes']) == 4:
		viernes = 'Viernes ✅ '
		context.user_data['dias'].append(4)
	if int(context.user_data['sabado']) == 5:
		sabado = 'Sabado ✅'
		context.user_data['dias'].append(5)
	if int(context.user_data['domingo']) == 6:
		domingo = 'Domingo ✅'
		context.user_data['dias'].append(6)

	valor = str(context.user_data['dias'])
	columna = 'dias_rutina'
	separator = ''
	context.user_data['dias_g'] = separator.join(valor) #

	id = str(context.user_data['id_usuario'])
	nombre_alarma = now.strftime(id +"-%d-%m-%Y-%H:%M:%S")
	chat_id= query.message.chat_id
	mi_hora= datetime.strptime(context.user_data['hora_recordr'], "%H:%M")
	hora = mi_hora.hour
	minuto = mi_hora.minute


	valor2 = context.user_data['dias_g']
	id_rutina =  context.user_data['id_rutina']
	columna = 'dias_rutina'
	bd_bot.actualizar_campor(columna,valor2,id_rutina)


	# creción del recordatorio para la rutina
	zona_horaria = tz.gettz('Europe/Madrid')
	recor = context.user_data['nombre_rutina']
	context.job_queue.run_daily(alarma_rutina, time(hour=hora, minute=minuto, tzinfo=zona_horaria), days=(tuple(context.user_data['dias'])), context=(query.message.chat_id,recor,tuple(context.user_data['dias'])), name=nombre_alarma)


	teclado_volver= [
								[InlineKeyboardButton("Volver a menú rutinas", callback_data=str(VOLVER_MENU_RUTINAS))],
							]

	reply_markup = InlineKeyboardMarkup(teclado_volver)
	context.bot.send_message(
					text="💬 Se ha guardado su rutina con recordatorio. 💾\n",
					parse_mode=telegram.ParseMode.HTML,
					chat_id = query.message.chat_id,
	)
	context.bot.send_message(
					text='<b>Resumem del recordatorio:</b>\n\n' \
					+ '🔷 <b>Nombre: </b>'+  str(context.user_data['nombre_rutina']) + '\n' \
					+ '🔷 <b>Sonará a las: </b>'+ str(context.user_data['hora_recordr']) + '\n' \
					+'🔷 <b>Los días marcados</b>\n➖ ' + lunes + '\n➖ '+ martes+ '\n➖ '+  miercoles+ '\n➖ '+  jueves+ '\n➖ '+  viernes+ '\n➖ '+ sabado+ '\n➖ '+ domingo,
					parse_mode=telegram.ParseMode.HTML,
					chat_id = query.message.chat_id,
					reply_markup=reply_markup
	)


	return EDICIONES_RUTINA


def alarma_rutina(context):
	job = context.job
	teclado_volver_recordatorios = [
				[InlineKeyboardButton("🔙 Volver al menú rutinas", callback_data=str(VOLVER_MENU_RUTINAS))],
				]
	reply_markup = InlineKeyboardMarkup(teclado_volver_rutinas)
	context.bot.send_message(
	job.context[0],
	text="<b> ⏰ Te recuerdo que tienes pendiente la siguiente rutina: ⏰</b> \n ➡️ "+ job.context[1],
	parse_mode=telegram.ParseMode.HTML,
	reply_markup=reply_markup

	)

def visualizar_rutinas(update: Update, context: CallbackContext):
	logger.info("El usuario %s visualiza las rutinas para editar", context.user_data["nombre_usuario"])
	query = update.callback_query
	keyboard = []
	datos = bd_bot.leer_rutinas(str(context.user_data["id_usuario"]))
	#muestra datos de la bd y de callback data te devuelve el id
	if datos:
		for data in datos:
			keyboard.append([InlineKeyboardButton('🔹 ' + str(data[2]),
							callback_data=data[0])])
		reply_markup = InlineKeyboardMarkup(keyboard)
		context.bot.send_message(
			text="<b>📋 Edición de rutinas 📋  </b>\n\n Seleciona una rutina para editar ✏",
			parse_mode=telegram.ParseMode.HTML,
			chat_id = query.message.chat_id,
			reply_markup=reply_markup
		)
		return OBTIENE_ID_RUTINA
	else:
		reply_markup = InlineKeyboardMarkup(teclado_mod_rutinas)
		context.bot.send_message(
			text="<b>⚠ No hay datos para las rutinas, vuelve al menú y crea tus rutinas ⚠</b>",
			parse_mode=telegram.ParseMode.HTML,
			chat_id = query.message.chat_id,
			reply_markup=reply_markup
		)
		return RUTINAS_GESTION


def obtener_id_rutinas(update: Update, context: CallbackContext):
	 logger.info("El usuario %s visualiza los campos de su rutina para editar", context.user_data["nombre_usuario"])
	 query = update.callback_query
	 context.user_data['id_rutina'] = query.data
	 id_rutina =  context.user_data['id_rutina']
	 datos = bd_bot.leerid_rutina(id_rutina)
	 keyboard = []
	 context.user_data['dias_mostrar'] = []
	 dia_semana = date.today().weekday()
	 separator = ''
	 for data in datos:
			 context.user_data['nombre_rutina']  = str(data[2])

	 if datos:
				for data in datos:
					context.user_data['lista'] = str(data[6])
					for n in context.user_data['lista']:
						if n == '0':
							print('hay un 0 lunes')
							context.user_data['dias_mostrar'].append('L')
						if n == '1':
							print('hay un 1 martes')
							context.user_data['dias_mostrar'].append('M')
						if n == '2':
							print('hay un 2 miercoles')
							context.user_data['dias_mostrar'].append('X')
						if n == '3':
							print('hay un 3 jueves')
							context.user_data['dias_mostrar'].append('J')
						if n == '4':
							print('hay un 4 viernes')
							context.user_data['dias_mostrar'].append('V')
						if n == '5':
							print('hay un 5 sabado')
							context.user_data['dias_mostrar'].append('S')
						if n == '6':
							print('hay un 6 domingo')
							context.user_data['dias_mostrar'].append('D')

					# for i in context.user_data['dias_mostrar']:
					# 	context.user_data['dias_mostrar'].remove(i)

					original = str(context.user_data['dias_mostrar'])
					original = original.replace("[", "")
					original = original.replace("]", "")
					context.user_data['dias_mostrar'] = original.replace("'", "")
					print('removed',context.user_data['dias_mostrar'])
				keyboard.append([InlineKeyboardButton(text='✏ Nombre: ' + str(data[2]),   callback_data=str(EDICIONR))])
				keyboard.append([InlineKeyboardButton(text='✏ Categoria: ' + str(data[3]), callback_data=str(EDICION2R))])
				keyboard.append([InlineKeyboardButton(text='✏ Repetición: ' + str(data[4]) + ' días a la semana', callback_data=str(EDICION3R))])
				keyboard.append([InlineKeyboardButton(text='✏ Se repite los días: ' + str(context.user_data['dias_mostrar']), callback_data=str(EDICION5R))])
				keyboard.append([InlineKeyboardButton(text='✏ Duración por día: ' + str(data[5]) + ' horas', callback_data=str(EDICION4R))])

				keyboard.append([InlineKeyboardButton(text="❌ Eliminar rutina", callback_data=str(ELIMINAR_RUTINA)),
								InlineKeyboardButton(text='⏰ Recordatorio ', callback_data=str(RECORDATORIO_RUTINA))])
				for data in datos:
					if(str(dia_semana) in str(data[6])):
						print('dia de la semana',dia_semana)
						print('str eeee',str(data[6]))
						keyboard.append([InlineKeyboardButton(text="✅ Rutina realizada ", callback_data=str(MARCAR_RUTINA))])


				keyboard.append([InlineKeyboardButton(text=' 🔙 Volver al menú rutinas', callback_data=str(VOLVER_MENU_RUTINAS))])
				reply_markup = InlineKeyboardMarkup(keyboard)
				context.bot.send_message(
						text="<b>📋 Editando la rutina: </b> " + str(data[2]) + " 📋\n\nSeleciona un campo para editar o realice otra de las opciones disponibles para su rutina.",
						parse_mode=telegram.ParseMode.HTML,
						chat_id = query.message.chat_id,
						reply_markup=reply_markup
				)

	 return EDICIONES_RUTINA


def marcar_rutina(update: Update, context: CallbackContext):
		logger.info("El usuario %s marca como realizada hoy su rutina", context.user_data["nombre_usuario"])
		query = update.callback_query
		id_rutina =  context.user_data['id_rutina']
		datos = bd_bot.leerid_rutina(id_rutina)
		reply_markup = InlineKeyboardMarkup(teclado_volver_rutinas)
		columna = 'premio_rutina'
		valor = 1
		for data in datos:
			context.user_data['puntos'] = int(data[7]) + valor

		bd_bot.actualizar_campor(columna,context.user_data['puntos'],id_rutina)
		context.bot.send_message(
			text="\n\n<b>Has dedicado tiempo a tu rutina: </b> " + context.user_data['nombre_rutina'] + " ✅",
			chat_id = query.message.chat_id,
			parse_mode=telegram.ParseMode.HTML,
			reply_markup=reply_markup
		)

		return RUTINAS_GESTION

def edita_rutina(update: Update, context: CallbackContext):
	logger.info("El usuario %s escribe el nuevo nombre de su rutina", context.user_data["nombre_usuario"])
	query = update.callback_query
	context.bot.send_message(
			text="¿Cuál es el nuevo nombre de su rutina?",
			chat_id = query.message.chat_id,
		)
	return EDITANOMBRE1R

def editanombrer(update: Update, context: CallbackContext):
	logger.info("El usuario %s actualiza el nombre de su rutina", context.user_data["nombre_usuario"])
	columna = 'nombre_rutina'
	valor = update.message.text
	id_rutina =  context.user_data['id_rutina']
	if (update.message.text.upper() == '/salir'.upper()):
		update.message.reply_text(
			text="¡Hasta pronto!"
		)
		return ConversationHandler.END
	datos = bd_bot.leer_rutinas(str(context.user_data['id_usuario']))
	for data in datos:
		if(str(data[2].upper()) == update.message.text.upper()):
			update.message.reply_text(
			text ='💬 Ya existe una rutina con ese nombre. Vuelve a escribir el nombre de su rutina.',
			parse_mode=telegram.ParseMode.HTML,

			)
			return EDITANOMBRE1R

	bd_bot.actualizar_campor(columna,valor,id_rutina)
	update.message.reply_text(
		text ='💬 Nombre de la rutina modificado con éxito ✍✅'
		)
	reply_markup = InlineKeyboardMarkup(teclado_menu_rutinas)
	update.message.reply_text(
			text="<b>📋 Menú rutinas 📋</b>\n\n<b>Rutinas</b> \n"+ funciones.rutinaspendientes(str(context.user_data["id_usuario"])),
			parse_mode=telegram.ParseMode.HTML,
			reply_markup=reply_markup
	)

	return RUTINAS_GESTION


def edita_rutina2(update: Update, context: CallbackContext):
	logger.info("El usuario %s escribe el nuevo nombre de su categoría", context.user_data["nombre_usuario"])
	query = update.callback_query
	id_usuario =  str(context.user_data['id_usuario'])
	datos = bd_bot.leer_categorias_rutina(id_usuario)
	keyboard = []
	if datos:
		for data in datos:
			keyboard.append([InlineKeyboardButton('🔹 ' + str(data[2]),
								callback_data=data[2])])
		reply_markup = InlineKeyboardMarkup(keyboard)

		context.bot.send_message(
				text="¿Cuál es el nuevo nombre para la categoria?",
				parse_mode=telegram.ParseMode.HTML,
				chat_id = query.message.chat_id,
				reply_markup=reply_markup
			)
		return EDITANOMBRE2R



def editacategoria(update: Update, context: CallbackContext):
	logger.info("El usuario %s actualiza la categoría de su rutina", context.user_data["nombre_usuario"])
	columna = 'categoria_rutina'
	query = update.callback_query
	valor = query.data
	id_rutina =  context.user_data['id_rutina']
	bd_bot.actualizar_campor(columna,valor,id_rutina)
	reply_markup = InlineKeyboardMarkup(teclado_menu_rutinas)
	context.bot.send_message(
		text ='💬 Categoría de la rutina modificada con éxito ✍✅',
		parse_mode=telegram.ParseMode.HTML,
		chat_id = query.message.chat_id,
		)
	context.bot.send_message(
			text="<b>📋 Menú rutinas 📋</b>\n\n<b>Rutinas</b> \n"+ funciones.rutinaspendientes(str(context.user_data["id_usuario"])),
			parse_mode=telegram.ParseMode.HTML,
			chat_id = query.message.chat_id,
			reply_markup=reply_markup
	)
	return RUTINAS_GESTION



def edita_rutina3(update: Update, context: CallbackContext):
	logger.info("El usuario %s escribe la nueva repetición de su rutina", context.user_data["nombre_usuario"])
	query = update.callback_query
	teclado_vecesemana= [
				[InlineKeyboardButton("1 vez por semana",   callback_data='1')],
				[InlineKeyboardButton("2 veces por semana", callback_data='2')],
				[InlineKeyboardButton("3 veces por semana", callback_data='3')],
				[InlineKeyboardButton("4 veces por semana", callback_data='4')],
				[InlineKeyboardButton("5 veces por semana", callback_data='5')],
				[InlineKeyboardButton("6 veces por semana", callback_data='6')],
				[InlineKeyboardButton("7 veces por semana", callback_data='7')],
				]
	reply_markup = InlineKeyboardMarkup(teclado_vecesemana)
	context.bot.send_message(
			text="¿Cuantos días dedicarás a la semana en tu rutina?",
			chat_id = query.message.chat_id,
			reply_markup=reply_markup
		)

	return EDITANOMBRE3R

def editadescripcionr(update: Update, context: CallbackContext):
	logger.info("El usuario %s actualiza la repetición de su rutina", context.user_data["nombre_usuario"])
	query = update.callback_query
	valor = query.data
	columna = 'repeticion_rutina'
	id_usuario = str(context.user_data["id_usuario"])
	id_rutina =  context.user_data['id_rutina']
	bd_bot.actualizar_campor(columna,valor,id_rutina)
	reply_markup = InlineKeyboardMarkup(teclado_menu_rutinas)
	context.bot.send_message(
		text="💬 Repetición de la rutina modificada con éxito ✍✅. \n Recuerde que también debe editar los días elegidos para su rutina.",
		parse_mode=telegram.ParseMode.HTML,
		chat_id = query.message.chat_id)
	context.bot.send_message(
		text="<b>📋 Menú rutinas 📋</b>\n\n<b>Rutinas</b> \n"+ funciones.rutinaspendientes(id_usuario),
		parse_mode=telegram.ParseMode.HTML,
		chat_id = query.message.chat_id,
		reply_markup=reply_markup
	)
	return RUTINAS_GESTION


def edita_rutina4(update: Update, context: CallbackContext):
	logger.info("El usuario %s escribe la nueva duración de su rutina", context.user_data["nombre_usuario"])
	query = update.callback_query
	context.bot.send_message(
			text="¿Cuántas horas por día dedicarás en tu rutina?",
			chat_id = query.message.chat_id,
		)

	return EDITANOMBRE4R

def editaduracionr(update: Update, context: CallbackContext):
	logger.info("El usuario %s actualiza la repetición de su rutina", context.user_data["nombre_usuario"])
	columna = 'duracion_rutina'
	valor = update.message.text
	id_rutina =  context.user_data['id_rutina']
	bd_bot.actualizar_campor(columna,valor,id_rutina)
	reply_markup = InlineKeyboardMarkup(teclado_menu_rutinas)
	if (update.message.text.upper() == '/salir'.upper()):
		update.message.reply_text(
			text="¡Hasta pronto!"
		)
		return ConversationHandler.END
	print('valor',str(valor))
	entero = funciones.valida_entero(str(valor))
	flotant = funciones.valida_float(str(valor))
	print(entero)
	print(flotant)
	if not entero and not flotant:
		update.message.reply_text(
		text="Error al escribir el número de horas ❌, solo se admiten números positivos. Vuelva a escribir el número de horas.\n",
		parse_mode=telegram.ParseMode.HTML,
		)
		return EDITANOMBRE4R
	else:
		update.message.reply_text(
			text="💬 Duración de la rutina modificada con éxito ✍✅",
			parse_mode=telegram.ParseMode.HTML,
			)
		update.message.reply_text(
				text="<b>📋 Menú rutinas 📋</b>\n\n<b>Rutinas</b> \n"+ funciones.rutinaspendientes(str(context.user_data["id_usuario"])),
				parse_mode=telegram.ParseMode.HTML,
				reply_markup=reply_markup
		)
		return RUTINAS_GESTION

def edita_rutina5(update: Update, context: CallbackContext):
	logger.info("El usuario %s edita los dias en los que se repite su rutina", context.user_data["nombre_usuario"])
	query = update.callback_query
	id_rutina = context.user_data['id_rutina']
	datos= bd_bot.leerid_rutina(id_rutina)
	for data in datos:
		 print('repeticion',str(data[4]))

	context.user_data['repeticion_rutina'] = str(data[4])
	context.user_data['lunes'] = 7
	context.user_data['martes'] = 7
	context.user_data['miercoles'] = 7
	context.user_data['jueves'] = 7
	context.user_data['viernes'] = 7
	context.user_data['sabado'] = 7
	context.user_data['domingo'] = 7
	teclado_diassemana= [
						[InlineKeyboardButton("Lunes", callback_data='0')],
						[InlineKeyboardButton("Martes", callback_data='1')],
						[InlineKeyboardButton("Miercoles", callback_data='2')],
						[InlineKeyboardButton("Jueves", callback_data='3')],
						[InlineKeyboardButton("Viernes", callback_data='4')],
						[InlineKeyboardButton("Sabado", callback_data='5')],
						[InlineKeyboardButton("Domingo", callback_data='6')],
						]

	reply_markup = InlineKeyboardMarkup(teclado_diassemana)
	context.bot.send_message(
				text ='¿Qué días de la semana quieres que se repita?',
				parse_mode=telegram.ParseMode.HTML,
				chat_id = query.message.chat_id,
				reply_markup=reply_markup
	)

	return EDITANOMBRE5R


def edita_diasemana(update: Update, context: CallbackContext):
	logger.info("El usuario %s edita guarda los dias elegidos para su rutina", context.user_data["nombre_usuario"])
	query = update.callback_query
	veces = int(context.user_data['repeticion_rutina'])
	context.user_data['repeticion_rutina'] =  int(context.user_data['repeticion_rutina'])-1
	int(context.user_data['repeticion_rutina'])
	# print('veces -- ',int(context.user_data['repeticion_rutina']))

	if int(context.user_data['repeticion_rutina']) == 0:
		if int(query.data) == 0:
			context.user_data['lunes'] = 0
		elif int(query.data) == 1:
			context.user_data['martes'] = 1
		elif int(query.data) == 2:
				context.user_data['miercoles'] = 2
		elif int(query.data) == 3:
			context.user_data['jueves'] = 3
		elif int(query.data) == 4:
			context.user_data['viernes'] = 4
		elif int(query.data) == 5:
			context.user_data['sabado'] = 5
		elif int(query.data) == 6:
			context.user_data['domingo'] = 6

		teclado_diassemana= [
							[InlineKeyboardButton("🔙 Cancelar", callback_data=str(VOLVER_MENU_RUTINAS))],
							[InlineKeyboardButton("💾 Guardar", callback_data=str(GUARDA_DIAS))],
							]

		reply_markup = InlineKeyboardMarkup(teclado_diassemana)
		context.bot.send_message(
				text="¿Quiere guardar los días elegidos?\n",
				parse_mode=telegram.ParseMode.HTML,
				chat_id = query.message.chat_id,
				reply_markup=reply_markup

			)

		return EDICIONES_RUTINA
	else:

		if int(query.data) == 0:
			context.user_data['lunes'] = 0
			teclado_diassemana= [
								[InlineKeyboardButton("Lunes ✅", callback_data='0')],
								[InlineKeyboardButton("Martes", callback_data='1')],
								[InlineKeyboardButton("Miercoles", callback_data='2')],
								[InlineKeyboardButton("Jueves", callback_data='3')],
								[InlineKeyboardButton("Viernes", callback_data='4')],
								[InlineKeyboardButton("Sabado", callback_data='5')],
								[InlineKeyboardButton("Domingo", callback_data='6')],
								]

			reply_markup = InlineKeyboardMarkup(teclado_diassemana)
			context.bot.send_message(
						text ='¿Qué días de la semana quieres que se repita?',
						parse_mode=telegram.ParseMode.HTML,
						chat_id = query.message.chat_id,
						reply_markup=reply_markup
			)
			return EDITANOMBRE5R
		elif int(query.data) == 1:
			context.user_data['martes'] = 1
			teclado_diassemana= [
								[InlineKeyboardButton("Lunes ", callback_data='0')],
								[InlineKeyboardButton("Martes ✅", callback_data='1')],
								[InlineKeyboardButton("Miercoles", callback_data='2')],
								[InlineKeyboardButton("Jueves", callback_data='3')],
								[InlineKeyboardButton("Viernes", callback_data='4')],
								[InlineKeyboardButton("Sabado", callback_data='5')],
								[InlineKeyboardButton("Domingo", callback_data='6')],
								]

			reply_markup = InlineKeyboardMarkup(teclado_diassemana)
			context.bot.send_message(
						text ='¿Qué días de la semana quieres que se repita?',
						parse_mode=telegram.ParseMode.HTML,
						chat_id = query.message.chat_id,
						reply_markup=reply_markup
			)
			return EDITANOMBRE5R
		elif int(query.data) == 2:
				context.user_data['miercoles'] = 2
				teclado_diassemana= [
									[InlineKeyboardButton("Lunes ", callback_data='0')],
									[InlineKeyboardButton("Martes", callback_data='1')],
									[InlineKeyboardButton("Miercoles ✅", callback_data='2')],
									[InlineKeyboardButton("Jueves", callback_data='3')],
									[InlineKeyboardButton("Viernes", callback_data='4')],
									[InlineKeyboardButton("Sabado", callback_data='5')],
									[InlineKeyboardButton("Domingo", callback_data='6')],
									]

				reply_markup = InlineKeyboardMarkup(teclado_diassemana)
				context.bot.send_message(
							text ='¿Qué días de la semana quieres que se repita?',
							parse_mode=telegram.ParseMode.HTML,
							chat_id = query.message.chat_id,
							reply_markup=reply_markup
				)
				return EDITANOMBRE5R
		elif int(query.data) == 3:
			context.user_data['jueves'] = 3
			teclado_diassemana= [
									[InlineKeyboardButton("Lunes ", callback_data='0')],
									[InlineKeyboardButton("Martes", callback_data='1')],
									[InlineKeyboardButton("Miercoles", callback_data='2')],
									[InlineKeyboardButton("Jueves ✅", callback_data='3')],
									[InlineKeyboardButton("Viernes", callback_data='4')],
									[InlineKeyboardButton("Sabado", callback_data='5')],
									[InlineKeyboardButton("Domingo", callback_data='6')],
									]

			reply_markup = InlineKeyboardMarkup(teclado_diassemana)
			context.bot.send_message(
							text ='¿Qué días de la semana quieres que se repita?',
							parse_mode=telegram.ParseMode.HTML,
							chat_id = query.message.chat_id,
							reply_markup=reply_markup
			)
			return EDITANOMBRE5R
		elif int(query.data) == 4:
			context.user_data['viernes'] = 4
			teclado_diassemana= [
									[InlineKeyboardButton("Lunes ", callback_data='0')],
									[InlineKeyboardButton("Martes", callback_data='1')],
									[InlineKeyboardButton("Miercoles", callback_data='2')],
									[InlineKeyboardButton("Jueves", callback_data='3')],
									[InlineKeyboardButton("Viernes ✅", callback_data='4')],
									[InlineKeyboardButton("Sabado", callback_data='5')],
									[InlineKeyboardButton("Domingo", callback_data='6')],
									]

			reply_markup = InlineKeyboardMarkup(teclado_diassemana)
			context.bot.send_message(
							text ='¿Qué días de la semana quieres que se repita?',
							parse_mode=telegram.ParseMode.HTML,
							chat_id = query.message.chat_id,
							reply_markup=reply_markup
				)
			return EDITANOMBRE5R
		elif int(query.data) == 5:
			context.user_data['sabado'] = 5
			teclado_diassemana= [
									[InlineKeyboardButton("Lunes ", callback_data='0')],
									[InlineKeyboardButton("Martes", callback_data='1')],
									[InlineKeyboardButton("Miercoles", callback_data='2')],
									[InlineKeyboardButton("Jueves", callback_data='3')],
									[InlineKeyboardButton("Viernes", callback_data='4')],
									[InlineKeyboardButton("Sabado ✅", callback_data='5')],
									[InlineKeyboardButton("Domingo", callback_data='6')],
									]

			reply_markup = InlineKeyboardMarkup(teclado_diassemana)
			context.bot.send_message(
							text ='¿Qué días de la semana quieres que se repita?',
							parse_mode=telegram.ParseMode.HTML,
							chat_id = query.message.chat_id,
							reply_markup=reply_markup
				)
			return EDITANOMBRE5R
		elif int(query.data) == 6:
			context.user_data['domingo'] = 6
			teclado_diassemana= [
									[InlineKeyboardButton("Lunes ", callback_data='0')],
									[InlineKeyboardButton("Martes", callback_data='1')],
									[InlineKeyboardButton("Miercoles", callback_data='2')],
									[InlineKeyboardButton("Jueves", callback_data='3')],
									[InlineKeyboardButton("Viernes", callback_data='4')],
									[InlineKeyboardButton("Sabado", callback_data='5')],
									[InlineKeyboardButton("Domingo ✅", callback_data='6')],
									]

			reply_markup = InlineKeyboardMarkup(teclado_diassemana)
			context.bot.send_message(
							text ='¿Qué días de la semana quieres que se repita?',
							parse_mode=telegram.ParseMode.HTML,
							chat_id = query.message.chat_id,
							reply_markup=reply_markup
				)


			return EDITANOMBRE5R

def guarda_dias (update: Update, context: CallbackContext):
	logger.info("El usuario %s guarda su los dias de su rutina", context.user_data["nombre_usuario"])
	query = update.callback_query

	lunes = 'Lunes'
	martes = 'Martes'
	miercoles = 'Miercoles'
	jueves = 'Jueves'
	viernes = 'Viernes'
	sabado = 'Sabado'
	domingo = 'Domingo'
	context.user_data['dias'] = []

	if int(context.user_data['lunes']) == 0:
		lunes = 'Lunes ✅'
		context.user_data['dias'].append(0)
		# print('diasssssssssssss', str(context.user_data['dias']))
	if int(context.user_data['martes']) == 1:
		martes = 'Martes ✅'
		context.user_data['dias'].append(1)
		# print('diasssssssssssss', str(context.user_data['dias']))
	if int(context.user_data['miercoles']) == 2:
		miercoles = 'Miercoles ✅'
		context.user_data['dias'].append(2)
	if int(context.user_data['jueves'] ) == 3:
		jueves = 'Jueves ✅'
		context.user_data['dias'].append(3)
	if int(context.user_data['viernes']) == 4:
		viernes = 'Viernes ✅ '
		context.user_data['dias'].append(4)
	if int(context.user_data['sabado']) == 5:
		sabado = 'Sabado ✅'
		context.user_data['dias'].append(5)
	if int(context.user_data['domingo']) == 6:
		domingo = 'Domingo ✅'
		context.user_data['dias'].append(6)


	id_rutina = context.user_data['id_rutina']
	valor = str(context.user_data['dias'])
	columna = 'dias_rutina'
	separator = ''
	context.user_data['dias'] = separator.join(valor) # transformo la lista a str para insertar en bd
	bd_bot.actualizar_campor(columna,str(context.user_data['dias']),id_rutina)


	teclado_volver= [
							[InlineKeyboardButton("Volver a menú rutinas", callback_data=str(VOLVER_MENU_RUTINAS))],
						]

	reply_markup = InlineKeyboardMarkup(teclado_menu_rutinas)
	context.bot.send_message(
					text="<b>💬 Se han guardado los datos de su rutina. 💾'</b>\n",
					parse_mode=telegram.ParseMode.HTML,
					chat_id = query.message.chat_id,
	)
	context.bot.send_message(
					text ='<b>Resumen:</b>\n Rutina establecida para los dias marcados:\n'+ \
					lunes + '\n'+ martes+ '\n'+  miercoles+ '\n'+  jueves+ '\n'+  viernes+ '\n'+ sabado+ '\n'+ domingo,
					parse_mode=telegram.ParseMode.HTML,
					chat_id = query.message.chat_id,

	)
	context.bot.send_message(
					text="<b>📋 Menú rutinas 📋</b>\n\n<b>Rutinas</b> \n"+ funciones.rutinaspendientes(str(context.user_data["id_usuario"])),
					parse_mode=telegram.ParseMode.HTML,
					chat_id = query.message.chat_id,
					reply_markup=reply_markup

	)



	return RUTINAS_GESTION


# Funciones para eliminar rutinas

def eliminar_rutina (update: Update, context: CallbackContext):
	logger.info("El usuario %s ha eliminado la rutina", context.user_data["nombre_usuario"])
	query = update.callback_query
	id_rutina = context.user_data['id_rutina']
	id_usuario = str(context.user_data["id_usuario"])
	bd_bot.eliminar_rutina('bd_bot.db','rutinas', 'id_rutina', id_rutina)
	reply_markup = InlineKeyboardMarkup(teclado_menu_rutinas)
	context.bot.send_message(
			text="💬 Rutina eliminada con éxito ✅\n",
			parse_mode=telegram.ParseMode.HTML,
			chat_id = query.message.chat_id,
	)
	context.bot.send_message(
			text="<b>Rutinas</b>\n" + funciones.rutinaspendientes(id_usuario),
			parse_mode=telegram.ParseMode.HTML,
			chat_id = query.message.chat_id,
			reply_markup=reply_markup
	)

	return RUTINAS_GESTION


################################### FUNCIONES DE LOGROS ####################################


# PREMIOS
teclado_volver_logros = [
		 [InlineKeyboardButton(text=' 🔙 Volver al menú logros', callback_data=str(VOLVER))],
	]


def premios(update: Update, context: CallbackContext):
	logger.info("El usuario %s entra en los premios obtenidos de tareas", context.user_data["nombre_usuario"])
	query = update.callback_query
	premio = funciones.premios_tarea(str(context.user_data['id_usuario']))
	reply_markup = InlineKeyboardMarkup(teclado_volver_logros)

	context.bot.send_message(
				text="<b>Premios obtenidos de tareas </b>\n" + premio,
				parse_mode=telegram.ParseMode.HTML,
				chat_id = query.message.chat_id,
				reply_markup=reply_markup
	)

	return GESTION_LOGROS



def menu_logros(update: Update, context: CallbackContext):
	logger.info("El usuario %s entra en el menú de logros", context.user_data["nombre_usuario"])
	query = update.callback_query
	id = str(context.user_data["id_usuario"])
	tareas_completadas = bd_bot.contar_tareas_completas(id)
	tarea_c = tareas_completadas[0]



	if tarea_c:
		keyboard = [

			[InlineKeyboardButton(text='📊 Gráficas de productividad',  callback_data=str(GRAFICAS))],
			[InlineKeyboardButton(text=' 🔙 Volver menu principal', callback_data=str(VOLVER_MENU_PRINCIPAL))],
		]
	else:
			keyboard = [

				[InlineKeyboardButton(text=' 🔙 Volver menu principal', callback_data=str(VOLVER_MENU_PRINCIPAL))],
			]
	reply_markup = InlineKeyboardMarkup(keyboard)
	id_usuario = str(context.user_data["id_usuario"])
	premio_r  = funciones.premios_rutina(id_usuario)
	premio_t = funciones.premios_tarea(id_usuario)
	tareas_c = funciones.tareascompletadas(id_usuario)

	context.bot.send_message(
			text="<b> 🎖 Logros y premios 🎖 </b>\n\n Puedes visualizar los premios obtenidos para rutinas y tareas, visualizar tus tareas completadas y consultar las gráficas de productividad asociadas a tus tareas.",
			chat_id = query.message.chat_id,
			parse_mode=telegram.ParseMode.HTML,

	)
	context.bot.send_message(
			text= "<b>➡️ Premios de rutinas 🎁 📋 </b>\n" + premio_r + "\n\n" \
			"<b>➡️ Premios de tareas  🎁 📝</b>\n" + premio_t  \
			+ "\n\n<b>➡️ Tareas completadas</b> 📝 ✅ \n" + tareas_c ,
			chat_id = query.message.chat_id,
			parse_mode=telegram.ParseMode.HTML,
			reply_markup=reply_markup
	)


	return GESTION_LOGROS


teclado_graficas = [
	[InlineKeyboardButton(text='Visualizar gráficas de tareas',  callback_data=str(GRAFICAMES))],
	# [InlineKeyboardButton(text='Por año', callback_data=str(ENCONSTRUCCION))],
	[InlineKeyboardButton(text='🔙 Volver al menú logros', callback_data=str(VOLVER))],

]

teclado_volver_graficas= [
	# [InlineKeyboardButton(text='Por mes',  callback_data=str(GRAFICAMES))],
	# [InlineKeyboardButton(text='Por año', callback_data=str(ENCONSTRUCCION))],
	[InlineKeyboardButton(text='🔙 Volver al menú logros', callback_data=str(VOLVER))],

]

def graficas(update: Update, context: CallbackContext):
	logger.info("El usuario %s está en graficas", context.user_data["nombre_usuario"])
	query = update.callback_query

	reply_markup = InlineKeyboardMarkup(teclado_graficas)
	context.bot.send_message(
		text="<b> 📊 Gráficas de productividad 📊 </b>\n",
		chat_id = query.message.chat_id,
		parse_mode=telegram.ParseMode.HTML,
		reply_markup=reply_markup

	)

def generargrafica1(update: Update, context: CallbackContext):

		query = update.callback_query
		id = str(context.user_data["id_usuario"])
		tareas_completadas = bd_bot.contar_tareas_completas(id)
		tareas_pendientes = bd_bot.contar_tareas_pendientes(id)
		tareas = bd_bot.contar_tareas(id)
		# print('completadas',tareas_completadas[0])
		# print('pendientes',tareas_pendientes[0])
		tarea_c = tareas_completadas[0]
		tarea_p = tareas_pendientes[0]
		now = datetime.now()
		mes = now.month
		v1 = tareas_completadas[0]
		v2 = tareas_pendientes[0]

		if(tareas):
			# grafica
			tareas = ('Completadas','Pendientes')
			valores = (v1,v2)
			colores = ('green','red')
			v = (0.1,0)
			_, _, texto = pyplot.pie(valores,colors=colores, labels=tareas, autopct='%1.1f%%',
			explode=v)
			for tex in texto:
				tex.set_color('white')
			#visualizar grafica
			pyplot.axis('equal')
			pyplot.title('Progreso de tareas')
			now = datetime.now()
			dt_string = now.strftime(id+"-%d-%m-%Y-%H:%M:%S.png")
			context.user_data["nombre_grafica1"] = dt_string
			pyplot.savefig('graficas/'+ dt_string)
			pyplot.close()

			if not tarea_c: # y no hay ninguna completada
				context.bot.send_message(
					text="<b> Por ahora no has completado ninguna tarea. Realiza tus tareas y obtendrás mejores estadísticas.</b>",
					chat_id = query.message.chat_id,
					parse_mode=telegram.ParseMode.HTML,

				)

			if tarea_c and not tarea_p: # si hay tareas completadas y ninguna pendiente
				context.bot.send_message(
					text="<b> Bien por ahora has completado todas tus tareas y no tienes ninguna pendiente.</b>",
					chat_id = query.message.chat_id,
					parse_mode=telegram.ParseMode.HTML,

				)


		else:
			reply_markup = InlineKeyboardMarkup(teclado_graficas)
			context.bot.send_message(
				text="<b> No hay resultados para tu gráfica, crea tareas ‼</b>",
				chat_id = query.message.chat_id,
				parse_mode=telegram.ParseMode.HTML,
				reply_markup=reply_markup

			)

def generargrafica2(update: Update, context: CallbackContext):

		query = update.callback_query
		id = str(context.user_data["id_usuario"])
		tareas = bd_bot.contar_tareas(id)
		now = datetime.now()
		mes = now.month
		tareas_completadas = bd_bot.contar_tareas_completas(id)
		tareas_pendientes = bd_bot.contar_tareas_pendientes(id)
		tareas = bd_bot.contar_tareas(id)
		v1 = tareas_completadas[0]
		v2 = tareas_pendientes[0]

		if tareas:

			dt_stringb = now.strftime(id+"-%d-%m-%Y-%H:%M:%S-b.png")
			context.user_data["nombre_grafica2"] = dt_stringb
			names = ['Alta', 'Media', 'Baja']
			prioridad1= bd_bot.contar_tareas_prioridad1(id)
			# print('prioridad1',prioridad1[0])
			prioridad2= bd_bot.contar_tareas_prioridad2(id)
			# print('prioridad2',prioridad2[0])
			prioridad3= bd_bot.contar_tareas_prioridad3(id)
			# print('prioridad3',prioridad3[0])
			values = [prioridad1[0], prioridad2[0],prioridad3[0]]

			# pyplot.subplot(131)
			pyplot.figure(figsize=(10,9))
			colores2 = ('red','orange','green')
			pyplot.bar(names, values, color=colores2)
			pyplot.title('Tareas completadas por prioridad')
			pyplot.savefig('graficas/'+dt_stringb)
			pyplot.close()

			context.bot.send_message(
				text="<b> 📊 Gráficas de tareas 📊 </b>",
				chat_id = query.message.chat_id,
				parse_mode=telegram.ParseMode.HTML,

			)
			if not v1:
				context.bot.send_message(
					text="<b> No has completado ninguna tarea </b>",
					chat_id = query.message.chat_id,
					parse_mode=telegram.ParseMode.HTML,

				)


		else:
			reply_markup = InlineKeyboardMarkup(teclado_graficas)
			context.bot.send_message(
				text="<b> No hay resultados para tu gráfica, crea tareas ‼</b>",
				chat_id = query.message.chat_id,
				parse_mode=telegram.ParseMode.HTML,
				reply_markup=reply_markup

			)

def graficames(update: Update, context: CallbackContext):
	logger.info("El usuario %s está visualizando la grafica mes", context.user_data["nombre_usuario"])
	query = update.callback_query

	generargrafica1(update,context)
	generargrafica2(update,context)
	grafica1 = 'graficas/'+context.user_data["nombre_grafica1"]
	grafica2 = 'graficas/'+context.user_data["nombre_grafica2"]
	reply_markup = InlineKeyboardMarkup(teclado_volver_graficas)

	context.bot.send_photo(
		text="<b> 📊 Gráficas de tareas pendientes y completadas 📊 </b>\n",
		chat_id = query.message.chat_id,
		photo=open(grafica1, 'rb'),
	)
	context.bot.send_photo(
		text="<b> 📊 Gráfica según prioridad de tareas realizadas 📊 </b>\n",
		chat_id = query.message.chat_id,
		photo=open(grafica2, 'rb'),
		reply_markup=reply_markup
	)
	funciones.borrar_graficas()
	return GESTION_LOGROS



################################### FUNCIONES DE BUSCADOR ####################################

teclado_buscador= [
			[InlineKeyboardButton("🔷 Búsqueda de rutinas ",  callback_data=str(BUSQUEDA_RUTINA))],
			[InlineKeyboardButton("🔷 Búsqueda de tareas ",  callback_data=str(BUSQUEDA_TAREA))],
			[InlineKeyboardButton(text='🔙 Volver menú principal', callback_data=str(VOLVER_MENU_PRINCIPAL))]
		]

teclado_buscador_t= [
			[InlineKeyboardButton("🔷 Búsqueda de tareas ",  callback_data=str(BUSQUEDA_TAREA))],
			[InlineKeyboardButton(text='🔙 Volver menú principal', callback_data=str(VOLVER_MENU_PRINCIPAL))]
		]

teclado_buscador_r= [
			[InlineKeyboardButton("🔷 Búsqueda de rutinas ",  callback_data=str(BUSQUEDA_RUTINA))],
			[InlineKeyboardButton(text='🔙 Volver menú principal', callback_data=str(VOLVER_MENU_PRINCIPAL))]
		]

teclado_buscador_tarea = [
		[InlineKeyboardButton("🔷 Por nombre",  callback_data=str(BUSQUEDA_NOMBRE))],
		[InlineKeyboardButton("🔷 Fecha de vencimiento", callback_data=str(BUSQUEDA_FECHA))],
		[InlineKeyboardButton(text='🔙 Volver menú principal', callback_data=str(VOLVER_MENU_PRINCIPAL))]

	]

teclado_buscador_rutina= [
		[InlineKeyboardButton("🔷 Por nombre",  callback_data=str(BUSQUEDA_NOMBRE_R))],
		[InlineKeyboardButton("🔷 Categoria",  callback_data=str(BUSQUEDA_CATEGORIA))],
		[InlineKeyboardButton(text='🔙 Volver menú principal', callback_data=str(VOLVER_MENU_PRINCIPAL))]

	]
teclado_volver_menu_inicial = [
		[InlineKeyboardButton(text='🔙 Volver menú principal', callback_data=str(VOLVER_MENU_PRINCIPAL))]

	]

teclado_volver_buscador = [
						[InlineKeyboardButton(text='🔙 Volver menú buscador', callback_data=str(VOLVER_MENU_BUSCADOR))]

		]


def menu_buscador(update: Update, context: CallbackContext):
	logger.info("El usuario %s ha entrado en el menú buscador", context.user_data["nombre_usuario"])
	query = update.callback_query
	id_usuario = context.user_data["id_usuario"]
	datos_tarea = bd_bot.leer_tareas_todas(str(id_usuario))
	datos_rutina= bd_bot.leer_rutinas(str(id_usuario))
	reply_markup = InlineKeyboardMarkup(teclado_buscador)
	reply_markup2 = InlineKeyboardMarkup(teclado_buscador_t)
	reply_markup3= InlineKeyboardMarkup(teclado_buscador_r)
	reply_markup4 = InlineKeyboardMarkup(teclado_volver_menu_inicial)
	if datos_tarea and not datos_rutina:
			context.bot.send_message(
				text="<b> 🔎 Buscador 🔎 </b>\n\n",
				chat_id = query.message.chat_id,
				parse_mode=telegram.ParseMode.HTML,
			)
			context.bot.send_message(
				text="➡ Busqueda por:\n",
				chat_id = query.message.chat_id,
				parse_mode=telegram.ParseMode.HTML,
				reply_markup=reply_markup2
			)
	elif(datos_rutina and not datos_tarea):
			context.bot.send_message(
				text="<b> 🔎 Buscador 🔎 </b>\n\n",
				chat_id = query.message.chat_id,
				parse_mode=telegram.ParseMode.HTML,
			)
			context.bot.send_message(
				text="➡ Busqueda por:\n",
				chat_id = query.message.chat_id,
				parse_mode=telegram.ParseMode.HTML,
				reply_markup=reply_markup3
			)
	elif(datos_rutina and datos_tarea):
				context.bot.send_message(
					text="<b> 🔎 Buscador 🔎 </b>\n\n",
					chat_id = query.message.chat_id,
					parse_mode=telegram.ParseMode.HTML,
				)
				context.bot.send_message(
					text="➡ Busqueda por:\n",
					chat_id = query.message.chat_id,
					parse_mode=telegram.ParseMode.HTML,
					reply_markup=reply_markup
				)

	else:
			context.bot.send_message(
				text="<b>⚠ No puede realizar búsquedas.⚠ Primero cree rutinas o tareas. </b>\n" ,
				chat_id = query.message.chat_id,
				parse_mode=telegram.ParseMode.HTML,
				reply_markup=reply_markup4
			)


	return GESTION_BUSCADOR


def menu_buscador_rutina(update: Update, context: CallbackContext):
	logger.info("El usuario %s ha entrado en el menú buscador de rutinas", context.user_data["nombre_usuario"])
	query = update.callback_query
	id_usuario = context.user_data["id_usuario"]
	datos = bd_bot.leer_rutinas(str(id_usuario))
	reply_markup = InlineKeyboardMarkup(teclado_buscador_rutina)
	reply_markup2 = InlineKeyboardMarkup(teclado_volver_menu_inicial)

	if datos:

			context.bot.send_message(
				text="<b> 🔎 Buscador 🔎 </b>\n\n Elige el filtro por el que quieras buscar.\n",
				chat_id = query.message.chat_id,
				parse_mode=telegram.ParseMode.HTML,
			)
			context.bot.send_message(
				text="➡ Busqueda por:\n",
				chat_id = query.message.chat_id,
				parse_mode=telegram.ParseMode.HTML,
				reply_markup=reply_markup
			)
	else:
			context.bot.send_message(
				text="<b>⚠ No hay rutinas, vuelva al menú de tareas y cree una. ⚠</b>\n" ,
				chat_id = query.message.chat_id,
				parse_mode=telegram.ParseMode.HTML,
				reply_markup=reply_markup2
			)


	return GESTION_BUSCADOR

def menu_buscador_tarea(update: Update, context: CallbackContext):
	logger.info("El usuario %s ha entrado en el menú buscador de tareas", context.user_data["nombre_usuario"])
	query = update.callback_query
	id_usuario = context.user_data["id_usuario"]
	datos = bd_bot.leer_tareas_todas(str(id_usuario))
	reply_markup = InlineKeyboardMarkup(teclado_buscador_tarea)
	reply_markup2 = InlineKeyboardMarkup(teclado_volver_menu_inicial)

	if datos:
			context.bot.send_message(
				text="<b> 🔎 Buscador 🔎 </b>\n\n Elige el filtro por el que quieras buscar.\n",
				chat_id = query.message.chat_id,
				parse_mode=telegram.ParseMode.HTML,
			)
			context.bot.send_message(
				text="➡ Busqueda por:\n",
				chat_id = query.message.chat_id,
				parse_mode=telegram.ParseMode.HTML,
				reply_markup=reply_markup
			)
	else:
			context.bot.send_message(
				text="<b>⚠ No hay tareas, vuelva al menú de tareas y cree una. ⚠</b>\n" ,
				chat_id = query.message.chat_id,
				parse_mode=telegram.ParseMode.HTML,
				reply_markup=reply_markup2
			)

	return GESTION_BUSCADOR



def busqueda_nombre(update: Update, context: CallbackContext):
	logger.info("El usuario %s introduce busqueda por nombre de tareas", context.user_data["nombre_usuario"])
	query = update.callback_query
	context.bot.send_message(
		text="<b> 🔎 Búsqueda de tareas por nombre 🔎 </b>\n\n Escribe el nombre de la tarea que quieras buscar .\n",
		chat_id = query.message.chat_id,
		parse_mode=telegram.ParseMode.HTML,
	)

	return RESULTADO_BNOMBRE

def resultado_bnombre(update: Update, context: CallbackContext):
	logger.info("El usuario %s obtiene resultado de su busqueda por nombre de tareas", context.user_data["nombre_usuario"])
	valor = update.message.text
	id_usuario = context.user_data["id_usuario"]
	if (update.message.text.upper() == '/salir'.upper()):
			update.message.reply_text(
				text="¡Hasta pronto!"
			)
			return ConversationHandler.END
	datos = bd_bot.leer_tareas_todas(str(id_usuario))
	reply_markup = InlineKeyboardMarkup(teclado_volver_buscador)
	context.user_data["encontrado"] = False
	if datos:
		update.message.reply_text(
			text="<b>Resultado de la búsqueda de su tarea por nombre:</b> \n\n",
			parse_mode=telegram.ParseMode.HTML,
		)
		for data in datos:
			if str(data[2].upper()) == str(valor.upper()):
				context.user_data["encontrado"] = True
				if(str(data[6]) == 'NO'):
					context.user_data["realizada"] = '❌'
				elif(str(data[6]) == 'SI'):
					context.user_data["realizada"] = '✅'
				context.user_data["comentario"] = str(data[5])
				if(str(data[5]) == 'None'):
					context.user_data["comentario"] = '❌'
				if(str(data[3]) == '1'):
					context.user_data["prioridad"] = '🛑 Alta'
				elif(str(data[3]) == '2'):
					context.user_data["prioridad"] = '✴️ Media'
				elif(str(data[3]) == '3'):
					context.user_data["prioridad"] = '❇️ Baja'

				update.message.reply_text(
					text='🔷 <b>Nombre:</b> '+ str(data[2]) + '\n' \
					+ '🔷 <b>Prioridad: </b>'+ context.user_data["prioridad"] + '\n' \
					+ '🔷 <b>Fecha de vencimiento: </b>' + str(data[4]) + '\n' \
					+ '🔷 <b>Comentario: </b>' + str(context.user_data["comentario"]) + '\n' \
					+ '🔷 <b>¿Tarea realizada? </b>' + context.user_data["realizada"],
					parse_mode=telegram.ParseMode.HTML,
					reply_markup=reply_markup
				)

		if context.user_data["encontrado"] == False:
					update.message.reply_text(
						text="No existe ninguna tarea con ese nombre. 💬\n",
						parse_mode=telegram.ParseMode.HTML,
						reply_markup=reply_markup
					)


	return GESTION_BUSCADOR


def busqueda_nombre_r(update: Update, context: CallbackContext):
	logger.info("El usuario %s introduce busqueda de rutina por nombre", context.user_data["nombre_usuario"])
	query = update.callback_query
	context.bot.send_message(
		text="<b> 🔎 Búsqueda de rutinas por nombre 🔎 </b>\n\n Escribe el nombre de la rutina que quieras buscar.\n",
		chat_id = query.message.chat_id,
		parse_mode=telegram.ParseMode.HTML,
	)

	return RESULTADO_BNOMBRE_R

def resultado_bnombre_r(update: Update, context: CallbackContext):
	logger.info("El usuario %s obtiene resultado de su busqueda por nombre de rutina", context.user_data["nombre_usuario"])
	valor = update.message.text
	id_usuario = context.user_data["id_usuario"]
	if (update.message.text.upper() == '/salir'.upper()):
			update.message.reply_text(
				text="¡Hasta pronto!"
			)
			return ConversationHandler.END
	datos = bd_bot.leer_rutinas(str(id_usuario))
	reply_markup = InlineKeyboardMarkup(teclado_volver_buscador)
	context.user_data["encontrado"] = False
	context.user_data['dias_mostrar'] = []
	context.user_data['lista'] = []
	update.message.reply_text(
		text=" 💬 Resultado de la búsqueda de su rutina.\n\n",
		parse_mode=telegram.ParseMode.HTML,
	)

	if datos:
		for data in datos:
			if str(data[2].upper()) == str(valor.upper()):
				context.user_data["encontrado"] = True
				context.user_data['lista'] = data[6]
				listadias = []
				for n in context.user_data['lista']:
					if n == '0':
						listadias.append(' Lunes ')
					if n == '1':
						listadias.append(' Martes ')
					if n == '2':
						listadias.append(' Miércoles ')
					if n == '3':
						listadias.append(' Jueves ')
					if n == '4':
						listadias.append(' Viernes ')
					if n == '5':
						listadias.append(' Sábado ')
					if n == '6':
						listadias.append(' Domingo ')
				original = str(listadias)
				original = original.replace("[", "")
				original = original.replace("]", "")
				listadias = original.replace("'", "")

				update.message.reply_text(
					text='🔷 <b>Nombre:</b> '+ str(data[2]) + '\n' \
					+ '🔷 <b>Categoría: </b>'+ str(data[3]) + '\n' \
					+ '🔷 <b>Repetición: </b>' + str(data[4]) + ' dias a la semana.\n' \
					+ '🔷 <b>Se repite los días</b> ' + str(listadias) \
					+ '\n🔷 <b>Duración: </b>' + str(data[5]) + ' horas por día.\n',
					parse_mode=telegram.ParseMode.HTML,
					reply_markup=reply_markup
				)

		if context.user_data["encontrado"] == False:
					update.message.reply_text(
						text="No existe ninguna rutina con ese nombre. 💬\n",
						parse_mode=telegram.ParseMode.HTML,
						reply_markup=reply_markup
					)
	else:
			update.message.reply_text(
				text="<b>⚠ No hay rutinas, vuelva al menú de rutinas y cree una. ⚠</b>\n" ,
				parse_mode=telegram.ParseMode.HTML,
				reply_markup=reply_markup
			)

	return GESTION_BUSCADOR

def busqueda_fecha(update: Update, context: CallbackContext):
	logger.info("El usuario %s introduce busqueda por fecha de vencimiento", context.user_data["nombre_usuario"])
	query = update.callback_query
	context.bot.send_message(
		text="<b> 🔎 Búsqueda por fecha de vencimiento 🔎 </b>\n\n Escribe la fecha de la tarea que quieras buscar .\n",
		chat_id = query.message.chat_id,
		parse_mode=telegram.ParseMode.HTML,
	)
	return RESULTADO_FECHA


def resultado_fecha(update: Update, context: CallbackContext):
	logger.info("El usuario %s obtiene resultado de su busqueda por fecha de tareas", context.user_data["nombre_usuario"])
	valor = update.message.text
	id_usuario = context.user_data["id_usuario"]
	fecha_valida = funciones.valida_fecha_busqueda(update.message.text)
	if (update.message.text.upper() == '/salir'.upper()):
			update.message.reply_text(
				text="¡Hasta pronto!"
			)
			return ConversationHandler.END
	if not fecha_valida:
		update.message.reply_text(
								text="💬 Has introducido una fecha incorrecta ❌. Indique la fecha de vencimiento con el formato correcto y comprueba que no sea una fecha pasada. Ej. " + funciones.dia_prox(),
								parse_mode=telegram.ParseMode.HTML
								)
		return RESULTADO_FECHA
	else:

		datos = bd_bot.leer_tareas_todas(str(id_usuario))
		reply_markup = InlineKeyboardMarkup(teclado_volver_buscador)
		context.user_data["encontrado"] = False

		if datos:
			update.message.reply_text(
				text="<b>Resultado de la búsqueda de su tarea por fecha de vencimiento:</b> \n\n",
				parse_mode=telegram.ParseMode.HTML,
			)
			for data in datos:
				if str(data[4]) == str(valor):

					context.user_data["encontrado"] = True
					if(str(data[6]) == 'NO'):
						context.user_data["realizada"] = '❌'
					elif(str(data[6]) == 'SI'):
						context.user_data["realizada"] = '✅'
					if(str(data[5]) == 'None'):
						context.user_data["comentario"] = '❌'
					if(str(data[3]) == '1'):
						context.user_data["prioridad"] = '🛑 Alta'
					elif(str(data[3]) == '2'):
						context.user_data["prioridad"] = '✴️ Media'
					elif(str(data[3]) == '3'):
						context.user_data["prioridad"] = '❇️ Baja'

					update.message.reply_text(
						text='🔷 <b>Nombre:</b> '+ str(data[2]) + '\n' \
						+ '🔷 <b>Prioridad: </b>'+ context.user_data["prioridad"] + '\n' \
						+ '🔷 <b>Fecha de vencimiento: </b>' + str(data[4]) + '\n' \
						+ '🔷 <b>Comentario: </b>' + context.user_data["comentario"] + '\n' \
						+ '🔷 <b>¿Tarea realizada? </b>' + context.user_data["realizada"],
						parse_mode=telegram.ParseMode.HTML,
					)
			if context.user_data["encontrado"] == True:
				update.message.reply_text(
						text='➖➖➖➖➖',
						reply_markup=reply_markup
				)

			if context.user_data["encontrado"] == False:
						update.message.reply_text(
							text="💬 No existe ninguna tarea con esa fecha de vencimiento.\n",
							parse_mode=telegram.ParseMode.HTML,
							reply_markup=reply_markup
						)


			return GESTION_BUSCADOR

def busqueda_categoria(update: Update, context: CallbackContext):
	logger.info("El usuario %s visualiza las categorias de las rutinas", context.user_data["nombre_usuario"])
	query = update.callback_query
	datos = bd_bot.leer_rutinas_t(str(context.user_data["id_usuario"]))
	keyboard = []
	#muestra datos de la bd y de callback data te devuelve el id
	if  datos:
		context.bot.send_message(
			text="<b> Categorias de Rutinas</b>\nElige una para visualizar las rutinas asociadas a esa categoría.\n",
			chat_id = query.message.chat_id,
			parse_mode=telegram.ParseMode.HTML,
		)
		for data in datos:

			keyboard.append([InlineKeyboardButton('🔹 ' + str(data[3]),
							callback_data=data[3])])

		reply_markup = InlineKeyboardMarkup(keyboard)
		context.bot.send_message(
			text="➡ Busqueda por categoría\n",
			chat_id = query.message.chat_id,
			parse_mode=telegram.ParseMode.HTML,
			reply_markup=reply_markup
		)
		return VISUALIZAR_CATEGORIAS
	else:
		reply_markup = InlineKeyboardMarkup(teclado_buscador)
		context.bot.send_message(
			text="<b>⚠ No has creado ninguna rutina. Vuelva al menú principal y crea una rutina con su categoría.⚠</b>\n",
			parse_mode=telegram.ParseMode.HTML,
			chat_id = query.message.chat_id,
			reply_markup=reply_markup
		)
		return GESTION_BUSCADOR



def visualizar_categorias(update: Update, context: CallbackContext):
	logger.info("El usuario %s visualiza las rutinas con la categoria elegida.)", context.user_data["nombre_usuario"])
	query =  update.callback_query
	id_usuario = context.user_data["id_usuario"]

	datos = bd_bot.leer_rutinas(str(id_usuario))
	reply_markup = InlineKeyboardMarkup(teclado_volver_buscador)
	context.user_data["encontrado"] = False
	context.user_data['dias_mostrar'] = []


	if datos:
		context.bot.send_message(
			text="<b>Resultado de la búsqueda de su rutina por categoría.</b>\n\n",
			chat_id = query.message.chat_id,
			parse_mode=telegram.ParseMode.HTML,
		)
		for data in datos:
			if str(data[3]) == str(query.data):
				context.user_data["encontrado"] = True
				context.user_data['lista'] = data[6]
				listadias = []
				for n in context.user_data['lista']:
					if n == '0':
						listadias.append(' Lunes ')
					if n == '1':
						listadias.append(' Martes ')
					if n == '2':
						listadias.append(' Miércoles ')
					if n == '3':
						listadias.append(' Jueves ')
					if n == '4':
						listadias.append(' Viernes ')
					if n == '5':
						listadias.append(' Sábado ')
					if n == '6':
						listadias.append(' Domingo ')
				original = str(listadias)
				original = original.replace("[", "")
				original = original.replace("]", "")
				listadias = original.replace("'", "")

				context.bot.send_message(
					text='🔷 <b>Nombre:</b> '+ str(data[2]) + '\n' \
					+ '🔷 <b>Categoría: </b>'+ str(data[3]) + '\n' \
					+ '🔷 <b>Repetición: </b>' + str(data[4]) + ' dias a la semana.\n' \
					+ '🔷 <b>Se repite los días</b> ' + str(listadias) \
					+ '\n🔷 <b>Duración: </b>' + str(data[5]) + ' horas por día.\n',
					parse_mode=telegram.ParseMode.HTML,
					chat_id = query.message.chat_id,
					reply_markup=reply_markup
				)

		if context.user_data["encontrado"] == False:
					context.bot.send_message(
						text="<b>💬  No existe ninguna rutina con ese nombre.</b>\n",
						parse_mode=telegram.ParseMode.HTML,
						chat_id = query.message.chat_id,
						reply_markup=reply_markup
					)
	else:
			context.bot.send_message(
				text="<b>⚠ No hay rutinas, vuelva al menú de rutinas y cree una. ⚠</b>\n" ,
				parse_mode=telegram.ParseMode.HTML,
				chat_id = query.message.chat_id,
				reply_markup=reply_markup
			)

	return GESTION_BUSCADOR

################################### FUNCIONES DE AYUDA ####################################


def comando_ayuda(update: Update, context: CallbackContext):
	datos_user = update.message.from_user
	nombre_usuario = datos_user.first_name
	context.user_data["nombre_usuario"] = nombre_usuario
	logger.info("El usuario %s entra en el menú de ayuda mediane el comando /ayuda", context.user_data["nombre_usuario"])
	# query = update.message
	keyboard = [
		[InlineKeyboardButton("💡 Consejos",  callback_data=str(CONSEJOS)),
		InlineKeyboardButton("📘 Guía rápida",callback_data=str(GUIA_RAPIDA))],
		[InlineKeyboardButton("ℹ Acerca de...", callback_data=str(ACERCA_DE)),
		InlineKeyboardButton(text='✉ Contacto ', callback_data=str(CONTACTO))],
		[InlineKeyboardButton(text='🔙 Volver menú principal', callback_data=str(VOLVER_MENU_PRINCIPAL))],

	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	update.message.reply_text(
		text="<b> ❓ Menú de ayuda ❓ </b>\n",
		parse_mode=telegram.ParseMode.HTML,
		reply_markup=reply_markup
	)


	return GESTION_AYUDA

def menu_ayuda(update: Update, context: CallbackContext):
	logger.info("El usuario %s entra en el menú de ayuda", context.user_data["nombre_usuario"])
	query = update.callback_query
	keyboard = [
		[InlineKeyboardButton("💡 Consejos",  callback_data=str(CONSEJOS)),
		InlineKeyboardButton("📘 Guía rápida",callback_data=str(GUIA_RAPIDA))],
		[InlineKeyboardButton("ℹ Acerca de...", callback_data=str(ACERCA_DE)),
		InlineKeyboardButton(text='✉ Contacto ', callback_data=str(CONTACTO))],
		[InlineKeyboardButton(text='🔙 Volver menú principal', callback_data=str(VOLVER_MENU_PRINCIPAL))],

	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	context.bot.send_message(
		text="<b> ❓ Menú de ayuda ❓ </b>\n",
		chat_id = query.message.chat_id,
		parse_mode=telegram.ParseMode.HTML,
		reply_markup=reply_markup
	)


	return GESTION_AYUDA

def consejos(update: Update, context: CallbackContext):
	logger.info("El usuario %s entra en consejos", context.user_data["nombre_usuario"])
	query = update.callback_query
	keyboard = [
			[
			# InlineKeyboardButton("💡 Más",  callback_data=str(CONSEJOS)),
			InlineKeyboardButton(text='🔙 Volver al menú ayuda', callback_data=str(VOLVER_MENU_AYUDA))],

		]
	reply_markup = InlineKeyboardMarkup(keyboard)
	context.bot.send_message(
			text="<b>💡 Consejos 💡</b>\n\n \
			➡ No olvides realizar tus tareas de prioridad alta.\n \
			➡ Crea recordatorios para no olvidar tus tareas y rutinas.\n \
			➡ No te olvides del descanso para ser más productivo.\n \
			➡ No te excedas con el número de horas destinadas a una rutina.\n" ,
			chat_id = query.message.chat_id,
			parse_mode=telegram.ParseMode.HTML,
			reply_markup=reply_markup
	)
	return GESTION_AYUDA

def guia_rapida(update: Update, context: CallbackContext):
	logger.info("El usuario %s entra en  guía rápida", context.user_data["nombre_usuario"])
	query = update.callback_query
	teclado_menu_principal_ayuda = [
					[InlineKeyboardButton(text='📋 Rutinas ', callback_data=str(RUTINAS_AYUDA))],
					[InlineKeyboardButton(text='📝 Tareas ', callback_data=str(TAREAS_AYUDA))],
					[InlineKeyboardButton(text='🎖 Logros ', callback_data=str(LOGROS_AYUDA))],
					[InlineKeyboardButton(text='🔎 Buscador ', callback_data=str(BUSCADOR_AYUDA))],
					[InlineKeyboardButton(text='🔙 Volver al menú de ayuda ', callback_data=str(VOLVER_MENU_AYUDA))],
				  ]
	reply_markup = InlineKeyboardMarkup(teclado_menu_principal_ayuda)
	context.bot.send_message(
			text="<b>📘 Guía rápida 📘</b>\n\n ¿Sobre qué funcionalidad del menú necesitas ayuda?.",
			chat_id = query.message.chat_id,
			parse_mode=telegram.ParseMode.HTML,
			reply_markup=reply_markup
	)
	return OPCIONES_GUIA_RAPIDA

volver_menu_ayuda = [
				[InlineKeyboardButton(text='🔙 Volver al menú ayuda ', callback_data=str(VOLVER_MENU_AYUDA))],
			  ]
volver_menu_guiarapida = [
				[InlineKeyboardButton(text='🔙 Volver al menú de guía rápida ', callback_data=str(VOLVER_MENU_GUIARAPIDA))],
			  ]
def rutinas_ayuda(update: Update, context: CallbackContext):
	logger.info("El usuario %s entra en el menú de ayuda de rutinas", context.user_data["nombre_usuario"])
	query = update.callback_query
	boton = query.data
	reply_markup = InlineKeyboardMarkup(volver_menu_guiarapida)
	context.bot.send_message(
			text="<b> 📋 Ayuda de rutinas 📋 </b>\n\n En este menú podrás crear tus rutinas semanales estableciendo su nombre, dias de repetición, horas que dedicarás cada día, además de la posiblidad de crear recordatorios diarios para los días establecidos de tu rutina.",
			chat_id = query.message.chat_id,
			parse_mode=telegram.ParseMode.HTML,
			reply_markup=reply_markup
	)
	return GESTION_AYUDA

def tareas_ayuda(update: Update, context: CallbackContext):
	logger.info("El usuario %s entra en el menú de ayuda de tareas", context.user_data["nombre_usuario"])
	query = update.callback_query
	boton = query.data
	reply_markup = InlineKeyboardMarkup(volver_menu_guiarapida)
	context.bot.send_message(
			text="<b> 📝 Ayuda de tareas 📝 </b>\n\n Este menú te da la posiblidad de crear tareas independientes a las que podrás asignar una prioridad según su urgencia, fecha de vencimiento, además de marcar como completada y crear un recordatorio en la fecha deseada para no olvidarlo.",
			chat_id = query.message.chat_id,
			parse_mode=telegram.ParseMode.HTML,
			reply_markup=reply_markup
	)
	return GESTION_AYUDA

def logros_ayuda(update: Update, context: CallbackContext):
	logger.info("El usuario %s entra en el menú de ayuda de tareas", context.user_data["nombre_usuario"])
	query = update.callback_query
	boton = query.data
	reply_markup = InlineKeyboardMarkup(volver_menu_guiarapida)
	context.bot.send_message(
			text='''<b> 🎖 Ayuda de logros 🎖 </b>\n\nEn el menú de logros podrás visualizar los premios obtenidos sobre tareas y rutinas.
			Además podrás visualizar la productividad sobre tus tareas mediante gráficas, sobre las tareas
			completas e incompletas y sobre tareas completadas por prioridad''',
			chat_id = query.message.chat_id,
			parse_mode=telegram.ParseMode.HTML,
			reply_markup=reply_markup
	)
	return GESTION_AYUDA

def buscador_ayuda(update: Update, context: CallbackContext):
	logger.info("El usuario %s entra en el menú de ayuda de tareas", context.user_data["nombre_usuario"])
	query = update.callback_query
	boton = query.data
	reply_markup = InlineKeyboardMarkup(volver_menu_guiarapida)
	context.bot.send_message(
			text='''<b> 📋 Ayuda del buscador 📋 </b>\n\nEn este menú podrás realizar búsquedas sobre tus rutinas filtrando por categoría o nombre, tambien podrás buscar tus tareas mediante el filtro de nombre o su fecha de vencimiento''',
			chat_id = query.message.chat_id,
			parse_mode=telegram.ParseMode.HTML,
			reply_markup=reply_markup
	)
	return GESTION_AYUDA

def contacto(update: Update, context: CallbackContext):
	logger.info("El usuario %s entra en el menú de ayuda de tareas", context.user_data["nombre_usuario"])
	query = update.callback_query
	context.bot.send_message(
			text="<b> ✉️ Contacto ✉️ </b>\n\n Ponte en conctacto con nosotros escribiendo alguna sugerencia o problema. ✍",
			chat_id = query.message.chat_id,
			parse_mode=telegram.ParseMode.HTML,
	)
	return ENVIAR_MENSAJE

def enviar_mensaje(update: Update, context: CallbackContext):
	logger.info("El usuario %s envia la sugerencia o duda", context.user_data["nombre_usuario"])
	valor = update.message.text
	if (update.message.text.upper() == '/salir'.upper()):
			update.message.reply_text(
				text="¡Hasta pronto!"
			)
			return ConversationHandler.END
	reply_markup = InlineKeyboardMarkup(volver_menu_ayuda)
	context.bot.send_message(
			text="<b> Sugerencia del usuario: "+valor+" </b>\n",
			chat_id = 1147037883, #132091398
			parse_mode=telegram.ParseMode.HTML,

	)
	update.message.reply_text(
		text="<b>💬 Mensaje enviado. 💬</b>",
		parse_mode=telegram.ParseMode.HTML,
	)
	update.message.reply_text(
		text="<b>Gracias por contribuir a la mejora del bot. ✌</b>",
		parse_mode=telegram.ParseMode.HTML,
		reply_markup=reply_markup
	)
	return GESTION_AYUDA


def acerca_de(update: Update, context: CallbackContext):
	logger.info("El usuario %s entra en el menú de ayuda de tareas", context.user_data["nombre_usuario"])
	query = update.callback_query
	reply_markup = InlineKeyboardMarkup(volver_menu_ayuda)
	context.bot.send_message(
		text="<b> ℹ Acerca de ... ℹ </b>\n\n 🔹 <b>Nombre:</b> PlanningUGR.\n 🔹 <b>Autor:</b> Patricia Maldonado \n 🔹 <b>Directora:</b> Rosana Montes \n 🔹 <b>Contacto:</b> @rosanamontes \n 🔹 <b>Trabajo de fin de Grado de Ingeniería Informática:</b> \n 🔹 <b> Universidad de Granada. Curso 2019-2020.</b>",
		chat_id = query.message.chat_id,
		parse_mode=telegram.ParseMode.HTML,
		reply_markup=reply_markup
	)
	return GESTION_AYUDA


 ############################## OTROS #####################################################

def enconstruccion(update: Update, context: CallbackContext):
	logger.info("El usuario %s entra en una opción en construcción", context.user_data["nombre_usuario"])
	query = update.callback_query
	context.bot.send_message(
			text="<b>Próximamente</b>\n<b></b>",
			parse_mode=telegram.ParseMode.HTML,
			chat_id = query.message.chat_id,
	)


def salir(update: Update, context: CallbackContext):
	logger.info("El usuario %s sale del bot mediante el comando salir", context.user_data["nombre_usuario"])
	valor = update.message.text
	update.message.reply_text(
		text="¡Hasta pronto!"
	)
	return ConversationHandler.END

def end(update: Update, context: CallbackContext):
	logger.info("El usuario %s sale del bot", context.user_data["nombre_usuario"])
	query = update.callback_query
	context.bot.send_message(
		text="¡Hasta pronto!",
		chat_id = query.message.chat_id,
	)
	return ConversationHandler.END

def error(update, context):
	"""Log Errors caused by Updates."""
	logger.warning('Update "%s" caused error "%s"', update, context.error)


def unknown(update: Update, context: CallbackContext):
	context.bot.send_message(chat_id=update.message.chat_id, text="Lo siento, ese comando no existe.")





def main():
    # Creamos el update pasándole el token del bot
	mi_bot = telegram.Bot(token =token)
	updater = Updater(mi_bot.token, use_context=True)

	# Get the dispatcher to register handlers
	dp = updater.dispatcher

	# Conversación de menú principal
	conv_handler = ConversationHandler(
		entry_points=[CommandHandler('start', start)],
		states={

			# ESTADOS MENU PRINCIPAL
			MENU_PRINCIPAL: [
								CallbackQueryHandler(menu_rutinas, pattern=str(MENU_RUTINAS)),
								CallbackQueryHandler(menu_tareas, pattern='^' + str(MENU_TAREAS) + '$'),
								CallbackQueryHandler(menu_ayuda, pattern='^' + str(MENU_AYUDA) + '$'),
								CallbackQueryHandler(menu_logros, pattern='^' + str(MENU_LOGROS) + '$'),
								CallbackQueryHandler(menu_buscador, pattern='^' + str(MENU_BUSCADOR) + '$'),
								CallbackQueryHandler(end, pattern='^' + str(FINALIZAR) + '$'),
							],

			# ESTADOS PARA TAREAS
			GESTION_TAREAS: [
								 CallbackQueryHandler(pregunta1_tareas,pattern='^' + str(TAREAS) + '$'),
								 CallbackQueryHandler(menu_tareas, pattern='^' + str(MENU_TAREAS) + '$'),
								 CallbackQueryHandler(visualizar_tareas,pattern='^' + str(EDICION_TAREAS)),
								 CallbackQueryHandler(menu_tareas_fecha,pattern='^' + str(TAREAS_PORFECHA)),
								 CallbackQueryHandler(menu_principal, pattern='^' + str(VOLVER_MENU_PRINCIPAL) + '$'),
								 CallbackQueryHandler(menu_tareas, pattern='^' + str(VOLVER_MENU_TAREAS_P) + '$'),
								 CallbackQueryHandler(menu_tareas_fecha, pattern='^' + str(VOLVER_MENU_TAREAS_F) + '$'),
								 CallbackQueryHandler(end, pattern='^' + str(FINALIZAR) + '$'),
							],

			PREGUNTA2_TAREAS: [MessageHandler(Filters.text, pregunta2_tareas)],
			PRIORIDADES_TAREA:[CallbackQueryHandler(prioridadt_alta, pattern='^' + str(PRIORIDAD_ALTA) + '$'),
							  CallbackQueryHandler(prioridadt_media, pattern='^' + str(PRIORIDAD_MEDIA) + '$'),
							  CallbackQueryHandler(prioridadt_baja, pattern='^' + str(PRIORIDAD_BAJA) + '$'),
							],
			PREGUNTA4_TAREAS: [MessageHandler(Filters.text, pregunta4_tareas)],
			PREGUNTA_COMENT: [CallbackQueryHandler(coment_tarea_si, pattern='^' + str(COMENT_TAREA_SI) + '$'),
							  CallbackQueryHandler(pregunta5_tareas_noc, pattern='^' + str(COMENT_TAREA_NO) + '$')
							  ],
			PREGUNTA5_TAREAS: [MessageHandler(Filters.text, pregunta5_tareas)],

			OBTIENE_ID_TAREA:[CallbackQueryHandler(recojo_id_ediciontarea, pass_user_data=True)],
			EDICIONES_TAREA:[CallbackQueryHandler(edicion_tarea1,pattern='^' + str(EDICION)  + '$'),
								CallbackQueryHandler(edicion_tarea2,pattern='^' + str(EDICION2)  + '$'),
								CallbackQueryHandler(edicion_tarea22,pattern='^' + str(EDICION22)  + '$'),
								CallbackQueryHandler(edicion_tarea3,pattern='^' + str(EDICION3)  + '$'),
								CallbackQueryHandler(estado_tarea,pattern='^' + str(ESTADO_TAREA)  + '$'),
								CallbackQueryHandler(end, pattern='^' + str(FINALIZAR) + '$'),
								CallbackQueryHandler(menu_tareas, pattern='^' + str(VOLVER_MENU_TAREAS_P) + '$'),
								CallbackQueryHandler(menu_tareas_fecha, pattern='^' + str(VOLVER_MENU_TAREAS_F) + '$'),
								CallbackQueryHandler(crear_recordatorios, pattern='^' + str(RECORDATORIO_TAREA) + '$'),
								CallbackQueryHandler(eliminar_tarea,pattern='^' + str(ELIMINAR_TAREA_ACTUAL) + '$'),
								CallbackQueryHandler(alarma_maniana, pattern='^' + str(ALARMA_MANIANA) + '$'),
								CallbackQueryHandler(alarma_semanaprox, pattern='^' + str(ALARMA_SEMANAPROX) + '$'),
								CallbackQueryHandler(alarma_elegirfecha, pattern='^' + str(ALARMA_ELEGIRFECHA) + '$'),
								# CallbackQueryHandler(premios,pattern='^' + str(PREMIOS))
								],

			EDITANOMBRE1:[MessageHandler(Filters.text, editanombre_tarea)],
			EDITAPRIORIDAD:[CallbackQueryHandler(guardaprioridad_tarea)],
			EDITANOMBRE22:[MessageHandler(Filters.text, editafecha_tarea)],
			EDITANOMBRE3:[MessageHandler(Filters.text, editacomentario_tarea)],
			ALARM_MHORA: [MessageHandler(Filters.text, alarm_mhora)],
			ALARM_PHORA: [MessageHandler(Filters.text, alarm_phora)],
			ALARM_ELIGEH:[MessageHandler(Filters.text, alarm_eligeh)],
			ALARM_ELIGEG:[MessageHandler(Filters.text, alarm_eligeg)],

			# ESTADOS PARA RUTINAS

			RUTINAS_GESTION: [
							 CallbackQueryHandler(categorias_gestion,pattern='^' + str(CATEGORIAS_GESTION)),
							 CallbackQueryHandler(categorias_rutina, pattern='^' + str(CATEGORIAS_RUTINA) + '$'),
							 CallbackQueryHandler(pregunta1_rutinas,pattern='^' + str(RUTINAS)),
							 CallbackQueryHandler(edita_nombrec,pattern='^' + str(EDITA_NOMBREC)),
							 CallbackQueryHandler(nueva_categoria,pattern='^' + str(NUEVA_CATEGORIA)),
							 CallbackQueryHandler(eliminar_categoria,pattern='^' + str(ELIMINAR_CATEGORIA)),
							 CallbackQueryHandler(visualizar_rutinas,pattern='^' + str(EDICION_RUTINAS)),
							 CallbackQueryHandler(menu_principal, pattern='^' + str(VOLVER_MENU_PRINCIPAL) + '$'),
							 CallbackQueryHandler(categorias_rutina, pattern='^' + str(VOLVER_MENU_CATEGORIAS) + '$'),
							 CallbackQueryHandler(menu_rutinas, pattern='^' + str(VOLVER_MENU_RUTINAS) + '$'),
							 CallbackQueryHandler(enconstruccion, pattern='^' + str(ENCONSTRUCCION) + '$'),


							],
			PREGUNTA11_RUTINAS:[MessageHandler(Filters.text,pregunta11_rutinas)],
			PREGUNTA2_RUTINAS: [CallbackQueryHandler(pregunta2_rutinas)],
			PREGUNTA3_RUTINAS: [CallbackQueryHandler(pregunta3_rutinas)],
			PREGUNTA4_RUTINAS: [CallbackQueryHandler(pregunta4_rutinas)],
			HORAS_RUTINA:[MessageHandler(Filters.text, horas_rutina)],
			PREGUNTA5_RUTINAS: [CallbackQueryHandler(pregunta5_rutinas)],
			EDITADIAS_RECORD: [CallbackQueryHandler(editadias_record)],
			OBTIENE_ID_RUTINA:[CallbackQueryHandler(obtener_id_rutinas)],
			GUARDAR_CATEGORIA:[MessageHandler(Filters.text, guardar_categoria)],
			OBTIENE_ID_CATEGORIA:[CallbackQueryHandler(obtiene_id_categoria)],
			EDITA_CATEGORIA:[MessageHandler(Filters.text, edita_categoria)],
			EDICIONES_RUTINA:[
							CallbackQueryHandler(pregunta6_rutinas,pattern='^' + str(PREGUNTA6_RUTINAS)),
							CallbackQueryHandler(pregunta6_rutinas_hora,pattern='^' + str(PREGUNTA6_RUTINAS_HORA)),
							CallbackQueryHandler(edita_rutina,pattern='^' + str(EDICIONR)),
							CallbackQueryHandler(edita_rutina2,pattern='^' + str(EDICION2R)),
							CallbackQueryHandler(edita_rutina3,pattern='^' + str(EDICION3R)),
							CallbackQueryHandler(edita_rutina4,pattern='^' + str(EDICION4R)),
							CallbackQueryHandler(edita_rutina5,pattern='^' + str(EDICION5R)),
							CallbackQueryHandler(marcar_rutina,pattern='^' + str(MARCAR_RUTINA)  + '$'),
							CallbackQueryHandler(guarda_dias,pattern='^' + str(GUARDA_DIAS)),
							CallbackQueryHandler(guarda_dias_record,pattern='^' + str(GUARDA_DIAS_RECORD)),
							CallbackQueryHandler(pregunta3_rutinas,pattern='^' + str(PREGUNTA3_RUTINAS)),
							CallbackQueryHandler(pregunta4_rutinas,pattern='^' + str(PREGUNTA4_RUTINAS)),
							CallbackQueryHandler(pregunta4_rutinas_horas,pattern='^' + str(PREGUNTA4_RUTINAS_HORAS)),
							CallbackQueryHandler(menu_rutinas, pattern='^' + str(VOLVER_MENU_RUTINAS) + '$'),
							CallbackQueryHandler(recordatorio_rutina, pattern='^' + str(RECORDATORIO_RUTINA) + '$'),
							CallbackQueryHandler(menu_rutinas, pattern='^' + str(VOLVER_MENU_RUTINAS)),
							CallbackQueryHandler(eliminar_rutina,pattern='^' + str(ELIMINAR_RUTINA)),
							CallbackQueryHandler(enconstruccion, pattern='^' + str(ENCONSTRUCCION) + '$'),


						 ],

			PREGUNTA6_RUTINAS_R:[MessageHandler(Filters.text, pregunta6_rutinas_r)],
			EDITANOMBRE1R:[MessageHandler(Filters.text & (~Filters.command), editanombrer)],
			EDITANOMBRE2R:[CallbackQueryHandler(editacategoria)],
			EDITANOMBRE3R:[CallbackQueryHandler(editadescripcionr)],
			EDITANOMBRE4R:[MessageHandler(Filters.text & (~Filters.command), editaduracionr)],
			EDITANOMBRE5R:[CallbackQueryHandler(edita_diasemana)],
			ELIMINACION_RUTINA: [CallbackQueryHandler(eliminar_rutina, pattern='^' + str(ELIMINAR_RUTINAS)),
								 CallbackQueryHandler(menu_rutinas, pattern='^' + str(VOLVER_MENU_RUTINAS) + '$')],
			HORA_RECORDATORIOR:[MessageHandler(Filters.text, hora_recordatorior)],
			HORA_RECORDATORIO2:[CallbackQueryHandler(recordatorio_rutina)],

			# ESTADOS DE AYUDA


			GESTION_AYUDA: [CallbackQueryHandler(consejos, pattern='^' + str(CONSEJOS) + '$'),
							CallbackQueryHandler(guia_rapida, pattern='^' + str(GUIA_RAPIDA) + '$'),
							CallbackQueryHandler(contacto, pattern='^' + str(CONTACTO) + '$'),
							CallbackQueryHandler(acerca_de, pattern='^' + str(ACERCA_DE) + '$'),
							CallbackQueryHandler(guia_rapida, pattern='^' + str(VOLVER_MENU_GUIARAPIDA) + '$'),
							CallbackQueryHandler(menu_ayuda, pattern='^' + str(VOLVER_MENU_AYUDA) + '$'),
							CallbackQueryHandler(menu_principal, pattern='^' + str(VOLVER_MENU_PRINCIPAL) + '$')],


			OPCIONES_GUIA_RAPIDA:[CallbackQueryHandler(rutinas_ayuda, pattern='^' + str(RUTINAS_AYUDA) + '$'),
								  CallbackQueryHandler(tareas_ayuda, pattern='^' + str(TAREAS_AYUDA) + '$'),
								  CallbackQueryHandler(logros_ayuda, pattern='^' + str(LOGROS_AYUDA) + '$'),
								  CallbackQueryHandler(buscador_ayuda, pattern='^' + str(BUSCADOR_AYUDA) + '$'),
								  CallbackQueryHandler(menu_ayuda, pattern='^' + str(VOLVER_MENU_AYUDA) + '$'),
								  CallbackQueryHandler(menu_principal, pattern='^' + str(VOLVER_MENU_PRINCIPAL) + '$')],
			ENVIAR_MENSAJE:[MessageHandler(Filters.text, enviar_mensaje)],


			# ESTADOS DE LOGROS

			GESTION_LOGROS: [CallbackQueryHandler(graficas, pattern='^' + str(GRAFICAS) + '$'),
							 CallbackQueryHandler(graficames, pattern='^' + str(GRAFICAMES) + '$'),
							 CallbackQueryHandler(menu_logros, pattern='^' + str(VOLVER) + '$'),
							 CallbackQueryHandler(enconstruccion, pattern='^' + str(ENCONSTRUCCION) + '$'),
							 CallbackQueryHandler(menu_principal, pattern='^' + str(VOLVER_MENU_PRINCIPAL) + '$')
							 ],

			# ESTADOS DEl BUSCADOR
			GESTION_BUSCADOR: [CallbackQueryHandler(menu_principal, pattern='^' + str(VOLVER_MENU_PRINCIPAL) + '$'),
							   CallbackQueryHandler(menu_buscador_rutina,pattern='^' + str(BUSQUEDA_RUTINA)),
							   CallbackQueryHandler(menu_buscador_tarea,pattern='^' + str(BUSQUEDA_TAREA)),
							   CallbackQueryHandler(busqueda_nombre,pattern='^' + str(BUSQUEDA_NOMBRE)),
							   CallbackQueryHandler(busqueda_nombre_r,pattern='^' + str(BUSQUEDA_NOMBRE_R)),
							   CallbackQueryHandler(busqueda_fecha,pattern='^' + str(BUSQUEDA_FECHA)),
							   CallbackQueryHandler(busqueda_categoria,pattern='^' + str(BUSQUEDA_CATEGORIA)),
							   CallbackQueryHandler(menu_principal, pattern='^' + str(VOLVER_MENU_PRINCIPAL) + '$'),
							   CallbackQueryHandler(menu_buscador, pattern='^' + str(VOLVER_MENU_BUSCADOR) + '$')


			],

			RESULTADO_BNOMBRE: [MessageHandler(Filters.text, resultado_bnombre)],
			RESULTADO_BNOMBRE_R:[MessageHandler(Filters.text, resultado_bnombre_r)],
			RESULTADO_FECHA: [MessageHandler(Filters.text, resultado_fecha)],
			VISUALIZAR_CATEGORIAS: [CallbackQueryHandler(visualizar_categorias)],
	},
		fallbacks=[CommandHandler('start', start),
				   CommandHandler('salir',salir),
				   CommandHandler('ayuda',comando_ayuda)
						]
	)


	# Add ConversationHandler to dispatcher that will be used for handling
	# updates


	dp.add_handler(conv_handler)
	dp.add_handler(CommandHandler("ayuda", comando_ayuda))
	#dp.add_handler(MessageHandler((~Filters.command), unknown))

	# log all errors
	dp.add_error_handler(error)

	# Start the Bot ,pregunta constantemente a nuestro bot si hay nuevos mensajes
	updater.start_polling()

	# Permite finalizar el bot con ctrl + C
	updater.idle()


if __name__ == '__main__':
	bd_bot.crear_bd()
	main()
