#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

def crear_bd():
	con = sqlite3.connect('./bd_bot.db')

	cur = con.cursor()

	cur.execute('CREATE TABLE IF NOT EXISTS usuarios(id_usuario INTEGER PRIMARY KEY NOT NULL, '
													'nombre_usuario TEXT NOT NULL)')

	cur.execute('CREATE TABLE IF NOT EXISTS tareas(id_tarea INTEGER PRIMARY KEY NOT NULL, '
															'id_usuario INTEGER NOT NULL, '
															'nombre_tarea TEXT NOT NULL, '
															'prioridad_tarea INTEGER NOT NULL, '
															'fecha_tarea TEXT NOT NULL,'
															'comentario_tarea TEXT,'
															'estado_tarea TEXT NOT NULL,'
															'premio_tarea TEXT,'
															'CONSTRAINT fk_id_usuariot FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario))')

	cur.execute('CREATE TABLE IF NOT EXISTS rutinas(id_rutina INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, '
														'id_usuario INTEGER NOT NULL, '
														'nombre_rutina TEXT NOT NULL, '
														'categoria_rutina TEXT NOT NULL, '
														'repeticion_rutina INTEGER NOT NULL, '
														'duracion_rutina INTEGER NOT NULL, '
														'dias_rutina TEXT NOT NULL,'
														'premio_rutina INTEGER,'
 														'CONSTRAINT clave_exter FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),'
														'CONSTRAINT clave_exter2 FOREIGN KEY (categoria_rutina) REFERENCES categoria(id_categoria))')

	cur.execute('CREATE TABLE IF NOT EXISTS categoria(id_categoria INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, '
														'id_usuario INTEGER NOT NULL, '
														'nombre_categoria TEXT NOT NULL, '
 														'CONSTRAINT clave_cat FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario))')

	# Categorías predefinidas
	cur.execute("""INSERT INTO categoria (id_usuario, nombre_categoria) SELECT 0, 'Ocio' WHERE NOT EXISTS (SELECT * FROM categoria WHERE id_usuario = 0 and nombre_categoria = 'Ocio')""")
	cur.execute("""INSERT INTO categoria (id_usuario, nombre_categoria) SELECT 0, 'Estudio' WHERE NOT EXISTS (SELECT * FROM categoria WHERE id_usuario = 0 and nombre_categoria = 'Estudio')""")
	cur.execute("""INSERT INTO categoria (id_usuario, nombre_categoria) SELECT 0, 'Trabajo' WHERE NOT EXISTS (SELECT * FROM categoria WHERE id_usuario = 0 and nombre_categoria = 'Trabajo')""")

	cur.close()
	con.commit()

global data_base
data_base = 'bd_bot.db'

##################################### FUNCIONES USUARIOS ############################################

def comprueba_usuario(id):
	data_base ='./bd_bot.db'
	con = sqlite3.connect(data_base)
	cur = con.cursor()
	cur.execute('SELECT * FROM usuarios WHERE id_usuario= ' + id)
	data = cur.fetchall()
	cur.close()
	con.close()

	return data

def crear_usuario(id,nombre):
	data_base ='./bd_bot.db'
	con = sqlite3.connect(data_base)
	cur = con.cursor()
	cur.execute('INSERT INTO usuarios (id_usuario,nombre_usuario) VALUES (?, ?)', (id,nombre))
	con.commit()
	cur.close()
	con.close()

##################################### FUNCIONES TAREAS ############################################


# Contar tareas Pendientes

def contar_tareas_pendientes(id):
	con = sqlite3.connect('./bd_bot.db')
	cur = con.cursor()

	cur.execute('''SELECT COUNT(estado_tarea) FROM tareas WHERE estado_tarea='NO' and id_usuario= ''' + id)
	data = cur.fetchone()
	cur.close()
	con.close()

	return data

# Contar tareas completas

def contar_tareas_completas(id):
	con = sqlite3.connect('./bd_bot.db')
	cur = con.cursor()

	cur.execute('''SELECT COUNT (estado_tarea) FROM tareas WHERE estado_tarea='SI' and id_usuario= ''' + id)
	data = cur.fetchone()
	cur.close()
	con.close()

	return data


# Contar total de tareas

def contar_tareas(id):
	con = sqlite3.connect('./bd_bot.db')
	cur = con.cursor()

	cur.execute('''SELECT COUNT(estado_tarea) FROM tareas WHERE id_usuario= ''' + id)
	data = cur.fetchone()
	cur.close()
	con.close()

	return data


def contar_tareas_prioridad1(id):
	con = sqlite3.connect('./bd_bot.db')
	cur = con.cursor()
	cur.execute('''SELECT COUNT(prioridad_tarea) FROM tareas WHERE prioridad_tarea=1 and estado_tarea='SI' and id_usuario= ''' + id)
	data = cur.fetchone()
	cur.close()
	con.close()

	return data

def contar_tareas_prioridad2(id):
	con = sqlite3.connect('./bd_bot.db')
	cur = con.cursor()
	cur.execute('''SELECT COUNT(prioridad_tarea) FROM tareas WHERE prioridad_tarea=2 and estado_tarea='SI' and id_usuario= ''' + id)
	data = cur.fetchone()
	cur.close()
	con.close()

	return data

def contar_tareas_prioridad3(id):
	con = sqlite3.connect('./bd_bot.db')
	cur = con.cursor()
	cur.execute('''SELECT COUNT(prioridad_tarea) FROM tareas WHERE prioridad_tarea=3 and estado_tarea='SI' and id_usuario= ''' + id)
	data = cur.fetchone()
	cur.close()
	con.close()

	return data

# Leer todas las tareas (pendientes y realizadas)
def leer_tareas_todas(id):
	con = sqlite3.connect('./bd_bot.db')
	cur = con.cursor()

	cur.execute('''SELECT * FROM tareas WHERE id_usuario= ''' + id )
	data = cur.fetchall()
	cur.close()
	con.close()

	return data


# Leer tareas pendientes

def leer_tareas(id):
	con = sqlite3.connect('./bd_bot.db')
	cur = con.cursor()
	cur.execute('''SELECT * FROM tareas WHERE estado_tarea = 'NO' and id_usuario= ''' + id )
	data = cur.fetchall()
	cur.close()
	con.close()
	return data

# Leer tareas que hayan sido completadas

def leer_tareas_completadas(id):
	con = sqlite3.connect('./bd_bot.db')
	cur = con.cursor()

	cur.execute('''SELECT * FROM tareas WHERE estado_tarea='SI' and id_usuario= ''' + id)
	data = cur.fetchall()
	cur.close()
	con.close()

	return data

# Leer tareas segun prioridad

def leer_tareas_prioridad1(id):
	con = sqlite3.connect('./bd_bot.db')
	cur = con.cursor()

	cur.execute('''SELECT * FROM tareas WHERE estado_tarea = 'NO' and prioridad_tarea = 1 and id_usuario= ''' + id)
	data = cur.fetchall()
	cur.close()
	con.close()

	return data

def leer_tareas_prioridad2(id):
	con = sqlite3.connect('./bd_bot.db')
	cur = con.cursor()

	cur.execute('''SELECT * FROM tareas WHERE estado_tarea = 'NO' and prioridad_tarea = 2 and id_usuario= ''' + id)
	data = cur.fetchall()
	cur.close()
	con.close()

	return data

def leer_tareas_prioridad3(id):
	con = sqlite3.connect('./bd_bot.db')
	cur = con.cursor()

	cur.execute('''SELECT * FROM tareas WHERE estado_tarea = 'NO' and prioridad_tarea = 3 and id_usuario= ''' + id)
	data = cur.fetchall()
	cur.close()
	con.close()

	return data


# Leer tarea por id

def leerid_tarea(id):
	con = sqlite3.connect('./bd_bot.db')
	cur = con.cursor()
	cur.execute('''SELECT * FROM tareas WHERE id_tarea= ''' + id)
	data = cur.fetchall()
	cur.close()
	con.close()

	return data


# Leer suma de puntos en tareas
def leer_tareas_suma(id):
	con = sqlite3.connect('./bd_bot.db')
	cur = con.cursor()
	cur.execute('''SELECT sum(premio_tarea) as 'total' FROM tareas WHERE id_usuario= ''' + id )
	data = cur.fetchall()
	cur.close()
	con.close()

	return data


# Insercción de una tarea

def insertar_tareas(user_id,nombre_tarea, prioridad_tarea, fecha_tarea,texto_tarea,estado_tarea,premio_tarea):
	data_base ='./bd_bot.db'
	con = sqlite3.connect(data_base)
	cur = con.cursor()
	cur.execute('INSERT INTO tareas (id_usuario,nombre_tarea,prioridad_tarea,fecha_tarea,comentario_tarea,estado_tarea,premio_tarea) VALUES (?, ?, ?, ?, ?, ?,?)', (user_id,nombre_tarea, prioridad_tarea, fecha_tarea,texto_tarea,estado_tarea,premio_tarea))
	con.commit()
	cur.close()
	con.close()

# Insercción de una tarea sin comentario

def insertar_tareas_nc(user_id,nombre_tarea, prioridad_tarea, fecha_tarea,estado_tarea,premio_tarea):
	data_base ='./bd_bot.db'
	con = sqlite3.connect(data_base)
	cur = con.cursor()
	cur.execute('INSERT INTO tareas (id_usuario,nombre_tarea,prioridad_tarea,fecha_tarea,estado_tarea,premio_tarea) VALUES (?, ?, ?, ?, ?, ?)', (user_id,nombre_tarea, prioridad_tarea, fecha_tarea,estado_tarea,premio_tarea))
	con.commit()
	cur.close()
	con.close()

# Actualizar campo de una tarea

def actualizar_campot(columna,valor,id):

	con = sqlite3.connect('./bd_bot.db')
	cur = con.cursor()
	query = '''UPDATE OR IGNORE tareas SET {} = ? WHERE id_tarea = ?'''.format(columna)
	cur.execute(query,(valor, id,))
	con.commit()
	cur.close()
	con.close()


# Eliminar tarea por id

def eliminar_tarea(data_base, table, id_column, record_id):
	con = sqlite3.connect(data_base)
	cur = con.cursor()
	query = 'DELETE FROM '+table+' WHERE '+id_column+" = '"+record_id+"'"
	cur.execute(query)
	con.commit()
	cur.close()
	con.close()


##################################### FUNCIONES RUTINAS ############################################


def contar_rutinas_pendientes(id):
	con = sqlite3.connect('./bd_bot.db')
	cur = con.cursor()
	cur.execute('''SELECT COUNT(*) FROM rutinas WHERE id_usuario= ''' + id)
	data = cur.fetchone()
	cur.close()
	con.close()

	return data

def contar_categorias_usuario(id):
	con = sqlite3.connect('./bd_bot.db')
	cur = con.cursor()
	cur.execute('''SELECT COUNT(*) FROM categoria WHERE id_usuario= ''' + id)
	data = cur.fetchone()
	cur.close()
	con.close()

	return data

def leer_categorias_rutina(id):
	con = sqlite3.connect('./bd_bot.db')
	cur = con.cursor()
	cur.execute('''SELECT * FROM categoria where id_usuario = 0 or id_usuario ='''+id)
	data = cur.fetchall()
	cur.close()
	con.close()

	return data

def leer_categorias_rutina_usuario(id):
	con = sqlite3.connect('./bd_bot.db')
	cur = con.cursor()
	cur.execute('''SELECT * FROM categoria where id_usuario ='''+id)
	data = cur.fetchall()
	cur.close()
	con.close()

	return data

def leer_categorias_rutina_usuario2(id):
	con = sqlite3.connect('./bd_bot.db')
	cur = con.cursor()
	cur.execute('''SELECT * FROM categoria where id_usuario=0  or id_usuario='''+id)
	data = cur.fetchall()
	cur.close()
	con.close()

	return data

def leer_rutinas(id):
	con = sqlite3.connect('./bd_bot.db')
	cur = con.cursor()
	cur.execute('''SELECT * FROM rutinas WHERE id_usuario= ''' + id)
	data = cur.fetchall()
	cur.close()
	con.close()
	return data

def leer_rutinas_t(id):
	con = sqlite3.connect('./bd_bot.db')
	cur = con.cursor()
	query = '''SELECT * FROM rutinas WHERE id_usuario = ? group by categoria_rutina'''
	cur.execute(query,(id,))
	data = cur.fetchall()
	cur.close()
	con.close()

	return data

def leerid_categoria(id):
	con = sqlite3.connect('./bd_bot.db')
	cur = con.cursor()
	cur.execute('''SELECT * FROM categoria WHERE id_categoria = ''' + id)
	data = cur.fetchall()
	cur.close()
	con.close()
	return data

def leerid_rutina(id):
	con = sqlite3.connect('./bd_bot.db')
	cur = con.cursor()

	cur.execute('''SELECT * FROM rutinas WHERE id_rutina= ''' + id)
	data = cur.fetchall()
	cur.close()
	con.close()
	return data


def insertar_rutina(id_usuario,nombre_rutina, categoria_rutina,repeticion_rutina,duracion_rutina,dias_rutina,premio_rutina):
	data_base ='./bd_bot.db'
	con = sqlite3.connect(data_base)
	cur = con.cursor()
	cur.execute('INSERT INTO rutinas (id_usuario,nombre_rutina, categoria_rutina,repeticion_rutina,duracion_rutina,dias_rutina,premio_rutina) VALUES (?,?,?,?,?,?,?)', (id_usuario,nombre_rutina, categoria_rutina,repeticion_rutina,duracion_rutina,dias_rutina,premio_rutina))
	con.commit()
	cur.close()
	con.close()


def insertar_categoria(id_usuario,nombre_categoria):
	data_base ='./bd_bot.db'
	con = sqlite3.connect(data_base)
	cur = con.cursor()
	cur.execute('INSERT INTO categoria (id_usuario,nombre_categoria) VALUES (?,?)', (id_usuario,nombre_categoria))
	con.commit()
	cur.close()
	con.close()

def actualizar_campoc(columna,valor,id):
	con = sqlite3.connect('./bd_bot.db')
	cur = con.cursor()
	query = '''UPDATE OR IGNORE categoria SET {} = ? WHERE id_categoria= ?'''.format(columna)
	cur.execute(query,(valor, id,))
	con.commit()
	cur.close()
	con.close()

def actualizar_campor(columna,valor,id):

		con = sqlite3.connect('./bd_bot.db')
		cur = con.cursor()
		query = '''UPDATE OR IGNORE rutinas SET {} = ? WHERE id_rutina= ?'''.format(columna)
		cur.execute(query,(valor, id,))
		con.commit()
		cur.close()
		con.close()


def eliminar_rutina(data_base, table, id_column, record_id):
	con = sqlite3.connect(data_base)
	#habilitar claves externas
	# con.execute("PRAGMA foreign_keys = ON")
	cur = con.cursor()
	query = 'DELETE FROM '+table+' WHERE '+id_column+" = '"+record_id+"'"
	cur.execute(query)
	con.commit()

	cur.close()
	con.close()


# if __name__ == '__main__':
