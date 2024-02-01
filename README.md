# api_final

#### Как запустить проект:

## 1. Клонируйте репозиторий и перейдите в него в командной строке:
    - git clone https://github.com/IvanKalug-QA/api_final_yatube.git
    - cd api_final_yatube

## 2. Создайте и активируйте виртуальное окружение:
    - python3 -m venv env

    # Если у вас Linux/macOS:
        - source env/bin/activate

    # Если у вас windows:
        - source env/scripts/activate

## 3. Установите зависимости из файла requirements.txt:
    - pip install -r requirements.txt

## 4. Выполните миграции:
    - python3 manage.py migrate

## 5. Запустите проект:
    - python3 manage.py runserver
