
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'FORMATS ID IDm IDo IDv IGNORED PF PP PYTHON REGEX UNIVERSE VIRFSGram : Prods UNIVERSE FORMATS IGNOREDProds : Prod ProdsProds : ProdProd : ID PP IDS PFProd : ID PP REGEXIDS : IDS VIR IDgenIDS : IDgenIDgen : IDIDgen : IDmIDgen : IDvIDS : IDo'
    
_lr_action_items = {'ID':([0,3,7,11,17,18,],[4,4,9,-5,-4,9,]),'$end':([1,16,],[0,-1,]),'UNIVERSE':([2,3,6,11,17,],[5,-3,-2,-5,-4,]),'PP':([4,],[7,]),'FORMATS':([5,],[8,]),'REGEX':([7,],[11,]),'IDo':([7,],[13,]),'IDm':([7,18,],[14,14,]),'IDv':([7,18,],[15,15,]),'IGNORED':([8,],[16,]),'PF':([9,10,12,13,14,15,19,],[-8,17,-7,-11,-9,-10,-6,]),'VIR':([9,10,12,13,14,15,19,],[-8,18,-7,-11,-9,-10,-6,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'FSGram':([0,],[1,]),'Prods':([0,3,],[2,6,]),'Prod':([0,3,],[3,3,]),'IDS':([7,],[10,]),'IDgen':([7,18,],[12,19,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> FSGram","S'",1,None,None,None),
  ('FSGram -> Prods UNIVERSE FORMATS IGNORED','FSGram',4,'p_FSGram','FSGram.py',26),
  ('Prods -> Prod Prods','Prods',2,'p_Prods','FSGram.py',51),
  ('Prods -> Prod','Prods',1,'p_Prodsingle','FSGram.py',55),
  ('Prod -> ID PP IDS PF','Prod',4,'p_Prod','FSGram.py',59),
  ('Prod -> ID PP REGEX','Prod',3,'p_ProdSimple','FSGram.py',70),
  ('IDS -> IDS VIR IDgen','IDS',3,'p_IDS','FSGram.py',81),
  ('IDS -> IDgen','IDS',1,'p_IDgen','FSGram.py',85),
  ('IDgen -> ID','IDgen',1,'p_IDSingle','FSGram.py',89),
  ('IDgen -> IDm','IDgen',1,'p_IDPLUS','FSGram.py',93),
  ('IDgen -> IDv','IDgen',1,'p_IDTIMES','FSGram.py',97),
  ('IDS -> IDo','IDS',1,'p_IDOPTN','FSGram.py',101),
]