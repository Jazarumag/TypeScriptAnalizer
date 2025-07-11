import sys
import os
import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFileDialog, QProgressBar, QTextEdit, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer
import subprocess
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QFont, QFontDatabase


class TSAnalyzer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TSANALYZER")
        self.setGeometry(100, 100, 1000, 600)

        main_layout = QVBoxLayout()
        
        font_path = os.path.join(os.path.dirname(__file__), "font", "space.ttf")
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.setFont(QFont(font_family, 10))
        else:
            print(f"No se pudo cargar la fuente desde {font_path}")
        
        title = QLabel("TSANALYZER")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 70px; font-weight: bold; margin: 20px;")
        main_layout.addWidget(title)

        content_layout = QHBoxLayout()

        code_label = QLabel("Código a Analizar")
        code_label.setStyleSheet("font-size: 22px; font-weight: bold; color: white;")

        self.load_btn = QPushButton("Cargar Código")
        self.load_btn.clicked.connect(self.load_file)
        self.load_btn.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            background-color: #7357ff;
            color: white;
            padding: 6px 12px;
        """)
        self.load_btn.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)

        top_left_bar = QHBoxLayout()
        top_left_bar.addWidget(code_label)
        top_left_bar.addStretch()
        top_left_bar.addWidget(self.load_btn)

        self.code_view = QTextEdit()
        self.code_view.setReadOnly(True)
        self.code_view.setStyleSheet("background-color: #1e1e1e; color: white; font-size: 15px;")
        self.code_view.setPlaceholderText("Código TypeScript cargado...")

        left_layout = QVBoxLayout()
        left_layout.addLayout(top_left_bar)
        left_layout.addWidget(self.code_view)
        content_layout.addLayout(left_layout, 2)
        
        right_layout = QVBoxLayout()

        self.label_lex = QLabel("Analizador Léxico")
        self.label_lex.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.progress_lex = QProgressBar()
        right_layout.addWidget(self.label_lex)
        right_layout.addWidget(self.progress_lex)

        self.label_sin = QLabel("Analizador Sintáctico")
        self.label_sin.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.progress_sin = QProgressBar()
        right_layout.addWidget(self.label_sin)
        right_layout.addWidget(self.progress_sin)

        self.label_sem = QLabel("Analizador Semántico")
        self.label_sem.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.progress_sem = QProgressBar()
        right_layout.addWidget(self.label_sem)
        right_layout.addWidget(self.progress_sem)

        self.start_btn = QPushButton("Comenzar Análisis")
        self.start_btn.clicked.connect(self.run_analysis)
        self.start_btn.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            background-color: #7357ff;
            color: white;
            padding: 6px 12px;
        """)
        self.start_btn.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.start_btn)
        right_layout.addLayout(btn_layout)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setPlaceholderText("Resultados del análisis...")
        self.result_text.setStyleSheet("background-color: #1e1e1e; color: white; font-size: 15px;")
        right_layout.addWidget(self.result_text)

        content_layout.addLayout(right_layout, 2)

        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

        self.ts_file = None
        
        fondo = QPixmap("img/fondo.png")
        fondo = fondo.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(fondo))
        self.setPalette(palette)

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar archivo TypeScript", "", "Archivos TypeScript (*.ts)"
        )
        if file_path:
            self.ts_file = file_path
            with open(file_path, "r", encoding="utf-8") as f:
                contenido = f.read()
                self.code_view.setPlainText(contenido)
                self.result_text.clear()
                self.result_text.append(f"Archivo cargado: {os.path.basename(file_path)}")

    def run_analysis(self):
        if not self.ts_file:
            self.result_text.append("Debes cargar un archivo primero.")
            return

        os.system(f"cp '{self.ts_file}' algoritmo-1.ts")

        self.result_text.clear()
        self.progress_lex.setValue(0)
        self.progress_sin.setValue(0)
        self.progress_sem.setValue(0)

        file_name = os.path.splitext(os.path.basename(self.ts_file))[0]
        self.analyze("Léxico", [sys.executable, "lexicon.py", file_name], self.progress_lex, self.next_syntactic)   

    def analyze(self, label, script_args, progress_bar, callback_next):
        self.result_text.append(f"Ejecutando análisis {label}...")

        def simulate_progress():
            value = progress_bar.value()
            if value < 90:
                progress_bar.setValue(value + 10)
            else:
                timer.stop()
                self.execute_script(label, script_args, progress_bar, callback_next)


        timer = QTimer()
        timer.timeout.connect(simulate_progress)
        timer.start(100)

    def execute_script(self, label, script_args, progress_bar, callback_next):
        try:
            result = subprocess.run(
                script_args,
                capture_output=True,
                text=True,
                timeout=15
            )

            progress_bar.setValue(100)

            output = result.stdout.strip()
            if "ERROR" in output or "Syntax error" in output:
                self.result_text.append(f"Error en análisis {label}")
                for line in output.splitlines():
                    if "ERROR" in line or "Syntax error" in line:
                        self.result_text.append(line)
                return
            else:
                self.result_text.append(f"Análisis {label} completado con éxito")

                if callback_next:
                    callback_next()

        except subprocess.TimeoutExpired:
            self.result_text.append(f"{label} tardó demasiado.")
        except Exception as e:
            self.result_text.append(f"Fallo ejecutando {label}: {str(e)}")

    def next_syntactic(self):
        self.analyze("Sintáctico", "./sintactico.py", self.progress_sin, self.next_semantic)

    def next_semantic(self):
        self.analyze("Semántico", "./semantico.py", self.progress_sem, None)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TSAnalyzer()
    window.show()
    sys.exit(app.exec_())
