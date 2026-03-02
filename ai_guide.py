# ai_guide.py


import re


from datetime import datetime





class LocalAIGuide:


    """Ghid local inteligent pentru aplicație - fără API, fără internet"""


    


    def __init__(self, parent_app):


        self.parent_app = parent_app


        self.current_step = 0


        self.tutorial_active = False


        self.conversation_history = []


        


        # Baza de cunoștințe - răspunsuri pre-definite


        self.knowledge_base = self._build_knowledge_base()


        


        # Tutorial pas-cu-pas


        self.tutorial_steps = self._build_tutorial()


        


        # Detectare probleme comune


        self.common_issues = self._build_common_issues()


    


    def _build_knowledge_base(self):


        """Construiește baza de cunoștințe cu răspunsuri"""


        return {


            # ===== ÎNCEPĂTORI =====


            "cum folosesc": """


╔══════════════════════════════════════════════════════════════════╗


║  GHID PAS CU PAS PENTRU ÎNCEPĂTORI                           ║


╚══════════════════════════════════════════════════════════════════╝





🎯 PROCESUL COMPLET ÎN 5 PAȘI:





📝 PAS 1: PREGĂTEȘTE TEMPLATE-UL WORD


   • Deschide Microsoft Word


   • Scrie documentul normal


   • Unde vrei date variabile, pune: {{NumeColoană}}


   • Exemplu: "Bună ziua, {{Nume}} {{Prenume}}!"


   • Salvează ca .docx





PAS 2: PREGĂTEȘTE FIȘIERUL EXCEL


   • Prima linie = numele coloanelor (EXACT ca în template!)


   • Fără {{}} în Excel, doar: Nume, Prenume, etc.


   • Fiecare rând = un document generat


   


   Exemplu Excel:


   | Nume    | Prenume | Functie  |


   |---------|---------|----------|


   | Popescu | Ion     | Manager  |


   | Ionescu | Maria   | Director |





⚙PAS 3: ÎN APLICAȚIE


   • Tab "Pasul 2: Generează documente"


   • Click "Alege fișier Excel" → selectează Excel-ul


   • Click "Alege dosar" → unde vrei documentele


   • Click "Adaugă fișiere" → selectează template-ul Word





PAS 4: GENEREAZĂ


   • Click "Generează documente" sau "Procesare în lot"


   • Așteaptă finalizarea


   • Verifică log-ul pentru erori





✅ PAS 5: VERIFICĂ REZULTATELE


   • Mergi în folder-ul de ieșire


   • Deschide documentele generate


   • Verifică că totul arată corect





💡 SFAT: Începe cu un Excel cu 2-3 rânduri pentru testare!





Vrei să începem tutorial-ul interactiv? (Scrie: "start tutorial")


""",





            # ===== TEMPLATE-URI =====


            "cum creez template": """


╔══════════════════════════════════════════════════════════════════╗


║  📝 CUM SĂ CREEZI UN TEMPLATE WORD CORECT                       ║


╚══════════════════════════════════════════════════════════════════╝





🎨 CREAREA TEMPLATE-ULUI:





1⃣ DESCHIDE WORD


   • Microsoft Word (nu WordPad!)


   • Document nou sau editează unul existent





2⃣ SCRIE CONȚINUTUL NORMAL


   • Scrie tot textul fix (care nu se schimbă)


   • Adaugă formatare: bold, italic, font, culori


   • Adaugă tabele, imagini, header, footer





3⃣ ADAUGĂ TAG-URI PENTRU DATE VARIABILE


   Sintaxă: {{NumeColoană}}


   


   ✅ CORECT:


   • {{Nume}}


   • {{Prenume}}


   • {{Data_Nasterii}}


   • {{Functie}}


   • {{Salariu}}


   


   ❌ GREȘIT:


   • {Nume} (un singur bracket)


   • {{ Nume }} (spații în interior)


   • {{nume}} vs {{Nume}} (case sensitive!)





4⃣ EXEMPLE PRACTICE:





   SCRISOARE:


   "


   Bună ziua, {{Titlu}} {{Nume}} {{Prenume}},


   


   Prin prezenta vă confirmăm funcția de {{Functie}}


   în cadrul departamentului {{Departament}}.


   


   Salariu: {{Salariu}} RON


   Data angajării: {{Data_Angajare}}


   


   Cu stimă,


   {{Manager_Nume}}


   "





   CERTIFICAT:


   "


   CERTIFICAT DE ABSOLVIRE


   


   Se certifică că {{Nume}} {{Prenume}}


   CNP: {{CNP}}


   


   A absolvit cursul de {{Nume_Curs}}


   în data de {{Data_Absolvire}}


   cu media {{Media}}.


   "





5⃣ VERIFICĂ TAG-URILE


   • Toate tag-urile trebuie să existe în Excel!


   • Ortografia trebuie să fie IDENTICĂ


   • {{Nume}} ≠ {{nume}} ≠ {{NUME}}





6⃣ SALVEAZĂ


   • Salvează ca .docx (nu .doc vechi!)


   • Dă un nume sugestiv: "Template_Scrisoare.docx"





💡 SFATURI:


   ✓ Testează cu 1-2 rânduri mai întâi


   ✓ Folosește Preview în aplicație


   ✓ Păstrează o copie a template-ului original





Ai alte întrebări despre template-uri?


""",





            # ===== EXCEL =====


            "format excel": """


╔══════════════════════════════════════════════════════════════════╗


║  CUM SĂ FORMATEZI CORECT FIȘIERUL EXCEL                      ║


╚══════════════════════════════════════════════════════════════════╝





REGULI PENTRU EXCEL:





1⃣ PRIMA LINIE = HEADER (Numele Coloanelor)


   ✅ CORECT:


   | Nume | Prenume | Functie | Salariu |


   


   ❌ GREȘIT:


   | {{Nume}} | {{Prenume}} | {{Functie}} | (NU pune {{}})


   | Nume     |              |              | (NU lăsa goale)





2⃣ RESTUL LINIILOR = DATE


   • Fiecare rând = un document generat


   • Completează TOATE celulele


   • Evită celule goale (pune "-" sau "N/A")


   


   Exemplu complet:


   | Nume    | Prenume | Functie  | Salariu | Data      |


   |---------|---------|----------|---------|-----------|


   | Popescu | Ion     | Manager  | 5000    | 15.01.2024|


   | Ionescu | Maria   | Director | 7000    | 20.02.2024|





3⃣ MATCH CU TEMPLATE-UL


   Excel:     Nume | Prenume | Functie


   Template:  {{Nume}} {{Prenume}} {{Functie}}


   


   ⚠TREBUIE SĂ FIE IDENTICE (case-sensitive)!





4⃣ TIPURI DE DATE ACCEPTATE:


   ✅ Text: "Popescu", "Manager"


   ✅ Numere: 5000, 123.45


   ✅ Date: 15.01.2024, 2024-01-15


   ✅ Caractere speciale: ă, â, î, ș, ț





5⃣ CE SĂ EVIȚI:


   ❌ Formule Excel (=SUM, =IF)


   ❌ Celule îmbinate (merged cells)


   ❌ Rânduri goale între date


   ❌ Formatare complexă (păstrează doar text)





6⃣ STRUCTURA RECOMANDATĂ:


   


   Rândul 1: HEADER (numele coloanelor)


   Rândurile 2-N: DATE (fără rânduri goale)


   


   BUNE PRACTICI:


   • Coloană "Nume_Fisier" pentru nume personalizat


   • Coloană "Departament" pentru sub-foldere


   • Păstrează o copie backup a Excel-ului





7⃣ FORMATE ACCEPTATE:


   ✅ .xlsx (recomandat)


   ✅ .xls


   ✅ .csv (encoding UTF-8!)





💡 VERIFICARE RAPIDĂ:


   1. Prima linie = nume coloane fără {{}}


   2. Toate coloanele au header


   3. Nu există celule goale


   4. Numele coloanelor match template-ul





Ai specificat corect Excel-ul?


""",





            # ===== ERORI =====


            "erori comune": """


╔══════════════════════════════════════════════════════════════════╗


║  ⚠ERORI COMUNE ȘI SOLUȚII                                     ║


╚══════════════════════════════════════════════════════════════════╝





🔴 EROARE: "KeyError: 'Nume'"


📝 Cauză: Tag-ul {{Nume}} din template nu există în Excel


✅ Soluție:


   1. Deschide Excel-ul


   2. Verifică prima linie (header)


   3. Asigură-te că există coloana "Nume" (exact!)


   4. {{Nume}} în template = "Nume" în Excel (case-sensitive)





🔴 EROARE: "Template nu conține tag-uri valide"


📝 Cauză: Template-ul nu are {{tag-uri}} corect formatate


✅ Soluție:


   1. Deschide template-ul Word


   2. Verifică că folosești {{}} (două acolade)


   3. Nu pune spații: {{Nume}} ✓, {{ Nume }} ✗


   4. Salvează și reîncearcă





🔴 EROARE: "Excel nu a fost încărcat"


📝 Cauză: Fișierul Excel este deschis sau corupt


✅ Soluție:


   1. Închide Excel-ul dacă este deschis


   2. Verifică că fișierul nu este Read-Only


   3. Încearcă să copiezi fișierul și folosește copia





🔴 EROARE: "Document generat este gol"


📝 Cauză: Excel are celule goale sau date lipsă


✅ Soluție:


   1. Verifică că toate celulele au date


   2. Pentru câmpuri opționale, pune "-" sau "N/A"


   3. Evită formule Excel în celule





🔴 EROARE: "Caractere ciudate în document (Ă → ‚)"


📝 Cauză: Probleme de encoding UTF-8


✅ Soluție:


   1. Activează "Curățare automată date" în Setări


   2. Salvează Excel ca .xlsx (nu .xls vechi)


   3. Pentru CSV: Save As → CSV UTF-8





🔴 PROBLEMA: "Generează prea încet"


📝 Cauză: Procesare secvențială


✅ Soluție:


   1. Activează "Procesare Paralelă" în Setări


   2. Activează "Mod Fast" și "Smart Cache" (dacă există)


   3. Folosește SSD pentru output folder





🔴 PROBLEMA: "Memoria se umple"


📝 Cauză: Prea multe documente mari


✅ Soluție:


   1. Reduce "Batch Size" în Setări


   2. Generează în loturi mai mici


   3. Închide alte aplicații





📱 VERIFICARE RAPIDĂ (CHECKLIST):


   ☐ Excel închis înainte de generare


   ☐ Template are {{tag-uri}} corecte


   ☐ Prima linie Excel = header-e


   ☐ Nume coloane match perfect cu tag-urile


   ☐ Nu există celule goale


   ☐ Template și Excel în locații accesibile





Ai întâmpinat o altă eroare? Descrie-o!


""",





            # ===== FUNCȚII AVANSATE =====


            "functii avansate": """


╔══════════════════════════════════════════════════════════════════╗


║  FUNCȚII AVANSATE ALE APLICAȚIEI                             ║


╚══════════════════════════════════════════════════════════════════╝





⚙SETĂRI DISPONIBILE:





1⃣ CONVERTIRE AUTOMATĂ PDF


   • Ce face: Convertește fiecare .docx generat în .pdf


   • Când: După generarea fiecărui document


   • Avantaj: Documente finale gata de distribuit


   • Necesită: docx2pdf (pip install docx2pdf)





2⃣ 🔗 MERGE DOCUMENTE (Document Master)


   • Ce face: Îmbină toate documentele într-unul singur


   • Rezultat: Un fișier "_MASTER_MERGED_*.docx"


   • Folositor: Pentru arhivare sau print masiv


   • Necesită: docxcompose (pip install docxcompose)





3⃣ 📦 ARHIVARE ZIP


   • Ce face: Creează un .zip cu toate documentele


   • Avantaj: Ușor de distribuit sau arhivat


   • Include: Toate .docx (și .pdf dacă sunt)





4⃣ 📁 SUB-FOLDERE AUTOMATE


   • Ce face: Organizează documentele pe foldere


   • Bazat pe: Coloane din Excel (ex: Departament)


   • Exemplu: 


     Output/


       ├─ IT/


       │   ├─ Popescu_Ion.docx


       │   └─ Marinescu_Ana.docx


       └─ HR/


           └─ Ionescu_Maria.docx





5⃣ ⚡ PROCESARE PARALELĂ


   • Ce face: Generează mai multe documente simultan


   • Viteză: Până la 4-5x mai rapid!


   • CPU: Folosește toate core-urile procesorului


   • Recomandat: Pentru 50+ documente





6⃣ 🛡AUTO-RECOVERY


   • Ce face: Salvează progresul periodic


   • Permite reluarea generării de unde a rămas


   • Checkpoint-uri în folderul "checkpoints/"





7⃣ 📈 DASHBOARD STATISTICI


   • Unde: Tab "📈 DASHBOARD"


   • Afișează:


     - Număr rânduri și coloane


     - Celule goale


     - Grafic distribuție


     - Statistici de generare





💡 COMBINAȚII RECOMANDATE:





Pentru VITEZĂ MAXIMĂ:


✓ Procesare Paralelă


✓ Auto-Recovery activat





Pentru ARHIVARE COMPLETĂ:


✓ Convert to PDF


✓ Merge Documents


✓ Create ZIP





Pentru ORGANIZARE:


✓ Subfolder după coloană


✓ Pattern numire personalizat





Ce funcție vrei să explorezi în detaliu?


""",





            # ===== TUTORIAL =====


            "tutorial": """


╔══════════════════════════════════════════════════════════════════╗


║  TUTORIAL INTERACTIV - PAS CU PAS                            ║


╚══════════════════════════════════════════════════════════════════╝





Bine ai venit la tutorial-ul interactiv! 👋





Voi să te ghidez prin procesul complet de generare documente.


La fiecare pas, îți voi spune exact ce să faci.





STRUCTURA TUTORIAL-ULUI:


   1. Pregătire Template Word


   2. Pregătire Excel


   3. Configurare Aplicație


   4. Generare Documente


   5. Verificare Rezultate





⏱Durată: ~10 minute





🎯 La final vei știi să:


   ✓ Creezi template-uri profesionale


   ✓ Formatezi corect Excel-ul


   ✓ Configurezi toate setările


   ✓ Rezolvi probleme comune





Ești gata să începem? 


Scrie: "DA" sau "START" pentru a începe primul pas!


""",


        }


    


    def _build_tutorial(self):


        """Construiește pașii tutorial-ului interactiv"""


        return [


            {


                "title": "PAS 1: PREGĂTIRE TEMPLATE WORD",


                "content": """


╔══════════════════════════════════════════════════════════════════╗


║  📝 PAS 1/5: PREGĂTIRE TEMPLATE WORD                            ║


╚══════════════════════════════════════════════════════════════════╝





Hai să creăm primul template!





CE TREBUIE SĂ FACI:





1. Deschide Microsoft Word (nu OpenOffice, nu WordPad)


2. Creează un document nou


3. Scrie următorul text:





   ═══════════════════════════════════════


   


   CONFIRMARE PARTICIPARE


   


   Bună ziua, {{Titlu}} {{Nume}} {{Prenume}},


   


   Confirmăm participarea dumneavoastră la:


   


   Eveniment: {{Eveniment}}


   Data: {{Data}}


   Locație: {{Locatie}}


   


   Funcție: {{Functie}}


   Departament: {{Departament}}


   


   Vă așteptăm cu drag!


   


   ═══════════════════════════════════════





4. IMPORTANT: Copiază exact textul de mai sus!


5. {{...}} înseamnă "aici va veni data din Excel"


6. Salvează documentul ca: "Template_Tutorial.docx"


7. Reține unde l-ai salvat (Desktop recomandat)





✅ Când ai terminat, scrie: "GATA PAS 1"


❓ Dacă ai probleme, scrie: "AJUTOR"


""",


                "next_keywords": ["gata", "pas 1", "terminat", "ready"],


                "help": "Asigură-te că folosești Word, nu alt editor. Tag-urile trebuie să aibă {{ și }} (două acolade)."


            },


            {


                "title": "PAS 2: PREGĂTIRE EXCEL",


                "content": """


╔══════════════════════════════════════════════════════════════════╗


║  PAS 2/5: PREGĂTIRE EXCEL                                    ║


╚══════════════════════════════════════════════════════════════════╝





Acum creăm fișierul Excel cu datele!





CE TREBUIE SĂ FACI:





1. Deschide Microsoft Excel (sau Google Sheets apoi exportă)


2. În PRIMA LINIE scrie (EXACT ca mai jos):


   


   A1: Titlu


   B1: Nume  


   C1: Prenume


   D1: Eveniment


   E1: Data


   F1: Locatie


   G1: Functie


   H1: Departament





3. În rândurile 2-3 pune date de test:





   Rând 2:


   A2: Dl.    B2: Popescu   C2: Ion       D2: Conferință IT


   E2: 15.03.2024   F2: București   G2: Manager   H2: IT





   Rând 3:


   A3: Dna.   B3: Ionescu   C3: Maria     D3: Conferință IT


   E3: 15.03.2024   F3: București   G3: Director  H3: HR





4. Salvează ca: "Date_Tutorial.xlsx"


5. Reține unde l-ai salvat (Desktop recomandat)





⚠VERIFICĂ:


   ☐ Prima linie = header-e (Titlu, Nume, etc.)


   ☐ NU ai pus {{}} în Excel!


   ☐ Toate celulele au date (nu există goale)





✅ Când ai terminat, scrie: "GATA PAS 2"


❓ Dacă ai probleme, scrie: "AJUTOR"


""",


                "next_keywords": ["gata", "pas 2", "terminat", "ready"],


                "help": "Prima linie = doar numele coloanelor, fără {{}}. Fiecare rând = un document."


            },


            {


                "title": "PAS 3: CONFIGURARE APLICAȚIE",


                "content": """


╔══════════════════════════════════════════════════════════════════╗


║  ⚙PAS 3/5: CONFIGURARE APLICAȚIE                              ║


╚══════════════════════════════════════════════════════════════════╝





Acum configurăm aplicația!





CE TREBUIE SĂ FACI:





1. Mergi la tab-ul "Pasul 2: Generează documente"





2. SECȚIUNEA "Fișier Excel completat":


   ├─ Click "Alege fișier"


   └─ Selectează "Date_Tutorial.xlsx"





3. SECȚIUNEA "Dosar pentru documentele generate":


   ├─ Click "Alege dosar"


   └─ Creează un folder nou "Rezultate_Tutorial" pe Desktop


   └─ Selectează-l





4. SECȚIUNEA "Fișiere șablon":


   ├─ Click "Adaugă fișiere"


   └─ Selectează "Template_Tutorial.docx"





5. VERIFICĂ LOG-UL:


   ├─ Ar trebui să vezi fișierele adăugate





⚙SETĂRI OPȚIONALE (le poți lăsa implicite):





✅ Când ai configurat tot, scrie: "GATA PAS 3"


❓ Dacă ai probleme, scrie: "AJUTOR"


""",


                "next_keywords": ["gata", "pas 3", "terminat", "configurat"],


                "help": "Asigură-te că toate cele 3 componente sunt selectate: Excel, Folder Output, Template."


            },


            {


                "title": "PAS 4: GENERARE DOCUMENTE",


                "content": """


╔══════════════════════════════════════════════════════════════════╗


║  PAS 4/5: GENERARE DOCUMENTE                                 ║


╚══════════════════════════════════════════════════════════════════╝





E momentul magic! Generăm documentele! 🎉





CE TREBUIE SĂ FACI:





1. Verifică că ești în tab-ul "Pasul 2: Generează documente"





2. Verifică CHECKLIST-UL:


   ☐ Excel selectat ✓


   ☐ Folder output selectat ✓


   ☐ Template adăugat ✓





3. Click pe butonul "Generează documente"





4. URMĂREȘTE PROCESUL:


   ├─ Progress bar-ul va arăta avansul


   ├─ Log-ul va afișa fiecare pas


   └─ La final, vei vedea "Generare finalizată!"





5. AȘTEAPTĂ finalizarea (câteva secunde)





⚠DACĂ APARE O EROARE:


   • Citește mesajul de eroare


   • Scrie "AJUTOR" pentru diagnostic





✅ Când generarea este completă, scrie: "GATA PAS 4"


❓ Dacă ai probleme, scrie: "AJUTOR"


""",


                "next_keywords": ["gata", "pas 4", "terminat", "generat"],


                "help": "Dacă apar erori, cel mai probabil numele coloanelor din Excel nu match tag-urile din template."


            },


            {


                "title": "PAS 5: VERIFICARE REZULTATE",


                "content": """


╔══════════════════════════════════════════════════════════════════╗


║  ✅ PAS 5/5: VERIFICARE REZULTATE                               ║


╚══════════════════════════════════════════════════════════════════╝





Ultimul pas! Verificăm ce am generat! 🎊





CE TREBUIE SĂ FACI:





1. Deschide File Explorer / Finder





2. Navighează la folder-ul "Rezultate_Tutorial" (Desktop)





3. AR TREBUI SĂ VEZI 2 FIȘIERE:


   ├─ Popescu_Ion.docx


   └─ Ionescu_Maria.docx





4. DESCHIDE primul document (Popescu_Ion.docx):


   


   Ar trebui să conțină:


   


   ═══════════════════════════════════════


   


   CONFIRMARE PARTICIPARE


   


   Bună ziua, Dl. Popescu Ion,


   


   Confirmăm participarea dumneavoastră la:


   


   Eveniment: Conferință IT


   Data: 15.03.2024


   Locație: București


   


   Funcție: Manager


   Departament: IT


   


   Vă așteptăm cu drag!


   


   ═══════════════════════════════════════





5. VERIFICĂ că:


   ☐ Toate {{tag-urile}} au fost înlocuite cu date


   ☐ NU mai apar {{}} în document


   ☐ Datele sunt corecte


   ☐ Formatarea arată bine





6. Deschide și al doilea document pentru verificare





🎉 FELICITĂRI! AI TERMINAT TUTORIAL-UL! 🎉





Acum știi să:


   ✓ Creezi template-uri Word cu tag-uri


   ✓ Formatezi corect Excel-ul


   ✓ Configurezi aplicația


   ✓ Generezi documente personalizate


   ✓ Verifici rezultatele





PAȘI URMĂTORI:


   • Creează propriile template-uri pentru nevoile tale


   • Explorează funcțiile avansate (PDF, Merge, ZIP)


   • Generează documente reale pentru proiectele tale





💡 SFATURI FINALE:


   • Păstrează template-urile într-un folder dedicat


   • Fă backup la Excel-urile cu date


   • Testează întotdeauna cu 2-3 rânduri înainte de generare mare


   • Folosește "Preview" pentru verificare rapidă





✅ Scrie: "MULTUMESC" pentru a încheia tutorial-ul


❓ Sau scrie orice întrebare ai despre aplicație!


""",


                "next_keywords": ["multumesc", "gata", "terminat", "finish"],


                "help": "Dacă documentele nu arată corect, verifică din nou Excel-ul și template-ul."


            }


        ]


    


    def _build_common_issues(self):


        """Detectare și soluții pentru probleme comune"""


        return {


            "keyerror": {


                "problema": "Tag-ul {{X}} nu există în Excel",


                "cauze": [


                    "Numele coloanei în Excel diferă de tag-ul din template",


                    "Ai uitat să pui coloana în Excel",


                    "Diferență de case ({{Nume}} vs {{nume}})"


                ],


                "solutii": [


                    "1. Deschide Excel-ul și verifică prima linie (header)",


                    "2. Compară EXACT cu tag-urile din template",


                    "3. Asigură-te că există coloana cu acelați nume",


                    "4. Case-sensitive: {{Nume}} ≠ {{nume}}"


                ]


            },


            "template_gol": {


                "problema": "Template-ul nu conține tag-uri",


                "cauze": [


                    "Ai uitat să pui {{tag-uri}} în template",


                    "Folosești { } în loc de {{ }}",


                    "Template-ul este un document gol"


                ],


                "solutii": [


                    "1. Deschide template-ul Word",


                    "2. Verifică că ai {{tag-uri}} cu două acolade",


                    "3. Sintaxa corectă: {{NumeColoană}}",


                    "4. Salvează și reîncearcă"


                ]


            },


            "excel_locked": {


                "problema": "Nu poate citi Excel-ul",


                "cauze": [


                    "Excel-ul este deschis în alt program",


                    "Fișierul este Read-Only",


                    "Nu ai permisiuni de citire"


                ],


                "solutii": [


                    "1. Închide Excel-ul dacă este deschis",


                    "2. Click dreapta pe fișier → Properties → Debifează Read-Only",


                    "3. Copiază fișierul și folosește copia",


                    "4. Verifică permisiunile de acces"


                ]


            }


        }


    


    def get_response(self, user_input: str) -> str:


        """Generează răspuns bazat pe input utilizator"""


        user_input = user_input.lower().strip()


        


        # Adaugă în istoric


        self.conversation_history.append(user_input)


        


        # Tutorial activ - navighează prin pași


        if self.tutorial_active:


            return self._handle_tutorial_step(user_input)


        


        # Start tutorial


        if "tutorial" in user_input or "start" in user_input:


            return self._start_tutorial()


        


        # Detectare întrebări despre început/cum folosesc


        if any(word in user_input for word in ["cum folosesc", "cum incep", "ghid", "pas cu pas", "începător"]):


            return self.knowledge_base["cum folosesc"]


        


        # Template-uri


        if any(word in user_input for word in ["template", "creez", "tag", "{{"]):


            return self.knowledge_base["cum creez template"]


        


        # Excel


        if any(word in user_input for word in ["excel", "format", "coloana", "celula"]):


            return self.knowledge_base["format excel"]


        


        # Erori


        if any(word in user_input for word in ["eroare", "error", "problema", "nu merge", "nu funcționează"]):


            return self.knowledge_base["erori comune"]


        


        # Funcții avansate


        if any(word in user_input for word in ["avansat", "pdf", "merge", "zip", "paralel", "funcții"]):


            return self.knowledge_base["functii avansate"]


        


        # Default - răspuns general


        return self._get_default_response(user_input)


    


    def _start_tutorial(self):


        """Inițiază tutorial-ul interactiv"""


        self.tutorial_active = True


        self.current_step = 0


        return self.knowledge_base["tutorial"]


    


    def _handle_tutorial_step(self, user_input: str) -> str:


        """Gestionează pașii tutorial-ului"""


        # Verifică dacă userul vrea să oprească tutorial-ul


        if any(word in user_input for word in ["stop", "oprește", "ieși", "exit", "quit"]):


            self.tutorial_active = False


            return "\n✋ Tutorial oprit.\n\nPoți relua oricând scriind: 'tutorial'\n\nCu ce te pot ajuta?"


        


        # Verifică dacă userul cere ajutor


        if "ajutor" in user_input or "help" in user_input:


            current = self.tutorial_steps[self.current_step]


            return f"\n💡 AJUTOR pentru {current['title']}:\n\n{current.get('help', 'Urmează instrucțiunile pas cu pas.')}\n"


        


        # Verifică dacă userul e gata să treacă la următorul pas


        if self.current_step < len(self.tutorial_steps):


            current = self.tutorial_steps[self.current_step]


            


            # Verifică keyword-uri pentru avansare


            if any(kw in user_input for kw in current.get('next_keywords', [])):


                self.current_step += 1


                


                # Verifică dacă mai sunt pași


                if self.current_step < len(self.tutorial_steps):


                    next_step = self.tutorial_steps[self.current_step]


                    return f"\n✅ Perfect! Să trecem mai departe!\n\n{next_step['content']}"


                else:


                    # Tutorial terminat


                    self.tutorial_active = False


                    return """


╔══════════════════════════════════════════════════════════════════╗


║  🎉 FELICITĂRI! AI TERMINAT TUTORIAL-UL!                        ║


╚══════════════════════════════════════════════════════════════════╝





Bravo! 👏 Acum știi să folosești aplicația!





CE AI ÎNVĂȚAT:


   ✓ Creare template-uri Word cu tag-uri


   ✓ Formatare corectă Excel


   ✓ Configurare aplicație


   ✓ Generare documente


   ✓ Verificare rezultate





ACUM POȚI:


   • Crea propriile template-uri


   • Genera sute/mii de documente automat


   • Folosi funcții avansate (PDF, Merge, etc.)


   • Rezolva probleme comune





💡 DACĂ AI NEVOIE DE AJUTOR:


   • Scrie întrebarea ta


   • Eu sunt aici 24/7! 





Cu ce te pot ajuta acum?


"""


            else:


                # Nu a dat keyword corect, reamintește ce trebuie să facă


                return f"\n⏳ Aștept să finalizezi {current['title']}.\n\nCând ai terminat, scrie: 'GATA'\n\nSau scrie 'AJUTOR' dacă ai nevoie de suport."


        


        # Dacă ajunge aici, tutorial-ul e finalizat


        self.tutorial_active = False


        return "\nTutorial-ul s-a încheiat. Cu ce te pot ajuta?"


    


    def _get_default_response(self, user_input: str) -> str:


        """Răspuns default când nu se potrivește nimic"""


        suggestions = []


        


        # Sugestii bazate pe cuvinte cheie


        if any(word in user_input for word in ["ajutor", "help"]):


            suggestions = [


                "- 'cum folosesc' - ghid complet pentru începători",


                "- 'tutorial' - tutorial interactiv pas cu pas",


                "- 'cum creez template' - despre template-uri Word",


                "- 'format excel' - cum să formatez Excel-ul",


                "- 'erori comune' - rezolvare probleme",


                "- 'funcții avansate' - PDF, merge, ZIP, etc."


            ]


        


        response = """


╔══════════════════════════════════════════════════════════════════╗


║  NU AM ÎNȚELES EXACT ÎNTREBAREA                              ║


╚══════════════════════════════════════════════════════════════════╝





Încearcă să reformulezi sau alege din:





GHIDURI DISPONIBILE:


   • "cum folosesc" - Ghid complet începători


   • "tutorial" - Tutorial interactiv pas cu pas


   • "cum creez template" - Despre template-uri Word


   • "format excel" - Formatare corectă Excel


   • "erori comune" - Probleme și soluții


   • "funcții avansate" - PDF, Merge, ZIP, etc.





💡 SAU FOLOSEȘTE BUTOANELE RAPIDE de mai jos!





Ce vrei să știi?


"""


        


        if suggestions:


            response += "\n\n🎯 SUGESTII:\n" + "\n".join(suggestions)


        


        return response


    


    def get_contextual_help(self, context: str) -> str:


        """Oferă ajutor contextual bazat pe unde se află utilizatorul"""


        contexts = {


            "main_tab": """


💡 AJUTOR RAPID - Tab "Pasul 2: Generează documente":





Pașii de urmat:


1⃣ Selectează Excel cu date


2⃣ Alege folder pentru rezultate


3⃣ Adaugă template(uri) Word


4⃣ Click "Generează documente"





⚠VERIFICĂ ÎNAINTE:


   ☐ Excel are prima linie cu nume coloane


   ☐ Template are {{tag-uri}} corecte


   ☐ Numele coloanelor match tag-urile





Scrie 'erori comune' pentru probleme frecvente!


""",


            "excel_tab": """


💡 AJUTOR RAPID - Tab "Vizualizare Excel":





Aici poți:


   • Vezi toate datele din Excel


   • Sortezi coloanele


   • Cauți în date


   • Editezi valori (dublu-click)


   • Exporți ca CSV





💡 SFAT: Folosește această vedere pentru a verifica datele


înainte de generare!





Scrie 'format excel' pentru detalii despre structură!


""",


            "settings": """


💡 AJUTOR RAPID - SETĂRI:





⚙SETĂRI DISPONIBILE:


   • Convert to PDF - Generează și PDF-uri


   • Merge Documents - Îmbină toate doc-urile


   • Create ZIP - Arhivă automată


   • Parallel Processing - Procesare rapidă





Scrie 'funcții avansate' pentru detalii complete!


"""


        }


        


        return contexts.get(context, "Scrie o întrebare sau alege din butoanele rapide!")


    


    def diagnose_error(self, error_message: str) -> str:


        """Diagnostichează o eroare și oferă soluții"""


        error_lower = error_message.lower()


        


        if "keyerror" in error_lower:


            issue = self.common_issues["keyerror"]


            return f"""


╔══════════════════════════════════════════════════════════════════╗


║  🔴 DIAGNOSTIC EROARE: {issue['problema']}


╚══════════════════════════════════════════════════════════════════╝





❓ CAUZE POSIBILE:


{chr(10).join('   • ' + c for c in issue['cauze'])}





✅ SOLUȚII:


{chr(10).join('   ' + s for s in issue['solutii'])}





💡 EXEMPLU CORECT:


   Excel (prima linie): | Nume | Prenume | Functie |


   Template Word: Bună {{Nume}} {{Prenume}}, {{Functie}}


   


   ⚠Trebuie să fie IDENTICE (case-sensitive)!





Ai rezolvat? Sau ai nevoie de mai multe detalii?


"""


        


        elif "template" in error_lower and "tag" in error_lower:


            issue = self.common_issues["template_gol"]


            return f"""


╔══════════════════════════════════════════════════════════════════╗


║  🔴 DIAGNOSTIC EROARE: {issue['problema']}


╚══════════════════════════════════════════════════════════════════╝





❓ CAUZE POSIBILE:


{chr(10).join('   • ' + c for c in issue['cauze'])}





✅ SOLUȚII:


{chr(10).join('   ' + s for s in issue['solutii'])}





Scrie 'cum creez template' pentru ghid detaliat!


"""


        


        elif "excel" in error_lower:


            issue = self.common_issues["excel_locked"]


            return f"""


╔══════════════════════════════════════════════════════════════════╗


║  🔴 DIAGNOSTIC EROARE: {issue['problema']}


╚══════════════════════════════════════════════════════════════════╝





❓ CAUZE POSIBILE:


{chr(10).join('   • ' + c for c in issue['cauze'])}





✅ SOLUȚII:


{chr(10).join('   ' + s for s in issue['solutii'])}





Scrie 'format excel' pentru ghid detaliat!


"""


        


        return """


╔══════════════════════════════════════════════════════════════════╗


║  🔴 DIAGNOSTIC EROARE                                            ║


╚══════════════════════════════════════════════════════════════════╝





Nu am putut identifica automat eroarea.





PAȘI DE DEPANARE:





1⃣ VERIFICĂ LOG-UL:


   • Citește mesajul complet de eroare


   • Notează ce rând/document a dat eroarea





2⃣ VERIFICĂRI RAPIDE:


   ☐ Excel închis?


   ☐ Template are {{tag-uri}}?


   ☐ Coloanele Excel match tag-urile?


   ☐ Nu există celule goale?





3⃣ ÎNCEARCĂ:


   • Generează doar primul rând (testare)


   • Verifică template-ul în Preview


   • Compară Excel cu tag-urile





💡 Descrie-mi eroarea în detaliu și te ajut!


Sau scrie 'erori comune' pentru lista completă.


"""
    def _build_enterprise_knowledge(self):
        return {
            "statistici enterprise": """
Aplicația oferă acum analize avansate pentru:
1. Academic: Identificare automată Studenți, Masteranzi, Doctoranzi.
2. Cercetare: Distribuție pe grade (CSI, CSII, etc.).
3. Integritate: Audit pentru celule goale și cereri de asistență.
4. Activități: Monitorizare participare pe activități de proiect.
""",
            "scripting multi": """
Puteți activa mai multe scripturi simultan.
Folosiți butonul 'Adaugă Script' pentru a stivui procesările (ex: Uppercase + Semicolon Convert).
"""
        }
