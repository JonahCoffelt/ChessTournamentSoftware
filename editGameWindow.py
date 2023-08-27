import customtkinter as ctk

import TournamentClass

class editWin():
    def __init__(self, players, is_team, name):
        
        if is_team:
            self.playersList = []
            for team in list(players):
                players = [player for player in list(players[team][2])]
                players.insert(0, team)
                print(players)
                self.playersList.append(players)
            #self.playersList = [[team, player] for team in list(players) for player in list(players[team][2])]
        else:
            self.playersList = [[player] for player in list(players)]

        self.is_team = is_team
        self.name = name

        print(self.playersList)

        self.teamsMode = is_team
        self.warningMessage = False
        self.gridSize = (4, 40)
        self.resizeNeeded = False

        # setup root
        self.root = ctk.CTk()
        self.root.title("Chess Tournament")
        self.root.geometry("1200x700")

        # configure grid layout
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure((2, 3), weight=0)
        self.root.grid_rowconfigure((0, 1, 2), weight=1)
        self.root.bind('<Configure>', self.resize)
        self.root.bind("<Return>", self.keyup)

        # configure sidebar
        self.sidebarFrame = ctk.CTkFrame(self.root, width=600, corner_radius=0)
        self.sidebarFrame.grid(row=0, column=0, padx=5, pady=5, rowspan=4, sticky="nsew")
        self.sidebarFrame.grid_rowconfigure(4, weight=1)
        self.titleFrame = ctk.CTkFrame(self.sidebarFrame)
        self.titleFrame.pack(pady=10, padx=10, fill="both")
        title = ctk.CTkLabel(master=self.titleFrame, text="     Edit Game     ", font=("Lucida Console", 24))
        title.pack(pady=12, padx=10)
        self.finalizeButton = ctk.CTkButton(master = self.sidebarFrame, text="Finalize/Save Game", font=("Lucida Console", 16), command=self.saveChanges)
        self.finalizeButton.pack(pady=10, padx=10, fill="both")
        self.resizeButton = ctk.CTkButton(master = self.sidebarFrame, text="Resize Grid", font=("Lucida Console", 16), command=self.updateResize)
        self.resizeButton.pack(pady=10, padx=10, fill="both")
        # initialize player/team add frame
        if self.is_team:
            self.addTeamsFrame(6)
        else:
            self.addPlayersFrame()

        #configure current players frame
        self.currentPlayersFrame = ctk.CTkFrame(self.root)
        self.currentPlayersFrame.grid(row=0, column=1, padx=5, pady=5, rowspan=4, sticky="nsew")

        # configure edit-bar
        self.editbarFrame = ctk.CTkFrame(self.root, width=250, corner_radius=0)
        self.editbarFrame.grid(row=0, column=2, padx=5, pady=5, rowspan=4, sticky="nsew")
        self.editbarFrame.grid_rowconfigure(4, weight=1)

        if self.is_team:
            self.showTeamList()
        else:
            self.showPlayerList()

        self.root.mainloop() 

    def showEditbarPlayer(self, player):
        self.editbarFrame.destroy()
        self.editbarFrame = ctk.CTkFrame(self.root, width=250, corner_radius=0)
        self.editbarFrame.grid(row=0, column=2, padx=5, pady=5, rowspan=4, sticky="nsew")
        self.editbarFrame.grid_rowconfigure(4, weight=1)

        self.editTitleFrame = ctk.CTkFrame(self.editbarFrame, width=200)
        self.editTitleFrame.pack(pady=5, padx=5, fill="both")
        editName = ctk.CTkLabel(master=self.editTitleFrame, text=f"{self.playersList[player][0]}", font=("Lucida Console", 16), width=200)
        editName.pack(pady=5, padx=5, fill="both", expand=True)
        self.editNameButton =ctk.CTkButton(master = self.editbarFrame, text=f"Edit Name", font=("Lucida Console", 20), command=lambda x=player: self.editPlayerName(x))
        self.editNameButton.pack(pady=5, padx=5, fill="both")
        self.removePlayerButton =ctk.CTkButton(master = self.editbarFrame, text=f"Remove Player", font=("Lucida Console", 20), command=lambda x=player: self.removePlayerPopup(x))
        self.removePlayerButton.pack(pady=5, padx=5, fill="both")
    
    def showEditbarTeam(self, team):
        self.editbarFrame.destroy()
        self.editbarFrame = ctk.CTkFrame(self.root, width=250, corner_radius=0)
        self.editbarFrame.grid(row=0, column=2, padx=5, pady=5, rowspan=4, sticky="nsew")
        self.editbarFrame.grid_rowconfigure(4, weight=1)

        self.editTitleFrame = ctk.CTkFrame(self.editbarFrame, width=200)
        self.editTitleFrame.pack(pady=5, padx=5, fill="both")
        editName = ctk.CTkLabel(master=self.editTitleFrame, text=f"{self.playersList[team][0]}", font=("Lucida Console", 16), width=200)
        editName.pack(pady=5, padx=5, fill="both", expand=True)
        self.editNameButton =ctk.CTkButton(master = self.editbarFrame, text=f"Edit Team Name", font=("Lucida Console", 20), command=lambda x=team: self.editPlayerName(0, x))
        self.editNameButton.pack(pady=5, padx=5, fill="both")
        self.removeTeamButton =ctk.CTkButton(master = self.editbarFrame, text=f"Remove Team", font=("Lucida Console", 20), command=lambda x=team: self.removePlayerPopup(x))
        self.removeTeamButton.pack(pady=5, padx=5, fill="both")

        self.editTeamTitleFrame = ctk.CTkFrame(self.editbarFrame, width=200)
        self.editTeamTitleFrame.pack(pady=20, padx=5)
        editName = ctk.CTkLabel(master=self.editTeamTitleFrame, text="Edit Player Names", font=("Lucida Console", 16), width=200)
        editName.pack(pady=5, padx=5)

        self.teamPlayerEdits = []
        self.teamPlayerRemovals = []

        i = 0
        for player in self.playersList[team][1:]:
            self.teamPlayerEdits.append(ctk.CTkButton(master = self.editbarFrame, text=f"Edit {player}", font=("Lucida Console", 20), command=lambda x=i+1, t=team: self.editPlayerName(x, t)))
            self.teamPlayerEdits[-1].pack(pady=5, padx=5, fill="both")
            i += 1


    def showPlayerList(self):
        self.currentPlayersFrame.destroy()
        self.currentPlayersFrame = ctk.CTkFrame(self.root)
        self.currentPlayersFrame.grid(row=0, column=1, padx=5, pady=5, rowspan=4, sticky="nsew")
        self.playerFrames = [] 
        self.playerEditButtons = []
        i = 0
        for player in self.playersList:
            self.playerFrames.append(ctk.CTkFrame(self.currentPlayersFrame))
            self.playerFrames[-1].grid(row=i//self.gridSize[0], column=i%self.gridSize[0], padx=5, pady=5)
            self.playerEditButtons.append(ctk.CTkButton(master = self.playerFrames[-1], text=f"{player[0]}", font=("Lucida Console", 20), width=self.gridSize[1], command=lambda x=i: self.showEditbarPlayer(x)))
            self.playerEditButtons[-1].pack(pady=5, padx=5, fill="both")
            i += 1
    
    def showTeamList(self):
        self.currentPlayersFrame.destroy()
        self.currentPlayersFrame = ctk.CTkFrame(self.root)
        self.currentPlayersFrame.grid(row=0, column=1, padx=5, pady=5, rowspan=4, sticky="nsew")
        self.teamFrames = [] 
        self.teamEditButtons = []
        i = 0
        for team in self.playersList:
            self.teamFrames.append(ctk.CTkFrame(self.currentPlayersFrame))
            self.teamFrames[-1].grid(row=i//self.gridSize[0], column=i%self.gridSize[0], padx=5, pady=5)
            self.teamEditButtons.append(ctk.CTkButton(master = self.teamFrames[-1], text=f"{team[0]}", font=("Lucida Console", 20), width=self.gridSize[1], command=lambda x=i: self.showEditbarTeam(x)))
            self.teamEditButtons[-1].pack(pady=5, padx=5, fill="both")
            for player in range(1, len(team)):
                teamPlayerLabel = ctk.CTkLabel(master=self.teamFrames[-1], text=f"{team[player]}", font=("Lucida Console", 12))
                teamPlayerLabel.pack(pady=0, padx=0)
            i += 1

    def addPlayerEntry(self):
        if str(self.individualEntry.get()) != "":
            self.playersList.append([f"{self.individualEntry.get()}"])
            self.showPlayerList()
            self.individualEntry.delete(0, len(self.individualEntry.get()))

    def addTeamEntry(self):
        add = True
        for playerName in self.entries:
            if str(playerName.get()) == "":
                add = False
        if add:
            self.playersList.append([f"{etry.get()}" for etry in self.entries])
            for playerName in self.entries:
                playerName.delete(0, len(playerName.get()))
            self.showTeamList()
        print(self.playersList)

    def addPlayersFrame(self):
        self.addButtonFrame = ctk.CTkFrame(self.sidebarFrame)
        self.addButtonFrame.pack(pady=10, padx=10, fill="both", expand=True)
        self.individualEntry = ctk.CTkEntry(master=self.addButtonFrame, placeholder_text="Player Name", font=("Lucida Console", 12))
        self.individualEntry.pack(pady=10, padx=10, fill="both")
        self.addPlayerButton = ctk.CTkButton(master = self.addButtonFrame, text="Add Player", font=("Lucida Console", 20), command=self.addPlayerEntry)
        self.addPlayerButton.pack(pady=20, padx=30, fill="both")
    
    def addTeamsFrame(self, teamSize):
        self.addButtonFrame = ctk.CTkFrame(self.sidebarFrame)
        self.addButtonFrame.pack(pady=10, padx=10, fill="both", expand=True)
        self.entries = []
        self.entries.append(ctk.CTkEntry(master=self.addButtonFrame, placeholder_text="Team Name", font=("Lucida Console", 12)))
        self.entries[0].pack(pady=20, padx=40, fill="both")
        for player in range(teamSize):
            self.entries.append(ctk.CTkEntry(master=self.addButtonFrame, placeholder_text="Player {} Name".format(player+1), font=("Lucida Console", 12)))
            self.entries[-1].pack(pady=10, padx=10, fill="both")
        self.addTeamButton = ctk.CTkButton(master = self.addButtonFrame, text="Add Team", font=("Lucida Console", 20), command=self.addTeamEntry)
        self.addTeamButton.pack(pady=10, padx=30, fill="both")

    def resize(self, event):
        if event.widget == self.root:
            if (event.width-700)/6 != self.gridSize[1]:
                self.gridSize = (self.gridSize[0], (event.width-720)/(self.gridSize[0]+2))
    
    def editPlayerName(self, player, team=None):
        self.dialog = ctk.CTkInputDialog(text="Enter New Name:", title="Change Player Name")
        nameValue =self.dialog.get_input()
        if nameValue != "":
            if team != None:
                self.playersList[team][player] = nameValue
                self.showTeamList()
                self.showEditbarTeam(team)
            else:
                self.playersList[player][0] = nameValue
                self.showPlayerList()
                self.showEditbarPlayer(player)
    
    def removePlayer(self, player, team=None):
        if team:
            self.playersList.pop(team[player])
        else:
            self.playersList.pop(player)

        self.window.destroy()
        if self.teamsMode:
            self.showTeamList()
        else:
            self.showPlayerList()
        self.editbarFrame.destroy()
        self.editbarFrame = ctk.CTkFrame(self.root, width=250, corner_radius=0)
        self.editbarFrame.grid(row=0, column=2, padx=5, pady=5, rowspan=4, sticky="nsew")
        self.editbarFrame.grid_rowconfigure(4, weight=1)

    def removePlayerPopup(self, player, team=None):
        self.window = ctk.CTkToplevel(self.root)
        self.window.geometry("400x200")

        self.label = ctk.CTkLabel(self.window, text="Are you sure you want to remove this player?")
        self.label.pack(side="top", fill="both", expand=True, padx=40, pady=40)
        self.confirmRemoval = ctk.CTkButton(self.window, text="Remove Player", font=("Lucida Console", 20), command=lambda x=player: self.removePlayer(x, team))
        self.confirmRemoval.pack(pady=10, padx=30, fill="both")

    def keyup(self, e):
        if self.teamsMode:
            self.addTeamEntry()
        else:
            self.addPlayerEntry()

    def updateResize(self):
        if self.teamsMode:
            self.showTeamList()
        else:
            self.showPlayerList()

    def saveChanges(self):
        self.window = ctk.CTkToplevel(self.root)
        self.window.geometry("400x200")

        self.label = ctk.CTkLabel(self.window, text="Are you sure you want save? \nDoing this will overwrite the current game")
        self.label.pack(side="top", fill="both", expand=True, padx=40, pady=40)
        self.confirmRemoval = ctk.CTkButton(self.window, text="Save Changes", font=("Lucida Console", 20), command=lambda: self.updateOldGame())
        self.confirmRemoval.pack(pady=10, padx=30, fill="both")
    
    def updateOldGame(self):
        i = 0
        for game in TournamentClass.global_tounraments:
            if game.name == self.name:
                TournamentClass.global_tounraments[i] = TournamentClass.Tournament(self.name, self.playersList, is_team = self.is_team)
            i += 1
        self.root.destroy()

    def closeWindow(self):
        self.load = False
        self.root.destroy()