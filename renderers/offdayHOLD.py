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
    NetworkErrorRenderer(self.canvas, self.data).render()
    return text_len

  def __render_clock(self):
    time_format_str = "{}:%M:%S".format(self.data.config.time_format)
    if self.data.config.time_format == "%-I":
      time_format_str += " %p"
    time_text = time.strftime(time_format_str)
    coords = self.layout.coords("offday.time")
    font = self.layout.font("offday.time")
    color = self.colors.graphics_color("offday.time")
    graphics.DrawText(self.canvas, font["font"], coords["x"], coords["y"], color, time_text)

  def __render_weather(self):
    if self.data.weather.available():
      self.__render_weather_icon()
      self.__render_weather_text(self.data.weather.conditions, "conditions")
      self.__render_weather_text(self.data.weather.temperature_string(), "temperature")
#      self.__render_weather_text(self.data.weather.wind_speed_string(), "wind_speed")
#      self.__render_weather_text(self.data.weather.wind_dir_string(), "wind_dir")
      self.__render_weather_text(self.data.weather.wind_string(), "wind")

  def __render_weather_text(self, text, keyname):
    coords = self.layout.coords("offday.{}".format(keyname))
    font = self.layout.font("offday.{}".format(keyname))
    font2 = self.layout.font("offday.time")
    color = self.colors.graphics_color("offday.{}".format(keyname))
    text_x = center_text_position(text, coords["x"], font["size"]["width"])
    graphics.DrawText(self.canvas, font["font"], coords["x"], coords["y"], color, text)
    graphics.DrawText(self.canvas, font["font"], 20, 52, color, "MLB News")
    for x in range(0,88):
     for y in range(14,15):
      self.canvas.SetPixel(x,y,255,181,0)
    for x in range (88,89):
     for y in range (0,64):
      self.canvas.SetPixel(x,y,255,181,0)
    for x in range(0,88):
     for y in range(41,42):
      self.canvas.SetPixel(x,y,255,181,0)

  def __render_weather_icon(self):
    coords = self.layout.coords("offday.weather_icon")
    color = self.colors.color("offday.weather_icon")
    for x in range(self.weather_icon.size[0]):
      for y in range(self.weather_icon.size[1]):
        pixel = self.weather_icon.getpixel((x,y))
        if pixel[3] > 0:
          self.canvas.SetPixel(coords["x"] + x, coords["y"] + y, color["r"], color["g"], color["b"])

    image_file = get_file("Assets/BrewersSide.jpg")
    image = Image.open(image_file)
    image_rgb = image.convert("RGB")

    self.canvas.SetImage(image_rgb, 90, 12)

#    image_file3 = get_file("Assets/BrewersTextSide.jpg")
#    image3 = Image.open(image_file3)
#    image_rgb3 = image3.convert("RGB")

#    self.canvas.SetImage(image_rgb3, 90, 50)

    image_file2 = get_file("Assets/MLBIcon.jpg")
    image2 = Image.open(image_file2)
    image_rgb2 = image2.convert("RGB")

    self.canvas.SetImage(image_rgb2, 1, 44)

  def __render_news_ticker(self):
    coords = self.layout.coords("offday.scrolling_text")
    font = self.layout.font("offday.scrolling_text")
    color = self.colors.graphics_color("offday.scrolling_text")
    ticker_text = self.data.headlines.ticker_string()
    return ScrollingText(self.canvas, coords["x"], coords["y"], coords["width"], font, color, self.bgcolor, ticker_text).render(self.scrolling_text_pos)

  def __str_(self):
    s = "<{} {}> Date: {}".format(self.__class__.__name__, hex(id(self)), self.data.date())
    return s
