from tkinter.ttk import *
from tkinter import *
from tkinter.messagebox import *
from re import *
import json

tk = Tk()
tk.title("ТРЗ помощник")


def render_main_view():
    clear_view()
    Button(tk, text="Работници", command=render_workers).grid(row=0, column=0, padx=10, pady=10)
    Button(tk, text="Отработено време").grid(row=0, column=1, padx=10, pady=10)
    Button(tk, text="Отпуски").grid(row=0, column=2, padx=10, pady=10)
    Button(tk, text="Болнични").grid(row=0, column=3, padx=10, pady=10)
    Button(tk, text="Разходи по обекти").grid(row=0, column=4, padx=10, pady=10)
    Button(tk, text="Удръжки").grid(row=0, column=5, padx=10, pady=10)
    Button(tk, text="Списък с работещи за деня").grid(row=0, column=5, padx=10, pady=10)
    Button(tk, text="Зануляване на месеца").grid(row=0, column=6, padx=10, pady=10)


def render_workers():
    clear_view()
    Button(tk, text="Добавяне на работник", command=render_add_worker).grid(row=0, column=0, padx=10, pady=10)
    Button(tk, text="Изтриване/редакция/справка", command=render_delete_worker).grid(row=0, column=1, padx=10, pady=10)
    Button(tk, text="Назад", command=render_main_view).grid(row=0, column=4, padx=10, pady=10)


def render_delete_worker():
    clear_view()
    box = Combobox(tk, width=40)
    info = read_file()
    box["values"] = list(info.keys())
    Label(tk, text="Изберете работник:").grid(row=0, column=0, padx=10, pady=10)
    box.grid(row=1, column=0, padx=10, pady=10)
    Button(tk, text="Назад", command=render_workers).grid(row=3, column=1, padx=10, pady=10)
    Button(tk, text="Изтриване", command=lambda: delete_worker(box.get())).grid(row=2, column=0, padx=10, pady=10)
    Button(tk, text="Редакция", command=lambda: render_edit_worker(box.get())).grid(row=2, column=1, padx=10, pady=10)
    Button(tk, text="Справка", command=lambda: render_reference(box.get())).grid(row=3, column=0, padx=10, pady=10)


def render_reference(worker):
    if not worker:
        return
    clear_view()
    info = read_file()
    Label(tk, text=f"Име: {worker}").grid(row=0, column=0, padx=10, pady=10)
    Label(tk, text=f"ЕГН: {info[worker]['pin']}").grid(row=0, column=1, padx=10, pady=10)
    Label(tk, text=f"Брутна месечна заплата: {info[worker]['salary']}").grid(row=0, column=2, padx=10, pady=10)
    Label(tk, text=f"Използван платен отпуск: {info[worker]['paid_leave']}").grid(row=1, column=0, padx=10, pady=10)
    Label(tk, text=f"Оставащ платен отпуск: {20 - int(info[worker]['paid_leave'])}").grid(row=1, column=1, padx=10,
                                                                                          pady=10)
    Label(tk, text=f"Използван неплатен отпуск: {info[worker]['unpaid_leave']}").grid(row=2, column=0, padx=10, pady=10)
    Label(tk, text=f"Оставащ неплатен отпуск: {30 - int(info[worker]['unpaid_leave'])}").grid(row=2, column=1, padx=10,
                                                                                              pady=10)
    Label(tk, text=f"Болнични: {info[worker]['sick_leave']}").grid(row=3, column=0, padx=10, pady=10)
    Button(tk, text="Назад", command=render_delete_worker).grid(row=3, column=3, padx=10, pady=10)


def read_file():
    with open("database.txt", "r") as file:
        try:
            info = json.load(file)
        except json.decoder.JSONDecodeError:
            info = {}
    return info


def write_to_file(data):
    with open("database.txt", "w") as file:
        json.dump(data, file)


def delete_worker(value):
    if not value:
        return
    workers = read_file()
    workers.pop(value)
    write_to_file(workers)
    showinfo('Готово', 'Работникът е успешно изтрит')
    render_delete_worker()


def clear_view():
    for slave in tk.grid_slaves():
        slave.destroy()


def add_worker(name_, pin_, job_, salary_):
    pin_pattern = r"\b\d{10}\b"
    pin = findall(pin_pattern, pin_)
    salary_pattern = r"\b(\d+(?:\.\d+)?)\b"
    salary = findall(salary_pattern, salary_)
    data = read_file()
    if not pin:
        showerror('Грешка', 'Грешно ЕГН')
    elif not name_ or not job_:
        showerror('Грешка', 'Непопълнени полета')
    elif not salary:
        showerror('Грешка', 'Грешна заплата')
    elif name_ in data.keys():
        showerror('Грешка', 'Работникът вече е регистриран')
    else:
        pin = pin[0]
        salary = salary[0]
        info = {"pin": pin, "job": job_, "salary": salary, "paid_leave": 0, "unpaid_leave": 0,
                "sick_leave": 0, "leftover_leave": 0}

        data[name_] = info
        write_to_file(data)
        showinfo('Готово', 'Работникът е успешно добавен')


def render_add_worker():
    clear_view()
    Label(tk, text="Име:").grid(row=0, column=0, padx=10, pady=10)
    name = Entry(tk)
    name.grid(row=0, column=1, padx=10, pady=10)
    Label(tk, text="ЕГН:").grid(row=1, column=0, padx=10, pady=10)
    pin = Entry(tk)
    pin.grid(row=1, column=1, padx=10, pady=10)
    Label(tk, text="Длъжност:").grid(row=2, column=0, padx=10, pady=10)
    job = Entry(tk)
    job.grid(row=2, column=1, padx=10, pady=10)
    Label(tk, text="Брутна месечна заплата в лв.:").grid(row=3, column=0, padx=10, pady=10)
    salary = Entry(tk)
    salary.grid(row=3, column=1, padx=10, pady=10)
    Button(tk, text="Назад", command=render_workers).grid(row=4, column=1, padx=10, pady=10)
    Button(tk, text="Запазване", command=lambda: add_worker(name.get(), pin.get(), job.get(),
                                                            salary.get())).grid(row=4, column=0,
                                                                                padx=10,
                                                                                pady=10)


def render_edit_worker(key):
    if not key:
        return
    clear_view()
    Label(tk, text="Име:").grid(row=0, column=0, padx=10, pady=10)
    name = Entry(tk)
    name.grid(row=0, column=1, padx=10, pady=10)
    Label(tk, text="ЕГН:").grid(row=1, column=0, padx=10, pady=10)
    pin = Entry(tk)
    pin.grid(row=1, column=1, padx=10, pady=10)
    Label(tk, text="Длъжност:").grid(row=2, column=0, padx=10, pady=10)
    job = Entry(tk)
    job.grid(row=2, column=1, padx=10, pady=10)
    Label(tk, text="Брутна месечна заплата в лв.:").grid(row=3, column=0, padx=10, pady=10)
    salary = Entry(tk)
    salary.grid(row=3, column=1, padx=10, pady=10)
    Button(tk, text="Назад", command=render_delete_worker).grid(row=4, column=1, padx=10, pady=10)
    Button(tk, text="Запазване", command=lambda: edit_worker(name.get(), pin.get(), job.get(),
                                                             salary.get(), key)).grid(row=4, column=0,
                                                                                      padx=10,
                                                                                      pady=10)


def edit_worker(name_, pin_, job_, salary_, key):
    pin_pattern = r"\b\d{10}\b"
    pin = findall(pin_pattern, pin_)
    salary_pattern = r"\b(\d+(?:\.\d+)?)\b"
    salary = findall(salary_pattern, salary_)
    data = read_file()
    if not pin:
        showerror('Грешка', 'Грешно ЕГН')
    elif not name_ or not job_:
        showerror('Грешка', 'Непопълнени полета')
    elif not salary:
        showerror('Грешка', 'Грешна заплата')
    else:
        pin = pin[0]
        salary = salary[0]
        if name_ == key:
            data[name_]["pin"] = pin
            data[name_]["job"] = job_
            data[name_]["salary"] = salary
        else:
            data[name_] = data[key]
            data.pop(key)
        write_to_file(data)
        showinfo('Готово', 'Работникът е успешно редактиран')


render_main_view()
tk.mainloop()
