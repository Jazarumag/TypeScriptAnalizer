# TypeScript Analyzer

Este proyecto es un **analizador léxico, sintáctico y semántico** para el lenguaje **TypeScript**, desarrollado en Python con la biblioteca **PLY (Python Lex-Yacc)**. El análisis se presenta mediante una interfaz gráfica implementada con **PyQt5**.

## Requisitos

Asegúrate de tener instalado Python 3.7 o superior. Luego, instala las dependencias necesarias con:

```bash
pip install ply pyqt5
```

## Estructura del Proyecto

- `lexicon.py`: Analizador léxico.
- `sintactico.py`: Analizador sintáctico.
- `semantico.py`: Analizador semántico.
- `tsanalyzer_gui.py`: Interfaz gráfica para cargar archivos `.ts` y visualizar los resultados.
- `algoritmo-1.ts`, `algoritmo-2.ts`, `algoritmo-3.ts`: Archivos de prueba.
- `logs/`: Carpeta donde se generan los logs de cada ejecución.
- `font/`: Contiene la fuente personalizada utilizada por la GUI.
- `img/`: Imágenes decorativas para la interfaz.

## Ejecución

1. Clona este repositorio o descomprímelo en tu equipo.
2. Instala las dependencias:

```bash
pip install ply pyqt5
```

3. Ejecuta la interfaz gráfica:

```bash
python tsanalyzer_gui.py
```

4. Usa el botón **“Subir archivo”** para cargar un archivo TypeScript `.ts`, luego haz clic en **“Comenzar análisis”** para visualizar los resultados léxico, sintáctico y semántico.
