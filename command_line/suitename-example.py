# LIBTBX_SET_DISPATCHER_NAME phenix.suitename
# LIBTBX_SET_DISPATCHER_NAME molprobity.suitename

from iotbx.cli_parser import CCTBXParser
from libtbx.program_template import ProgramTemplate
from libtbx.utils import multi_out, show_total_time
import argparse, sys, os

# argv for example: "2xLk.pdb", "-chart", "-causes", "noinc=true"

def run(args):
  # create parser
  logger = multi_out()
  logger.register('stderr', sys.stderr)
  logger2 = multi_out()
  logger2.register('stdout', sys.stdout)

  working_phil = parseArgs1(Program, logger)
  working_phil.show()


# def rest_of_old_run(args):
#   # start program
#   print('Starting job', file=logger)
#   print('='*79, file=logger)
#   phil1 = parser.working_phil.extract()
#   args2 = parseCommandLine()
#   task = Program(
#     parser.data_manager, phil1, logger=logger2)  
#   main()


def parseArgs1(Program, logger):
  # create the cctbx aspect of the parser
  parser = CCTBXParser(
    program_class = Program,
    # custom_process_arguments = custom_args_proc,
    logger=logger)
    
  # add the old suitename aspect of the parser
  parser = buildParser(parser)
  # do it
  namespace = parser.parse_args(sys.argv[1:])
  print(parser.working_phil)
  return parser.working_phil




class Program(ProgramTemplate):
  prog = os.getenv('LIBTBX_DISPATCHER_NAME')
  program_name = "suitename"
  description="""
   < insert help text here>
""" % locals()

  master_phil_str = """
    suitename {
    string=False  
      .type=bool
      .help="output in string format, 3 characters per suite"
    kinemage=False
      .type=bool
      .help="output in kinemage format, useful for visualization"
    chart=False
      .type=bool
      .help="modifier to standard report, output without statistical summary"
    nosequence = False
      .type=bool
      .help="modifier to string format, do not include base letters"
    causes=False
      .type=bool
      .help="output extra details concerning the causes of each assignment made"
    satellites=False
      .type=bool
      .help="use the special satelliteWidths values for satellites" 
    nowannabe=False
      .type=bool
      .help="do not consider 'wannabe' clusters"
    noinc=False
      .type=bool
      .help="do not display incomplete suites"
    etatheta=False
      .type=bool
    test=False
      .type=bool
      .help="display a lat of additional information about program internals"
    anglefields = 9
      .type=int
      .help="number of angle fields provided, for textual input only"
    pointidfields = 7
      .type=int
      .help="number of point id fields before the angle fields"
    altid="A"
      .type=str
      .help="which alternate conformer to use"
    altidfield = 3
  .type=int
      .help="which field gives the alternate conformer code"
  }
"""
  datatypes = ['model', 'phil']  # also 

  def validate(self):
    pass

  def run(self):
    pass
  # end of class Program


def buildParser(parser):
    "Old fashioned way: set up the expected arguments, ready for parsing"
    
    # the input file may be given as an argument or as a redirect
    parser.add_argument("infile", nargs="?", default="")

    # input styles
    parser.add_argument("--residuein", "-residuein", action="store_true")
    parser.add_argument("--residuesin", "-residuesin", action="store_true")
    parser.add_argument("--suitein", "-suitein", action="store_true")
    parser.add_argument("--suitesin", "-suitesin", action="store_true")

    # output styles (default is --report)
    outputStyle = parser.add_mutually_exclusive_group()
    outputStyle.add_argument("--report", "-report", action="store_true")
    outputStyle.add_argument("--string", "-string", action="store_true")
    outputStyle.add_argument("--kinemage", "-kinemage", action="store_true")
    parser.add_argument(
        "--chart", "-chart", action="store_true"
    )  # a modifier to --report    
    parser.add_argument(
        "--causes", "-causes", action="store_true"
    )  # a modifier to --report, reveals algorithm details

    # additional options
    parser.add_argument("--satellites", "-satellites", action="store_true")
    parser.add_argument("--nowannabe", "-nowannabe", action="store_true")
    parser.add_argument("--nosequence", "-nosequence", action="store_true")
    parser.add_argument("--noinc", "-noinc", action="store_true")
    parser.add_argument("--thetaeta", "-thetaeta", action="store_true")
    parser.add_argument("--etatheta", "-etatheta", action="store_true")
    parser.add_argument("--test", "-test", action="store_true")
    parser.add_argument("--version", "-version", action="store_true")
    #            "--help" is automatically available, it summarizes this list.

    # numerical options
    parser.add_argument("--anglefields", "-anglefields", type=int, default=9)
    parser.add_argument("--pointidfields", "-pointidfields", type=int, default=7)
    parser.add_argument("--ptid", "-ptid", type=int, default=0)
    parser.add_argument("--altid", "-altid", type=str, default="A")
    parser.add_argument("--altidval", "-altidval", type=str, default="A")
    parser.add_argument("--altidfield", "-altidfield", type=int, default=4)

    # the following are deprecated:
    parser.add_argument("--angles", type=int, default=9)
    parser.add_argument("--resAngles", type=int, default=6)
    return parser


if (__name__ == "__main__"):
  run(sys.argv[1:])
