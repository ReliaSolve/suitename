import suiteninit, argparse
from suiteninit import buildParser

from iotbx.cli_parser import CCTBXParser
import sys


# suitename first
def parseArgs(programClass, logger):
  for i, arg in enumerate(sys.argv):  # make case insensitive
      sys.argv[i] = arg.lower()
  parser = argparse.ArgumentParser()
  buildParser(parser)  # set up the arguments for suite name
  args, others = parser.parse_known_args()
  print(args)
  # print(others)

  # create the cctbx aspect of the parser
  parser2 = CCTBXParser(
    program_class = programClass,
    # custom_process_arguments = custom_args_proc,
    logger=logger)
  # do it
  namespace = parser2.parse_args(others)
  extracted = parser2.working_phil.extract()
  for name, value in extracted.suitename.__dict__.items():
    print(name, ":", value)
  # for x in parser2.working_phil:
  #   print(x)
  print("kinemage=",extracted.suitename.kinemage)
  print("noinc=", extracted.suitename.noinc)
  
  return parser2.working_phil

# CCTBX first
def parseArgs1(Program, logger):
  # create the cc tbx aspect of the parser
  parser = CCTBXParser(
    program_class = Program,
    # custom_process_arguments = custom_args_proc,
    logger=logger)
    
  # add the old suitename aspect of the parser
  buildParser(parser)
  # do it
  namespace = parser.parse_args(sys.argv[1:])
  return parser.working_phil
  


