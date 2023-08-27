import TournamentClass
import random
from fpdf import FPDF
from fpdf import XPos, YPos
import json
import random

ET_rooms = ['1']
HI_rooms = ['2']
HT_rooms = ['3', '4'] 
ET_rooms = ['5', '6']

c = 0
r = 0

def writepdf(pairings, roomsize, rooms, name, is_team):
    global c, r
    shuffled_pairings = []
    for match in pairings:
        shuffled_pairings.append(tuple(random.sample(match, 2)))
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=26)
    line_height = pdf.font_size * 2
    col_width = pdf.epw / 4
    pdf.cell(200, 10, name, align = 'C')
    pdf.ln(line_height)
    pdf.set_font("Times", size=14)
    line_height = pdf.font_size * 2.5
    pdf.cell(col_width, line_height, 'White', border=1, align='C')
    pdf.cell(col_width, line_height, 'Black', border=1, align='C')
    pdf.cell(col_width, line_height, 'Room #', border=1, align='C')
    pdf.cell(col_width, line_height, 'Board #', border=1, align='C')
    pdf.ln(line_height)
    for item in shuffled_pairings:
        if c == roomsize:
            r+=1
            c = 0
        for value in item:
            if is_team:
                #player = f'{value[0]} ({value[1]})'
                player = f'{value[0]}'
            else:
                player = f'{value[0]}'
            if len(player) > 25:
                pdf.set_font("Times", size=int(14/(len(player)/23)))
            pdf.cell(col_width, line_height, player, border=1, align='C')
            pdf.set_font("Times", size=14)
        pdf.cell(col_width, line_height, rooms[r], border=1, align='C')
        pdf.cell(col_width, line_height, str(c+1), border=1, align='C')
        pdf.ln(line_height)
        c+=1

    pdf.output(f"PrintableMatches/{name}.pdf")

def generateTournmanetPDFs():
    global c, r
    c = 0
    r = 0

    with open('Data/data.json', 'r') as openfile:
        room_data = json.load(openfile)

    for game in TournamentClass.global_tounraments:
        writepdf(game.pairs, room_data[0], room_data[1], game.name, game.is_team)
        c = 0
        r += 1