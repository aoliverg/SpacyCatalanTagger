from PyInstaller.utils.hooks import get_package_paths, collect_data_files

# 1. Obtenim la ruta del paquet ca_core_news_sm
# Aquesta funció fa la mateixa feina que buscar la ruta manualment
package_path = get_package_paths('ca_core_news_sm')[0]

# 2. Copiem tots els fitxers d'aquest paquet (el model)
datas = collect_data_files('ca_core_news_sm', include_py_files=True)

# 3. Afegeix la ruta del model a les dades, assegurant-se que es copia 
# amb el mateix nom de directori intern (ca_core_news_sm)
datas.extend([(package_path[1], 'ca_core_news_sm')]) 

# Llista de dades que PyInstaller ha d'incloure
hiddenimports = ['ca_core_news_sm']
'''
eof

### 2. Utilitza la Comanda PyInstaller Corregida

Ara, utilitza la comanda PyInstaller apuntant a aquest nou hook amb l'opció `--additional-hooks-dir`. Aquesta comanda és molt més neta i fiable que l'anterior amb `--add-data`.

**Comanda de PyInstaller:**

```bash
pyinstaller --onefile --additional-hooks-dir=. SpacyCatalanTagger.py
'''