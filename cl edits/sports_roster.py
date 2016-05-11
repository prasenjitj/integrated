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

from google3.pyglib import app
from google3.pyglib import flags
from google3.pyglib import logging

from google3.experimental.users.prasenjitj.sports_roster.mlb_thali import mlb_thali
from google3.experimental.users.prasenjitj.sports_roster.nba_thali import nba_thali
from google3.experimental.users.prasenjitj.sports_roster.nfl_thali import nfl_thali
from google3.experimental.users.prasenjitj.sports_roster.nhl_thali import nhl_thali
from google3.experimental.users.prasenjitj.sports_roster.soccer_thali import soccer_dedup
from google3.experimental.users.prasenjitj.sports_roster.soccer_thali import soccer_thali

FLAGS = flags.FLAGS

flags.DEFINE_string('input_file_path', None, 'File path to input file TSV.')
flags.DEFINE_string('output_file_path', None, 'File path to output file TSV.')
flags.DEFINE_string('soccer_final_file_path', None,
                    'File path to soccer_final TSV.')


class Sport(object):
  """calls appropriate methods based on input file name for thali conversion."""

  def __init__(self, input_file, output_file, final_file):
    self.infile = input_file
    self.outfile = output_file
    self.input_file = basename(self.infile)
    self.output_file = basename(self.outfile)
    self.final = final_file

  def converts(self):
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


def main(unused_argv):
  if FLAGS.input_file_path is None:
    logging.fatal('No input_file_path specified argument --input_file_path.')

  if FLAGS.output_file_path is None:
    logging.fatal('No output_file_path specified'
                  'argument --output_file_path.')
  final_file = FLAGS.soccer_final_file_path

  Sport(FLAGS.input_file_path, FLAGS.output_file_path, final_file).converts()


if __name__ == '__main__':
  app.run()
