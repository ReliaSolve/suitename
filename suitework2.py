from iotbx.data_manager import DataManager    #   Load in the DataManager

dm = DataManager()                            #   Initialize the DataManager and call it dm
dm.set_overwrite(True)         #   tell the DataManager to overwrite files with the same name
model_filename="test/2v7r.pdb"                         #   Name of model file
model = dm.get_model(model_filename)    

pdb_hierarchy = model.get_hierarchy()
grm = model.get_restraints_manager()  # came up None
print(grm)
