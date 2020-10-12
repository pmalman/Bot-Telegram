# PlanningUGR

Trabajo de Fin de Grado

Grado Ingeniería Informática 2019-2020

Universidad de Granada

## Descripción

Con este proyecto se proporciona un Bot de Telegram para estudiantes y otras personas
interesadas en organizar el uso del tiempo en la realización de tareas a fin del mejor
aprovechamiento del mismo. Es un medio de interacción simple y fiable.

La aplicación evalúa su desarrollo y cumplimiento mediante recordatorios y refuerzos
definidos por ciertas reglas dependientes del objetivo elegido. Para permitir incorporar
técnicas de gamificación, esta aplicación también consta de un set de premios, los cuales
se otorgarán al usuario en caso de éxito, siguiendo ciertos criterios.

Permite que los usuarios puedan manejarlo con facilidad con un menú destinado a la
ayuda del usuario proporcionando una guía rápida para consultar cualquier aspecto del
mismo y una serie de consejos para que logren cumplir sus objetivos con la mayor efectividad.

Ofrece la posibilidad de visualizar el progreso de la productividad de sus tareas de manera
gráfica y también permite realizar búsquedas mediante una serie de filtros relativas a sus
tareas o rutinas.


## Instalación

Para su completo funcionamiento tenemos que instalar una serie de librerías
y herramientas que se describen a continuación:

* El lenguaje utilizado
   > Python 3.7
* Para instalar paquetes de Python, pip3
   > sudo apt update && sudo apt install python3-pip
* La librería de Telegram:
    > pip3 install python-telegram-bot
* Instalación de SQLite:
    > pip3 install db-sqlite3
* Instalación de la librería para el uso de gráficas:
  > pip3 install matplotlib
* Y por último ejecutar el bot mediante
  > python3 planningUGR.py
