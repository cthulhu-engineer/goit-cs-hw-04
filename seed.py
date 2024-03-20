# Створимо декілька тестових текстових файлів з прикладами тексту
file_contents = [
    "This is a test file. It contains keywords such as example and nothing else.",
    "Another test file here. It includes a keyword, but also more text to test.",
    "The last test file does not contain any of the specified keywords."
]

# Вказуємо шлях для збереження файлів
file_paths = ["file1.txt", "file2.txt", "file3.txt"]

# Записуємо вміст у файли
for path, content in zip(file_paths, file_contents):
    with open(f"./{path}", "w") as file:
        file.write(content)
