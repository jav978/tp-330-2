       IDENTIFICATION DIVISION.
       PROGRAM-ID. LEER330.
      *----------------------------------------------------------------*
      * Programa de verificacion: lee y muestra los registros de los   *
      * archivos indexados MAESTRO-PROD.DAT y PROVEEDORES.DAT.          *
      *----------------------------------------------------------------*
       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT MAESTRO-PRODFI ASSIGN TO "MAESTRO-PROD.DAT"
                  ORGANIZATION IS INDEXED
                  ACCESS MODE IS DYNAMIC
                  RECORD KEY IS RP-ID-PRODUCTO
                  FILE STATUS IS WS-FS-PROD.
           SELECT PROVEEDORES ASSIGN TO "PROVEEDORES.DAT"
                  ORGANIZATION IS INDEXED
                  ACCESS MODE IS DYNAMIC
                  RECORD KEY IS RP-ID-PROVEEDOR
                  FILE STATUS IS WS-FS-PROV.

       DATA DIVISION.
       FILE SECTION.
       FD  MAESTRO-PRODFI.
       01  REG-PRODUCTO.
           05 RP-ID-PRODUCTO        PIC 9(05).
           05 RP-NOMBRE-PRODUCTO    PIC X(20).
           05 RP-STOCK-ACTUAL       PIC 9(04).
           05 RP-PRECIO-UNITARIO    PIC 9(04)V99.
       FD  PROVEEDORES.
       01  REG-PROVEEDOR.
           05 RP-ID-PROVEEDOR       PIC 9(03).
           05 RP-NOMBRE-EMPRESA     PIC X(25).
           05 RP-CIUDAD-PROV        PIC X(15).

       WORKING-STORAGE SECTION.
       01  WS-FS-PROD               PIC XX.
       01  WS-FS-PROV               PIC XX.
       01  WS-CONT                  PIC X.
       01  WS-PRECIO-ED             PIC ZZ,ZZ9.99.

       PROCEDURE DIVISION.
       000-PRINCIPAL.
           OPEN INPUT MAESTRO-PRODFI
           IF WS-FS-PROD NOT = "00"
               DISPLAY "ERROR ABRIENDO MAESTRO-PROD.DAT STATUS="
                   WS-FS-PROD
               GO TO 100-PROVEEDORES
           END-IF
           DISPLAY "=== CONTENIDO DE MAESTRO-PROD.DAT ==="
           DISPLAY "ID    NOMBRE               STOCK PRECIO"
           MOVE "N" TO WS-CONT
           READ MAESTRO-PRODFI NEXT
               AT END MOVE "S" TO WS-CONT
           END-READ
           PERFORM UNTIL WS-CONT = "S"
               MOVE RP-PRECIO-UNITARIO TO WS-PRECIO-ED
               DISPLAY RP-ID-PRODUCTO " " RP-NOMBRE-PRODUCTO
                       " " RP-STOCK-ACTUAL "  " WS-PRECIO-ED
               READ MAESTRO-PRODFI NEXT
                   AT END MOVE "S" TO WS-CONT
               END-READ
           END-PERFORM
           CLOSE MAESTRO-PRODFI.

       100-PROVEEDORES.
           OPEN INPUT PROVEEDORES
           IF WS-FS-PROV NOT = "00"
               DISPLAY "ERROR ABRIENDO PROVEEDORES.DAT STATUS="
                   WS-FS-PROV
               STOP RUN
           END-IF
           DISPLAY "=== CONTENIDO DE PROVEEDORES.DAT ==="
           DISPLAY "ID  EMPRESA                  CIUDAD"
           MOVE "N" TO WS-CONT
           READ PROVEEDORES NEXT
               AT END MOVE "S" TO WS-CONT
           END-READ
           PERFORM UNTIL WS-CONT = "S"
               DISPLAY RP-ID-PROVEEDOR " " RP-NOMBRE-EMPRESA
                       " " RP-CIUDAD-PROV
               READ PROVEEDORES NEXT
                   AT END MOVE "S" TO WS-CONT
               END-READ
           END-PERFORM
           CLOSE PROVEEDORES
           STOP RUN.
