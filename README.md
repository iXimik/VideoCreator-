# VideoCreator-
# Video Creator from Images / Создание видео из изображений

## English Description

### Overview
This application creates video files from a sequence of images with a user-friendly GUI interface. It supports:
- Selecting multiple images from folders
- Adjustable frame rate (FPS) and video quality (CRF)
- Progress tracking during video creation
- Automatic sorting of images by frame number

### Key Features
- Simple and intuitive graphical interface
- Support for common image formats (PNG, JPG, JPEG, BMP)
- Multi-threaded processing to keep UI responsive
- Detailed error reporting
- Progress bar showing conversion status

### Requirements
- Python 3.6+
- PyQt5
- OpenCV (optional, for image processing)
- FFmpeg (must be installed system-wide)

### Installation
1. Install Python dependencies:
```bash
pip install PyQt5 opencv-python
```

2. Install FFmpeg:
- **Windows**: Download from https://ffmpeg.org/
- **Linux**: `sudo apt install ffmpeg`
- **Mac**: `brew install ffmpeg`

### Usage
Run the application:
```bash
python video_creator.py
```

1. Select source folder with images
2. Choose output video file location
3. Set FPS (frames per second)
4. Set CRF quality (18-28, lower is better)
5. Click "Create Video"

### Creating Executable
To build a standalone Windows executable:

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Create executable:
```bash
pyinstaller --onefile --windowed --icon=app.ico video_creator.py
```

3. The executable will be in the `dist` folder

# Video Creator from Images - Windows Guide


### Overview
This Windows application creates video files from image sequences with a simple GUI interface. It automatically sorts images by their frame numbers and processes them using FFmpeg.

### System Requirements
- Windows 10 or 11
- Python 3.9+ (64-bit recommended)
- FFmpeg installed

### Installation

#### 1. Install Python
Open **Command Prompt (Admin)** and run:
```cmd
winget install Python.Python.3.10
```

Verify installation:
```cmd
python --version
pip --version
```

#### 2. Install FFmpeg
Download FFmpeg from [official site](https://ffmpeg.org/download.html) or install via Chocolatey (admin shell):
```cmd
choco install ffmpeg
```

Add FFmpeg to PATH:
```cmd
setx /M PATH "%PATH%;C:\Program Files\FFmpeg\bin"
```

#### 3. Install Required Libraries
In normal Command Prompt:
```cmd
python -m pip install --upgrade pip
pip install PyQt5 opencv-python pyinstaller
```

### Running the Application
```cmd
python video_creator.py
```

### Compiling to EXE
Create a single executable file:
```cmd
pyinstaller --onefile --windowed --icon=app.ico video_creator.py
```

The executable will be in the `dist` folder.


## Описание 

### Обзор
Это приложение создает видеофайлы из последовательности изображений с удобным графическим интерфейсом. Возможности:
- Выбор нескольких изображений из папок
- Настройка частоты кадров (FPS) и качества видео (CRF)
- Отслеживание прогресса создания видео
- Автоматическая сортировка изображений по номерам кадров

### Основные функции
- Простой и интуитивно понятный интерфейс
- Поддержка распространенных форматов изображений (PNG, JPG, JPEG, BMP)
- Многопоточная обработка для отзывчивого интерфейса
- Подробные сообщения об ошибках
- Индикатор прогресса конвертации

### Требования
- Python 3.6+
- PyQt5
- OpenCV (опционально, для обработки изображений)
- FFmpeg (должен быть установлен в системе)

### Установка
1. Установите зависимости Python:
```bash
pip install PyQt5 opencv-python
```

2. Установите FFmpeg:
- **Windows**: Скачайте с https://ffmpeg.org/
- **Linux**: `sudo apt install ffmpeg`
- **Mac**: `brew install ffmpeg`

### Использование
Запустите приложение:
```bash
python video_creator.py
```

1. Выберите папку с исходными изображениями
2. Укажите место сохранения видеофайла
3. Установите FPS (кадров в секунду)
4. Установите качество CRF (18-28, меньше - лучше)
5. Нажмите "Создать видео"

### Создание EXE-файла
Для сборки исполняемого файла в Windows:

1. Установите PyInstaller:
```bash
pip install pyinstaller
```

2. Создайте исполняемый файл:
```bash
pyinstaller --onefile --windowed --icon=app.ico video_creator.py
```

3. Исполняемый файл будет в папке `dist`

### Дополнительная информация
- Приложение автоматически сортирует изображения по номерам кадров в имени файла (ищет pattern `frame_XXXX`)
- Для оптимального качества используйте CRF 18-23
- Рекомендуемый FPS: 24-30 для плавного видео
- Приложение создает временный файл со списком изображений и удаляет его после завершения

## Русское описание

### Обзор
Это приложение для Windows создает видео из последовательности изображений через простой графический интерфейс. Автоматически сортирует кадры по номерам и обрабатывает их через FFmpeg.

### Системные требования
- Windows 10 или 11
- Python 3.9+ (рекомендуется 64-битная версия)
- Установленный FFmpeg

### Установка

#### 1. Установка Python
Откройте **Командную строку (Администратор)** и выполните:
```cmd
winget install Python.Python.3.10
```

Проверьте установку:
```cmd
python --version
pip --version
```

#### 2. Установка FFmpeg
Скачайте с [официального сайта](https://ffmpeg.org/download.html) или через Chocolatey (админская строка):
```cmd
choco install ffmpeg
```

Добавьте в PATH:
```cmd
setx /M PATH "%PATH%;C:\Program Files\FFmpeg\bin"
```

#### 3. Установка библиотек
В обычной командной строке:
```cmd
python -m pip install --upgrade pip
pip install PyQt5 opencv-python pyinstaller
```

### Запуск приложения
```cmd
python video_creator.py
```

### Компиляция в EXE
Создание единого исполняемого файла:
```cmd
pyinstaller --onefile --windowed --icon=app.ico video_creator.py
```

Готовый файл появится в папке `dist`.

### Дополнительные команды

**Create virtual environment (Создать виртуальное окружение):**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Check FFmpeg (Проверить FFmpeg):**
```cmd
ffmpeg -version
```

**Troubleshooting (Решение проблем):**
- If you get DLL errors, install Visual C++ Redistributable  
  (При ошибках DLL установите Visual C++ Redistributable)
- For PyInstaller errors, try:  
  (При ошибках PyInstaller попробуйте:)
  ```cmd
  pip install --upgrade pyinstaller
  ```
