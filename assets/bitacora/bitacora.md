Bitácora: Trabajo de Titulación
===============================

> Alumno: __Andrés García García__

****

Datos del proyecto
------------------

> Título del proyecto: __Reconstrucción de la historia mutacional en tumores cancerosos__
> Asesor: __Maribel Hernandez Rosales__

### Objetivo general
  1. Generar una simulación del crecimiento de un tumor tomando en cuenta factores genéticos.
  2. Desarrollar un algoritmo que permita reconstruir la historia mutacional de un tumor dado su estado final.

### Objetivos particulares
 + Implementar un modelo de crecimiento tumoral basado en el trabajo de [Ferreira, et. al. ](https://doi.org/10.1103/PhysRevE.65.021907) en Python.
 + Modificar el modelo de [Ferreira, et. al.](https://doi.org/10.1103/PhysRevE.65.021907) para tomar en cuenta el material genético celular y mutaciones en él.
 + Utilizar las simulaciones para desarrollar un algoritmo que permita reconstruir la historia mutacional de un tumor dado su estado final.

### Seguimiento a futuro
 + Acelerar las simulaciones haciendo una implementación en lenguaje C/C++/Rust.
 + Acelerar aún más modificando la implementación existente utilizando herramientas de supercómputo (CUDA-C, openMPI, C++Threads)
 
 
 ---

 
### Parte I: Semestre _Agosto-Noviembre_ 2017
 
#### Actividades a realizar
 + __Actividad 1__: Implementar un modelo que tome en cuenta división celular, muerte y migración celular. Sin contar difusión y consumo de nutrientes.
 + __Actividad 2__: Añadir a las células un genoma y la posibilidad de mutar.
 + __Actividad 3__: Investigar las diversas medidas de distancia (diferencia) genómica para su uso en la reconstrucción.
 + __Actividad 4__: Explorar las alternativas para realizar la reconstrucción de la historia mutacional.
 + __Actividad 5__: Implementar de forma robusta el algoritmo seleccionado de reconstrucción.
 + __Actividad 6__: Añadir al modelo la difusión de nutrientes, y cómo las acciones de la célula dependen de estos.
 + __Actividad 7__: Comenzar los trabajos orientados a la extención del modelo a supercómputo.

#### Cronograma semanal

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

#### Registro de actividades


##### 10 de Agosto de 2017
Se comienza la implementación de la simulación en Python. Se utiliza [Processing.py](http://py.processing.org/) para su visualización.


##### 25 de Agosto de 2017
_Terminada actividad 1*_ (Implementar un modelo que tome en cuenta división celular, muerte y migración celular. Sin contar difusión y consumo de nutrientes.) 
___*Nota posterior:___ Véase la nota del 10 de septiembre de 2017

##### 7 de Septiembre de 2017
_Terminada actividad 2*_ (Añadir a las células un genoma y la posibilidad de mutar.) 
___*Nota posterior:___ Véase la nota del 10 de septiembre de 2017

##### 10 de Septiembre de 2017
Debido a un fallo de la computadora, el trabajo de los últimos días se perdió. El proyecto quedó en un estado anterior al 25 de Agosto, está implementada la división celular y una parte de migración celular. Se requiere reponer migración, muerte y mutación celular :( 

##### 12 de Septiembre de 2017
Se ha añadido el código fuente del proyecto a GitHub, el repositorio está en: https://github.com/Ad115/Cell-System. Todos los cambios desde este día se podrán encontrar en la [historia del proyecto](https://github.com/Ad115/Cell-System/commits/master).

Este cambio permitirá evitar que suceda lo del pasado 10 de septiembre, ya que si alguna parte del proyecto se pierde o es eliminada por error, se puede recuperar mediante este repositorio.

##### 17 de Septiembre de 2017
Terminada actividad:
 + __Actividad 1__: Implementar un modelo que tome en cuenta división celular, muerte y migración celular. Sin contar difusión y consumo de nutrientes.
 
 El registro de los cambios se encuentra en la [historia del proyecto](https://github.com/Ad115/Cell-System/commits/master).


##### 21 de Septiembre de 2017
Terminada actividad:
 + __Actividad 2__: Añadir a las células un genoma y la posibilidad de mutar.

 El registro de los cambios se encuentra en la [historia del proyecto](https://github.com/Ad115/Cell-System/commits/master).


##### 2 de Octubre de 2017
Añadido ejemplo de uso al README del repositorio.

Se limpió el código con PyLint para encontrar segmentos de código que podrían ocasionar algún problema en el futuro.

El registro de los cambios se encuentra en la [historia del proyecto](https://github.com/Ad115/Cell-System/commits/master).


##### 20 de Noviembre
Se limpió el código con _pydocstyle_ y _pycodestyle_ para ajustarlo a las convenciones en Python. Además, se trabajó en unificar la API y en limpiar y reestructurar lo que ya está escrito.
Se modificó el script de Processing para ajustar los nuevos cambios. Se puede consultar el [historial de cambios](https://github.com/Ad115/ICGC-data-parser/commits/python).


##### 21 de Noviembre
Se ha detectado la necesidad de añadir más de un tipo de células y de que el modelo no sólo sirva para cáncer, sino que pueda reutilizarse para otro tipo de simulaciones basadas en agentes, por lo que el código requiere una reestructuración general. Esta semana se trabajará en el nuevo diseño. También se puede consultar el [historial de cambios](https://github.com/Ad115/ICGC-data-parser/commits/python).


##### 22 de Noviembre
Se ha elegido basarse en el paradigma llamado [Clean Arquitecture](https://8thlight.com/blog/uncle-bob/2012/08/13/the-clean-architecture.html) de Bob Martin para estructurar el código. Este paradigma promueve la desacoplación de la lógica del modelo, es decir, el núcleo de la simulación, de los casos especificos de uso y de la interfaz externa. Esto permite una gran reusabilidad, y facilidad para modificar y realizar tests.

#### Fin de la parte I, discusión.
Se ha estructurado 
 

 
### Parte II: Semestre _Febrero-Junio_ 2017
 
#### Actividades a realizar
 + __Actividad 1__: Estudiar e implementar los algoritmos que se utilizan para la reconstrucción de árboles filogenéticos.
 + __Actividad 2__: Añadir al modelo la difusión de nutrientes, y cómo las acciones de la célula dependen de estos.
 + __Actividad 3__: Publicar el modelo de simulación en PyPI.
 + __Actividad 4__: Evaluar y realizar la transición del modelo de Python a C/C++/Rust
 + __Actividad 5__: Explorar las alternativas para realizar la reconstrucción de la historia mutacional.
 + __Actividad 6__: Implementar de forma robusta el algoritmo seleccionado de reconstrucción.
 + __Actividad 7__: Comenzar los trabajos orientados a la extención del modelo a supercómputo.

#### Cronograma semanal

El semestre tiene 16 semanas: desde la semana 1 (5 a 9 de Febrero) hasta la semana 16 (21 al 25 de Mayo). Las actividades se distribuirán de la siguiente manera:

| Actividad\Semana | Feb 5-9 | 12-16 | 19-23 | 26-Mar 2 | 5-9 | 12-16 | 19-23 | 26-30 | Abr 2-6 | 9-13 | 16-20 | 23-27 | 30-May 4 | 7-11 | 14-18 | 21-25 |
|------------------|---------|-------|-------|----------|-----|-------|-------|-------|---------|------|-------|-------|----------|------|-------|-------|
| A1               | x       | x     | x     | x        | x   | x     | x     | x     |         |      |       |       |          |      |       |       |
| A2               |         |       |       | x        | x   | x     | x     |       |         |      |       |       |          |      |       |       |
| A3               |         |       |       | x        | x   | x     | x     | x     |         |      |       |       |          |      |       |       |
| A4               | x       | x     | x     | x        | x   | x     | x     | x     | x       | x    | x     | x     | x        | x    | x     | x     |
| A5               |         |       |       |          |     |       |       | x     | x       | x    | x     | x     | x        | x    |       |       |
| A6               |         |       |       |          |     |       |       |       |         |      |       | x     | x        | x    | x     | x     |
| A7               |         |       |       |          |     |       |       |       |         |      |       |       | x        | x    | x     | x     |


*****

#### Registro de actividades


##### 10 de Agosto de 2017
Se comienza la implementación de la simulación en Python. Se utiliza [Processing.py](http://py.processing.org/) para su visualización.


##### 25 de Agosto de 2017
_Terminada actividad 1*_ (Implementar un modelo que tome en cuenta división celular, muerte y migración celular. Sin contar difusión y consumo de nutrientes.) 
___*Nota posterior:___ Véase la nota del 10 de septiembre de 2017

