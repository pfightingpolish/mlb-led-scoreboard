from bases import Bases
from inning import Inning
from pitches import Pitches
from atbat import AtBat
from outs import Outs
from team import Team
import datetime
import debug

class Scoreboard:
  """Contains data for a current game.
  The data contains runs scored for both teams, and details about the current at-bat,
  including runners on base, balls, strikes, and outs.
  """

  def __init__(self, overview, linescore):
    self.away_team = Team(overview.away_name_abbrev, overview.away_team_runs, overview.away_team_hits, overview.away_team_errors, overview.away_team_name)
    self.home_team = Team(overview.home_name_abbrev, overview.home_team_runs, overview.home_team_hits, overview.home_team_errors, overview.home_team_name)
    self.inning = Inning(overview)
    self.bases = Bases(overview)
    self.pitches = Pitches(overview)
    self.outs = Outs(overview)
    self.game_status = overview.status
    self.atbat = AtBat(linescore)
    self.batter = self.atbat.get_batter()
    self.pitcher = self.atbat.get_pitcher()

    try:
      self.note = overview.note
    except:
      self.note = None

    try:
      self.reason = overview.reason
    except:
      self.reason = None

  def get_text_for_reason(self):
    if self.note:
      return self.note

    if self.reason:
      return self.reason

    return None

  def __str__(self):
    s = "<{} {}> {} ({} {} {}) @ {} ({} {} {}); Status: {}; Inning: (Number: {}; State: {}); AB: {}, P: {}, B:{} S:{} O:{}; Bases: {};".format(
      self.__class__.__name__, hex(id(self)),
      self.away_team.abbrev,
      str(self.away_team.runs),
      str(self.away_team.hits),
      str(self.away_team.errors),
      self.home_team.abbrev,
      str(self.home_team.runs),
      str(self.home_team.hits),
      str(self.home_team.errors),
      self.game_status,
      str(self.inning.number),
      str(self.inning.state),
      self.batter,
      self.pitcher,
      str(self.pitches.balls),
      str(self.pitches.strikes),
      str(self.outs.number),
      str(self.bases))
#      str(self.atbat.batter),
#      str(self.atbat.pitcher))
    if self.reason:
      s += " Reason: '{}';".format(self.reason)
    if self.note:
      s += " Notes: '{}';".format(self.note)
    return s
