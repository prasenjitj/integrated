"""This script converts sports roster raw data to thali format.

usage : $ python sportsRoster.py <raw_data_input> <thali_formated_output>!

Different methods are called based on the names of the input file, hence

<raw_data_input> file should be in tsv format and the naming should adhere to

the following rules:
-------------------------------------------------------
Leagues         | input file      | output file       |
-------------------------------------------------------
Soccer Leagues  | soccer_raw.tsv  | soccer_thali.tsv  |
-------------------------------------------------------
MLB League      | mlb_raw.tsv     | mlb_thali.tsv     |
-------------------------------------------------------
NBA League      | nba_raw.tsv     | nba_thali.tsv     |
-------------------------------------------------------
NFL League      | nfl_raw.tsv     | nfl_thali.tsv     |
-------------------------------------------------------
NHL League      | nhl_raw.tsv     | nhl_thali.tsv     |
-------------------------------------------------------
"""
from os.path import basename
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
  input_file = basename(infile)
  output_file = basename(outfile)
  # final = Flags.soccer_final_file_path
  final = 'soccer_final.tsv'
  # final = sys.argv[3]
  
  def main(self):
    if self.input_file == 'mlb_raw.tsv':
      mlb_thali(self.infile, self.outfile)
    elif self.input_file == 'nba_raw.tsv':
      nba_thali(self.infile, self.outfile)
    elif self.input_file == 'nfl_raw.tsv':
      nfl_thali(self.infile, self.outfile)
    elif self.input_file == 'nhl_raw.tsv':
      nhl_thali(self.infile, self.outfile)
    elif self.input_file == 'soccer_raw.tsv':
      soccer_thali(self.infile, self.outfile)
      soccer_dedup(self.outfile, self.final)
    else:
      print 'failed!'


if __name__ == '__main__':
  Sport().main()
