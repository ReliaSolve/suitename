from suitenamedefs import Residue, Suite

def suitename(
# input_modes: specify at most one of these.
# if none are specified, the first command line argument or 
# the standard input will be used, 
# interpreted according and comment to command line options
  model=None,  # a cctbx model object that has a geometry manager
  filename="", # a file containing residue dihedral angles in dangle format
  kinemageFile="", # a file containing suite dihedral angles in kinemage format
  
# output stream: if not provided, will write to standard output
  outFile=None, 

  options=""  # options: text in phil format
):


# The following are the component parts of suitename
# Here would be a typical workflow:
# <aquire a model somehow>
# suites = suitesFromModel(model)
# suites = suitename.compute(suites)
# suitename.finalStats()   -- if wanting a statistical summary
# <use the information in suites>

def read(inFile, options=""):
  """
  Read a file containing dihedral angle information,
  and return a list of suites.
  Options may guide the interpretationOptions may guide the interpretation
  of the file and its format.
  """

def suitesFromModel(model, options=""):
  """
  Given a model that has been processed so as to have a geometry manager,
  return the corresponding list of suites
  """

def compute(suites, options=""):
  """
  Given a list of suites, perform the suitename computation.
  The list of suites will be returned modified, each suite annotated
  with additional attributes giving the bin, cluster, suiteness
  (accuracy of fit) and more.
  """

def computeStats():
  """
  Compute statistics for each bin, based on suites already processed
  and statistics already attached to clusters. Note that these bin
  and cluster data structures are inherent to Suitename; thus
  Suitename is NOT re-entrant.
  """

def clearStats():
  """
  Clear the statistics stored in bin and cluster data structures by suitename
  """

def write(suites, outFile=None, options=""):
  """
  write out the results of suitename computation, in one of three
  formats based on options:
  report - the default,a list with a statistical summary
  string - a very compact presentation with3 characters per suite
  kinemage - a format useful for graphical visualization
  """
