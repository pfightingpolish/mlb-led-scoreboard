from PIL import Image
from rgbmatrix import graphics
from utils import get_font, get_file, center_text_position
from renderers.network import NetworkErrorRenderer
from renderers.offday import OffdayRenderer
import time

class StandingsRenderer:
  def __init__(self, matrix, canvas, data):
    self.matrix = matrix
    self.canvas = canvas
    self.data = data
    self.colors = data.config.scoreboard_colors
    self.bg_color = self.colors.graphics_color("standings.background")
    self.divider_color = self.colors.graphics_color("standings.divider")
    self.stat_color = self.colors.graphics_color("standings.stat")
    self.team_stat_color = self.colors.graphics_color("standings.team.stat")
    self.team_name_color = self.colors.graphics_color("standings.team.name")

  def render(self):
    self.__fill_bg()
    if self.__is_dumpster_fire():
      self.__render_dumpster_fire()
    else:
      if self.canvas.width > 32:
        self.__render_static_wide_standings()
      else:
        self.__render_rotating_standings()
    NetworkErrorRenderer(self.canvas, self.data).render()

  def __fill_bg(self):
    coords = self.data.config.layout.coords("standings")
    for y in range(0, coords["height"]):
      graphics.DrawLine(self.canvas, 0, y, coords["width"], y, self.bg_color)

  def __render_rotating_standings(self):
    coords = self.data.config.layout.coords("standings")
    font = self.data.config.layout.font("standings")
    stat = 'w'
    starttime = time.time()
#    while True:
#      offset = coords["offset"]
#      graphics.DrawText(self.canvas, font["font"], coords["stat_title"]["x"], offset, self.stat_color, stat.upper())
#      graphics.DrawLine(self.canvas, coords["divider"]["x"], 0, coords["divider"]["x"], coords["height"], self.divider_color)

#      interator = 0
#      for team in self.data.current_standings().get('teams')[iterator]:
#        graphics.DrawLine(self.canvas, 0, offset, coords["width"], offset, self.divider_color)

#        team_text = "{:13s}".format(team.team_name)
#        stat_text = str(getattr(team, stat))
#        graphics.DrawText(self.canvas, font["font"], coords["team"]["name"]["x"], offset, self.team_name_color, team_text)
#        graphics.DrawText(self.canvas, font["font"], coords["team"]["record"]["x"], offset, self.team_stat_color, stat_text)
      
#        offset += coords["offset"]
      
#      self.matrix.SwapOnVSync(self.canvas)
#      time.sleep(5.0)

#      self.__fill_bg()

#      if stat == 'l':
#        self.data.advance_to_next_standings()
#        stat = 'w'
#      else:
#        stat = 'l'

  def __render_static_wide_standings(self):
    coords = self.data.config.layout.coords("standings")
    font = self.data.config.layout.font("standings")
    font2 = self.data.config.layout.font("standings_title")

    offset = coords["offset"]
#      graphics.DrawLine(self.canvas, coords["divider"]["x"], 0, coords["divider"]["x"], coords["height"], self.divider_color)

#      for team in self.data.current_standings().get('teams')[0]:
#        graphics.DrawLine(self.canvas, 0, offset, coords["width"], offset, self.divider_color)

    i = 0

    while i < 6:
      division_name = self.data.current_standings().get('div_name')
      if division_name == "American League West":
        division_name = "AL WEST"

        image_file =  get_file("Assets/ALWatermark.jpg")
        image = Image.open(image_file)
        image_rgb = image.convert("RGB")
	self.canvas.SetImage(image_rgb,28,0)

      elif division_name == "American League Central":
        division_name = "AL CENTRAL"

        image_file =  get_file("Assets/ALWatermark.jpg")
        image = Image.open(image_file)
        image_rgb = image.convert("RGB")
	self.canvas.SetImage(image_rgb,28,0)

      elif division_name == "American League East":
        division_name = "AL EAST"

        image_file =  get_file("Assets/ALWatermark.jpg")
        image = Image.open(image_file)
        image_rgb = image.convert("RGB")
	self.canvas.SetImage(image_rgb,28,0)

      elif division_name == "National League West":
        division_name = "NL WEST"

        image_file =  get_file("Assets/NLWatermark.jpg")
        image = Image.open(image_file)
        image_rgb = image.convert("RGB")
	self.canvas.SetImage(image_rgb,57,0)

      elif division_name == "National League Central":
        division_name = "NL CENTRAL"

        image_file =  get_file("Assets/NLWatermark.jpg")
        image = Image.open(image_file)
        image_rgb = image.convert("RGB")
	self.canvas.SetImage(image_rgb,57,0)

      elif division_name == "National League East":

        division_name = "NL EAST"

        image_file =  get_file("Assets/NLWatermark.jpg")
        image = Image.open(image_file)
        image_rgb = image.convert("RGB")
	self.canvas.SetImage(image_rgb,57,0)

      else:
        division_name = "#ERROR!"

      record_start = 76
      gb_start = 108

      graphics.DrawText(self.canvas, font2["font"], 2, 11, self.team_name_color, division_name)

      graphics.DrawLine(self.canvas, 0, 13, 164, 13, self.divider_color)

      team_text = self.__team_shortener(self.data.current_standings().get('teams')[0].get('name'))
      graphics.DrawText(self.canvas, font["font"], 2, 22, self.team_name_color, team_text)

      record_text = "{}-{}".format(self.data.current_standings().get('teams')[0].get('w'), self.data.current_standings().get('teams')[0].get('l'))

      if "-" in self.data.current_standings().get('teams')[0].get('gb'):
        gb_text = " -  "
      else:
        gb_text = format(self.data.current_standings().get('teams')[0].get('gb'))

      graphics.DrawText(self.canvas, font["font"], record_start, 22, self.team_stat_color, record_text)
      graphics.DrawText(self.canvas, font["font"], gb_start, 22, self.team_stat_color, gb_text)

      team_text = self.__team_shortener(self.data.current_standings().get('teams')[1].get('name'))
      graphics.DrawText(self.canvas, font["font"], 2, 32, self.team_name_color, team_text)

      record_text = "{}-{}".format(self.data.current_standings().get('teams')[1].get('w'), self.data.current_standings().get('teams')[1].get('l'))

      if "-" in self.data.current_standings().get('teams')[1].get('gb'):
        gb_text = " -  "
      else:
        gb_text = format(self.data.current_standings().get('teams')[1].get('gb'))

      graphics.DrawText(self.canvas, font["font"], record_start, 32, self.team_stat_color, record_text)
      graphics.DrawText(self.canvas, font["font"], gb_start, 32, self.team_stat_color, gb_text)

      team_text = self.__team_shortener(self.data.current_standings().get('teams')[2].get('name'))
      graphics.DrawText(self.canvas, font["font"], 2, 42, self.team_name_color, team_text)

      record_text = "{}-{}".format(self.data.current_standings().get('teams')[2].get('w'), self.data.current_standings().get('teams')[2].get('l'))

      if "-" in self.data.current_standings().get('teams')[2].get('gb'):
        gb_text = " -  "
      else:
        gb_text = format(self.data.current_standings().get('teams')[2].get('gb'))

      graphics.DrawText(self.canvas, font["font"], record_start, 42, self.team_stat_color, record_text)
      graphics.DrawText(self.canvas, font["font"], gb_start, 42, self.team_stat_color, gb_text)

      team_text = self.__team_shortener(self.data.current_standings().get('teams')[3].get('name'))
      graphics.DrawText(self.canvas, font["font"], 2, 52, self.team_name_color, team_text)

      record_text = "{}-{}".format(self.data.current_standings().get('teams')[3].get('w'), self.data.current_standings().get('teams')[3].get('l'))

      if "-" in self.data.current_standings().get('teams')[3].get('gb'):
        gb_text = " -  "
      else:
        gb_text = format(self.data.current_standings().get('teams')[3].get('gb'))

      graphics.DrawText(self.canvas, font["font"], record_start, 52, self.team_stat_color, record_text)
      graphics.DrawText(self.canvas, font["font"], gb_start, 52, self.team_stat_color, gb_text)

      team_text = self.__team_shortener(self.data.current_standings().get('teams')[4].get('name'))
      graphics.DrawText(self.canvas, font["font"], 2, 62, self.team_name_color, team_text)

      record_text = "{}-{}".format(self.data.current_standings().get('teams')[4].get('w'), self.data.current_standings().get('teams')[4].get('l'))

      if "-" in self.data.current_standings().get('teams')[4].get('gb'):
        gb_text = " -  "
      else:
        gb_text = format(self.data.current_standings().get('teams')[4].get('gb'))

      graphics.DrawText(self.canvas, font["font"], record_start, 62, self.team_stat_color, record_text)
      graphics.DrawText(self.canvas, font["font"], gb_start, 62, self.team_stat_color, gb_text)

      offset += coords["offset"]
      
      self.__fill_standings_footer()

      self.canvas = self.matrix.SwapOnVSync(self.canvas)
      time.sleep(10.0)

      self.__fill_bg()
      self.data.advance_to_next_standings()

      i +=1

  def __fill_standings_footer(self):
    coords = self.data.config.layout.coords("standings")
#    graphics.DrawLine(self.canvas, 0, coords["height"], coords["width"], coords["height"], self.bg_color)
#    graphics.DrawLine(self.canvas, coords["divider"]["x"], 0, coords["divider"]["x"], coords["height"], self.divider_color)
#    graphics.DrawLine(self.canvas, 0, coords["height"]+1, coords["width"], coords["height"]+1, self.bg_color)
#    graphics.DrawLine(self.canvas, coords["divider"]["x"], 0, coords["divider"]["x"], coords["height"]+1, self.divider_color)
    

  def __is_dumpster_fire(self):
    return "comedy" in self.data.config.preferred_divisions[self.data.current_division_index].lower()

  def __render_dumpster_fire(self):
    image_file = get_file("Assets/fire.jpg")
    image = Image.open(image_file)
    image_rgb = image.convert("RGB")
    image_x = (self.canvas.width / 2) - 16

    self.matrix.Clear()
    while True:
      self.matrix.SetImage(image_rgb, image_x, 0)
      time.sleep(20.0)

  def __team_shortener(self, team_name):
    if team_name == "Arizona Diamondbacks":
      return "Arizona"
    elif team_name == "Atlanta Braves":
      return "Atlanta"
    elif team_name == "Baltimore Orioles":
      return "Baltimore"
    elif team_name == "Boston Red Sox":
      return "Boston"
    elif team_name == "Chicago White Sox":
      return "Chicago"
    elif team_name == "Chicago Cubs":
      return "Chicago"
    elif team_name == "Cincinnati Reds":
      return "Cincinnati"
    elif team_name == "Cleveland Indians":
      return "Cleveland"
    elif team_name == "Colorado Rockies":
      return "Colorado"
    elif team_name == "Detroit Tigers":
      return "Detroit"
    elif team_name == "Houston Astros":
      return "Houston"
    elif team_name == "Kansas City Royals":
      return "Kansas City"
    elif team_name == "Los Angeles Angels":
      return "Los Angeles"
    elif team_name == "Los Angeles Dodgers":
      return "Los Angeles"
    elif team_name == "Miami Marlins":
      return "Miami"
    elif team_name == "Milwaukee Brewers":
      return "Milwaukee"
    elif team_name == "Minnesota Twins":
      return "Minnesota"
    elif team_name == "New York Yankees":
      return "New York"
    elif team_name == "New York Mets":
      return "New York"
    elif team_name == "Oakland Athletics":
      return "Oakland"
    elif team_name == "Philadelphia Phillies":
      return "Philadelphia"
    elif team_name == "Pittsburgh Pirates":
      return "Pittsburgh"
    elif team_name == "San Diego Padres":
      return "San Diego"
    elif team_name == "San Francisco Giants":
      return "S. Francisco"
    elif team_name == "Seattle Mariners":
      return "Seattle"
    elif team_name == "St. Louis Cardinals":
      return "St. Louis"
    elif team_name == "Tampa Bay Rays":
      return "Tampa Bay"
    elif team_name == "Texas Rangers":
      return "Texas"
    elif team_name == "Toronto Blue Jays":
      return "Toronto"
    elif team_name == "Washington Nationals":
      return "Washington"
    else:
      return "#ERROR!"
