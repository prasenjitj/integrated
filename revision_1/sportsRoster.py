"""This script converts sports roster raw data to thali format.

usage : $ python sportsRoster.py <raw_data_input> <thali_formated_output>!
"""
import sys
from mlb_thali import mlb_thali
from nba_thali import nba_thali
from nfl_thali import nfl_thali
from nhl_thali import nhl_thali
from soccer_thali import soccer_dedup
from soccer_thali import soccer_thali


class Sport(object):
  infile = sys.argv[1]
  outfile = sys.argv[2]
  third = 'soccer_final.tsv'

  def main(self):
    if self.infile == 'mlb_raw.tsv':
      mlb_thali(self.infile, self.outfile)
    elif self.infile == 'nba_raw.tsv':
      nba_thali(self.infile, self.outfile)
    elif self.infile == 'nfl_raw.tsv':
      nfl_thali(self.infile, self.outfile)
    elif self.infile == 'nhl_raw.tsv':
      nhl_thali(self.infile, self.outfile)
    elif self.infile == 'soccer_raw.tsv':
      soccer_thali(self.infile, self.outfile)
      soccer_dedup(self.outfile, self.third)
    else:
      print 'failed!'


if __name__ == '__main__':
  Sport().main()
