import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

TASKS_FILE = "tasks.json"
HISTORY_FILE = "history.json"


class TaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("450x550")

        self.tasks = self.load_data(TASKS_FILE)
        self.history = self.load_data(HISTORY_FILE)

        # --- Фильтр ---
        self.filter_var = tk.StringVar(value="Все")
        ttk.Label(root, text="Фильтр:").pack()

        self.filter_menu = ttk.Combobox(
            root,
            textvariable=self.filter_var,
            values=["Все", "Учёба", "Спорт", "Работа"],
            state="readonly"
        )
        self.filter_menu.pack(pady=5)

        # --- История ---
        self.history_listbox = tk.Listbox(root, width=50, height=15)
        self.history_listbox.pack(pady=10)

        # --- Кнопки ---
        ttk.Button(root, text="Сгенерировать задачу", command=self.generate_task).pack(pady=5)
        ttk.Button(root, text="Удалить выбранное", command=self.delete_selected).pack(pady=5)
        ttk.Button(root, text="Очистить историю", command=self.clear_history).pack(pady=5)

        # --- Добавление ---
        ttk.Label(root, text="Новая задача:").pack()

        self.entry_task = ttk.Entry(root, width=30)
        self.entry_task.pack(pady=5)

        self.entry_type = ttk.Combobox(
            root,
            values=["Учёба", "Спорт", "Работа"],
            state="readonly"
        )
        self.entry_type.pack(pady=5)
        self.entry_type.set("Учёба")

        ttk.Button(root, text="Добавить задачу", command=self.add_task).pack(pady=10)

        self.update_history()

    # --- Работа с файлами ---
    def load_data(self, file):
        if os.path.exists(file):
            with open(file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_data(self, file, data):
        with open(file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    # --- Обновление списка ---
    def update_history(self):
        self.history_listbox.delete(0, tk.END)
        for item in self.history:
            self.history_listbox.insert(tk.END, f"{item['task']} ({item['type']})")

    # --- Генерация ---
    def generate_task(self):
        selected_type = self.filter_var.get()

        filtered = self.tasks if selected_type == "Все" else [
            t for t in self.tasks if t["type"] == selected_type
        ]

        if not filtered:
            messagebox.showwarning("Ошибка", "Нет задач этого типа")
            return

        task = random.choice(filtered)

        self.history.append(task)
        self.save_data(HISTORY_FILE, self.history)
        self.update_history()

    # --- Добавление ---
    def add_task(self):
        text = self.entry_task.get().strip()
        t_type = self.entry_type.get()

        if not text:
            messagebox.showwarning("Ошибка", "Введите задачу")
            return

        # Проверка на дубликаты
        for t in self.tasks:
            if t["task"].lower() == text.lower():
                messagebox.showwarning("Ошибка", "Такая задача уже есть")
                return

        new_task = {"task": text, "type": t_type}
        self.tasks.append(new_task)
        self.save_data(TASKS_FILE, self.tasks)

        self.entry_task.delete(0, tk.END)

    # --- Удаление ---
    def delete_selected(self):
        selected = self.history_listbox.curselection()
        if not selected:
            return

        index = selected[0]
        del self.history[index]

        self.save_data(HISTORY_FILE, self.history)
        self.update_history()

    # --- Очистка ---
    def clear_history(self):
        if messagebox.askyesno("Подтверждение", "Очистить всю историю?"):
            self.history.clear()
            self.save_data(HISTORY_FILE, self.history)
            self.update_history()


# --- Запуск ---
root = tk.Tk()
app = TaskApp(root)
root.mainloop()
