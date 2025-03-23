       IDENTIFICATION DIVISION.
       PROGRAM-ID. BZHCOBOL.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 USER-CODE PIC X(20).
       01 CORRECT-CODE PIC X(20) VALUE "BZHCTF{CoB0l_4_3v3r}".
       01 WS-MESSAGE PIC X(50).
       
       PROCEDURE DIVISION.
       MAIN-PROCEDURE.
           DISPLAY "[BANK-SIMULATOR]".
           DISPLAY "Bienvenue dans le simulateur bancaire ultime !".
           DISPLAY " ".
           DISPLAY "Voici les etapes :".
           DISPLAY "1. Rendez-vous en physique (9h45-10h12 le mardi).".
           DISPLAY "2. Completez le dossier (bonne chance pour".
           DISPLAY "   comprendre les formulaires).".
           DISPLAY "3. Retournez voir votre conseiller".
           DISPLAY "   (si vous le retrouvez).".
           DISPLAY "4. Ce n'etait pas le bon dossier,".
           DISPLAY "   mais on vous l'avait dit, non ? Recommencez".
           DISPLAY "5. Payez les frais de dossier (x2).".
           DISPLAY "6. Une lettre devrait arriver d'ici 1-2 ans".
           DISPLAY "   (ou pas).".
           DISPLAY "7. Ouvrez-la, un code vous est peut-etre donne".
           DISPLAY "   (si la poste ne l'a pas egare).".
           DISPLAY "8. Saisissez le code ci-dessous pour acceder a".
           DISPLAY "   l'ultime verite.".
           DISPLAY " ".
           DISPLAY "SAISIR LE CODE > "
           ACCEPT USER-CODE.
           IF USER-CODE = CORRECT-CODE THEN
               MOVE "Bravo, vous avez triomphe de la bureaucratie !"
               TO WS-MESSAGE
           ELSE
               MOVE "Mauvais code ! Un formulaire supplementaire vous " 
               TO WS-MESSAGE
               MOVE "sera envoye." TO WS-MESSAGE
           END-IF.
           DISPLAY WS-MESSAGE.
           STOP RUN.
