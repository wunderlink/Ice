
import os
import re
import unicodedata
import urllib2

import xml.etree.ElementTree as elt
gamedata = elt.parse('MAME.xml').getroot().findall('game')


from ice.logs import logger

class ROMParser(object):

  regexes = [
    # Regex that matches the entire string up until it hits the first '[',
    # ']', '(', ')', or '.'
    # DOESN'T WORK FOR GAMES WITH ()s IN THEIR NAME
    # ur"(?P<name>[^\(\)\[\]]*)(.*)\.(.+)",
    ur"(?P<name>[^\(\)\[\]]*).*",
  ]

  def __init__(self):
    logger.debug("Creating ROM parser with regexes: %s" % self.regexes)

  def parse(self, path, console):
    """Parses the name of the ROM given its path."""
    basename = os.path.basename(path)
    (filename, ext) = os.path.splitext(basename)
    if console.emulator.name == "mame":
      filename = self.get_real_arcade_title(filename)
    opts = re.IGNORECASE
    match = reduce(lambda match, regex: match if match else re.match(regex, filename, opts), self.regexes, None)
    if match:
      logger.debug("Matched game '%s' as %s using regular expression `%s`", filename, str(match.groupdict()), match.re.pattern)
      name = match.groupdict()["name"]
    else:
      logger.debug("No match found for '%s'", filename)
      name = filename
    return name.strip()

  def get_real_arcade_title(self, title):
    name = self.get_arcade_data(title)
    if name:
      print "Found real title %s for %s in local db" % (name, title)
      return name
    else:
      print "No title found for %s on mamedb.com" % title
      return title

  def get_arcade_data(self, title):
    for child in gamedata:
      if child.attrib['name'] == title:
        return child.find('description').text

    print "No title found for %s in local db" % title
    return title