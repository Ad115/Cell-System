Bitácora: Estancia de Investigación VII
===============================

24 de Noviembre de 2017
> Alumno: __Andrés García García__

****

Datos del proyecto
--------------------------

> Título del proyecto: __Reconstrucción de la historia mutacional en tumores cancerosos__
> Asesor: __Maribel Hernandez Rosales__

### Objetivo general
Generar una simulación del crecimiento de un tumor tomando en cuenta factores genéticos.

### Objetivos particulares
 + Implementar el modelo de crecimiento tumoral de [Ferreira, et. al. ](https://doi.org/10.1103/PhysRevE.65.021907) en Python.
 + Modificar el modelo de [Ferreira, et. al.](https://doi.org/10.1103/PhysRevE.65.021907) para tomar en cuenta el material genético celular y mutaciones en él.
 + Utilizar las simulaciones para desarrollar un algoritmo que permita reconstruir la historia mutacional de un tumor dado su estado final.

### Seguimiento a futuro
+ Acelerar las simulaciones haciendo una implementación en lenguaje C++.
+ Acelerar aún más modificando la implementación existente utilizando herramientas de supercómputo (CUDA-C, openMPI, C++Threads)

### Actividades a realizar
 + __Actividad 1__: Implementar un modelo que tome en cuenta división celular, muerte y migración celular. Sin contar difusión y consumo de nutrientes.
 +  __Actividad 2__: Añadir a las células un genoma y la posibilidad de mutar.
 + __Actividad 3__: Investigar las diversas medidas de distancia (diferencia) genómica para su uso en la reconstrucción.
 + __Actividad 4__: Explorar las alternativas para realizar la reconstrucción de la historia mutacional.
 + __Actividad 5__: Implementar de forma robusta el algoritmo seleccionado de reconstrucción.
 + __Actividad 6__: Añadir al modelo la difusión de nutrientes, y cómo las acciones de la célula dependen de estos.
 + __Actividad 7__: Comenzar los trabajos orientados a la extención del modelo a supercómputo.

### Cronograma semanal

El semestre tiene 16 semanas: desde la semana 1 (7 a 12 de Agosto) hasta la semana 16 (20 al 25 de Noviembre). Las actividades se distribuirán de la siguiente manera:

| Actividad\Semana | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
|------------------|---|---|---|---|---|---|---|---|---|----|----|----|----|----|----|----|
| A1               | x | x | x | x | x |   |   |   |   |    |    |    |    |    |    |    |
| A2               |   |   |   |   | x | x |   |   |   |    |    |    |    |    |    |    |
| A3               |   |   |   |   |   | x | x | x |   |    |    |    |    |    |    |    |
| A4               |   |   |   |   |   |   |   | x | x | x  | x  |    |    |    |    |    |
| A5               |   |   |   |   |   |   |   |   |   |    | x  | x  | x  |    |    |    |
| A6               |   |   |   |   |   |   |   |   |   |    |    |    | x  | x  | x  |    |
| A7               |   |   |   |   |   |   |   |   |   |    |    |    |    |    | x  | x  |

*****

Registro de actividades
---------------------------------

### 10 de Agosto de 2017
Se comienza la implementación de la simulación en Python. Se utiliza [Processing.py](http://py.processing.org/) para su visualización.


### 25 de Agosto de 2017
_Terminada actividad 1*_ (Implementar un modelo que tome en cuenta división celular, muerte y migración celular. Sin contar difusión y consumo de nutrientes.) 
___*Nota posterior:___ Véase la nota del 10 de septiembre de 2017

### 7 de Septiembre de 2017
_Terminada actividad 2*_ (Añadir a las células un genoma y la posibilidad de mutar.) 
___*Nota posterior:___ Véase la nota del 10 de septiembre de 2017

### 10 de Septiembre de 2017
Debido a un fallo de la computadora, el trabajo de los últimos días se perdió. El proyecto quedó en un estado anterior al 25 de Agosto, está implementada la división celular y una parte de migración celular. Se requiere reponer migración, muerte y mutación celular :( 

### 12 de Septiembre de 2017
Se ha añadido el código fuente del proyecto a GitHub, el repositorio está en: https://github.com/Ad115/Cell-System. Todos los cambios desde este día se podrán encontrar en la [historia del proyecto](https://github.com/Ad115/Cell-System/commits/master).

Este cambio permitirá evitar que suceda lo del pasado 10 de septiembre, ya que si alguna parte del proyecto se pierde o es eliminada por error, se puede recuperar mediante este repositorio.

### 17 de Septiembre de 2017
Terminada actividad:
 + __Actividad 1__: Implementar un modelo que tome en cuenta división celular, muerte y migración celular. Sin contar difusión y consumo de nutrientes.
 
 El registro de los cambios se encuentra en la [historia del proyecto](https://github.com/Ad115/Cell-System/commits/master).


### 21 de Septiembre de 2017
Terminada actividad:
 + __Actividad 2__: Añadir a las células un genoma y la posibilidad de mutar.

 El registro de los cambios se encuentra en la [historia del proyecto](https://github.com/Ad115/Cell-System/commits/master).

### 2 de Octubre de 2017
Añadido ejemplo de uso al README del repositorio.

Se limpió el código con PyLint para encontrar segmentos de código que podrían ocasionar algún problema en el futuro.

El registro de los cambios se encuentra en la [historia del proyecto](https://github.com/Ad115/Cell-System/commits/master).

---

> __Nota__: Este proyecto es parte de un proyecto más grande registrado en CONACYT como: "__DNA-mutation simulation of tumor growth and reconstruction of cancer evolution__". Este proyecto está registrado por mi tutora Maribel Hernández Rosales del Instituto de Matemáticas en la modalidad de Joven Investigador. Otra parte importante de este proyecto es el análisis de datos ya existentes sobre cáncer y yo me encuentro involucrado en esa parte también. El producto (hasta ahora) de esa parte se encuentra en la página web del [ICGC Data Parser](icgc-data-parser.readthedocs.io) y el código para ello está en [el repositorio de GitHub](github.com/Ad115/ICGC-data-parser).

> Durante el mes de Octubre y principios de Noviembre se requirió atención a la parte del análisis de datos. Por lo que se muestra a continuación es trabajo realizado en ese momento. También se puede consultar el [historial de cambios](https://github.com/Ad115/ICGC-data-parser/commits/python).

### 11 de Octubre de 2017
Se limpió la documentación en la página web.
Se reestructuró el repositorio y se limpió el código como medida de mantenimiento.
Las medidas anteriores permitieron una mayor usabilidad, ya que es más fácil ahora para el usuario y para el programador saber dónde se encuentran las cosas.

### 17 de Octubre de 2017
Se continuaron los cambios anteriores (limpieza y reestructuración del repositorio y de la documentación).
Se detectó la necesidad de utilizar un manejador de base de datos para hacer los procesos más eficientes, así que también ha comenzado el proceso de planeación para implementarlo.

### 3 de Noviembre de 2017
Continúa el proceso de planeación de la base de datos. Además, debido al creciente desuso del lenguaje Perl y a la flexibilidad y manejabilidad de Python en cuanto a procesamiento general de texto, librerías de uso general y de manejo de bases de datos, se ha decidido implementar en Python la parte de base de datos del módulo. Lo cual, si funciona como se espera, dejaría obsoleta la mayor parte del código en Perl que se tiene hasta ahora y convertiría el proyecto en un proyecto de Python.

### 5 de Noviembre de 2017
Se han provado los primeros prototipos con Python, SQLite y PonyORM para el manejo de la base de datos y parecen prometedores con una pequeña cantidad de datos. Por ello, se ha iniciado la carga de todos los datos (~50Gb) a la base de datos, lo cual se estima, tendrá una duración de 10hrs.

### 13 de Noviembre de 2017
Debido a problemas con la carga, la base de datos apenas ha terminado de colocarse adecuadamente. Por lo que ya está lista para usarse y las primeras pruebas funcionaron bien.

### 15 de Noviembre
Se detectaron problemas, la base de datos resultó ser mucho más grande de lo que se esperaba, y pruebas adicionales detectaron problemas con datos repetidos. Esto aunado a la lenta carga de la base de datos hace que requiera una revisión. Se trabajará en el nuevo diseño en paralelo a un colaborador para detectar el modo más eficiente de hacer los cambios mientras se continúa trabajando en el proyecto de simulación.

### 20 de Noviembre
Se limpió el código con _pydocstyle_ y _pycodestyle_ para ajustarlo a las convenciones en Python. Además, se trabajó en unificar la API y en limpiar y reestructurar lo que ya está escrito.
Se modificó el script de Processing para ajustar los nuevos cambios.

### 21 de Noviembre
Se ha detectado la necesidad de añadir más de un tipo de células y de que el modelo no sólo sirva para cáncer, sino que pueda reutilizarse para otro tipo de simulaciones basadas en agentes, por lo que el código requiere una reestructuración general. Esta semana se trabajará en el nuevo diseño.

### 22 de Noviembre
Se ha elegido basarse en el paradigma llamado [Clean Arquitecture](https://8thlight.com/blog/uncle-bob/2012/08/13/the-clean-architecture.html) de Bob Martin para estructurar el código. Este paradigma promueve la desacoplació del modelo en sí, el núcleo, de los casos de uso y de la interfaz externa. Esto permite una gran reusabilidad, facilidad de modificación y para realizar tests.

> Written with [StackEdit](https://stackedit.io/).
