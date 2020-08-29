# -*- encoding: utf-8 -*-
from rgbmatrix import graphics
from PIL import Image
from utils import get_font, get_file, center_text_position
from renderers.scrollingtext import ScrollingText
from renderers.network import NetworkErrorRenderer
from data.data import Data
from rgbmatrix import graphics
import data.layout
import time
import random

class OffdayRenderer:
  def __init__(self, canvas, data, scrolling_text_pos):
    self.canvas = canvas
    self.data = data
    self.layout = data.config.layout
    self.colors = data.config.scoreboard_colors
    self.bgcolor = self.colors.graphics_color("default.background")
    self.scrolling_text_pos = scrolling_text_pos

    self.weather_icon = None
    if self.data.weather.available():
      image_file = get_file(self.data.weather.icon_filename())
      self.weather_icon = Image.open(image_file)

  def render(self):
    text_len = self.__render_news_ticker()
    self.__render_clock()
    self.__render_weather()
    self.__render_weather_text("temperature")
    NetworkErrorRenderer(self.canvas, self.data).render()
    return text_len

  def __render_weather(self):
    if self.data.weather.available():
      self.__render_weather_icon()

  def __render_clock(self):
    a = "a"

  def __render_weather_text(self, keyname):
    coords = self.layout.coords("offday.{}".format(keyname))
    font = self.layout.font("offday.{}".format(keyname))
    font2 = self.layout.font("offday.time")
    color = self.colors.graphics_color("offday.{}".format(keyname))

    w = 128
    h = 64

#    graphics.DrawText(self.canvas, font2["font"], 78, 30, color, "WILD")
#    graphics.DrawText(self.canvas, font2["font"], 74, 48, color, "THING")

#    graphics.DrawText(self.canvas, font2["font"], 3, 35, color, "Public Address")
#    graphics.DrawText(self.canvas, font2["font"], 13, 50, color, "Announcers")

#    image_file = get_file("Assets/IndiansLogo.jpg")
#    image = Image.open(image_file)
#    image_rgb = image.convert("RGB")

#    self.canvas.SetImage(image_rgb, 8, 2)

#    image_file2 = get_file("Assets/WildThing.bmp")
#    image2 = Image.open(image_file2)
#    image_rgb2 = image2.convert("RGB")

#    self.canvas.SetImage(image_rgb2, 62, 16)

# Blinking lights
#    for y in range (0, h):
#      for x in range (0, w):
#        if random.randint(0,42) > 41:
#          self.canvas.SetPixel(x, y, 255, 191, 0)

#    graphics.DrawText(self.canvas, font["font"], 6, 16, color, "Dedicated to")
#    graphics.DrawText(self.canvas, font["font"], 13, 25, color, "the great")
#    graphics.DrawText(self.canvas, font["font"], 9, 34, color, "fans of the")
    graphics.DrawText(self.canvas, font2["font"], 36, 20, color, "15")
    graphics.DrawText(self.canvas, font2["font"], 28, 32, color, "JEFF")
    graphics.DrawText(self.canvas, font2["font"], 14, 44, color, "BRUBAKER")
    graphics.DrawText(self.canvas, font["font"], 15, 53, color, "First Base")

#    for x in range(0,84):
#     for y in range(0,1):
#      self.canvas.SetPixel(x,y,255,191,0)
#    for x in range (0,1):
#     for y in range (0,64):
#      self.canvas.SetPixel(x,y,255,191,0)
#    for x in range(0,84):
#     for y in range(63,64):
#      self.canvas.SetPixel(x,y,255,191,0)
#    for x in range (83,84):
#     for y in range (0,64):
#      self.canvas.SetPixel(x,y,255,191,0)
# Single line bold: 14 height

  def __render_weather_icon(self):
    a = "a"

# Dan & Pam picture

#    image_file = get_file("Assets/DanPamFull.bmp")
#    image = Image.open(image_file)
#    image_rgb = image.convert("RGB")

#    self.canvas.SetImage(image_rgb, 1, 1)

#    image_file = get_file("Assets/CBS58.bmp")
#    image = Image.open(image_file)
#    image_rgb = image.convert("RGB")

#    self.canvas.SetImage(image_rgb, 5, 4)

# The Pfeifers Welcome

#    image_file = get_file("Assets/Welcome.bmp")
#    image = Image.open(image_file)
#    image_rgb = image.convert("RGB")

#    self.canvas.SetImage(image_rgb, 1, 1)

# Headshot
    image_file = get_file("Assets/Brubaker.bmp")
    image = Image.open(image_file)
    image_rgb = image.convert("RGB")

    self.canvas.SetImage(image_rgb, 84,0)

# Welcome

  def __render_news_ticker(self):
    coords = self.layout.coords("offday.scrolling_text")
    font = self.layout.font("offday.scrolling_text")
    color = self.colors.graphics_color("offday.scrolling_text")
    ticker_text = self.data.headlines.ticker_string()
    return ScrollingText(self.canvas, 129, 65, 0, font, color, self.bgcolor, ticker_text).render(self.scrolling_text_pos)

  def __str_(self):
    s = "<{} {}> Date: {}".format(self.__class__.__name__, hex(id(self)), self.data.date())
    return s
