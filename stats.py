import matplotlib.pyplot as plt
import json
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

window = tk.Tk()

message = None
listbox = None
stats_data = None
open_save_button = None
items = []
player_dict = {}
list_items = None
search_bar = None
save_path = ""
dropdown = None

def block_selected(event):
    global listbox, message
    selected_index = listbox.curselection()
    message.config(text=f"{listbox.get(selected_index)}")

def open_save_pressed(event):
    global player_dict, stats_data, items, listbox, save_path
    try:
        save_path = filedialog.askdirectory() + "/stats"
    except FileNotFoundError:
        player_dict = {}
        stats_data = None
        items = []
        return
    populate_listbox(save_path)

def populate_listbox(path, filter_text = "", category = "minecraft:used"):
    global player_dict, stats_data, items, listbox, dropdown
    player_stats = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    p_dict = {}
    all_items = []
    all_categories = []
    for player in player_stats:
        with open(path + "/" + player) as file:
            stats_data = json.load(file)['stats']
            for key, value in stats_data.items():
                if key not in all_categories:
                    all_categories.append(key)
            try:
                for item in stats_data[category]:
                    if item not in all_items and filter_text in item:
                        all_items.append(item)
                cut_name = player.split(".")[0]
                p_dict[cut_name] = stats_data[category]
            except KeyError:
                cut_name = player.split(".")[0]
                p_dict[cut_name] = None
    dropdown.set_menu(all_categories[0], *all_categories)
    player_dict = p_dict
    all_items.sort()
    listbox.config(listvariable=tk.Variable(value=all_items))
    items = all_items

def plot_data(event):
    global player_dict, message
    fig, ax = plt.subplots()
    players = []
    values = []
    item = message.cget("text")
    print(item)
    for player in player_dict:
        players.append(player)
        try:
            values.append(player_dict[player][item])
        except (KeyError, TypeError):
            values.append(0)

    print(f"Players: {players}")
    print(f"Values: {values}")
    ax.bar(players, values)
    ax.set_ylabel("Number of Uses")
    ax.set_xlabel("Player")
    ax.set_title(f"{item} uses by player")
    ax.tick_params(axis='x', labelsize=8)
    plt.show()

def search_feature(search_text):
    global save_path
    populate_listbox(save_path, filter_text=search_text.get())

def clear_search_bar(event):
    global search_bar
    search_bar.delete(0, tk.END)

def change_category(category):
    global save_path
    populate_listbox(save_path, category=category.get())

def main():

    blocks = []

    window.title("Minecraft Stats")
    window_width = 800
    window_height = 600

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    # WINDOW CONTENTS

    global message
    message = ttk.Label(window, text="Hello, World!")
    message.grid(column=0, row=0)

    global list_items
    list_items = tk.Variable(value=blocks)

    global listbox
    listbox_frame = tk.Frame(window)
    listbox_frame.grid(column=0, row=1, rowspan=2, sticky='nsew')
    listbox = tk.Listbox(listbox_frame, listvariable=list_items, width=50, selectmode=tk.SINGLE)
    listbox.bind("<<ListboxSelect>>", block_selected)
    listbox.pack()

    global open_save_button
    open_save_button = tk.Button(window, text="Open Save Folder")
    open_save_button.bind("<Button>", open_save_pressed)
    open_save_button.grid(column=0, row=3)

    plot_button = tk.Button(window, text="Plot Data")
    plot_button.bind("<Button>", plot_data)
    plot_button.grid(column=0, row=4)

    global search_bar
    search_text = tk.StringVar()
    search_label = tk.Label(window, text="Search for Item:")
    search_text.trace("w", lambda name, index, mode, var=search_text: search_feature(search_text))
    search_bar = ttk.Entry(window, textvariable=search_text)
    search_bar.bind("<Control-BackSpace>", clear_search_bar)
    search_label.grid(column=1, row=1)
    search_bar.grid(column=1, row=2)

    global dropdown
    active_stat = tk.StringVar()
    active_stat.trace("w", lambda name, index, mode, var=active_stat: change_category(active_stat))
    dropdown = ttk.OptionMenu(window, active_stat, "", *[])
    dropdown.grid(column=1, row=3)

    window.grid_rowconfigure(1, weight=0)

    window.mainloop()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
