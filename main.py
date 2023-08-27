import customtkinter as ctk

from loginWindow import loginWin
from tournamentWindow import tournamentWin
from gameSetUpWindow import setupWin

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

window = setupWin()
tournament_main = tournamentWin(window.load)
