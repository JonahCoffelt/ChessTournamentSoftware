global_tounraments = []

global_round_team_points = {}

import random
import math

class Tournament():

  def __init__(self, name, players, is_team=False):
    self.is_team = is_team
    self.name = name

    self.pairs = []

    # initialize players
    if not self.is_team:
      self.players = {
        player[0]: [0, []]
        for player in players
      }
    # initialize teams
    else:
      self.players = {
        team[0]: [
          0, [],
          {player: [0, []]
           for player in team[1:]}
        ]
        for team in players
      }

    
    l = list(self.players.items())
    random.shuffle(l)
    self.players = dict(l)

  def create_round(self):
    new_round = {}

    l = list(self.players.items())
    random.shuffle(l)
    self.players = dict(l)

    current_player_list = self.players
    current_player_list = {
      k: v
      for k, v in sorted(
        current_player_list.items(), key=lambda item: item[1][0], reverse=True)
    }

    pairs = []

    i = 1
    check_redundancy = True
    while len(current_player_list) > 1:
      player = list(current_player_list.keys())[0]
      opponent = list(current_player_list.keys())[i]
      #print(player)
      i+=1
      if not opponent in self.players[player][1] or not check_redundancy:
        new_round[player] = current_player_list[player]
        new_round[opponent] = current_player_list[opponent]
        current_player_list.pop(player)
        current_player_list.pop(opponent)
        pairs.append(((player, None), (opponent, None)))
        self.players[player][1].append(opponent)
        self.players[opponent][1].append(player)
        check_redundancy = True
        i=1
        
      if i >= len(current_player_list):
        check_redundancy = False
        i=1
    
    if len(current_player_list):
      self.players[list(current_player_list.keys())[0]][1].append("Magnus Carlsen")
      pairs.append(((list(current_player_list.keys())[0], None), ("Magnus Carlsen", None)))

    if self.is_team:
      pairs = self.pair_teams()

    #print("h:",new_round)
    self.pairs = pairs
    return pairs

  def sort_teams(self):
    for team in self.players:
      current_player_list = self.players[team][2]
      current_player_list = {
        k: v
        for k, v in sorted(current_player_list.items(),
                           key=lambda item: item[1][0],
                           reverse=True)
      }
      self.players[team][2] = current_player_list

  def pair_teams(self):
    self.sort_teams()

    team_list = list(self.players)
    
    bai_team = False
    for team in team_list:
      if list(self.players[team][1])[-1] == "Magnus Carlsen":
        bai_team = team
    if bai_team:
      team_list.remove(bai_team)
      team_list.append(bai_team)

    pairs = []

    team=0
    while len(team_list) > 1:
      team_players = list(self.players[team_list[team * 2]][2])
      opponent_team_players = list(self.players[self.players[team_list[team * 2]][1][-1]][2])
      i = 0
      check_redundancy = True
      while len(team_players):
        if not opponent_team_players[i] in self.players[team_list[team * 2]][2][team_players[0]][1] or not check_redundancy:
          pairs.append(((team_players[0], team_list[team * 2]), (opponent_team_players[i], self.players[team_list[team * 2]][1][-1])))
          self.players[team_list[team * 2]][2][team_players[0]][1].append(opponent_team_players[i])
          self.players[self.players[team_list[team * 2]][1][-1]][2][opponent_team_players[i]][1].append(team_players[0])
          team_players.pop(0)
          opponent_team_players.pop(i)
          i = -1
        i += 1
        if i >= len(opponent_team_players):
          check_redundancy = False
          i=0
      team_list.remove(self.players[team_list[team * 2]][1][-1])
      team_list.pop(0)

    i=1
    if len(team_list):
      current_player_list = list(self.players[team_list[-1]][2])
      check_redundancy = True
      while len(current_player_list) > 1:
        player = current_player_list[0]
        #print(current_player_list)
        opponent = current_player_list[i]
        i += 1
        if not opponent in self.players[team_list[0]][2][player][1] or not check_redundancy:
          self.players[team_list[0]][2][player][1].append(opponent)
          self.players[team_list[0]][2][opponent][1].append(player)
          pairs.append(((player, team_list[0]), (opponent, team_list[0])))
          #print("HHH:",(player, team_list[0], opponent, team_list[0]))
          current_player_list.remove(player)
          current_player_list.remove(opponent)
          check_redundancy = True
          i = 1
  
        if i >= len(current_player_list):
          check_redundancy = False
          i = 1

    return pairs

  def add_points(self, score, player, team=None):
    if team:
      self.players[team][2][player][0] += score
      if team in list(global_round_team_points):
        global_round_team_points[team] += score
      else:
        global_round_team_points[team] = score
    else:
      self.players[player][0] += score
  
  def finish_team_round(self):
    global global_round_team_points
    for team in list(global_round_team_points):
      if global_round_team_points[team] > 3.0:
        self.players[team][0] += 1.0
      elif self.players[team][1][-1] == "Magnus Carlsen":
        self.players[team][0] += 1.0
      elif global_round_team_points[team] == 3.0:
        self.players[team][0] += .5
    global_round_team_points = {}
    
  def get_rankings(self):
    ranking_list = self.players
    ranking_list = [
      (k, v[0]) for k, v in sorted(ranking_list.items(), key=lambda item: item[1][0], reverse=True)
    ]
    return ranking_list
    