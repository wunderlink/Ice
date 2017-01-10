
import os
import re
import unicodedata
import urllib2

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
    opts = re.IGNORECASE
    match = reduce(lambda match, regex: match if match else re.match(regex, filename, opts), self.regexes, None)
    if match:
      logger.debug("Matched game '%s' as %s using regular expression `%s`", filename, str(match.groupdict()), match.re.pattern)
      name = match.groupdict()["name"]
      if console.shortname == 'mame'
        name = get_real_arcade_title(name)
    else:
      logger.debug("No match found for '%s'", filename)
      name = filename
    return name.strip()

  def get_real_arcade_title(title):
    print "Fetching real title for %s from mamedb.com" % title
    URL = "http://www.mamedb.com/game/%s" % title
    data = "".join(urllib2.urlopen(URL).readlines())
    m = re.search('<b>Name:.*</b>(.+) .*<br/><b>Year', data)
    if m:
      print "Found real title %s for %s on mamedb.com" % (m.group(1), title)
      return m.group(1)
    else:
      print "No title found for %s on mamedb.com" % title
      return title


