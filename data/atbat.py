import statsapi

class AtBat:
  def __init__(self, linescore):
    self.batter =  str(linescore.get('offense').get('batter',{}).get('fullName',{}))
    self.pitcher = str(linescore.get('defense').get('pitcher',{}).get('fullName',{}))
    self.onDeck = str(linescore.get('offense').get('onDeck',{}).get('fullName',{}))
    self.inHole = str(linescore.get('offense').get('inHole',{}).get('fullName',{}))

  def get_batter(self):
    return format_statsapi_name(self, self.batter)

  def get_pitcher(self):
    return format_statsapi_name(self, self.pitcher)

  def get_onDeck(self):
    return format_statsapi_name(self, self.onDeck)

  def get_inHole(self):
    return format_statsapi_name(self, self.inHole)

def format_statsapi_name(self, name):
    SpcPos = name.find(" ") + 1
    playerLast = name[SpcPos:len(name)]

    if name:
      if name == "Jon Ryan Murphy":
        return "J.R. Murphy"
      elif name == "Chi Chi Gonzalez":
        return "C.C. Gonzalez"
      elif name == "Kwang Hyun Kim":
        return "K.-H. Kim"
      elif name == "Hyun Jin Ryu":
        return "H.-J. Ryu"
      elif len(playerLast) >= 9:
        return playerLast
      elif name[1] == ".":
        return name
      elif name == "{}":
        return " "
      else:
        return name[0] + ". " + playerLast
    else:
      return " "

