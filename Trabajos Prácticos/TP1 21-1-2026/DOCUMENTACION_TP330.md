# DOCUMENTACIÓN DEL PROGRAMA TP330
## Trabajo Práctico — Procesamiento de Datos (Cód. 330) — Lapso 2026-1 — Objetivo 5

**Estudiante:** José Vásquez — C.I. V-14.645.240
**Carrera:** Ingeniería de Sistemas (236)

---

# 1. DISEÑO DE LA ORGANIZACIÓN DE ARCHIVOS

## 1.1. Organización utilizada: SECUENCIAL

Ambos archivos se diseñan con **organización secuencial** (`ORGANIZATION IS
SEQUENTIAL`), lo que significa que los registros se graban **uno tras otro, en
el orden en que se capturan**, y para leer el último registro es necesario
pasar por todos los anteriores. Cada registro ocupa un **ancho fijo** (35 y 43
caracteres respectivamente). Cada archivo se crea **desde cero** con la
instrucción `OPEN OUTPUT` (si el archivo ya existía, su contenido se borra, lo
cual es correcto porque se trata de una operación de *creación*).

> **Nota sobre `LINE SEQUENTIAL`:** esta variante escribiría los archivos
> como líneas de texto legible, pero **elimina los espacios al final de cada
> registro**, por lo que los campos de ancho fijo (como Ciudad, de 15
> posiciones) perderían su tamaño real. Como el TP especifica anchos fijos,
> se emplea `SEQUENTIAL`.

## 1.2. Archivo Maestro de Productos (MAESTRO-PROD.DAT)

Contiene la información fija de los productos.

| Nombre del campo    | Clase        | PIC       | Tamaño | Descripción                                       |
|---------------------|--------------|-----------|:------:|---------------------------------------------------|
| RP-ID-PRODUCTO      | Numérico     | 9(05)     | 5      | Código de identificación del producto (5 dígitos) |
| RP-NOMBRE-PRODUCTO  | Alfanumérico | X(20)     | 20     | Nombre o descripción del producto                 |
| RP-STOCK-ACTUAL     | Numérico     | 9(04)     | 4      | Existencias actuales del producto                 |
| RP-PRECIO-UNITARIO  | Numérico     | 9(04)V99  | 6      | Precio: 6 dígitos con 2 decimales (9999.99)       |

**Longitud del registro: 35 caracteres.**
*Nota:* la `V` de la cláusula `9(04)V99` representa el punto decimal
**implícito**: no ocupa espacio de almacenamiento, solo indica al compilador
dónde se asume la coma decimal. Por eso `9(04)V99` = 6 dígitos con 2 decimales.

## 1.3. Archivo de Proveedores (PROVEEDORES.DAT)

Contiene los datos de contacto de los proveedores.

| Nombre del campo   | Clase        | PIC   | Tamaño | Descripción                                   |
|--------------------|--------------|-------|:------:|-----------------------------------------------|
| RP-ID-PROVEEDOR    | Numérico     | 9(03) | 3      | Código de identificación del proveedor        |
| RP-NOMBRE-EMPRESA  | Alfanumérico | X(25) | 25     | Razón social de la empresa proveedora         |
| RP-CIUDAD-PROV     | Alfanumérico | X(15) | 15     | Ciudad donde se ubica el proveedor            |

**Longitud del registro: 43 caracteres.**

---

# 2. ELEMENTOS DEL CÓDIGO FUENTE COBOL

Todo programa COBOL se estructura en **cuatro DIVISIONES**, en orden fijo. A
continuación se describe cada elemento utilizado en el programa TP330.

## 2.1. IDENTIFICATION DIVISION

Identifica al programa. No contiene lógica; es información administrativa.

* **PROGRAM-ID.** Nombre del programa: `TP330`.
* Autor (José Vásquez, C.I. V-14.645.240) y lapso (2026-1): documentados en
  el bloque de comentarios del encabezado. Los párrafos `AUTHOR.` y
  `DATE-WRITTEN.` se consideran **obsoletos** en GnuCOBOL/OpenCOBOL y generan
  advertencias de compilación, por ello la identificación se documenta como
  comentario.
* **Comentarios.** Las líneas con `*` en la columna 7 son comentarios de
  documentación; el compilador las ignora. En este programa documentan el
  objetivo y la descripción general del sistema.

## 2.2. ENVIRONMENT DIVISION

Relaciona al programa con el ambiente físico del computador: en este caso,
con los **archivos** que utilizará.

* **INPUT-OUTPUT SECTION.** Sección que agrupa las definiciones de entrada/salida.
* **FILE-CONTROL.** Definición y asignación de archivos al programa.
* **SELECT ... ASSIGN TO "..."**. Vincula un nombre interno (el que usará el
  programa, p. ej. `MAESTRO-PROD`) con el archivo físico en disco
  (`"MAESTRO-PROD.DAT"`).
* **ORGANIZATION IS SEQUENTIAL.** Declara la organización **secuencial**:
  los registros se graban uno tras otro, en **registros de ancho fijo**
  (35 caracteres en MAESTRO-PROD.DAT y 43 en PROVEEDORES.DAT), sin
  separador entre ellos.
  *Nota de implementación:* se usa `SEQUENTIAL` y no `LINE SEQUENTIAL`
  porque esta última **recorta los espacios finales** de cada registro, lo
  que destruye el ancho fijo exigido por las especificaciones (por ejemplo,
  el campo Ciudad de 15 posiciones se grabaría con menos caracteres).
  Para leer el archivo por bloques de ancho fijo se puede usar el Bloc de
  notas en "Ancho de columna" o un editor que muestre los bytes.
* **FILE STATUS IS ...**. Asigna una variable de 2 caracteres que el sistema
  llena automáticamente tras cada operación de E/S para indicar el resultado:
  `"00"` = operación exitosa; cualquier otro valor = error. Permite verificar
  y controlar fallos de apertura o grabación.

## 2.3. DATA DIVISION

Define **todas las estructuras de datos** del programa.

### FILE SECTION

Define la estructura del **registro** de cada archivo.

* **FD (File Description).** Descripción del archivo; hay una por cada SELECT.
* **Nivel 01.** Nombre del registro (`REG-PRODUCTO`, `REG-PROVEEDOR`).
* **Nivel 05.** Campos (ítems elementales) que componen el registro.
* La FILE SECTION es el área desde la cual `WRITE` graba físicamente el
  registro en el archivo.

### WORKING-STORAGE SECTION

Define las **variables de trabajo** en memoria (área de trabajo del programa):

* Variables de control: opción del menú (`WS-OPCION-MENU`), respuesta del
  ciclo S/N (`WS-CONTINUA`) y estados de archivo (`WS-FS-PROD`, `WS-FS-PROV`).
* Estructuras espejo (`WS-REG-PRODUCTO`, `WS-REG-PROVEEDOR`) donde el usuario
  captura los datos por teclado **antes** de transferirlos a la FILE SECTION.

### Niveles y cláusulas PIC

| Elemento   | Significado                                                        |
|------------|--------------------------------------------------------------------|
| `FD`       | Descripción de archivo (una por archivo físico)                    |
| `01`       | Nivel de registro o variable independiente (ítem elemental o grupo)|
| `05`       | Nivel de campo elemento dentro de un registro (ítem elemental)     |
| `PIC 9(n)` | Campo **numérico** de n dígitos (0-9)                              |
| `PIC X(n)` | Campo **alfanumérico** de n caracteres (letras, dígitos, símbolos) |
| `PIC V`    | Punto decimal **implícito** (indica dónde va la coma; no ocupa byte)|

## 2.4. PROCEDURE DIVISION

Contiene la **lógica del programa**, organizada en **párrafos (párrafos o
secciones) numerados** que se ejecutan de manera **ordenada y secuencial**
mediante verbos COBOL:

| Verbo COBOL              | Acción que realiza                                             |
|--------------------------|----------------------------------------------------------------|
| `PERFORM ... UNTIL`      | Ejecuta un párrafo **en forma repetida** hasta que se cumpla una condición (ciclo). |
| `PERFORM n TIMES`        | Repite un bloque de instrucciones **n veces** (usado en la limpieza de pantalla: 25 líneas en blanco). |
| `EVALUATE ... WHEN ...`  | Selección múltiple: ejecuta acciones según el valor de la opción (el MENÚ). |
| `OPEN OUTPUT archivo`    | Crea el archivo **desde cero** y lo deja listo para grabar (borra datos anteriores). |
| `CLOSE archivo`          | Cierra el archivo y lo libera (garantiza que los datos queden grabados). |
| `ACCEPT variable`        | Lee un dato desde el **teclado** hacia una variable.           |
| `DISPLAY ...`            | Muestra mensajes en **pantalla** (la consola). `WITH NO ADVANCING` deja el cursor en la misma línea, para leer el dato junto al mensaje. |
| `MOVE origen TO destino` | Transfiere datos de una variable a otra.                       |
| `WRITE registro`         | Graba el registro (contenido de la FILE SECTION) en el archivo, **al final** del mismo (escritura secuencial). |
| `IF / END-IF`            | Toma de decisiones: en este programa valida el FILE STATUS.    |
| `EXIT PARAGRAPH`         | Abandona el párrafo actual (salida por error de apertura).     |
| `STOP RUN`               | Finaliza la ejecución del programa.                            |

---

# 3. DICCIONARIO DE DATOS (DESCRIPCIÓN DE LAS VARIABLES)

## 3.1. Variables de la FILE SECTION (registros de archivo)

| Nivel | Nombre de la variable | PIC  | Tamaño | Descripción de la variable                |
|:-----:|-----------------------|------|:------:|-------------------------------------------|
| FD  | MAESTRO-PROD          | —    | —    | Descripción física del archivo de productos |
| 01  | REG-PRODUCTO          | —    | 35   | Registro del archivo maestro de productos |
| 05  | RP-ID-PRODUCTO        | 9(05)| 5    | Código del producto (numérico)            |
| 05  | RP-NOMBRE-PRODUCTO    | X(20)| 20   | Nombre del producto (alfanumérico)        |
| 05  | RP-STOCK-ACTUAL       | 9(04)| 4    | Stock o existencias actuales (numérico)   |
| 05  | RP-PRECIO-UNITARIO    | 9(04)V99 | 6 | Precio unitario: 6 dígitos, 2 decimales  |
| FD  | PROVEEDORES           | —    | —    | Descripción física del archivo de proveedores |
| 01  | REG-PROVEEDOR         | —    | 43   | Registro del archivo de proveedores       |
| 05  | RP-ID-PROVEEDOR       | 9(03)| 3    | Código del proveedor (numérico)           |
| 05  | RP-NOMBRE-EMPRESA     | X(25)| 25   | Nombre de la empresa proveedora           |
| 05  | RP-CIUDAD-PROV        | X(15)| 15   | Ciudad del proveedor                      |

## 3.2. Variables de la WORKING-STORAGE SECTION (área de trabajo)

| Nivel | Nombre de la variable | PIC  | Descripción de la variable                                    |
|:-----:|-----------------------|------|---------------------------------------------------------------|
| 01 | WS-OPCION-MENU        | X(01) | Guarda la opción del menú elegida por el usuario (1, 2 o 3)   |
| 01 | WS-CONTINUA           | X(01) | Respuesta del ciclo "¿Desea agregar otro registro? (S/N)"     |
| 01 | WS-PAUSA              | X(01) | Variable muda para la pausa "PRESIONE ENTER..." del menú      |
| 01 | WS-FS-PROD            | X(02) | FILE STATUS del MAESTRO-PROD ("00" = éxito)                   |
| 01 | WS-FS-PROV            | X(02) | FILE STATUS del archivo PROVEEDORES ("00" = éxito)            |
| 01 | WS-REG-PRODUCTO       | grupo | Estructura de captura de un producto (espejo del registro)    |
| 05 | WS-ID-PRODUCTO        | 9(05) | Captura del código del producto                                |
| 05 | WS-NOMBRE-PRODUCTO    | X(20) | Captura del nombre del producto                                |
| 05 | WS-STOCK-ACTUAL       | 9(04) | Captura del stock actual                                       |
| 05 | WS-PRECIO-UNITARIO    | 9(04)V99 | Captura del precio unitario                                 |
| 01 | WS-REG-PROVEEDOR      | grupo | Estructura de captura de un proveedor (espejo del registro)   |
| 05 | WS-ID-PROVEEDOR       | 9(03) | Captura del código del proveedor                               |
| 05 | WS-NOMBRE-EMPRESA     | X(25) | Captura del nombre de la empresa                               |
| 05 | WS-CIUDAD-PROV        | X(15) | Captura de la ciudad                                           |

**Prefijos utilizados (convención):** `WS-` = variable de WORKING-STORAGE;
`RP-` = campo del registro (FILE SECTION); `FS` = FILE STATUS.

---

# 4. PSEUDOCÓDIGO Y ANÁLISIS DE CADA FUNCIÓN DEL SISTEMA

El programa se organiza en párrafos con responsabilidades únicas. A
continuación se describe la acción de cada uno, junto con su pseudocódigo.

## 4.1. Párrafo 000-PRINCIPAL (módulo raíz)

**Acción:** es el punto de arranque y el esqueleto general del programa.
Inicializa la opción del menú y repite el menú principal **hasta que el
usuario elija salir (opción 3)**. Su ciclo garantiza que el sistema funcione
de manera ordenada y repetitiva.

```
INICIO-PRINCIPAL
    Mover espacio a WS-OPCION-MENU
    MIENTRAS WS-OPCION-MENU <> "3" HACER
        EJECUTAR 100-MENU-PRINCIPAL
    FIN-MIENTRAS
    ESCRIBIR "FIN DEL PROGRAMA. GRACIAS POR USAR EL SISTEMA."
    DETENER EJECUCION
FIN
```

### 4.1b. Párrafos de apoyo a la navegación del menú (050 y 060)

Estos dos párrafos mejoran la **experiencia de uso del menú**:

* **050-LIMPIAR-PANTALLA:** cada vez que el sistema va a mostrar el menú,
  limpia la consola desplegando 25 líneas en blanco (`PERFORM 25 TIMES`),
  de modo que las capturas y mensajes anteriores no se acumulen en pantalla
  y el menú siempre aparezca despejado.

```
INICIO-LIMPIAR-PANTALLA
    REPETIR 25 VECES
        ESCRIBIR línea en blanco
    FIN-REPETIR
FIN
```

* **060-PAUSA-SISTEMA:** después de cada operación (crear productos, crear
  proveedores u opción inválida), detiene el flujo con el mensaje
  *"PRESIONE ENTER PARA VOLVER AL MENU PRINCIPAL..."* y espera una entrada
  del usuario (`ACCEPT WS-PAUSA`). Así el usuario puede leer los resultados
  antes de que el menú reaparezca.

```
INICIO-PAUSA-SISTEMA
    ESCRIBIR "PRESIONE ENTER PARA VOLVER AL MENU PRINCIPAL..."
    LEER WS-PAUSA                     // espera un ENTER del usuario
FIN
```

## 4.2. Párrafo 100-MENU-PRINCIPAL (menú de opciones)

**Acción:** **limpia la pantalla**, despliega el menú del sistema, **lee la
opción elegida por teclado** y dirige el proceso hacia la rutina
correspondiente usando una estructura de selección (EVALUATE), terminando
cada operación con una **pausa** para que el usuario lea los mensajes antes
de regresar al menú. Si la opción no es válida, muestra un mensaje de error.
Cumple el requerimiento del TP de mostrar un menú con las opciones:
**1) Crear Archivo de Productos, 2) Crear Archivo de Proveedores, 3) Salir**.

```
INICIO-MENU
    EJECUTAR 050-LIMPIAR-PANTALLA                // navegación limpia
    ESCRIBIR menú (1-Crear Productos, 2-Crear Proveedores, 3-Salir)
    LEER WS-OPCION-MENU
    SEGUN WS-OPCION-MENU HACER
        CASO "1": EJECUTAR 200-CREAR-PRODUCTOS
                  EJECUTAR 060-PAUSA-SISTEMA
        CASO "2": EJECUTAR 300-CREAR-PROVEEDORES
                  EJECUTAR 060-PAUSA-SISTEMA
        CASO "3": ESCRIBIR "SALIENDO DEL SISTEMA..."
        EN OTRO CASO: ESCRIBIR "OPCION INVALIDA. ELIJA 1, 2 O 3."
                      EJECUTAR 060-PAUSA-SISTEMA
    FIN-SEGUN
FIN
```

## 4.3. Párrafo 200-CREAR-PRODUCTOS (creación del archivo de productos)

**Acción:** **crea el archivo MAESTRO-PROD.DAT desde cero** mediante
`OPEN OUTPUT` (borra datos anteriores, lo cual es correcto en una creación).
Verifica el FILE STATUS (validación de apertura); si hay error, avisa y
abandona la rutina. Luego ejecuta el **ciclo de entrada**: captura un
registro, lo graba y pregunta *"¿Desea agregar otro registro? (S/N)"*;
repite mientras la respuesta sea "S". Al final **cierra el archivo** con
`CLOSE`, garantizando la grabación física de los registros en secuencia.

```
INICIO-CREAR-PRODUCTOS
    ABRIR MAESTRO-PROD COMO SALIDA (crear desde cero)      // OPEN OUTPUT
    SI WS-FS-PROD <> "00" ENTONCES                         // validación de apertura
        ESCRIBIR "ERROR AL CREAR MAESTRO-PROD.DAT STATUS=" WS-FS-PROD
        SALIR DEL PARRAFO
    FIN-SI
    Mover "S" a WS-CONTINUA
    MIENTRAS WS-CONTINUA = "S" o "s" HACER                 // ciclo de entrada
        EJECUTAR 210-LEER-DATOS-PRODUCTO                   // captura
        EJECUTAR 220-ESCRIBIR-PRODUCTO                     // grabación
        EJECUTAR 400-PREGUNTAR-CONTINUA                    // ¿S/N?
    FIN-MIENTRAS
    CERRAR MAESTRO-PROD                                    // CLOSE
    ESCRIBIR "ARCHIVO MAESTRO-PROD.DAT CREADO EXITOSAMENTE."
FIN
```

## 4.4. Párrafo 210-LEER-DATOS-PRODUCTO (captura por teclado)

**Acción:** solicita al usuario, uno por uno, los campos del producto
(ID, nombre, stock y precio) y los almacena en la estructura de
**WORKING-STORAGE** (`WS-REG-PRODUCTO`), es decir, todavía **no** en el
archivo. Para el precio se instruye ingresar 6 dígitos sin punto decimal
(los últimos 2 son decimales), acorde a la PIC 9(04)V99.

```
INICIO-LEER-DATOS-PRODUCTO
    ESCRIBIR "NUEVO REGISTRO DE PRODUCTO"
    ESCRIBIR y LEER WS-ID-PRODUCTO        (5 dígitos)
    ESCRIBIR y LEER WS-NOMBRE-PRODUCTO    (20 caracteres)
    ESCRIBIR y LEER WS-STOCK-ACTUAL       (4 dígitos)
    ESCRIBIR nota de formato del precio (6 dígitos, 2 últimos decimales)
    ESCRIBIR y LEER WS-PRECIO-UNITARIO
FIN
```

## 4.5. Párrafo 220-ESCRIBIR-PRODUCTO (grabación del registro)

**Acción:** **transfiere** con `MOVE` cada dato desde las variables de
**WORKING-STORAGE hacia la FILE SECTION** (`REG-PRODUCTO`) y luego graba el
registro en el archivo con `WRITE` (escritura secuencial: el registro queda
al final del archivo). Verifica el FILE STATUS para confirmar la grabación.
Este párrafo cumple literalmente el requerimiento 4 del TP.

```
INICIO-ESCRIBIR-PRODUCTO
    MOVER WS-ID-PRODUCTO     A RP-ID-PRODUCTO
    MOVER WS-NOMBRE-PRODUCTO A RP-NOMBRE-PRODUCTO
    MOVER WS-STOCK-ACTUAL    A RP-STOCK-ACTUAL
    MOVER WS-PRECIO-UNITARIO A RP-PRECIO-UNITARIO
    GRABAR REG-PRODUCTO                                 // WRITE
    SI WS-FS-PROD <> "00" ENTONCES
        ESCRIBIR "ERROR AL GRABAR REGISTRO STATUS=" WS-FS-PROD
    SI-NO
        ESCRIBIR "REGISTRO GRABADO CORRECTAMENTE."
    FIN-SI
FIN
```

## 4.6. Párrafo 300-CREAR-PROVEEDORES (creación del archivo de proveedores)

**Acción:** idéntica a la de 200-CREAR-PRODUCTOS, pero sobre el archivo
**PROVEEDORES.DAT**: lo crea desde cero con `OPEN OUTPUT`, valida la
apertura, ejecuta el ciclo de entrada (captura → grabación → S/N) y cierra
el archivo con `CLOSE`.

```
INICIO-CREAR-PROVEEDORES
    ABRIR PROVEEDORES COMO SALIDA (crear desde cero)       // OPEN OUTPUT
    SI WS-FS-PROV <> "00" ENTONCES
        ESCRIBIR "ERROR AL CREAR PROVEEDORES.DAT STATUS=" WS-FS-PROV
        SALIR DEL PARRAFO
    FIN-SI
    Mover "S" a WS-CONTINUA
    MIENTRAS WS-CONTINUA = "S" o "s" HACER
        EJECUTAR 310-LEER-DATOS-PROVEEDOR
        EJECUTAR 320-ESCRIBIR-PROVEEDOR
        EJECUTAR 400-PREGUNTAR-CONTINUA
    FIN-MIENTRAS
    CERRAR PROVEEDORES
    ESCRIBIR "ARCHIVO PROVEEDORES.DAT CREADO EXITOSAMENTE."
FIN
```

## 4.7. Párrafo 310-LEER-DATOS-PROVEEDOR (captura por teclado)

**Acción:** solicita al usuario los campos del proveedor (ID, nombre de la
empresa y ciudad) y los guarda en la estructura `WS-REG-PROVEEDOR` de
WORKING-STORAGE.

```
INICIO-LEER-DATOS-PROVEEDOR
    ESCRIBIR "NUEVO REGISTRO DE PROVEEDOR"
    ESCRIBIR y LEER WS-ID-PROVEEDOR     (3 dígitos)
    ESCRIBIR y LEER WS-NOMBRE-EMPRESA   (25 caracteres)
    ESCRIBIR y LEER WS-CIUDAD-PROV      (15 caracteres)
FIN
```

## 4.8. Párrafo 320-ESCRIBIR-PROVEEDOR (grabación del registro)

**Acción:** transfiere con `MOVE` los datos desde WORKING-STORAGE hacia la
FILE SECTION (`REG-PROVEEDOR`) y graba el registro en PROVEEDORES.DAT con
`WRITE`, verificando el FILE STATUS.

```
INICIO-ESCRIBIR-PROVEEDOR
    MOVER WS-ID-PROVEEDOR    A RP-ID-PROVEEDOR
    MOVER WS-NOMBRE-EMPRESA  A RP-NOMBRE-EMPRESA
    MOVER WS-CIUDAD-PROV     A RP-CIUDAD-PROV
    GRABAR REG-PROVEEDOR                                // WRITE
    SI WS-FS-PROV <> "00" ENTONCES
        ESCRIBIR "ERROR AL GRABAR REGISTRO STATUS=" WS-FS-PROV
    SI-NO
        ESCRIBIR "REGISTRO GRABADO CORRECTAMENTE."
    FIN-SI
FIN
```

## 4.9. Párrafo 400-PREGUNTAR-CONTINUA (control del ciclo de entrada)

**Acción:** implementa el control del **ciclo de entrada** requerido por el
TP: pregunta *"¿Desea agregar otro registro? (S/N)"* y valida que la
respuesta sea únicamente **S** o **N** (mayúscula o minúscula); cualquier
otra tecla hace volver a preguntar. Su resultado permite a los párrafos
200 y 300 repetir o terminar la grabación de registros.

```
INICIO-PREGUNTAR-CONTINUA
    Mover espacio a WS-CONTINUA
    MIENTRAS WS-CONTINUA NO SEA "S", "s", "N" ni "n" HACER
        ESCRIBIR "DESEA AGREGAR OTRO REGISTRO? (S/N): "
        LEER WS-CONTINUA
    FIN-MIENTRAS
FIN
```

## 4.10. Pseudocódigo general del sistema (vista completa)

```
INICIO PROGRAMA TP330
    opcion <- ' '
    MIENTRAS opcion <> "3" HACER
        LIMPIAR PANTALLA
        MOSTRAR MENU (1. Crear Productos / 2. Crear Proveedores / 3. Salir)
        LEER opcion
        SEGUN opcion HACER
            CASO "1":
                ABRIR MAESTRO-PROD como SALIDA      // crea desde cero
                SI apertura exitosa ENTONCES
                    continua <- "S"
                    MIENTRAS continua = "S" HACER
                        CAPTURAR datos del producto en WORKING-STORAGE
                        MOVER datos a la FILE SECTION
                        GRABAR registro con WRITE secuencial
                        PEDIR "¿Desea agregar otro registro? (S/N)"
                    FIN-MIENTRAS
                    CERRAR MAESTRO-PROD
                FIN-SI
                PAUSA (PRESIONE ENTER PARA VOLVER AL MENU)
            CASO "2":
                ABRIR PROVEEDORES como SALIDA
                SI apertura exitosa ENTONCES
                    continua <- "S"
                    MIENTRAS continua = "S" HACER
                        CAPTURAR datos del proveedor en WORKING-STORAGE
                        MOVER datos a la FILE SECTION
                        GRABAR registro con WRITE secuencial
                        PEDIR "¿Desea agregar otro registro? (S/N)"
                    FIN-MIENTRAS
                    CERRAR PROVEEDORES
                FIN-SI
                PAUSA (PRESIONE ENTER PARA VOLVER AL MENU)
            CASO "3": MOSTRAR "SALIENDO DEL SISTEMA..."
            EN OTRO CASO: MOSTRAR "OPCION INVALIDA"
                          PAUSA (PRESIONE ENTER PARA VOLVER AL MENU)
        FIN-SEGUN
    FIN-MIENTRAS
    MOSTRAR "FIN DEL PROGRAMA"
FIN
```

## 4.11. Tabla de correspondencia requerimiento del TP ↔ solución

| Requerimiento del TP                                  | Dónde se cumple en el programa                     |
|-------------------------------------------------------|-----------------------------------------------------|
| Menú principal con las 3 opciones                     | Párrafo 100-MENU-PRINCIPAL (EVALUATE)               |
| Organización secuencial con ancho fijo                 | `ORGANIZATION IS SEQUENTIAL` + FD de ancho fijo     |
| Crear el archivo desde cero con OPEN OUTPUT           | Párrafos 200 y 300 (`OPEN OUTPUT`)                  |
| Validación de la apertura                             | `IF WS-FS = "00"` tras el OPEN                      |
| Ciclo "¿Desea agregar otro registro? (S/N)"           | Párrafo 400-PREGUNTAR-CONTINUA + PERFORM UNTIL      |
| Transferencia WORKING-STORAGE → FILE SECTION          | Párrafos 220 y 320 (instrucciones MOVE)             |
| Grabación con WRITE (organización secuencial)         | Párrafos 220 y 320 (`WRITE`)                        |
| Trabajo ordenado y secuencial                         | Estructura por párrafos numerados + PERFORM UNTIL   |
| Listado documentado (comentarios por proceso)         | Bloques `*----*` al inicio de cada párrafo          |

---

# 5. CÓMO COMPILAR Y EJECUTAR EL PROGRAMA (GNUCOBOL / OPENCOBOL)

1. Instalar GnuCOBOL (sucesor de OpenCOBOL):
   `choco install gnucobol`  (Windows, con Chocolatey)
2. Abrir una terminal en la carpeta del código y compilar:
   ```
   cobc -x TP330.cob
   ```
   (`-x` genera un ejecutable; el formato fijo de columnas es el formato por
   defecto del compilador, por eso no hace falta ninguna opción adicional).
3. Ejecutar:
   ```
   .\TP330.exe
   ```
4. Verificar el resultado: tras usar las opciones 1 y 2 del menú se crean, en
   la misma carpeta, los archivos **MAESTRO-PROD.DAT** y **PROVEEDORES.DAT**,
   con registros de ancho fijo. Para comprobarlo, Bloc de notas con
   `Formato → Ajustar al texto` desactivado, o bien desde el bloc de notas
   observar los grupos de 35 y 43 caracteres respectivamente.
5. Capturar pantallas del menú y de la creación de cada archivo para la
   evidencia de ejecución del TP.

### Nota sobre la compilación en OpenCobolIDE

OpenCobolIDE ya trae GnuCOBOL 2.0.0 y un botón de compilación (🔨). Si se
compila por consola con la instalación incluida en el IDE, hay que indicar
dónde está la configuración, de lo contrario aparece
`default.conf: No such file or directory`:

```powershell
$env:COB_CONFIG_DIR = "C:\Program Files (x86)\OpenCobolIDE\GnuCOBOL\config"
$env:PATH = "C:\Program Files (x86)\OpenCobolIDE\GnuCOBOL\bin;" + $env:PATH
cobc -x -fixed TP330.cob -o TP330.exe
```

Ejecutar el `.exe` generado directamente desde la terminal (CMD o PowerShell)
ofrece una visualización mucho más clara que el panel *Output* del IDE, ya que
este panel no dibuja correctamente las líneas de entrada.

> **Nota de formulario:** el documento final del TP debe entregarse con la
> nomenclatura `330_TP_14645240_2026-1` (código asignatura + tipo de trabajo
> + cédula sin puntos + lapso), en un solo archivo, con la carátula del
> instructivo, y citando el uso de IA si se empleó como apoyo (máx. 25%).
