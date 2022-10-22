
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ID IDM IDV IGNORED PF PP PYTHON REGEX VIRFSGram : Prods PYTHON IGNOREDProds : Prod ProdsProds : ProdProd : ID PP IDS PFProd : ID PP REGEXIDS : IDS VIR IDIDS : IDIDS : IDMIDS : IDV'
    
_lr_action_items = {'ID':([0,3,7,11,14,15,],[4,4,9,-5,-4,16,]),'$end':([1,8,],[0,-1,]),'PYTHON':([2,3,6,11,14,],[5,-3,-2,-5,-4,]),'PP':([4,],[7,]),'IGNORED':([5,],[8,]),'REGEX':([7,],[11,]),'IDM':([7,],[12,]),'IDV':([7,],[13,]),'PF':([9,10,12,13,16,],[-7,14,-8,-9,-6,]),'VIR':([9,10,12,13,16,],[-7,15,-8,-9,-6,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'FSGram':([0,],[1,]),'Prods':([0,3,],[2,6,]),'Prod':([0,3,],[3,3,]),'IDS':([7,],[10,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> FSGram","S'",1,None,None,None),
  ('FSGram -> Prods PYTHON IGNORED','FSGram',3,'p_FSGram','ANBcompiler_yacc.py',14),
  ('Prods -> Prod Prods','Prods',2,'p_Prods','ANBcompiler_yacc.py',32),
  ('Prods -> Prod','Prods',1,'p_Prodsingle','ANBcompiler_yacc.py',36),
  ('Prod -> ID PP IDS PF','Prod',4,'p_Prod','ANBcompiler_yacc.py',40),
  ('Prod -> ID PP REGEX','Prod',3,'p_ProdSimple','ANBcompiler_yacc.py',50),
  ('IDS -> IDS VIR ID','IDS',3,'p_IDS','ANBcompiler_yacc.py',66),
  ('IDS -> ID','IDS',1,'p_IDSingle','ANBcompiler_yacc.py',72),
  ('IDS -> IDM','IDS',1,'p_IDPLUS','ANBcompiler_yacc.py',76),
  ('IDS -> IDV','IDS',1,'p_IDTIMES','ANBcompiler_yacc.py',80),
]
