import TournamentClass
import random
from fpdf import FPDF
from fpdf import XPos, YPos
import json

def rank_pdf(ranking, game_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=26)
    line_height = pdf.font_size * 2
    col_width = pdf.epw / 2
    pdf.cell(200, 10, f"{game_name} Results", align = 'C')
    pdf.ln(line_height)
    pdf.set_font("Times", size=14)
    line_height = pdf.font_size * 2.5
    pdf.cell(col_width, line_height, 'Player', border=1, align='C')
    pdf.cell(col_width, line_height, 'Score', border=1, align='C')
    pdf.ln(line_height)
    for item in ranking:
        player = item[0]
        score = str(item[1])
        if len(player) > 25:
            pdf.set_font("Times", size=int(14/(len(player)/23)))
        pdf.cell(col_width, line_height, player, border=1, align='C')
        pdf.set_font("Times", size=14)
        pdf.cell(col_width, line_height, score, border=1, align='C')
        pdf.ln(line_height)

    pdf.output(f"PrintableMatches/{game_name} RankingsCurrent.pdf")