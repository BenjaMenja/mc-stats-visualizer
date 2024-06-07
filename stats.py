import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import json
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.colorchooser import askcolor

window = tk.Tk()

message = None
listbox = None
stats_data = None
open_save_button = None
items = []
player_dict = {}
list_items = None
search_bar = None
search_text = None
save_path = ""
dropdown = None
bar_color = None
color_display = None


def block_selected(event):
    global listbox, message
    selected_index = listbox.curselection()
    message.config(text=f"Selected Item: {listbox.get(selected_index)}")

def open_save_pressed(event):
    global player_dict, stats_data, items, listbox, save_path
    try:
        save_path = filedialog.askdirectory() + "/stats"
    except FileNotFoundError:
        player_dict = {}
        stats_data = None
        items = []
        return
    populate_listbox(save_path, filter_text="", category="minecraft:used")

def populate_listbox(path, **kwargs):
    global player_dict, stats_data, items, listbox, dropdown, search_bar, search_text
    category = kwargs.get("category", dropdown.cget("text"))
    filter_text = kwargs.get("filter_text", search_text.get())
    print(filter_text)
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
    if kwargs.get("category") is not None:
        dropdown.set_menu(all_categories[0], *all_categories)
    player_dict = p_dict
    all_items.sort()
    listbox.config(listvariable=tk.Variable(value=all_items))
    items = all_items

def custom_category_formatting(formatted_item):
    format_categories = {
        "Aviate One Cm": "Distance Traveled by Elytra",
        "Bell Ring": "Bells Rung",
        "Boat One Cm": "Distance by Boat",
        "Climb One Cm": "Distance Climbed Ladders/Vines",
        "Crouch One Cm": "Distance Crouched",
        "Damage Dealt": "Damage Dealt by Melee Attacks",
        "Drop": "Items Dropped",
        "Eat Cake Slice": "Cake Slices Eaten",
        "Enchant Item": "Number of Items Enchanted",
        "Fall One Cm": "Distance Fallen",
        "Fill Cauldron": "Cauldrons Filled",
        "Fly One Cm": "Distance Flown",
        "Horse One Cm": "Distance Traveled by Horse",
        "Inspect Dispenser": "Number of Dispenser Interactions",
        "Inspect Dropper": "Number of Dropper Interactions",
        "Inspect Hopper": "Number of Hopper Interactions",
        "Interact With Anvil": "Number of Anvil Interactions",
        "Interact With Beacon": "Number of Beacon Interactions",
        "Interact With Blast Furnace": "Number of Blast Furnace Interactions",
        "Interact With Brewingstand": "Number of Brewing Stand Interactions",
        "Interact With Campfire": "Number of Campfire Interactions",
        "Interact With Cartography Table": "Number of Cartography Table Interactions",
        "Interact With Crafting Table": "Number of Crafting Table Interactions",
        "Interact With Furnace": "Number of Furnace Interactions",
        "Interact With Grindstone": "Number of Grindstone Interactions",
        "Interact With Loom": "Number of Loom Interactions",
        "Interact With Smithing Table": "Number of Smithing Table Interactions",
        "Interact With Smoker": "Number of Smoker Interactions",
        "Interact With Stonecutter": "Number of Stonecutter Interactions",
        "Jump": "Jumps Performed",
        "Leave Game": "Number of Games Quit",
        "Minecart One Cm": "Distance Traveled by Minecart",
        "Mob Kills": "Number of Mob Kills",
        "Open Barrel": "Number of Barrel Interactions",
        "Open Chest": "Number of Chest Interactions",
        "Open Enderchest": "Number of Ender Chest Interactions",
        "Open Shulker Box": "Number of Shulker Box Interactions",
        "Play Noteblock": "Number of Note Blocks Hit",
        "Play Record": "Number of Music Discs Played",
        "Play Time": "Total Amount of Time Played",
        "Pot Flower": "Number of Plants Potted",
        "Raid Trigger": "Raids Triggered",
        "Raid Win": "Raids Won",
        "Sleep In Bed": "Times Slept in Beds",
        "Sneak Time": "Total Crouch Time",
        "Sprint One Cm": "Distance Traveled While Sprinting",
        "Strider One Cm": "Distance Traveled by Strider",
        "Swim One Cm": "Distance Swum",
        "Talked To Villager": "Number of Villager Interactions",
        "Target Hit": "Number of Targets Hit",
        "Time Since Death": "Time Since Last Death",
        "Time Since Rest": "Time Since Last Rest",
        "Total World Time": "Total Amount of Time Played",
        "Traded With Villager": "Number of Villager Trades Performed",
        "Tune Noteblock": "Number of Note Blocks Tuned",
        "Use Cauldron": "Number of Bottles Filled with Cauldron",
        "Walk On Water One Cm": "Distance Traveled While Bobbing Up and Down",
        "Walk One Cm": "Distance Walked",
        "Walk Under Water One Cm": "Distance Walked Underwater"
    }
    return format_categories.get(formatted_item, f"{formatted_item}")

def process_values(values, category):
    if 'One Cm' in category:
        return [x/100 for x in values]
    elif 'Time' in category:
        return [x/20 for x in values]
    elif 'Damage' in category:
        return [x/10 for x in values]
    else:
        return values

def format_ylabel(formatted_item, category):
    print(category)
    if category == "Dropped":
        return "Items Dropped"
    elif category == "Crafted":
        return "Items Crafted"
    elif category == "Killed":
        return "Entities Killed"
    elif category == "Mined":
        return "Blocks Broken"
    elif category == "Killed_by":
        return "Number of Deaths"
    elif category == "Picked_up":
        return "Items Picked Up"
    elif category == "Used":
        return "Items Used"
    elif category == "Broken":
        return "Items Broken"

    ylabels = {
        "Dropped": "Items Dropped",
        "Crafted": "Items Crafted",
        "Killed": "Entities Killed",
        "Mined": "Blocks Broken",
        "Killed_by": "Number of Deaths",
        "Picked_up": "Items Picked Up",
        "Used": "Items Used",
        "Broken": "Items Broken",
        "Custom": "custom"
    }

    special_ylabels = {
        "Aviate One Cm": "Distance Traveled (Blocks)",
        "Bell Ring": "Bells Rung",
        "Boat One Cm": "Distance Traveled (Blocks)",
        "Climb One Cm": "Distance Climbed (Blocks)",
        "Crouch One Cm": "Distance Crouched (Blocks)",
        "Drop": "Items Dropped",
        "Eat Cake Slice": "Cake Slices Eaten",
        "Enchant Item": "Items Enchanted",
        "Fall One Cm": "Distance Fallen (Blocks)",
        "Fill Cauldron": "Cauldrons Filled",
        "Fly One Cm": "Distance Flown (Blocks)",
        "Horse One Cm": "Distance Traveled (Blocks)",
        "Inspect Dispenser": "Dispenser Interactions",
        "Inspect Dropper": "Dropper Interactions",
        "Inspect Hopper": "Hopper Interactions",
        "Interact With Anvil": "Anvil Interactions",
        "Interact With Beacon": "Beacon Interactions",
        "Interact With Blast Furnace": "Blast Furnace Interactions",
        "Interact With Brewingstand": "Brewing Stand Interactions",
        "Interact With Campfire": "Campfire Interactions",
        "Interact With Cartography Table": "Cartography Table Interactions",
        "Interact With Crafting Table": "Crafting Table Interactions",
        "Interact With Furnace": "Furnace Interactions",
        "Interact With Grindstone": "Grindstone Interactions",
        "Interact With Loom": "Loom Interactions",
        "Interact With Smithing Table": "Smithing Table Interactions",
        "Interact With Smoker": "Smoker Interactions",
        "Interact With Stonecutter": "Stonecutter Interactions",
        "Jump": "Jumps Performed",
        "Leave Game": "Games Quit",
        "Minecart One Cm": "Distance Traveled (Blocks)",
        "Mob Kills": "Mob Kills",
        "Open Barrel": "Barrel Interactions",
        "Open Chest": "Chest Interactions",
        "Open Enderchest": "Ender Chest Interactions",
        "Open Shulker Box": "Shulker Box Interactions",
        "Play Noteblock": "Note Blocks Hit",
        "Play Record": "Music Discs Played",
        "Play Time": "Time Played (s)",
        "Pot Flower": "Plants Potted",
        "Raid Trigger": "Raids Triggered",
        "Raid Win": "Raids Won",
        "Sleep In Bed": "Times Slept",
        "Sneak Time": "Crouch Time (s)",
        "Sprint One Cm": "Distance Traveled (Blocks)",
        "Strider One Cm": "Distance Traveled (Blocks)",
        "Swim One Cm": "Distance Swum (Blocks)",
        "Talked To Villager": "Villager Interactions",
        "Target Hit": "Targets Hit",
        "Time Since Death": "Time (s)",
        "Time Since Rest": "Time Since Last Rest (s)",
        "Total World Time": "Time Played (s)",
        "Traded With Villager": "Trades Performed",
        "Tune Noteblock": "Note Blocks Tuned",
        "Use Cauldron": "Cauldron Uses",
        "Walk On Water One Cm": "Distance Traveled (Blocks)",
        "Walk One Cm": "Distance Walked (Blocks)",
        "Walk Under Water One Cm": "Distance Walked (Blocks)"
    }

    ylabel = ylabels.get(category)

    if ylabel == "custom":
        ylabel = special_ylabels.get(formatted_item, f"{formatted_item}")

    return ylabel



def plot_data(event):
    global player_dict, message, dropdown, bar_color
    fig, ax = plt.subplots(num="Minecraft Stats Viewer")
    players = []
    values = []
    item = message.cget("text")
    item = item.split("Selected Item: ")[1]
    formatted_array = item.split(":")[1].split("_")
    extra_s = "" if formatted_array[-1][-1] == 's' else "s"
    formatted_item = " ".join([w.capitalize() for w in formatted_array])
    for player in player_dict:
        players.append(player)
        try:
            values.append(player_dict[player][item])
        except (KeyError, TypeError):
            values.append(0)

    category = dropdown.cget("text").split(":")[1].capitalize()
    title_categories = {
        'Killed_by': f"Number of Deaths to {formatted_item}{extra_s}",
        'Picked_up': f"Number of {formatted_item}{extra_s} Picked Up",
        'Custom': custom_category_formatting(formatted_item)
    }

    processed_values = process_values(values, formatted_item)
    print(f"Values: {processed_values}")
    ylabel = format_ylabel(formatted_item, category)

    ax.bar(players, processed_values, color=bar_color)
    ax.set_ylabel(ylabel)
    ax.set_xlabel("Player")
    ax.set_title(title_categories.get(category, f"Number of {formatted_item}{extra_s} {category}") + " By Player")
    ax.tick_params(axis='x', labelsize=8)
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))

    plt.show()

def search_feature(text):
    global save_path
    populate_listbox(save_path, filter_text=text.get())

def clear_search_bar(event):
    global search_bar
    search_bar.delete(0, tk.END)

def change_category(category):
    global save_path
    populate_listbox(save_path, category=category.get())

def choose_color():
    global bar_color, color_display
    color = askcolor(title="Choose Bar Color")
    bar_color = color[1]
    color_display.configure(bg=color[1])


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
    message = ttk.Label(window, text="Welcome to Minecraft Stats Viewer!")
    message.grid(column=0, row=0, pady=10)

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
    open_save_button.bind("<ButtonRelease>", open_save_pressed)
    open_save_button.grid(column=0, row=3)

    plot_button = tk.Button(window, text="Plot Data")
    plot_button.bind("<ButtonRelease>", plot_data)
    plot_button.grid(column=0, row=4)

    global search_bar, search_text
    search_text = tk.StringVar()
    search_label = tk.Label(window, text="Search for Item:")
    search_text.trace("w", lambda name, index, mode, var=search_text: search_feature(search_text))
    search_bar = ttk.Entry(window, textvariable=search_text)
    search_bar.bind("<Control-BackSpace>", clear_search_bar)
    search_label.grid(column=1, row=1, pady=10)
    search_bar.grid(column=1, row=2)

    global dropdown
    active_stat = tk.StringVar()
    active_stat.trace("w", lambda name, index, mode, var=active_stat: change_category(active_stat))
    dropdown = ttk.OptionMenu(window, active_stat, "", *[])
    dropdown.grid(column=1, row=3)

    color_button = tk.Button(window, text="Change Bar Color", command=choose_color)
    color_button.grid(column=2, row=0, pady=10)

    global color_display
    color_display = tk.Frame(window, bg="#1f77b4", height=50, width=200)
    color_display.grid(column=2, row=1)

    window.grid_rowconfigure(1, weight=0)

    window.mainloop()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
