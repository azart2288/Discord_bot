import os

# Получаем текущую директорию
current_directory = os.getcwd()

# Отображаем все файлы и папки в текущей директории
for file_name in os.listdir(current_directory):
    print(file_name)

