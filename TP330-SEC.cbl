       IDENTIFICATION DIVISION.
       PROGRAM-ID. TP330SEC.
      *----------------------------------------------------------------*
      * AUTOR: JOSE VASQUEZ  (C.I. V-14.645.240)      LAPSO 2026-2     *
      * TRABAJO PRACTICO - PROCESAMIENTO DE DATOS (COD. 330)           *
      * UNIVERSIDAD NACIONAL ABIERTA  -  OBJETIVO 5                    *
      *                                                                *
      * VERSIÓN SECUENCIAL (RESPALDO): programa interactivo, con menu  *
      * de consola, que crea dos archivos con organizacion SECUENCIAL  *
      * (los registros se graban uno tras otro y para leer el ultimo   *
      * hay que pasar por todos los anteriores):                       *
      *   1) MAESTRO-PROD.DAT -> Archivo Maestro de Productos.         *
      *   2) PROVEEDORES.DAT  -> Archivo de Proveedores.               *
      * Cada opcion del menu crea el archivo desde cero (OPEN OUTPUT,  *
      * lo que borra los datos anteriores), captura los datos por      *
      * teclado en WORKING-STORAGE, los transfiere a la FILE SECTION   *
      * y los graba con WRITE, repitiendo el ciclo de entrada hasta    *
      * que el usuario responda "N" a "DESEA AGREGAR OTRO REGISTRO?".  *
      *----------------------------------------------------------------*

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
      *----------------------------------------------------------------*
      * FILE-CONTROL: asignacion de los archivos fisicos al programa.  *
      * Ambos usan ORGANIZATION SEQUENTIAL: los registros se graban    *
      * uno tras otro, en registros de ANCHO FIJO (35 y 43 caracteres) *
      * y sin caracter delimitador entre ellos. FILE STATUS permite    *
      * verificar el resultado de cada operacion de E/S.               *
      *----------------------------------------------------------------*
       FILE-CONTROL.
      *    Archivo Maestro de Productos: MAESTRO-PROD.DAT
           SELECT MAESTRO-PRODFI ASSIGN TO "MAESTRO-PROD.DAT"
                  ORGANIZATION IS SEQUENTIAL
                  FILE STATUS IS WS-FS-PROD.
      *    Archivo de Proveedores: PROVEEDORES.DAT
           SELECT PROVEEDORES ASSIGN TO "PROVEEDORES.DAT"
                  ORGANIZATION IS SEQUENTIAL
                  FILE STATUS IS WS-FS-PROV.

       DATA DIVISION.
      *----------------------------------------------------------------*
      * FILE SECTION: definicion de la estructura de registro de cada  *
      * archivo (area de registro asociada a la FD, donde se apoya     *
      * WRITE para grabar).                                            *
      *----------------------------------------------------------------*
       FILE SECTION.

      * FD del Archivo Maestro de Productos (MAESTRO-PROD.DAT)
      * Registro: ID(5) + NOMBRE(20) + STOCK(4) + PRECIO(6) = 35 car.
       FD  MAESTRO-PRODFI.
       01  REG-PRODUCTO.
           05 RP-ID-PRODUCTO        PIC 9(05).
           05 RP-NOMBRE-PRODUCTO    PIC X(20).
           05 RP-STOCK-ACTUAL       PIC 9(04).
           05 RP-PRECIO-UNITARIO    PIC 9(04)V99.

      * FD del Archivo de Proveedores (PROVEEDORES.DAT)
      * Registro: ID(3) + EMPRESA(25) + CIUDAD(15) = 43 caracteres
       FD  PROVEEDORES.
       01  REG-PROVEEDOR.
           05 RP-ID-PROVEEDOR       PIC 9(03).
           05 RP-NOMBRE-EMPRESA     PIC X(25).
           05 RP-CIUDAD-PROV        PIC X(15).

      *----------------------------------------------------------------*
      * WORKING-STORAGE SECTION: variables de trabajo del programa.    *
      * - Estructuras de entrada de datos (luego se transfieren a la   *
      *   FILE SECTION para grabarlas).                                *
      * - Variables de control del menu y del ciclo de entrada.        *
      * - Campos FILE STATUS para verificar las operaciones de E/S.    *
      *----------------------------------------------------------------*
       WORKING-STORAGE SECTION.
       01  WS-OPCION-MENU           PIC X(01).
       01  WS-CONTINUA              PIC X(01).
       01  WS-PAUSA                 PIC X(01).
       01  WS-FS-PROD               PIC XX.
       01  WS-FS-PROV               PIC XX.

      * Estructura de trabajo para capturar los datos de un producto
       01  WS-REG-PRODUCTO.
           05 WS-ID-PRODUCTO        PIC 9(05).
           05 WS-NOMBRE-PRODUCTO    PIC X(20).
           05 WS-STOCK-ACTUAL       PIC 9(04).
      *    El PRECIO se captura en un campo alfanumerico de 6 digitos
      *    y se transfiere sobre el area compartida con
      *    WS-PRECIO-UNITARIO mediante REDEFINES: los ultimos 2
      *    digitos quedan como decimales (ej: 125050 = 1250.50).
           05 WS-PRECIO-TXT         PIC X(06).
           05 WS-PRECIO-UNITARIO    PIC 9(04)V99.
           05 WS-PRECIO-CHAR REDEFINES WS-PRECIO-UNITARIO PIC 9(06).

      * Estructura de trabajo para capturar los datos de un proveedor
       01  WS-REG-PROVEEDOR.
           05 WS-ID-PROVEEDOR       PIC 9(03).
           05 WS-NOMBRE-EMPRESA     PIC X(25).
           05 WS-CIUDAD-PROV        PIC X(15).

       PROCEDURE DIVISION.
      *----------------------------------------------------------------*
      * 000-PRINCIPAL: modulo raiz del programa. Invoca el menu de     *
      * opciones de forma repetida hasta que el usuario elija "Salir". *
      *----------------------------------------------------------------*
       000-PRINCIPAL.
           MOVE " " TO WS-OPCION-MENU
           PERFORM 100-MENU-PRINCIPAL
               UNTIL WS-OPCION-MENU = "3"
           DISPLAY "FIN DEL PROGRAMA. GRACIAS POR USAR EL SISTEMA."
           STOP RUN.

      *----------------------------------------------------------------*
      * 050-LIMPIAR-PANTALLA: mejora la navegacion del menu limpiando  *
      * la consola (muestra lineas en blanco) cada vez que se vuelve   *
      * al menu principal, para que las pantallas no se acumulen.      *
      *----------------------------------------------------------------*
       050-LIMPIAR-PANTALLA.
           PERFORM 25 TIMES
               DISPLAY " "
           END-PERFORM.

      *----------------------------------------------------------------*
      * 060-PAUSA-SISTEMA: mejora la navegacion deteniendo el flujo    *
      * despues de cada operacion con "PRESIONE ENTER PARA CONTINUAR", *
      * de modo que el usuario pueda leer los mensajes del sistema     *
      * antes de regresar al menu principal.                           *
      *----------------------------------------------------------------*
       060-PAUSA-SISTEMA.
           DISPLAY "------------------------------------------------"
           DISPLAY " PRESIONE ENTER PARA VOLVER AL MENU PRINCIPAL..."
           ACCEPT WS-PAUSA.

      *----------------------------------------------------------------*
      * 100-MENU-PRINCIPAL: limpia la pantalla, despliega el menu,     *
      * lee la opcion elegida por el usuario y dirige el proceso       *
      * hacia la rutina correspondiente (con pausa posterior), o       *
      * informa si la opcion es invalida.                              *
      *----------------------------------------------------------------*
       100-MENU-PRINCIPAL.
           PERFORM 050-LIMPIAR-PANTALLA
           DISPLAY "==============================================="
           DISPLAY "  SISTEMA DE CREACION DE ARCHIVOS SECUENCIALES "
           DISPLAY "==============================================="
           DISPLAY " 1. CREAR ARCHIVO DE PRODUCTOS (MAESTRO-PROD.DAT)"
           DISPLAY " 2. CREAR ARCHIVO DE PROVEEDORES (PROVEEDORES.DAT)"
           DISPLAY " 3. SALIR DEL SISTEMA"
           DISPLAY "==============================================="
           DISPLAY " SELECCIONE UNA OPCION (1-3): "
           ACCEPT WS-OPCION-MENU
           EVALUATE WS-OPCION-MENU
               WHEN "1"
                   PERFORM 200-CREAR-PRODUCTOS
                   PERFORM 060-PAUSA-SISTEMA
               WHEN "2"
                   PERFORM 300-CREAR-PROVEEDORES
                   PERFORM 060-PAUSA-SISTEMA
               WHEN "3"
                   DISPLAY "SALIENDO DEL SISTEMA..."
               WHEN OTHER
                   DISPLAY "OPCION INVALIDA. ELIJA 1, 2 O 3."
                   PERFORM 060-PAUSA-SISTEMA
           END-EVALUATE.

      *----------------------------------------------------------------*
      * 200-CREAR-PRODUCTOS: crea MAESTRO-PROD.DAT desde cero (OPEN    *
      * OUTPUT borra los datos anteriores, lo cual es correcto para    *
      * una "creacion") y graba secuencialmente tantos registros de    *
      * productos como indique el usuario en el ciclo de entrada.      *
      *----------------------------------------------------------------*
       200-CREAR-PRODUCTOS.
           OPEN OUTPUT MAESTRO-PRODFI
           IF WS-FS-PROD NOT = "00"
               DISPLAY "ERROR AL CREAR MAESTRO-PROD.DAT  STATUS="
                   WS-FS-PROD
               EXIT PARAGRAPH
           END-IF
           MOVE "S" TO WS-CONTINUA
           PERFORM UNTIL WS-CONTINUA = "N" OR WS-CONTINUA = "n"
               PERFORM 210-LEER-DATOS-PRODUCTO
               PERFORM 220-ESCRIBIR-PRODUCTO
               PERFORM 400-PREGUNTAR-CONTINUA
           END-PERFORM
           CLOSE MAESTRO-PRODFI
           DISPLAY "ARCHIVO MAESTRO-PROD.DAT CREADO EXITOSAMENTE".

      *----------------------------------------------------------------*
      * 210-LEER-DATOS-PRODUCTO: captura por teclado los datos del     *
      * producto y los almacena en la estructura de WORKING-STORAGE.   *
      * Nota: el PRECIO se ingresa con 6 digitos SIN punto decimal;    *
      * los ultimos 2 digitos son los decimales (ej: 125050=1250.50).  *
      *----------------------------------------------------------------*
       210-LEER-DATOS-PRODUCTO.
           DISPLAY "------ NUEVO REGISTRO DE PRODUCTO ------"
           DISPLAY "INGRESE ID DEL PRODUCTO (5 DIGITOS): "
           ACCEPT WS-ID-PRODUCTO
           DISPLAY "INGRESE NOMBRE DEL PRODUCTO (20 CARACTERES): "
           ACCEPT WS-NOMBRE-PRODUCTO
           DISPLAY "INGRESE STOCK ACTUAL (4 DIGITOS): "
           ACCEPT WS-STOCK-ACTUAL
           DISPLAY "NOTA: ESCRIBA 6 DIGITOS SIN PUNTO; LOS ULTIMOS"
           DISPLAY "2 SON DECIMALES (EJ: 125050 = 1250.50)"
           DISPLAY "INGRESE PRECIO UNITARIO (6 DIGITOS): "
           ACCEPT WS-PRECIO-TXT
      *    La captura (X(06)) se transfiere al area compartida con
      *    WS-PRECIO-UNITARIO via REDEFINES, de modo que el valor
      *    queda con 4 digitos enteros y 2 decimales.
           MOVE WS-PRECIO-TXT TO WS-PRECIO-CHAR.

      *----------------------------------------------------------------*
      * 220-ESCRIBIR-PRODUCTO: transfiere el registro desde WORKING-   *
      * STORAGE hacia el registro de la FILE SECTION y lo graba en     *
      * MAESTRO-PROD.DAT con WRITE (escritura secuencial).             *
      *----------------------------------------------------------------*
       220-ESCRIBIR-PRODUCTO.
           MOVE WS-ID-PRODUCTO      TO RP-ID-PRODUCTO
           MOVE WS-NOMBRE-PRODUCTO  TO RP-NOMBRE-PRODUCTO
           MOVE WS-STOCK-ACTUAL     TO RP-STOCK-ACTUAL
           MOVE WS-PRECIO-UNITARIO  TO RP-PRECIO-UNITARIO
           WRITE REG-PRODUCTO
           IF WS-FS-PROD NOT = "00"
               DISPLAY "ERROR AL GRABAR REGISTRO.  STATUS="
                   WS-FS-PROD
           ELSE
               DISPLAY "REGISTRO GRABADO CORRECTAMENTE."
           END-IF.

      *----------------------------------------------------------------*
      * 300-CREAR-PROVEEDORES: crea PROVEEDORES.DAT desde cero (OPEN   *
      * OUTPUT) y graba secuencialmente los registros de proveedores   *
      * hasta que el usuario responda "N" al ciclo de entrada.         *
      *----------------------------------------------------------------*
       300-CREAR-PROVEEDORES.
           OPEN OUTPUT PROVEEDORES
           IF WS-FS-PROV NOT = "00"
               DISPLAY "ERROR AL CREAR PROVEEDORES.DAT  STATUS="
                   WS-FS-PROV
               EXIT PARAGRAPH
           END-IF
           MOVE "S" TO WS-CONTINUA
           PERFORM UNTIL WS-CONTINUA = "N" OR WS-CONTINUA = "n"
               PERFORM 310-LEER-DATOS-PROVEEDOR
               PERFORM 320-ESCRIBIR-PROVEEDOR
               PERFORM 400-PREGUNTAR-CONTINUA
           END-PERFORM
           CLOSE PROVEEDORES
           DISPLAY "ARCHIVO PROVEEDORES.DAT CREADO EXITOSAMENTE".

      *----------------------------------------------------------------*
      * 310-LEER-DATOS-PROVEEDOR: captura por teclado los datos del    *
      * proveedor y los almacena en la estructura de WORKING-STORAGE.  *
      *----------------------------------------------------------------*
       310-LEER-DATOS-PROVEEDOR.
           DISPLAY "------ NUEVO REGISTRO DE PROVEEDOR ------"
           DISPLAY "INGRESE ID DEL PROVEEDOR (3 DIGITOS): "
           ACCEPT WS-ID-PROVEEDOR
           DISPLAY "INGRESE NOMBRE DE LA EMPRESA (25 CARACTERES): "
           ACCEPT WS-NOMBRE-EMPRESA
           DISPLAY "INGRESE CIUDAD (15 CARACTERES): "
           ACCEPT WS-CIUDAD-PROV.

      *----------------------------------------------------------------*
      * 320-ESCRIBIR-PROVEEDOR: transfiere el registro desde WORKING-  *
      * STORAGE hacia el registro de la FILE SECTION y lo graba en     *
      * PROVEEDORES.DAT con WRITE (escritura secuencial).              *
      *----------------------------------------------------------------*
       320-ESCRIBIR-PROVEEDOR.
           MOVE WS-ID-PROVEEDOR    TO RP-ID-PROVEEDOR
           MOVE WS-NOMBRE-EMPRESA  TO RP-NOMBRE-EMPRESA
           MOVE WS-CIUDAD-PROV     TO RP-CIUDAD-PROV
           WRITE REG-PROVEEDOR
           IF WS-FS-PROV NOT = "00"
               DISPLAY "ERROR AL GRABAR REGISTRO.  STATUS="
                   WS-FS-PROV
           ELSE
               DISPLAY "REGISTRO GRABADO CORRECTAMENTE."
           END-IF.

      *----------------------------------------------------------------*
      * 400-PREGUNTAR-CONTINUA: control del ciclo de entrada.          *
      * Pregunta al usuario si desea agregar otro registro y solo      *
      * acepta como respuesta valida "S" o "N" (mayuscula o minuscula).*
      *----------------------------------------------------------------*
       400-PREGUNTAR-CONTINUA.
           MOVE " " TO WS-CONTINUA
           PERFORM UNTIL WS-CONTINUA IS = "S" OR "s" OR "N" OR "n"
               DISPLAY "DESEA AGREGAR OTRO REGISTRO? (S/N): "
               ACCEPT WS-CONTINUA
           END-PERFORM.
