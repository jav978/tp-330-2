# TP-330 — Procesamiento de Datos (Trabajo Práctico, Objetivo 5)

Trabajo Práctico de la asignatura **Procesamiento de Datos (código 330)** de la
Universidad Nacional Abierta, carrera Ingeniería de Sistemas.

**Autor:** José Vásquez — C.I. V-14.645.240
**Lapso:** 2026-1

## Descripción

Programa en COBOL con interfaz de consola y menús que crea dos archivos con
**organización secuencial** (los registros se graban uno tras otro y, para leer
el último, es necesario pasar por todos los anteriores):

| Archivo            | Contenido                  | Ancho de registro |
| ------------------ | -------------------------- | ----------------- |
| `MAESTRO-PROD.DAT` | Maestro de productos       | 35 caracteres     |
| `PROVEEDORES.DAT`  | Datos de proveedores       | 43 caracteres     |

### Estructura de los registros

**MAESTRO-PROD.DAT**

| Campo              | Clase        | PIC        |
| ------------------ | ------------ | ---------- |
| ID-Producto        | Numérico     | `9(05)`    |
| Nombre-Producto    | Alfanumérico | `X(20)`    |
| Stock-Actual       | Numérico     | `9(04)`    |
| Precio-Unitario    | Numérico     | `9(04)V99` |

**PROVEEDORES.DAT**

| Campo            | Clase        | PIC     |
| ---------------- | ------------ | ------- |
| ID-Proveedor     | Numérico     | `9(03)` |
| Nombre-Empresa   | Alfanumérico | `X(25)` |
| Ciudad           | Alfanumérico | `X(15)` |

## Requerimientos del enunciado

| Requerimiento                                            | Dónde se cumple                    |
| -------------------------------------------------------- | ---------------------------------- |
| Menú: crear productos / crear proveedores / salir        | `100-MENU-PRINCIPAL`               |
| Crear el archivo desde cero con `OPEN OUTPUT`            | `200-CREAR-PRODUCTOS`, `300-CREAR-PROVEEDORES` |
| Validación de la apertura (`FILE STATUS`)                | ambos párrafos de creación         |
| Ciclo "¿Desea agregar otro registro? (S/N)"              | `400-PREGUNTAR-CONTINUA`           |
| Transferir de WORKING-STORAGE a FILE SECTION y `WRITE`   | `220-ESCRIBIR-PRODUCTO`, `320-ESCRIBIR-PROVEEDOR` |
| Trabajo ordenado y secuencial                            | `PERFORM ... UNTIL`, organización secuencial |

## Estructura del programa

```
IDENTIFICATION DIVISION   -> identificación del programa
ENVIRONMENT DIVISION      -> FILE-CONTROL (SELECT, organización, FILE STATUS)
DATA DIVISION
  FILE SECTION            -> FD y registros de cada archivo
  WORKING-STORAGE SECTION -> variables de control y estructuras de captura
PROCEDURE DIVISION        -> 11 párrafos numerados y documentados
```

| Párrafo                 | Función                                              |
| ----------------------- | ---------------------------------------------------- |
| `000-PRINCIPAL`         | Módulo raíz: repite el menú hasta salir             |
| `050-LIMPIAR-PANTALLA`  | Limpia la consola antes de mostrar el menú           |
| `060-PAUSA-SISTEMA`     | Pausa para leer mensajes antes de volver al menú     |
| `100-MENU-PRINCIPAL`    | Menú de opciones (`EVALUATE`)                        |
| `200-CREAR-PRODUCTOS`   | Crea `MAESTRO-PROD.DAT` y graba los registros        |
| `210-LEER-DATOS-PRODUCTO` | Captura por teclado los datos del producto         |
| `220-ESCRIBIR-PRODUCTO` | `MOVE` a FILE SECTION y `WRITE`                      |
| `300-CREAR-PROVEEDORES` | Crea `PROVEEDORES.DAT` y graba los registros         |
| `310-LEER-DATOS-PROVEEDOR` | Captura por teclado los datos del proveedor       |
| `320-ESCRIBIR-PROVEEDOR`  | `MOVE` a FILE SECTION y `WRITE`                    |
| `400-PREGUNTAR-CONTINUA`  | Control del ciclo de entrada (S/N)                |

## Compilación y ejecución

Requiere **GnuCOBOL** (sucesor de OpenCOBOL). OpenCobolIDE ya lo incluye.

```powershell
$env:COB_CONFIG_DIR = "C:\Program Files (x86)\OpenCobolIDE\GnuCOBOL\config"
$env:PATH = "C:\Program Files (x86)\OpenCobolIDE\GnuCOBOL\bin;" + $env:PATH
cobc -x -fixed TP330.cob -o TP330.exe
.\TP330.exe
```

Ejecutar el `.exe` desde la terminal (CMD o PowerShell) ofrece una visualización
más clara que el panel *Output* del IDE.

## Documentación

`DOCUMENTACION_TP330.md` contiene el análisis completo: diseño de la
organización de archivos, elementos del código fuente COBOL, diccionario de
datos y pseudocódigo con el detalle de cada párrafo.

## Nota sobre la organización del archivo

Se emplea `ORGANIZATION IS SEQUENTIAL` y no `LINE SEQUENTIAL` porque esta
última **recorta los espacios finales** de cada registro, lo que destruiría el
ancho fijo exigido por las especificaciones (por ejemplo, el campo `Ciudad` de
15 posiciones).