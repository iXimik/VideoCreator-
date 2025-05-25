import os
import sys
import subprocess
import re
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QPushButton, QLabel, QFileDialog, QLineEdit,
                            QMessageBox, QProgressBar, QListWidget, QHBoxLayout)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from datetime import datetime


class VideoCreatorThread(QThread):
    progress_updated = pyqtSignal(int)
    finished = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, images, output_path, fps, crf):
        super().__init__()
        self.images = images
        self.output_path = output_path
        self.fps = fps
        self.crf = crf

    def run(self):
        try:
            # Сортируем изображения по номеру кадра перед созданием видео
            self.images.sort(key=lambda x: self.extract_frame_number(x))
            
            # Создаем временный файл со списком изображений
            list_file = os.path.join(os.path.dirname(self.output_path), "ffmpeg_list.txt")
            
            with open(list_file, 'w', encoding='utf-8') as f:
                for img in self.images:
                    f.write(f"file '{os.path.abspath(img)}'\nduration {1/float(self.fps)}\n")

            # Команда FFmpeg
            cmd = [
                'ffmpeg',
                '-f', 'concat',
                '-safe', '0',
                '-i', list_file,
                '-r', str(self.fps),
                '-c:v', 'libx264',
                '-pix_fmt', 'yuv420p',
                '-crf', str(self.crf),
                '-preset', 'fast',
                '-y',
                os.path.abspath(self.output_path)
            ]

            process = subprocess.Popen(
                cmd,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            while True:
                line = process.stderr.readline()
                if not line and process.poll() is not None:
                    break
                if 'frame=' in line:
                    try:
                        frame = int(line.split('frame=')[1].split()[0])
                        progress = min(100, int((frame / len(self.images)) * 100))
                        self.progress_updated.emit(progress)
                    except:
                        pass

            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, cmd)

            if not os.path.exists(self.output_path):
                raise Exception("Видеофайл не был создан")

            self.finished.emit(os.path.abspath(self.output_path))

        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            if os.path.exists(list_file):
                os.remove(list_file)

    def extract_frame_number(self, filename):
        """Извлекает номер кадра из имени файла"""
        match = re.search(r'frame_(\d+)', os.path.basename(filename))
        return int(match.group(1)) if match else 0


class FileSelectionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        layout = QHBoxLayout()
        
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.ExtendedSelection)
        self.file_list.setSortingEnabled(False)  # Отключаем стандартную сортировку
        
        self.select_all_btn = QPushButton("Выбрать все")
        self.select_all_btn.clicked.connect(self.select_all)
        
        self.clear_selection_btn = QPushButton("Сбросить")
        self.clear_selection_btn.clicked.connect(self.clear_selection)
        
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.select_all_btn)
        button_layout.addWidget(self.clear_selection_btn)
        button_layout.addStretch()
        
        layout.addWidget(self.file_list)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def select_all(self):
        self.file_list.selectAll()
    
    def clear_selection(self):
        self.file_list.clearSelection()
    
    def extract_frame_number(self, filename):
        """Извлекает номер кадра из имени файла для сортировки"""
        match = re.search(r'frame_(\d+)', os.path.basename(filename))
        return int(match.group(1)) if match else 0
    
    def load_files(self, folder):
        self.file_list.clear()
        supported_formats = ('.png', '.jpg', '.jpeg', '.bmp')
        
        files = []
        for root, _, filenames in os.walk(folder):
            for filename in filenames:
                if filename.lower().endswith(supported_formats):
                    filepath = os.path.join(root, filename)
                    files.append(filepath)
        
        # Сортируем файлы по номеру кадра
        files.sort(key=self.extract_frame_number)
        
        for filepath in files:
            self.file_list.addItem(filepath)
    
    def get_selected_files(self):
        selected = []
        for item in self.file_list.selectedItems():
            selected.append(item.text())
        return selected
    
    def get_all_files(self):
        all_files = []
        for i in range(self.file_list.count()):
            all_files.append(self.file_list.item(i).text())
        return all_files


class VideoCreatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Создание видео из изображений")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Виджет выбора файлов
        self.file_selection = FileSelectionWidget()
        
        # Элементы интерфейса
        self.folder_label = QLabel("Корневая папка с изображениями: не выбрана")
        self.select_folder_btn = QPushButton("Выбрать корневую папку")
        self.select_folder_btn.clicked.connect(self.select_folder)

        self.output_label = QLabel("Сохранить видео в:")
        self.output_path_edit = QLineEdit()
        self.select_output_btn = QPushButton("Выбрать место сохранения")
        self.select_output_btn.clicked.connect(self.select_output)

        self.fps_label = QLabel("Частота кадров (FPS):")
        self.fps_input = QLineEdit("25")

        self.quality_label = QLabel("Качество (CRF 18-28):")
        self.quality_input = QLineEdit("23")

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_label = QLabel("Готовность: 0%")

        self.create_btn = QPushButton("Создать видео")
        self.create_btn.clicked.connect(self.create_video)

        # Добавление элементов
        layout.addWidget(self.folder_label)
        layout.addWidget(self.select_folder_btn)
        layout.addWidget(self.file_selection)
        layout.addWidget(self.output_label)
        layout.addWidget(self.output_path_edit)
        layout.addWidget(self.select_output_btn)
        layout.addWidget(self.fps_label)
        layout.addWidget(self.fps_input)
        layout.addWidget(self.quality_label)
        layout.addWidget(self.quality_input)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.progress_label)
        layout.addWidget(self.create_btn)

        central_widget.setLayout(layout)

        # Переменные
        self.selected_folder = ""
        self.output_path = ""
        self.worker_thread = None

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите корневую папку с изображениями")
        if folder:
            self.selected_folder = folder
            self.folder_label.setText(f"Корневая папка: {folder}")
            default_output = os.path.join(folder, "output.mp4")
            self.output_path_edit.setText(default_output)
            self.file_selection.load_files(folder)

    def select_output(self):
        default_name = self.output_path_edit.text() or os.path.join(os.getcwd(), "output.mp4")
        path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить видео как", default_name, "MP4 Files (*.mp4)")
        if path:
            self.output_path = path
            self.output_path_edit.setText(path)

    def create_video(self):
        if not self.selected_folder:
            QMessageBox.warning(self, "Ошибка", "Выберите корневую папку с изображениями")
            return

        self.output_path = self.output_path_edit.text()
        if not self.output_path:
            QMessageBox.warning(self, "Ошибка", "Укажите путь для сохранения видео")
            return

        try:
            fps = int(self.fps_input.text())
            crf = int(self.quality_input.text())
            if not (18 <= crf <= 28):
                raise ValueError("CRF должен быть между 18 и 28")
            if fps <= 0:
                raise ValueError("FPS должен быть положительным")
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", str(e))
            return

        # Получаем выбранные файлы (или все, если ничего не выбрано)
        selected_files = self.file_selection.get_selected_files()
        if not selected_files:
            selected_files = self.file_selection.get_all_files()

        if not selected_files:
            QMessageBox.warning(self, "Ошибка", 
                              "Не найдены изображения в форматах: PNG, JPG, JPEG, BMP")
            return

        # Настраиваем UI
        self.progress_bar.setValue(0)
        self.progress_label.setText(f"Выбрано {len(selected_files)} изображений. Готовность: 0%")
        self.create_btn.setEnabled(False)

        # Создаем и запускаем поток
        self.worker_thread = VideoCreatorThread(selected_files, self.output_path, fps, crf)
        self.worker_thread.progress_updated.connect(self.update_progress)
        self.worker_thread.finished.connect(self.video_created)
        self.worker_thread.error_occurred.connect(self.show_error)
        self.worker_thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)
        self.progress_label.setText(f"Готовность: {value}%")

    def video_created(self, output_path):
        self.progress_bar.setValue(100)
        self.progress_label.setText("Готовность: 100%")
        self.create_btn.setEnabled(True)
        
        file_size = os.path.getsize(output_path) / (1024 * 1024)  # в MB
        QMessageBox.information(
            self,
            "Готово",
            f"Видео успешно создано!\n\n"
            f"Путь: {output_path}\n"
            f"Размер: {file_size:.2f} MB\n"
            f"Кадров: {len(self.worker_thread.images)}\n"
            f"Длительность: {len(self.worker_thread.images) / int(self.fps_input.text()):.1f} сек")

    def show_error(self, error_msg):
        self.progress_bar.setValue(0)
        self.progress_label.setText("Ошибка!")
        self.create_btn.setEnabled(True)
        QMessageBox.critical(
            self,
            "Ошибка",
            f"Ошибка при создании видео:\n{error_msg[:500]}" +
            ("..." if len(error_msg) > 500 else ""))

    def closeEvent(self, event):
        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.terminate()
            self.worker_thread.wait()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = VideoCreatorApp()
    window.show()
    sys.exit(app.exec_())
