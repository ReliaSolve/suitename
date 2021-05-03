import iotbx.phil

def get_master_phil():
  return iotbx.phil.parse(
    input_string="""
  suitename {
    string=False  
      .type=bool
      .help="output in string format, 3 characters per suite
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
  """,process_includes=True)


def main():
  master_phil = get_master_phil()
  master_phil.show();
  master_phil.format(master_phil.extract())
  
  import sys
  # does not work!:
  merge_phil = iotbx.phil.process_command_line(sys.argv, master_phil)
  
  input_objects = iotbx.phil.process_command_line_with_files(
    args=';'.join(sys.argv),
    master_phil=master_phil)


main()

