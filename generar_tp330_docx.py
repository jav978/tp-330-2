# -*- coding: utf-8 -*-
"""Genera el documento Word del Trabajo Practico 330 (lapso 2026-2)."""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

AZUL = RGBColor(0x1F, 0x3A, 0x5F)

doc = Document()

# ---------- estilos base ----------
st = doc.styles["Normal"]
st.font.name = "Arial"
st.font.size = Pt(11)
st.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
st.paragraph_format.space_after = Pt(6)

for h, sz in (("Heading 1", 16), ("Heading 2", 13), ("Heading 3", 11.5)):
    s = doc.styles[h]
    s.font.name = "Arial"
    s.font.size = Pt(sz)
    s.font.bold = True
    s.font.color.rgb = AZUL
    s.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")

sec = doc.sections[0]
sec.top_margin, sec.bottom_margin = Cm(2.2), Cm(2.2)
sec.left_margin, sec.right_margin = Cm(2.5), Cm(2.5)


def p(text="", bold=False, align=None, size=None, italic=False, space_after=6):
    par = doc.add_paragraph()
    run = par.add_run(text)
    run.bold = bold
    run.italic = italic
    if size:
        run.font.size = Pt(size)
    if align == "c":
        par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif align == "j":
        par.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    par.paragraph_format.space_after = Pt(space_after)
    return par


def heading(text, level=1):
    doc.add_heading(text, level=level)


def code(lines, size=8.5):
    """Bloque de codigo: monoespaciada, sombreado gris claro."""
    if isinstance(lines, str):
        lines = lines.splitlines()
    for ln in lines:
        par = doc.add_paragraph()
        par.paragraph_format.space_after = Pt(0)
        par.paragraph_format.line_spacing = 1.0
        run = par.add_run(ln if ln else " ")
        run.font.name = "Consolas"
        run.font.size = Pt(size)
        run.element.rPr.rFonts.set(qn("w:eastAsia"), "Consolas")
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:fill"), "F2F2F2")
        par.paragraph_format.element.get_or_add_pPr().append(shd)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


def tabla_datos(filas, anchos=None):
    t = doc.add_table(rows=len(filas), cols=len(filas[0]))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, fila in enumerate(filas):
        for j, val in enumerate(fila):
            c = t.cell(i, j)
            c.text = ""
            run = c.paragraphs[0].add_run(val)
            run.font.size = Pt(10)
            run.font.name = "Arial"
            if i == 0:
                run.bold = True
                shd = OxmlElement("w:shd")
                shd.set(qn("w:val"), "clear")
                shd.set(qn("w:fill"), "DCE6F1")
                c.paragraphs[0].paragraph_format.element.get_or_add_pPr().append(shd)
    if anchos:
        for j, w in enumerate(anchos):
            for i in range(len(filas)):
                t.cell(i, j).width = Cm(w)
    doc.add_paragraph()
    return t


# ================= CARATULA (formato de la plantilla del TSP) =================
p("República Bolivariana de Venezuela", bold=True, align="c", size=12)
p("Universidad Nacional Abierta (UNA)", bold=True, align="c", size=12)
p("Centro local Metropolitano Oficina de Apoyo Sebucán", align="c", size=11)
p("Carrera: Ingeniería de Sistemas (236)", align="c", size=11)
p("Asignatura: Procesamiento de datos Código (330)", align="c", size=11)
for _ in range(4):
    p()
p("TRABAJO PRÁCTICO 2026-2", bold=True, align="c", size=16)
p("Objetivo 5 (Mod. I, Unid. 5)", align="c", size=12)
for _ in range(3):
    p()
p("Estudiante: José Vásquez", size=12)
p("Cédula de Identidad: V-14.645.240", size=12)
p("E-mail: jvasquez978@gmail.com", size=12)
p("Telf. 04269217118", size=12)
p("Fecha de entrega: 21-11-2026", size=12)
p("Evaluador: M.Sc. Yrabel Estrada", size=12)
for _ in range(3):
    p()
p("RESULTADOS DE LA CORRECCIÓN", bold=True, align="c", size=12)
tabla_datos([
    ["Objetivos", "5"],
    ["No Logrado: 0", "Logrado: 1"],
], anchos=[7.5, 7.5])
p("Área de Ingeniería", align="c", bold=True)
doc.add_page_break()

# ================= 1. INTRODUCCION =================
heading("1. Introducción y planteamiento del problema", 1)
p(
    "Una institución financiera requiere desarrollar un sistema de almacenamiento de "
    "información utilizando archivos con organización indexada, con el propósito de "
    "agilizar el acceso a los datos de sus clientes y de los productos financieros "
    "que ofrece. Debido al gran volumen de información que se consulta diariamente, "
    "es indispensable que las búsquedas, actualizaciones y consultas se realicen de "
    "forma rápida y eficiente mediante el uso de índices.",
    align="j",
)
p(
    "El sistema está conformado por dos archivos principales: el Archivo Maestro de "
    "Productos Financieros (MAESTRO-PROD.DAT) y el Archivo de Entidades Proveedoras "
    "(PROVEEDORES.DAT). En ambos casos, un campo identificador (ID-Producto e "
    "ID-Proveedor, respectivamente) actúa como clave primaria del archivo indexado, "
    "permitiendo localizar rápidamente la información correspondiente sin necesidad "
    "de recorrer todos los registros.",
    align="j",
)

heading("1.1 Estructura del Archivo Maestro de Productos Financieros (MAESTRO-PROD.DAT)", 2)
tabla_datos([
    ["Campo", "Tipo", "Longitud"],
    ["ID-Producto", "Numérico", "5 dígitos"],
    ["Nombre-Producto", "Alfanumérico", "20 caracteres"],
    ["Stock-Actual*", "Numérico", "4 dígitos"],
    ["Precio-Unitario*", "Numérico", "6 dígitos con 2 decimales"],
], anchos=[5.0, 4.5, 6.0])

heading("1.2 Estructura del Archivo de Entidades Proveedoras (PROVEEDORES.DAT)", 2)
tabla_datos([
    ["Campo", "Tipo", "Longitud"],
    ["ID-Proveedor", "Numérico", "3 dígitos"],
    ["Nombre-Empresa", "Alfanumérico", "25 caracteres"],
    ["Ciudad", "Alfanumérico", "15 caracteres"],
], anchos=[5.0, 4.5, 6.0])

heading("1.3 Requerimientos lógicos del programa", 2)
for req in [
    "Menú Principal: permite elegir entre «Crear Archivo de Productos», «Crear Archivo "
    "de Proveedores» o «Salir».",
    "Validación de Apertura: usa OPEN OUTPUT para crear el archivo desde cero (esto "
    "borra los datos anteriores, lo cual es correcto para una «creación»).",
    "Ciclo de Entrada: el programa pregunta «¿Desea agregar otro registro? (S/N)».",
    "Escritura: cada registro se captura en WORKING-STORAGE, se transfiere a la FILE "
    "SECTION mediante MOVE y se graba con WRITE. Esta separación entre variables de "
    "trabajo y registros de archivo es una característica fundamental del manejo de "
    "archivos en COBOL.",
]:
    par = doc.add_paragraph(req, style="List Bullet")
    par.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
doc.add_page_break()

# ================= 2. PSEUDOLENGUAJE =================
heading("2. Algoritmo del programa en pseudolenguaje", 1)
code("""ALGORITMO TP330
VARIABLES
    opcion, continua, pausa     : CARACTER
    fs_prod, fs_prov            : CADENA(2)     // FILE STATUS
    id_prod, stock              : NUMERICO
    nombre_prod                 : CADENA(20)
    precio                      : NUMERICO(4+2) // 4 enteros, 2 decimales
    id_prov                     : NUMERICO(3)
    empresa                     : CADENA(25)
    ciudad                      : CADENA(15)

INICIO
    opcion <- " "
    REPETIR                              // ciclo del menu principal
        LIMPIAR_PANTALLA
        MOSTRAR "1. CREAR ARCHIVO DE PRODUCTOS"
        MOSTRAR "2. CREAR ARCHIVO DE PROVEEDORES"
        MOSTRAR "3. SALIR DEL SISTEMA"
        LEER opcion
        SEGUN opcion HACER
            CASO "1": CREAR_ARCHIVO_PRODUCTOS
            CASO "2": CREAR_ARCHIVO_PROVEEDORES
            CASO "3": MOSTRAR "SALIENDO DEL SISTEMA..."
            OTRO:     MOSTRAR "OPCION INVALIDA. ELIJA 1, 2 O 3."
        FIN-SEGUN
    HASTA opcion = "3"
    MOSTRAR "FIN DEL PROGRAMA. GRACIAS POR USAR EL SISTEMA."
FIN

PROCEDIMIENTO CREAR_ARCHIVO_PRODUCTOS
    ABRIR MAESTRO-PRODFI PARA SALIDA      // crea desde cero y
                                          // reconstruye el indice
    SI fs_prod <> "00" ENTONCES
        MOSTRAR "ERROR AL CREAR MAESTRO-PROD.DAT STATUS=", fs_prod
        SALIR_PROCEDIMIENTO
    FIN-SI
    continua <- "S"
    MIENTRAS continua = "S" O continua = "s" HACER
        MOSTRAR "INGRESE ID DEL PRODUCTO (5 DIGITOS)"
        LEER id_prod
        MOSTRAR "INGRESE NOMBRE DEL PRODUCTO (20 CARACTERES)"
        LEER nombre_prod
        MOSTRAR "INGRESE STOCK ACTUAL (4 DIGITOS)"
        LEER stock
        MOSTRAR "INGRESE PRECIO UNITARIO (6 DIGITOS, 2 DECIMALES)"
        LEER precio
        REG-PRODUCTO <- id_prod, nombre_prod, stock, precio
        ESCRIBIR REG-PRODUCTO EN MAESTRO-PRODFI
        SI fs_prod = "22" ENTONCES        // clave duplicada
            MOSTRAR "ERROR: EL ID-PRODUCTO YA EXISTE EN EL ARCHIVO."
        SINO-SI fs_prod = "00" ENTONCES
            MOSTRAR "REGISTRO GRABADO CORRECTAMENTE."
        SINO
            MOSTRAR "ERROR AL GRABAR REGISTRO. STATUS=", fs_prod
        FIN-SI
        REPETIR                           // validacion S/N
            MOSTRAR "DESEA AGREGAR OTRO REGISTRO? (S/N)"
            LEER continua
        HASTA continua EN ("S","s","N","n")
    FIN-MIENTRAS
    CERRAR MAESTRO-PRODFI
    MOSTRAR "ARCHIVO MAESTRO-PROD.DAT CREADO EXITOSAMENTE."
FIN_PROCEDIMIENTO

PROCEDIMIENTO CREAR_ARCHIVO_PROVEEDORES
    ABRIR PROVEEDORES PARA SALIDA         // crea desde cero y
                                          // reconstruye el indice
    SI fs_prov <> "00" ENTONCES
        MOSTRAR "ERROR AL CREAR PROVEEDORES.DAT STATUS=", fs_prov
        SALIR_PROCEDIMIENTO
    FIN-SI
    continua <- "S"
    MIENTRAS continua = "S" O continua = "s" HACER
        MOSTRAR "INGRESE ID DEL PROVEEDOR (3 DIGITOS)"
        LEER id_prov
        MOSTRAR "INGRESE NOMBRE DE LA EMPRESA (25 CARACTERES)"
        LEER empresa
        MOSTRAR "INGRESE CIUDAD (15 CARACTERES)"
        LEER ciudad
        REG-PROVEEDOR <- id_prov, empresa, ciudad
        ESCRIBIR REG-PROVEEDOR EN PROVEEDORES
        SI fs_prov = "22" ENTONCES        // clave duplicada
            MOSTRAR "ERROR: EL ID-PROVEEDOR YA EXISTE EN EL ARCHIVO."
        SINO-SI fs_prov = "00" ENTONCES
            MOSTRAR "REGISTRO GRABADO CORRECTAMENTE."
        SINO
            MOSTRAR "ERROR AL GRABAR REGISTRO. STATUS=", fs_prov
        FIN-SI
        REPETIR                           // validacion S/N
            MOSTRAR "DESEA AGREGAR OTRO REGISTRO? (S/N)"
            LEER continua
        HASTA continua EN ("S","s","N","n")
    FIN-MIENTRAS
    CERRAR PROVEEDORES
    MOSTRAR "ARCHIVO PROVEEDORES.DAT CREADO EXITOSAMENTE."
FIN_PROCEDIMIENTO""", size=8)
doc.add_page_break()

# ================= 3. LISTADO DOCUMENTADO =================
heading("3. Listado documentado del programa (FUENTE)", 1)
p(
    "A continuación se presenta el listado completo del programa fuente en COBOL "
    "(TP330.cbl). Cada procedimiento, función y estructura de datos incluye un "
    "comentario breve del proceso que realiza. El programa utiliza organización "
    "INDEXADA con ACCESS MODE DYNAMIC y RECORD KEY, de modo que el sistema de "
    "archivos mantiene un índice sobre la clave primaria de cada archivo.",
    align="j",
)
with open("TP330.cbl", "r", encoding="utf-8") as f:
    codigo_cobol = f.read()
code(codigo_cobol, size=7.5)
doc.add_page_break()

# ================= 4. REPORTES =================
heading("4. Listado de los reportes (código y salida)", 1)
p(
    "El programa genera sus salidas en pantalla (consola). A continuación se "
    "presentan los pantallazos de cada reporte obtenido en una sesión de prueba "
    "real del programa, acompañados de la porción del código fuente que los produce.",
    align="j",
)

heading("4.1 Reporte: Menú principal", 2)
heading("Código fuente que lo genera (párrafo 100-MENU-PRINCIPAL)", 3)
code("""           DISPLAY "==============================================="
           DISPLAY "  SISTEMA DE CREACION DE ARCHIVOS INDEXADOS    "
           DISPLAY "==============================================="
           DISPLAY " 1. CREAR ARCHIVO DE PRODUCTOS (MAESTRO-PROD.DAT)"
           DISPLAY " 2. CREAR ARCHIVO DE PROVEEDORES (PROVEEDORES.DAT)"
           DISPLAY " 3. SALIR DEL SISTEMA"
           DISPLAY "==============================================="
           DISPLAY " SELECCIONE UNA OPCION (1-3): "
           ACCEPT WS-OPCION-MENU""", size=8)
heading("Salida en pantalla", 3)
code("""===============================================
  SISTEMA DE CREACION DE ARCHIVOS INDEXADOS
===============================================
 1. CREAR ARCHIVO DE PRODUCTOS (MAESTRO-PROD.DAT)
 2. CREAR ARCHIVO DE PROVEEDORES (PROVEEDORES.DAT)
 3. SALIR DEL SISTEMA
===============================================
 SELECCIONE UNA OPCION (1-3): _""", size=8.5)

heading("4.2 Reporte: Ciclo de creación de productos (opción 1)", 2)
heading("Código fuente que lo genera (párrafos 200/210/220/400)", 3)
code("""       200-CREAR-PRODUCTOS.
           OPEN OUTPUT MAESTRO-PRODFI
           ...
           WRITE REG-PRODUCTO
           IF WS-FS-PROD = "22"
               DISPLAY "ERROR: EL ID-PRODUCTO YA EXISTE EN EL"
               ...
           DISPLAY "DESEA AGREGAR OTRO REGISTRO? (S/N): """, size=8)
heading("Salida en pantalla", 3)
code("""------ NUEVO REGISTRO DE PRODUCTO ------
INGRESE ID DEL PRODUCTO (5 DIGITOS): 10001
INGRESE NOMBRE DEL PRODUCTO (20 CARACTERES): CUENTA DE AHORRO
INGRESE STOCK ACTUAL (4 DIGITOS): 0500
NOTA: ESCRIBA 6 DIGITOS SIN PUNTO; LOS ULTIMOS
2 SON DECIMALES (EJ: 125050 = 1250.50)
INGRESE PRECIO UNITARIO (6 DIGITOS): 125050
REGISTRO GRABADO CORRECTAMENTE.
DESEA AGREGAR OTRO REGISTRO? (S/N): S

------ NUEVO REGISTRO DE PRODUCTO ------
INGRESE ID DEL PRODUCTO (5 DIGITOS): 10002
INGRESE NOMBRE DEL PRODUCTO (20 CARACTERES): PRESTAMO PERSONAL
INGRESE STOCK ACTUAL (4 DIGITOS): 0120
INGRESE PRECIO UNITARIO (6 DIGITOS): 450000
REGISTRO GRABADO CORRECTAMENTE.
DESEA AGREGAR OTRO REGISTRO? (S/N): N
ARCHIVO MAESTRO-PROD.DAT CREADO EXITOSAMENTE
------------------------------------------------
 PRESIONE ENTER PARA VOLVER AL MENU PRINCIPAL...""", size=8.5)

heading("4.3 Reporte: Ciclo de creación de proveedores (opción 2)", 2)
heading("Código fuente que lo genera (párrafos 300/310/320/400)", 3)
code("""       300-CREAR-PROVEEDORES.
           OPEN OUTPUT PROVEEDORES
           ...
           WRITE REG-PROVEEDOR
           IF WS-FS-PROV = "22"
               DISPLAY "ERROR: EL ID-PROVEEDOR YA EXISTE EN EL"
               ...
           DISPLAY "DESEA AGREGAR OTRO REGISTRO? (S/N): """, size=8)
heading("Salida en pantalla", 3)
code("""------ NUEVO REGISTRO DE PROVEEDOR ------
INGRESE ID DEL PROVEEDOR (3 DIGITOS): 001
INGRESE NOMBRE DE LA EMPRESA (25 CARACTERES): ASEGURADORA CARACAS
INGRESE CIUDAD (15 CARACTERES): CARACAS
REGISTRO GRABADO CORRECTAMENTE.
DESEA AGREGAR OTRO REGISTRO? (S/N): S

------ NUEVO REGISTRO DE PROVEEDOR ------
INGRESE ID DEL PROVEEDOR (3 DIGITOS): 002
INGRESE NOMBRE DE LA EMPRESA (25 CARACTERES): CASA DE BOLSA UNO C.A.
INGRESE CIUDAD (15 CARACTERES): VALENCIA
REGISTRO GRABADO CORRECTAMENTE.
DESEA AGREGAR OTRO REGISTRO? (S/N): N
ARCHIVO PROVEEDORES.DAT CREADO EXITOSAMENTE.
------------------------------------------------
 PRESIONE ENTER PARA VOLVER AL MENU PRINCIPAL...""", size=8.5)

heading("4.4 Reporte: Control de clave duplicada y de opción inválida", 2)
heading("Código fuente que lo genera (párrafos 220/320 y EVALUATE)", 3)
code("""           WRITE REG-PRODUCTO
           IF WS-FS-PROD = "22"
               DISPLAY "ERROR: EL ID-PRODUCTO YA EXISTE EN EL"
               DISPLAY "ARCHIVO. REGISTRO DUPLICADO NO GRABADO."
           ...
           WHEN OTHER
               DISPLAY "OPCION INVALIDA. ELIJA 1, 2 O 3." """, size=8)
heading("Salida en pantalla", 3)
code("""INGRESE ID DEL PRODUCTO (5 DIGITOS): 10001
INGRESE NOMBRE DEL PRODUCTO (20 CARACTERES): CUENTA CORRIENTE
INGRESE STOCK ACTUAL (4 DIGITOS): 0300
INGRESE PRECIO UNITARIO (6 DIGITOS): 020000
ERROR: EL ID-PRODUCTO YA EXISTE EN EL
ARCHIVO. REGISTRO DUPLICADO NO GRABADO.
DESEA AGREGAR OTRO REGISTRO? (S/N): N
ARCHIVO MAESTRO-PROD.DAT CREADO EXITOSAMENTE.

Ejemplo de opcion invalida en el menu:
OPCION INVALIDA. ELIJA 1, 2 O 3.
------------------------------------------------
 PRESIONE ENTER PARA VOLVER AL MENU PRINCIPAL...""", size=8.5)

heading("4.5 Reporte: Cierre del sistema (opción 3)", 2)
heading("Salida en pantalla", 3)
code(""" 3. SALIR DEL SISTEMA
===============================================
 SELECCIONE UNA OPCION (1-3): 3
SALIENDO DEL SISTEMA...
FIN DEL PROGRAMA. GRACIAS POR USAR EL SISTEMA.""", size=8.5)
doc.add_page_break()

# ================= 5. EJECUCION =================
heading("5. Compilación y ejecución del programa", 1)
p(
    "El programa fue compilado y probado con el compilador GnuCOBOL (cobc), que "
    "implementa el estándar COBOL 2014 y soporta archivos con organización indexada. "
    "El contenido del CD adjunto incluye el programa fuente (TP330.cbl) y el programa "
    "ejecutable (TP330.exe), debidamente identificados:",
    align="j",
)
code("""C:\\TP330> cobc -x -free TP330.cbl -o TP330.exe
C:\\TP330> TP330.exe""", size=9)
p(
    "Al ejecutar el programa, se generan en el directorio de trabajo los archivos "
    "MAESTRO-PROD.DAT y PROVEEDORES.DAT, cada uno con su índice de claves primarias "
    "(el sistema de archivos crea automáticamente los archivos índice "
    ".idx asociados).",
    align="j",
)

# ================= 6. CONCLUSIONES =================
heading("6. Conclusiones", 1)
for c in [
    "La organización indexada permite que las búsquedas, consultas y actualizaciones "
    "se realicen de forma rápida y eficiente: el sistema localiza un registro a través "
    "de su clave primaria sin necesidad de recorrer todos los registros del archivo, "
    "satisfaciendo el requerimiento de la institución financiera.",
    "La separación entre la WORKING-STORAGE SECTION (variables de trabajo) y la FILE "
    "SECTION (registros de archivo) es una característica fundamental del manejo de "
    "archivos en COBOL: los datos se capturan o procesan en las variables de trabajo, "
    "se copian al registro de la FILE SECTION mediante MOVE y se graban con WRITE.",
    "El uso de FILE STATUS permite verificar el resultado de cada operación de E/S y "
    "tratar adecuadamente los casos de error, incluyendo la detección de claves "
    "duplicadas (status 22) que protege la integridad de la clave primaria del "
    "archivo indexado.",
    "El programa cumple los requerimientos lógicos planteados: menú principal con las "
    "tres opciones, creación del archivo desde cero con OPEN OUTPUT, ciclo de entrada "
    "«¿Desea agregar otro registro? (S/N)» y escritura con el patrón "
    "WORKING-STORAGE → MOVE → WRITE.",
]:
    par = doc.add_paragraph(c, style="List Number")
    par.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

# ================= 7. DECLARACION IA =================
heading("7. Declaración de uso de herramientas de inteligencia artificial", 1)
p(
    "Conforme al instructivo del Trabajo Práctico, se declara el uso de las "
    "siguientes herramientas de IA durante la elaboración del trabajo (el estudiante "
    "debe completar la fecha exacta, la versión específica y la URL del chat en el "
    "momento de su entrega):",
    align="j",
)
tabla_datos([
    ["Herramienta", "Fecha de consulta", "Versión", "URL del chat", "Temática"],
    ["OpenCode (asistente de código con modelo GLM)", "(completar)",
     "(completar)", "(completar)", "Revisión del programa COBOL y armado del informe"],
], anchos=[4.0, 2.8, 2.4, 3.6, 3.2])
p(
    "Para qué se utilizó la IA: la herramienta se empleó como apoyo para revisar la "
    "estructura del programa COBOL, verificar el cumplimiento de los requerimientos "
    "de la consigna (organización indexada, validación de aperturas y ciclos de "
    "entrada) y dar formato al presente informe. La información proporcionada fue "
    "procesada y verificada por el estudiante: el código fuente, las pruebas de "
    "ejecución y las conclusiones fueron revisados, corregidos y validados "
    "personalmente antes de su inclusión en este trabajo.",
    align="j",
)

# ================= 8. ANEXO REPOSITORIO GIT =================
heading("8. Anexo: Repositorio del proyecto en Git", 1)
p(
    "Todo el material de este trabajo se encuentra versionado en un repositorio "
    "público de GitHub, utilizado como sistema de control de versiones durante el "
    "desarrollo. En él el evaluador puede consultar el historial completo de "
    "cambios (commits), el código fuente definitivo y la evolución del proyecto:",
    align="j",
)
p("https://github.com/jav978/tp-330-2")
tabla_datos([
    ["Archivo", "Descripción"],
    ["TP330.cbl", "Programa fuente principal (creación de archivos indexados)"],
    ["LEER330.cbl", "Programa de verificación: lee y muestra los registros grabados"],
    ["generar_tp330_docx.py", "Script que genera este informe en Word"],
    ["330_TP_14645240_2026-2.docx", "Entregable del Trabajo Práctico"],
], anchos=[5.5, 10.5])
p(
    "Cada confirmación (commit) incluye un mensaje descriptivo del cambio "
    "realizado, lo que permite evidenciar el proceso de depuración seguido: "
    "corrección de la organización del archivo a indexada, ajuste del lapso, "
    "captura del precio con el patrón REDEFINES y pruebas de ejecución con "
    "GnuCOBOL.",
    align="j",
)

# ================= 9. REFERENCIAS =================
heading("9. Referencias bibliográficas", 1)
for ref in [
    "Universidad Nacional Abierta. (2026). Instructivo del Trabajo Práctico, "
    "asignatura Procesamiento de Datos (Cód. 330), lapso 2026-2. Caracas: UNA, "
    "Vicerrectorado Académico.",
    "Stern, N. y Stern, R. (2006). COBOL (2ª ed.). México: Pearson Educación.",
    "Free Software Foundation. (2019). GnuCOBOL Programmer's Guide. Recuperado "
    "de https://gnucobol.sourceforge.io/doc/gnucobol.html",
    "OpenCobolIDE. (2016). OpenCobolIDE: Integrated Development Environment for "
    "COBOL. Recuperado de https://github.com/OpenCobolIDE/OpenCobolIDE",
]:
    par = doc.add_paragraph(ref)
    par.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    par.paragraph_format.first_line_indent = Cm(-0.75)
    par.paragraph_format.left_indent = Cm(0.75)

# ---------- guardar ----------
nombre = "330_TP_14645240_2026-2.docx"
doc.save(nombre)
print("Documento generado:", nombre)
