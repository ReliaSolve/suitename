import sys, os, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, "C:\\Users\\Ken\\Desktop\\Richardson\\cctbx_project") 
sys.path.insert(0, "C:\\Users\\Ken\\Desktop\\Richardson\\cctbx-build\\build\\lib") 

import pprint
pp = pprint.PrettyPrinter()
#pp.pprint(sys.path)

from iotbx.data_manager import DataManager    #   Load in the DataManager

dm = DataManager()                            #   Initialize the DataManager and call it dm
dm.set_overwrite(True)         #   tell the DataManager to overwrite files with the same name
#model_filename="model.pdb"                         #   Name of model file
model_filename="test/2v7r.pdb"                         #   Name of model file
model = dm.get_model(model_filename)
model.process_input_model(make_restraints=True)

from mmtbx.validation import utils
from cctbx import geometry_restraints
from _collections import defaultdict

def main():
  rna_bb = get_rna_backbone_dihedrals(model)
  print(rna_bb)


def get_rna_backbone_dihedrals(model):
  bb_dihedrals = defaultdict(dict)
  formatted_out = []
  alt_tracker = {}

  pdb_hierarchy = model.get_hierarchy()
  #print(help(pdb_hierarchy))
  geometry = model.get_restraints_manager()  # came up None
  # print(help(geometry))
  sites_cart = model.get_sites_cart() 
  #sites_cart = pdb_hierarchy.atoms().extract_xyz()
  dihedral_proxies = geometry.geometry.dihedral_proxies  #?!!!

  # here begins direct copy of utils code:
  i_seq_name_hash = utils.build_name_hash(pdb_hierarchy=pdb_hierarchy)

  def is_blank_or_alt_a(proxy):
    for i in proxy.i_seqs:
       alt = i_seq_name_hash[i][4:5]
       if alt not in [' ', 'A']:
         return False
    return True

  for dp in dihedral_proxies:
    atoms = []
    debug_key = ""
    invert_sign = False
    dp.sort_i_seqs()
    for i in dp.i_seqs:
      atoms.append(i_seq_name_hash[i][0:4].strip())
      debug_key = debug_key+i_seq_name_hash[i]
    if len(atoms) != 4:
      continue
    name = utils.match_dihedral_to_name(atoms=atoms)
    #handle dihedral equivalences
    if name == None:
      inverted_atoms = utils.get_inverted_atoms(atoms=atoms, improper=False)
      name = utils.match_dihedral_to_name(atoms=inverted_atoms)
      if name == None:
        inverted_atoms = utils.get_inverted_atoms(atoms=atoms, improper=True)
        name = utils.match_dihedral_to_name(atoms=inverted_atoms)
        if name is not None:
          invert_sign = True
    if (name is not None) and (is_blank_or_alt_a(dp)):
      restraint = geometry_restraints.dihedral(
                                               sites_cart=sites_cart,
                                               proxy=dp)
      key = i_seq_name_hash[dp.i_seqs[1]][4:]
      if alt_tracker.get(key[1:]) is None:
        alt_tracker[key[1:]] = []
      if key[0:1] not in alt_tracker[key[1:]]:
        alt_tracker[key[1:]].append(key[0:1])
      bb_dihedrals[key][name] = restraint.angle_model
      if invert_sign:
        bb_dihedrals[key][name] = bb_dihedrals[key][name] * -1.0
  for key in list(bb_dihedrals.keys()):
    altloc = key[0:1]
    resname = key[1:4]
    chainID = key[4:6]
    resnum = key[6:10]
    i_code = key[10:]
    if 'A' in alt_tracker[key[1:]]:
      if altloc != 'A':
        continue
    if bb_dihedrals[key].get('alpha') is not None:
      alpha = "%.3f" % bb_dihedrals[key]['alpha']
    # FIXME will the lookup below ever actually work?
    elif altloc == 'A' and \
         bb_dihedrals[' '+key[1:]].get('alpha') is not None:
      alpha = "%.3f" % bb_dihedrals[' '+key[1:]]['alpha']
    else:
      alpha = '__?__'
    if bb_dihedrals[key].get('beta') is not None:
      beta = "%.3f" % bb_dihedrals[key]['beta']
    elif altloc == 'A' and \
         bb_dihedrals[' '+key[1:]].get('beta') is not None:
      beta = "%.3f" % bb_dihedrals[' '+key[1:]]['beta']
    else:
      beta = '__?__'
    if bb_dihedrals[key].get('gamma') is not None:
      gamma = "%.3f" % bb_dihedrals[key]['gamma']
    elif altloc == 'A' and \
         bb_dihedrals[' '+key[1:]].get('gamma') is not None:
      gamma = "%.3f" % bb_dihedrals[' '+key[1:]]['gamma']
    else:
      gamma = '__?__'
    if bb_dihedrals[key].get('delta'):
      delta = "%.3f" % bb_dihedrals[key]['delta']
    elif altloc == 'A' and \
         bb_dihedrals[' '+key[1:]].get('delta') is not None:
      delta = "%.3f" % bb_dihedrals[' '+key[1:]]['delta']
    else:
      delta = '__?__'
    if bb_dihedrals[key].get('epsilon'):
      epsilon = "%.3f" % bb_dihedrals[key]['epsilon']
    elif altloc == 'A' and \
         bb_dihedrals[' '+key[1:]].get('epsilon') is not None:
      epsilon = "%.3f" % bb_dihedrals[' '+key[1:]]['epsilon']
    else:
      epsilon = '__?__'
    if bb_dihedrals[key].get('zeta'):
      zeta = "%.3f" % bb_dihedrals[key]['zeta']
    elif altloc == 'A' and \
         bb_dihedrals[' '+key[1:]].get('zeta') is not None:
      zeta = "%.3f" % bb_dihedrals[' '+key[1:]]['zeta']
    else:
      zeta = '__?__'
    eval = "%s:%s:%s:%s:%s:%s:%s:%s:%s:%s:%s:%s:%s" \
           % (" ",
              "1",
              chainID,
              resnum,
              i_code,
              altloc,
              resname,
              alpha,
              beta,
              gamma,
              delta,
              epsilon,
              zeta)
    formatted_out.append(eval)
  formatted_out.sort()
  backbone_dihedrals = ""
  for line in formatted_out:
    backbone_dihedrals += line+'\n'
  return backbone_dihedrals


main()
