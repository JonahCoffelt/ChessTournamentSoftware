import customtkinter as ctk
from tkinter import ttk
import json

import writePDF
import rankPDF
import TournamentClass

from gameSetUpWindow import setupWin
from editGameWindow import editWin
class tournamentWin():
    def __init__(self, load = False):

        self.startup = True
        self.window = False
        self.game_tab_items = {}
        self.gridSize = [10, 10]
        self.saved_pairs = {}

        self.cmds = {
            "save" : self.save_data,
            "backup" : self.backup_data,
            "load" : self.load_data
        }

        #self.games_list = TournamentClass.global_tounraments
        #self.games_list =   [TournamentClass.Tournament(
        #                        "Team",
        #                        [["Mag High", "Jonah", "Megan", "Christian", "JOSHHH", "name", "Anis"],
        #                        ["Mag West", "Ian", "John", "Justin", "harrison", "kid", "timmy"], ["Klein", "Bob", "Jacob", "Ismael", "boy", "lex", "angie"], ["West 2", "Dog", "cat", "bird", "chicken", "pig", "cow"]],
        #                        is_team=True),
        #                        TournamentClass.Tournament("Single", [["John"], ["Megan"], ["Jonah"], ["Andy"], ["Josh"]])
        #                    ]
        self.games_list = TournamentClass.global_tounraments
        self.game_tab = 0

        # setup root
        self.root = ctk.CTk()
        self.root.title("Chess Tournament")
        self.root.geometry("1200x700")
        self.root.bind('<Configure>', self.resize)
        
        # configure grid layout
        self.root.title("Chess Tournament")
        self.root.geometry(f"{900}x{600}")
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure((2, 3), weight=0)
        self.root.grid_rowconfigure((0, 1, 2), weight=1)

        # configure sidebar
        self.sidebarFrame = ctk.CTkFrame(self.root, width=600, corner_radius=0)
        self.sidebarFrame.grid(row=0, column=0, padx=5, pady=5, rowspan=4, sticky="nsew")
        self.sidebarFrame.grid_rowconfigure(4, weight=1)
        self.titleFrame = ctk.CTkFrame(self.sidebarFrame)
        self.titleFrame.pack(pady=10, padx=10, fill="both")
        title = ctk.CTkLabel(master=self.titleFrame, text="   Settings   ", font=("Lucida Console", 24))
        title.pack(pady=5, padx=10)
        self.getRankings = ctk.CTkButton(master = self.titleFrame, text="Rankings PDF!", font=("Lucida Console", 16), command=self.get_rankings)
        self.getRankings.pack(pady=5, padx=10, fill="both")
        self.resizeFrame = ctk.CTkFrame(self.sidebarFrame)
        self.resizeFrame.pack(pady=3, padx=9, fill="both")
        Formating = ctk.CTkLabel(master=self.resizeFrame, text="   Formating   ", font=("Lucida Console", 18))
        Formating.pack(pady=5, padx=5)
        self.resizeButton = ctk.CTkButton(master = self.resizeFrame, text="Resize Grid", font=("Lucida Console", 16), command=self.updateResize)
        self.resizeButton.pack(pady=5, padx=10, fill="both")
        self.updatetabsButton = ctk.CTkButton(master = self.resizeFrame, text="Update Tab Edits", font=("Lucida Console", 16), command=self.add_game_update)
        self.updatetabsButton.pack(pady=5, padx=10, fill="both")
        #self.updateEditsButton = ctk.CTkButton(master = self.resizeFrame, text="Update Game Edits", font=("Lucida Console", 16), command=self.edit_update)
        #self.updateEditsButton.pack(pady=10, padx=10, fill="both")
        self.gameEditFrame = ctk.CTkFrame(self.sidebarFrame)
        self.gameEditFrame.pack(pady=3, padx=9, fill="both")
        GameEdits = ctk.CTkLabel(master=self.gameEditFrame, text="  Game Edits  ", font=("Lucida Console", 18))
        GameEdits.pack(pady=5, padx=5)
        self.addPlayerButton = ctk.CTkButton(master = self.gameEditFrame, text="Add Player", font=("Lucida Console", 16), command=self.add_player)
        self.addPlayerButton.pack(pady=5, padx=10, fill="both")
        self.removePlayerButton = ctk.CTkButton(master = self.gameEditFrame, text="Remove Player", font=("Lucida Console", 16), command=self.remove_player)
        self.removePlayerButton.pack(pady=5, padx=10, fill="both")
        self.addGameButton = ctk.CTkButton(master = self.gameEditFrame, text="Add Game", font=("Lucida Console", 16), command=self.add_game)
        self.addGameButton.pack(pady=5, padx=10, fill="both")
        self.editGameButton = ctk.CTkButton(master = self.gameEditFrame, text="Edit Selected Game", font=("Lucida Console", 16), command=self.edit_current_game)
        self.editGameButton.pack(pady=5, padx=10, fill="both")
        self.fileFrame = ctk.CTkFrame(self.sidebarFrame)
        self.fileFrame.pack(pady=3, padx=9, fill="both")
        FileTitle = ctk.CTkLabel(master=self.fileFrame, text="   File   ", font=("Lucida Console", 18))
        FileTitle.pack(pady=5, padx=5)
        self.saveButton = ctk.CTkButton(master = self.fileFrame, text="Save Tournament", font=("Lucida Console", 16), command=lambda: self.confirm_popup(self.cmds["save"], "Are you sure you want to save?\n Doing this will overwrite save.json", "save"))
        self.saveButton.pack(pady=5, padx=10, fill="both")
        self.backupButton = ctk.CTkButton(master = self.fileFrame, text="Backup Tournament", font=("Lucida Console", 16), command=lambda: self.confirm_popup(self.cmds["backup"], "Are you sure you want to backup?\n Doing this will overwrite backup.json", "backup"))
        self.backupButton.pack(pady=5, padx=10, fill="both")
        self.loadButton = ctk.CTkButton(master = self.fileFrame, text="Load Tournament", font=("Lucida Console", 16), command=lambda: self.confirm_popup(self.cmds["load"], "Are you sure you want to load?\n Doing this will overwrite all current games", "load"))
        self.loadButton.pack(pady=5, padx=10, fill="both")
        self.pdfButton = ctk.CTkButton(master = self.fileFrame, text="Create PDF", font=("Lucida Console", 16), command=self.generate_pdf)
        self.pdfButton.pack(pady=5, padx=10, fill="both")

        self.initialize_tabview()

        if load:
            self.load_data()

        self.old_list = self.games_list

        self.root.mainloop() 
    
    def initialize_tabview(self):
        self.tabview = ctk.CTkTabview(master=self.root, width = self.root.winfo_screenwidth() - 20, height = self.root.winfo_screenwidth() - 20)

        self.set_game_tabs()

        self.tabview.grid(row=0, column=1, padx=5, pady=5, rowspan=4, sticky="nswe")
        self.tab_frames = []
        self.tab_create_round_buttons = []
        self.tab_input_button_frames = {}
        for game in self.games_list:
            self.tab_frames.append(ctk.CTkFrame(master=self.tabview.tab(game.name)))
            self.tab_frames[-1].pack(pady=5, padx=5, fill="both", expand=True)
            self.tab_create_round_buttons.append(ctk.CTkButton(master = self.tab_frames[-1], text=f"Generate Round", font=("Lucida Console", 20), command=lambda x=game: self.create_round(x)))
            self.tab_create_round_buttons[-1].pack(pady=5, padx=5)
            self.game_tab_items[game.name] = [0, [], []]
            self.game_tab_items[game.name][0] = (ctk.CTkFrame(master=self.tab_frames[-1]))
            self.game_tab_items[game.name][0].pack(pady=5, padx=5, fill="both", expand=True)

    def display_pairings(self, game, pairs):
        self.saved_pairs[game.name] = pairs
        for pair in self.game_tab_items[game.name][1]:
            pair.destroy()
        i = 0
        for pair in pairs:
            self.game_tab_items[game.name][1].append(ctk.CTkFrame(master=self.game_tab_items[game.name][0]))
            self.game_tab_items[game.name][1][-1].grid(row=i//self.gridSize[0], column=i%self.gridSize[0], padx=3, pady=3)
            self.game_tab_items[game.name][2].append(ctk.CTkButton(master = self.game_tab_items[game.name][1][-1], text=f"{pair[0][0]}", font=("Lucida Console", 10), width=self.gridSize[1], command=lambda x=pair: self.add_points(x, 1.0, x[0][0], x[0][1])))
            self.game_tab_items[game.name][2][-1].pack(pady=1, padx=1)
            self.game_tab_items[game.name][2].append(ctk.CTkButton(master = self.game_tab_items[game.name][1][-1], text="Draw", font=("Lucida Console", 10), width=self.gridSize[1], command=lambda x=pair: self.add_points(x, .5, x[0][0], x[0][1], x[1][0], x[1][1])))
            self.game_tab_items[game.name][2][-1].pack(pady=1, padx=1)
            self.game_tab_items[game.name][2].append(ctk.CTkButton(master = self.game_tab_items[game.name][1][-1], text=f"{pair[1][0]}", font=("Lucida Console", 10), width=self.gridSize[1], command=lambda x=pair: self.add_points(x, 1.0, x[1][0], x[1][1])))
            self.game_tab_items[game.name][2][-1].pack(pady=1, padx=1)
            i += 1

    def set_game_tabs(self):
        for game in self.games_list:
            self.tabview.add(game.name)

    def create_round(self, gamse):
        for game in self.games_list:
            if game.name == self.tabview.get():
                if game.name in self.saved_pairs:
                    if len(self.saved_pairs[game.name]) == 0:
                        pairs = game.create_round()
                        #print(pairs)
                        self.display_pairings(game, pairs)
                else:
                    pairs = game.create_round()
                    #print(pairs)
                    self.display_pairings(game, pairs)

    def add_points(self, pair, score, player, team, player_2=None, team_2=None):
        for game in self.games_list:
            if game.name == self.tabview.get():
                game.add_points(score, player, team)
                if player_2:
                    game.add_points(score, player_2, team_2)
                self.saved_pairs[game.name].remove(pair)
                self.display_pairings(game, self.saved_pairs[game.name])

                if len(self.saved_pairs[game.name]) == 0:
                    game.finish_team_round()

    def save_data(self):
        if self.window:
            self.window.destroy()

        # Serializing json
        TournamentClass.global_tounraments = self.games_list
        player_data = [(game.name, game.players, game.is_team) for game in TournamentClass.global_tounraments]
        json_object = json.dumps(player_data, indent=4)
        
        # Writing to sample.json
        with open("Saves/save.json", "w") as outfile:
            outfile.write(json_object)
    
    def backup_data(self):
        if self.window:
            self.window.destroy()

        # Serializing json
        TournamentClass.global_tounraments = self.games_list
        player_data = [(game.name, game.players, game.is_team) for game in TournamentClass.global_tounraments]
        json_object = json.dumps(player_data, indent=4)
        
        # Writing to sample.json
        with open("Saves/backup.json", "w") as outfile:
            outfile.write(json_object)

    def load_data(self):

        if self.window:
            self.window.destroy()

        # Reading from json file
        with open('Saves/save.json', 'r') as openfile:
            player_data = json.load(openfile)

        new_game_list = []

        for game in player_data:
            new_game_list.append(TournamentClass.Tournament(game[0], [], game[2]))
            new_game_list[-1].players = game[1]

        self.games_list = new_game_list
        TournamentClass.global_tounraments = self.games_list
        self.initialize_tabview()

    def edit_current_game(self):
        TournamentClass.global_tounraments = self.games_list
        for game in self.games_list:
            if game.name == self.tabview.get():
                editWin(game.players, game.is_team, game.name)
                self.games_list = TournamentClass.global_tounraments

    def edit_update(self):
        self.games_list = TournamentClass.global_tounraments
        self.games_list[0].create_round()

    def add_game(self):
        TournamentClass.global_tounraments = self.games_list
        setupWin()
    
    def add_player(self):
        self.dialog = ctk.CTkInputDialog(text="Enter New Player's Name:", title="Add New Player")
        nameValue =self.dialog.get_input()
        if nameValue != "":
            for game in self.games_list:
                if game.name == self.tabview.get():
                    game.players[nameValue] = [0, []]
    
    def remove_player(self):
        self.dialog = ctk.CTkInputDialog(text="Enter Player's Name:\nTHIS WILL REMOVE THEM", title="Remove Player")
        nameValue =self.dialog.get_input()
        if nameValue != "":
            for game in self.games_list:
                if game.name == self.tabview.get():
                    if nameValue in game.players:
                        del game.players[nameValue]

    def add_game_update(self):
        self.old_list = self.games_list
        self.games_list = TournamentClass.global_tounraments

        game = self.games_list[-1]

        self.tabview.add(game.name)

        self.tab_frames.append(ctk.CTkFrame(master=self.tabview.tab(game.name)))
        self.tab_frames[-1].pack(pady=5, padx=5, fill="both", expand=True)
        self.tab_create_round_buttons.append(ctk.CTkButton(master = self.tab_frames[-1], text=f"Generate Round", font=("Lucida Console", 20), command=lambda x=game: self.create_round(x)))
        self.tab_create_round_buttons[-1].pack(pady=5, padx=5)
        self.game_tab_items[game.name] = [0, [], []]
        self.game_tab_items[game.name][0] = (ctk.CTkFrame(master=self.tab_frames[-1]))
        self.game_tab_items[game.name][0].pack(pady=5, padx=5, fill="both", expand=True)

        #self.tabview.grid(row=0, column=1, padx=5, pady=5, rowspan=4, sticky="nswe")

    def resize(self, event):
        if event.widget == self.root:
            self.gridSize = [int(event.width/110), 10]
    
    def updateResize(self):
        for game in self.games_list:
            if game.name == self.tabview.get():
                self.display_pairings(game, self.saved_pairs[self.tabview.get()])

    def confirm_popup(self, cmd, msg, buttonmsg):
        self.window = ctk.CTkToplevel(self.root)
        self.window.geometry("400x200")

        self.label = ctk.CTkLabel(self.window, text=msg)
        self.label.pack(side="top", fill="both", expand=True, padx=40, pady=40)
        self.confirmSave = ctk.CTkButton(self.window, text=buttonmsg, font=("Lucida Console", 20), command=lambda: cmd())
        self.confirmSave.pack(pady=10, padx=30, fill="both")

    def get_rankings(self):
        for game in self.games_list:
            if game.name == self.tabview.get():
                rankings = game.get_rankings()
                rankPDF.rank_pdf(rankings, game.name)

    def closeWindow(self):
        self.root.destroy()

    def generate_pdf(self):
        writePDF.generateTournmanetPDFs()
        #writePDF.writepdf(self.saved_pairs[self.tabview.get()], 20, ['3', '4'], "PrintableMatches/test2.pdf")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

#test = tournamentWin()