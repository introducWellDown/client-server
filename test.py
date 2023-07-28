import tkinter as tk
from tkinter import ttk

def on_scroll(*args):
    fraction = scrollbar.get()
    rows_in_view = int(tree_height / row_height)
    rows_to_scroll = total_rows - rows_in_view
    scrolled_rows = rows_to_scroll * fraction
    print("fraction:" , fraction)
    print("rows_in_view:" , rows_in_view)
    print("rows_to_scroll:" , rows_to_scroll)
    print("Прокручено строк:", scrolled_rows)

root = tk.Tk()
root.title("Scrollbar Example")
root.geometry("500x300")

# Создаем Treeview с 100 строками
tree_height = 200
row_height = 20
total_rows = 100

columns = ttk.Treeview(root, column=("column_1", "column_2"), show='headings', height=tree_height // row_height)
columns.column("#1", anchor=tk.CENTER)
columns.column("#2", anchor=tk.CENTER)

# Создаем вертикальный скроллбар
scrollbar = ttk.Scrollbar(root, orient="vertical", command=columns.yview)
columns.configure(yscrollcommand=scrollbar.set)

# Размещаем Treeview и скроллбар на главном окне
columns.grid(row=0, column=0, sticky="nsew")
scrollbar.grid(row=0, column=1, sticky="ns")

# Настраиваем упаковку столбцов для заполнения доступной ширины окна
root.grid_columnconfigure(0, weight=1)

# Вставляем данные в Treeview
for i in range(total_rows):
    columns.insert('', 'end', values=("Column 1", "Column 2"))

# Связываем обработчик on_scroll с событием прокрутки скроллбара
scrollbar.bind("<B1-Motion>", on_scroll)

root.mainloop()
