from rgbmatrix import graphics
from utils import get_font, get_file
import json

class TeamsRenderer:
  """Renders the scoreboard team banners including background color, team abbreviation text,
  and their scored runs."""

  def __init__(self, canvas, home_team, away_team, data):
    self.canvas = canvas
    self.home_team = home_team
    self.away_team = away_team
    self.data = data
    self.default_colors = self.data.config.team_colors.color("default")

  def __team_colors(self, team_abbrev):
    try:
      team_colors = self.data.config.team_colors.color(team_abbrev.lower())
    except KeyError as e:
      team_colors = self.data.config.team_colors.color("default")
    return team_colors

  def __default_home_color(self):
    return self.data.config.team_colors.color("default.home")
  
  def __default_accent_color(self):
    return self.data.config.team_colors.color("default.accent")

  def render(self):
    away_colors = self.__team_colors(self.away_team.abbrev)
    try:
      away_team_color = away_colors['home']
    except KeyError as e:
      away_team_color = self.__default_home_color()
      
    home_colors = self.__team_colors(self.home_team.abbrev)
    try:
      home_team_color = home_colors['home']
    except KeyError as e:
      home_team_color = self.__default_home_color()
      
    away_accents = self.__team_colors(self.away_team.abbrev)
    try:
      away_team_accent = away_accents['accent']
    except KeyError as e:
      away_team_accent = self.__default_accent_color()
      
    home_accents = self.__team_colors(self.home_team.abbrev)
    try:
      home_team_accent = home_accents['accent']
    except KeyError as e:
      home_team_accent = self.__default_accent_color()

    bg_coords = {}
    bg_coords["away"] = self.data.config.layout.coords("teams.background.away")
    bg_coords["home"] = self.data.config.layout.coords("teams.background.home")
    
    accent_coords = {}
    accent_coords["away"] = self.data.config.layout.coords("teams.accent.away")
    accent_coords["home"] = self.data.config.layout.coords("teams.accent.home")

    away_name_coords = self.data.config.layout.coords("teams.name.away")
    home_name_coords = self.data.config.layout.coords("teams.name.home")

    away_score_coords = self.data.config.layout.coords("teams.runs.away")
    home_score_coords = self.data.config.layout.coords("teams.runs.home")
    away_hits_coords = self.data.config.layout.coords("teams.hits.away")
    home_hits_coords = self.data.config.layout.coords("teams.hits.home")
    away_errors_coords = self.data.config.layout.coords("teams.errors.away")
    home_errors_coords = self.data.config.layout.coords("teams.errors.home")

    for team in ["away","home"]:
      for x in range(bg_coords[team]["width"]):
        for y in range(bg_coords[team]["height"]):
          color = away_team_color if team == "away" else home_team_color
          x_offset = bg_coords[team]["x"]
          y_offset = bg_coords[team]["y"]
          self.canvas.SetPixel(x + x_offset, y + y_offset, color['r'], color['g'], color['b'])
    
    for team in ["away","home"]:
      for x in range(accent_coords[team]["width"]):
        for y in range(accent_coords[team]["height"]):
          color = away_team_accent if team == "away" else home_team_accent
          x_offset = accent_coords[team]["x"]
          y_offset = accent_coords[team]["y"]
          self.canvas.SetPixel(x + x_offset, y + y_offset, color['r'], color['g'], color['b'])
          
    self.__render_team_text(self.away_team, "away", away_colors, away_name_coords["x"], away_name_coords["y"])
    self.__render_team_text(self.home_team, "home", home_colors, home_name_coords["x"], home_name_coords["y"])
    self.__render_team_score(self.away_team.runs, self.away_team.hits, self.away_team.errors, "away", away_colors, away_score_coords["x"], away_score_coords["y"])
    self.__render_team_score(self.home_team.runs, self.home_team.hits, self.home_team.errors, "home", home_colors, home_score_coords["x"], home_score_coords["y"])
    self.__render_team_hits(self.away_team.hits, self.away_team.errors, "away", away_colors, away_hits_coords["x"], away_hits_coords["y"])
    self.__render_team_hits(self.home_team.hits, self.home_team.errors, "home", home_colors, home_hits_coords["x"], home_hits_coords["y"])
    self.__render_team_errors(self.away_team.errors, "away", away_colors, away_errors_coords["x"], away_errors_coords["y"])
    self.__render_team_errors(self.home_team.errors, "home", home_colors, home_errors_coords["x"], home_errors_coords["y"])

  def __render_team_text(self, team, homeaway, colors, x, y):
    text_color = colors.get('text', self.default_colors['text'])
    text_color_graphic = graphics.Color(text_color['r'], text_color['g'], text_color['b'])
    font = self.data.config.layout.font("teams.name.{}".format(homeaway))
    team_text = '{:3s}'.format(team.abbrev.upper())
    if self.data.config.full_team_names and self.canvas.width > 32:
      team_text = '{:13s}'.format(team.name)
    graphics.DrawText(self.canvas, font["font"], x, y, text_color_graphic, team_text)

  def __render_team_score(self, runs, hits, errors, homeaway, colors, x, y):
    text_color = colors.get('text', self.default_colors['text'])
    text_color_graphic = graphics.Color(text_color['r'], text_color['g'], text_color['b'])
    coords = self.data.config.layout.coords("teams.runs.{}".format(homeaway))
    font = self.data.config.layout.font("teams.runs.{}".format(homeaway))
    team_runs = str(runs)
    if runs == 1:
     team_runs_x = coords["x"] + 1
    elif runs == 11:
     team_runs_x = coords["x"] - 2
    elif (runs >=11 and runs <= 19) or runs == 10 or runs == 21 or runs == 31 or runs == 41:
     team_runs_x = coords["x"] - 3
    elif runs > 10:
     team_runs_x = coords["x"] - 4
    else:
     team_runs_x = coords["x"]
    graphics.DrawText(self.canvas, font["font"], team_runs_x, y, text_color_graphic, team_runs)

  def __render_team_hits(self, hits, errors, homeaway, colors, x, y):
    text_color = colors.get('text', self.default_colors['text'])
    text_color_graphic = graphics.Color(text_color['r'], text_color['g'], text_color['b'])
    coords = self.data.config.layout.coords("teams.hits.{}".format(homeaway))
    font = self.data.config.layout.font("teams.hits.{}".format(homeaway))
    team_hits = str(hits)
    if hits == 1:
     team_hits_x = coords["x"] + 1
    elif hits == 11:
     team_hits_x = coords["x"] - 2
    elif (hits >= 11 and hits <= 19) or hits == 10 or hits == 21 or hits == 31 or hits == 41:
     team_hits_x = coords["x"] - 3
    elif hits > 10:
     team_hits_x = coords["x"] - 4
    else:
     team_hits_x = coords["x"]
    graphics.DrawText(self.canvas, font["font"], team_hits_x, y, text_color_graphic, team_hits)

  def __render_team_errors(self, errors, homeaway, colors, x, y):
    text_color = colors.get('text', self.default_colors['text'])
    text_color_graphic = graphics.Color(text_color['r'], text_color['g'], text_color['b'])
    coords = self.data.config.layout.coords("teams.errors.{}".format(homeaway))
    font = self.data.config.layout.font("teams.errors.{}".format(homeaway))
    team_errors = str(errors)
    if errors == 1:
     team_errors_x = coords["x"] + 1
    else:
     team_errors_x = coords["x"]
    graphics.DrawText(self.canvas, font["font"], team_errors_x, y, text_color_graphic, team_errors)
