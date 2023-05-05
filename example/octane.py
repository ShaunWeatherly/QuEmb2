from pyscf import gto,scf,mp, cc, fci
from pbe.pbe import pbe
from pbe.fragment import fragpart
from pbe.helper import *
from pbe import sgeom, printatom
import sys, h5py, os


be_type = 'be2' #sys.argv[1]


# PYSCF for integrals and HF solution
mol = gto.M(atom='''
C   0.4419364699  -0.6201930287   0.0000000000
C  -0.4419364699   0.6201930287   0.0000000000
H  -1.0972005331   0.5963340874   0.8754771384
H   1.0972005331  -0.5963340874  -0.8754771384
H  -1.0972005331   0.5963340874  -0.8754771384
H   1.0972005331  -0.5963340874   0.8754771384
C   0.3500410560   1.9208613544   0.0000000000
C  -0.3500410560  -1.9208613544   0.0000000000
H   1.0055486349   1.9450494955   0.8754071298
H  -1.0055486349  -1.9450494955  -0.8754071298
H   1.0055486349   1.9450494955  -0.8754071298
H  -1.0055486349  -1.9450494955   0.8754071298
C  -0.5324834907   3.1620985364   0.0000000000
C   0.5324834907  -3.1620985364   0.0000000000
H  -1.1864143468   3.1360988730  -0.8746087226
H   1.1864143468  -3.1360988730   0.8746087226
H  -1.1864143468   3.1360988730   0.8746087226
H   1.1864143468  -3.1360988730  -0.8746087226
C   0.2759781663   4.4529279755   0.0000000000
C  -0.2759781663  -4.4529279755   0.0000000000
H   0.9171145792   4.5073104916   0.8797333088
H  -0.9171145792  -4.5073104916  -0.8797333088
H   0.9171145792   4.5073104916  -0.8797333088
H  -0.9171145792  -4.5073104916   0.8797333088
H   0.3671153250  -5.3316378285   0.0000000000
H  -0.3671153250   5.3316378285   0.0000000000
''',basis='631g', charge=0)

mf = scf.RHF(mol)
mf.conv_tol = 1e-12
mf.kernel()

dm_hf = mf.make_rdm1()

print(dm_hf.shape)
fobj = fragpart(1, be_type=be_type, frag_type='autogen', valence_basis='sto-3g',mol=mol,
                molecule=True,  valence_only =True,
                frozen_core=False)

mybe = pbe(mf, fobj, super_cell=True, lo_method='iao')

mybe.optimize(solver='CCSD',method='QN', nproc=1, ompnum=1)

rdm1, rdm2 = mybe.rdm1_fullbasis(return_ao=False)

