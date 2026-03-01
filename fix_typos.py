import os

REPLACEMENTS = {
    'Aplicație': 'Aplicație',
    'aplicație': 'aplicație',
    'Aplicației': 'Aplicației',
    'aplicației': 'aplicației',
    'Utilizați': 'Utilizați',
    'utilizați': 'utilizați',
    'funcțion': 'funcțion',
    'Funcțion': 'Funcțion',
    'garanție': 'garanție',
    'Garanție': 'Garanție',
    'informații': 'informații',
    'Informații': 'Informații',
    'Selecție': 'Selecție',
    'selecție': 'selecție',
    'Educație': 'Educație',
    'educație': 'educație',
    'Distribuție': 'Distribuție',
    'distribuție': 'distribuție',
    'Completați': 'Completați',
    'completați': 'completați',
    'Selectați': 'Selectați',
    'selectați': 'selectați',
    'Apăsați': 'Apăsați',
    'apăsați': 'apăsați',
    'Încărcați': 'Încărcați',
    'încărcați': 'încărcați',
    'Configurație': 'Configurație',
    'configurație': 'configurație',
    'locația': 'locația',
    'Locația': 'Locația',
    'locație': 'locație',
    'Locație': 'Locație',
    'detecție': 'detecție',
    'Detecție': 'Detecție',
    'corecție': 'corecție',
    'Corecție': 'Corecție',
    'atenție': 'atenție',
    'Atenție': 'Atenție',
    'conțin': 'conțin',
    'Conțin': 'Conțin',
    'opțiune': 'opțiune',
    'Opțiune': 'Opțiune',
    'opțiuni': 'opțiuni',
    'Opțiuni': 'Opțiuni',
    ' Ați ': ' Ați ',
    ' ați ': ' ați ',
    'Ați ': 'Ați ',
    'ați ': 'ați ',
    ' ați': ' ați',
    ' cți ': ' cți ', # dummy to keep comma
    ' cț': ' cț',
    ' pț': ' pț',
    'ecț': 'ecț',
    'cți ': 'cți ',
    'pți ': 'pți ',
    r'cție': 'cție',
    r'cția': 'cția',
    'Atenție': 'Atenție',
    'atenție': 'atenție',
    'intenție': 'intenție',
    'Intenție': 'Intenție',
    'situație': 'situație',
    ' Situație': ' Situație',
    'situații': 'situații',
    'rezoluție': 'rezoluție',
    'poziție': 'poziție',
    'Poziție': 'Poziție',
    'proporție': 'proporție',
    'Proporție': 'Proporție',
    'condiție': 'condiție',
    'Condiție': 'Condiție',
    'ediție': 'ediție',
    'Ediție': 'Ediție',
    'Tradiție': 'Tradiție',
    'tradiție': 'tradiție',
    ' spațiu': ' spațiu',
    ' Spațiu': ' Spațiu',
    'spațiul': 'spațiul',
    'soluție': 'soluție',
    'Soluție': 'Soluție',
    'instituție': 'instituție',
    'Instituție': 'Instituție',
    'Destinație': 'Destinație',
    'destinație': 'destinație',
    'Excepție': 'Excepție',
    'excepție': 'excepție',
    'Direcție': 'Direcție',
    'direcție': 'direcție',
    'Colecție': 'Colecție',
    'colecție': 'colecție',
    'Protecție': 'Protecție',
    'protecție': 'protecție',
    'Lecție': 'Lecție',
    'lecție': 'lecție',
    'Secție': 'Secție',
    'secție': 'secție',
    'Acțiune': 'Acțiune',
    'acțiune': 'acțiune',
    'acțiuni': 'acțiuni',
    'Acțiuni': 'Acțiuni',
}

base_dir = r"c:\Users\Administrator\Downloads\program expert"
changed_count = 0

for root, _, files in os.walk(base_dir):
    for fname in files:
        if fname.endswith('.py'):
            fpath = os.path.join(root, fname)
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            for bad, good in REPLACEMENTS.items():
                content = content.replace(bad, good)
            
            if content != original:
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(content)
                changed_count += 1
                diff = [l for l in content.splitlines() if 'ție' in l or 'ți' in l]
                print(f"Fixed {fname}")

print(f"Done. Fixed {changed_count} files.")
