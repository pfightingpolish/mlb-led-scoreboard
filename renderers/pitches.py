from rgbmatrix import graphics
from utils import get_font

class PitchesRenderer:
  """Renders balls and strikes on the scoreboard."""

  def __init__(self, canvas, pitches, data):
    self.canvas = canvas
    self.pitches = pitches
    self.layout = data.config.layout
    self.colors = data.config.scoreboard_colors

  def render(self):
    font = self.layout.font("batter_count")
    font2 = self.layout.font("batter_count_labels")
#    coords = self.layout.coords("batter_count")
    pitches_color = self.colors.graphics_color("batter_count")
    batter_count_bl = "B"
    batter_count_sl = "S"
    batter_count_ol = "O"
    batter_count_b = "{}".format(self.pitches.balls)
    batter_count_s = "{}".format(self.pitches.strikes)
    batter_count_o = "{}".format(self.pitches.outs)
    if batter_count_b == "1":
     balls_x = 11
    else:
     balls_x = 10
    if batter_count_s == "1":
     strikes_x = 30
    else:
     strikes_x = 29
    if batter_count_o == "1":
     outs_x = 49
    else:
     outs_x = 48
    graphics.DrawText(self.canvas, font2["font"], 2, 43, pitches_color, batter_count_bl)
    graphics.DrawText(self.canvas, font["font"], balls_x, 43, pitches_color, batter_count_b)
    graphics.DrawText(self.canvas, font2["font"], 21, 43, pitches_color, batter_count_sl)
    graphics.DrawText(self.canvas, font["font"], strikes_x, 43, pitches_color, batter_count_s)
    graphics.DrawText(self.canvas, font2["font"], 40, 43, pitches_color, batter_count_ol)
    graphics.DrawText(self.canvas, font["font"], outs_x, 43, pitches_color, batter_count_o)

#    batter_count_text = "{}-{}".format(self.pitches.balls, self.pitches.strikes)
#    graphics.DrawText(self.canvas, font["font"], coords["x"], coords["y"], pitches_color, batter_count_text)
