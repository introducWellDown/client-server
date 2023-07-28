import tkinter as tk
from tkinter import ttk

root_window = tk.Tk()
root_window.title("Scrollbar Example")
root_window.geometry("500x300")

# Создаем Treeview с 10 строками
columns = ttk.Treeview(root_window, column=("column_1", "column_2"), show='headings', height=10)
columns.column("#1", anchor=tk.CENTER)
columns.column("#2", anchor=tk.CENTER)

# Создаем вертикальный скроллбар
scrollbar = ttk.Scrollbar(root_window, orient="vertical", command=columns.yview)
columns.configure(yscrollcommand=scrollbar.set)

# Размещаем Treeview и скроллбар на главном окне
columns.grid(row=0, column=0, sticky="nsew")
scrollbar.grid(row=0, column=1, sticky="ns")

# Настраиваем упаковку столбцов для заполнения доступной ширины окна
root_window.grid_columnconfigure(0, weight=1)

# Вставляем данные в Treeview (создаем 10 пустых элементов для прокрутки)
for i in range(50):
    columns.insert('', 'end', values=("1 ", " 2"))
for i in range(50,100):
    columns.insert('', 'end', values=(" ", " "))

# Убираем вертикальную сетку
style = ttk.Style()
style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

root_window.mainloop()