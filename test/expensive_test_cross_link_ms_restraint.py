import IMP
import IMP.test
import IMP.core
import IMP.container
import IMP.pmi
import IMP.pmi.representation
import IMP.pmi.restraints
import IMP.pmi.restraints.crosslinking
from math import *

def sphere_cap(r1, r2, d):
    sc = 0.0
    if d <= max(r1, r2) - min(r1, r2):
        sc = min(4.0 / 3 * pi * r1 * r1 * r1,
                      4.0 / 3 * pi * r2 * r2 * r2)
    elif d >= r1 + r2 :
        sc = 0
    else:
        sc = (pi / 12 / d * (r1 + r2 - d) * (r1 + r2 - d)) * \
             (d * d + 2 * d * r1 - 3 * r1 * r1 + 2 * d * r2 + 6 * r1 * r2 -
              3 * r2 * r2)
    return sc

def get_probability(xyz1s,xyz2s,sigma1s,sigma2s,psis,length,slope):
    onemprob = 1.0

    for n in range(len(xyz1s)): 
      xyz1=xyz1s[n]
      xyz2=xyz2s[n] 
      sigma1=sigma1s[n]
      sigma2=sigma2s[n]
      psi = psis[n]
      psi = psi.get_scale()
      dist=IMP.core.get_distance(xyz1, xyz2)

      sigmai = sigma1.get_scale()
      sigmaj = sigma2.get_scale()
      voli = 4.0 / 3.0 * pi * sigmai * sigmai * sigmai
      volj = 4.0 / 3.0 * pi * sigmaj * sigmaj * sigmaj
      fi = 0
      fj = 0
      if dist < sigmai + sigmaj :
          xlvol = 4.0 / 3.0 * pi * (length / 2) * (length / 2) * \
                         (length / 2)
          fi = min(voli, xlvol)
          fj = min(volj, xlvol)
      else:
          di = dist - sigmaj - length / 2
          dj = dist - sigmai - length / 2
          fi = sphere_cap(sigmai, length / 2, abs(di))
          fj = sphere_cap(sigmaj, length / 2, abs(dj))
      pofr = fi * fj / voli / volj 

      factor = (1.0 - (psi * (1.0 - pofr) + pofr * (1 - psi))*exp(-slope*dist))      
      onemprob = onemprob * factor
    prob = 1.0 - onemprob
    return prob

def log_evaluate(restraints):       
   prob = 1.0
   score = 0.0

   for r in restraints:
      prob *= r.unprotected_evaluate(None)
      if prob<=0.0000000001: 
         score=score-log(prob)
         prob=1.0

   score=score-log(prob)
   return score        

def init_representation_complex(m):
    pdbfile = IMP.pmi.get_data_path("1WCM.pdb")
    fastafile = IMP.pmi.get_data_path("1WCM.fasta.txt")
    components = ["Rpb1","Rpb2","Rpb3","Rpb4"]
    chains = "ABCD"
    colors = [0.,0.1,0.5,1.0]
    beadsize = 20
    fastids = IMP.pmi.tools.get_ids_from_fasta_file(fastafile)
    
    r = IMP.pmi.representation.Representation(m)
    hierarchies = {}
    for n in range(len(components)):
        r.create_component(components[n], color=colors[n])
        r.add_component_sequence(components[n], fastafile, id="1WCM:"+chains[n]+"|PDBID|CHAIN|SEQUENCE")
        hierarchies[components[n]] = r.autobuild_model(
            components[n], pdbfile, chains[n],
            resolutions=[1, 10, 100], missingbeadsize=beadsize)
        r.setup_component_sequence_connectivity(components[n], 1)
    return r

def init_representation_beads(m):
    r = IMP.pmi.representation.Representation(m)
    r.create_component("ProtA",color=1.0)
    r.add_component_beads("ProtA", [(1,10)],incoord=(0,0,0))
    r.add_component_beads("ProtA", [(11,20)],incoord=(10,0,0))    
    r.add_component_beads("ProtA", [(21,30)],incoord=(20,0,0)) 
    r.create_component("ProtB",color=1.0)
    r.add_component_beads("ProtB", [(1,10)],incoord=(0,10,0))
    r.add_component_beads("ProtB", [(11,20)],incoord=(10,10,0))    
    r.add_component_beads("ProtB", [(21,30)],incoord=(20,10,0)) 
    r.set_floppy_bodies() 
    return r       


def setup_crosslinks_complex(representation,mode):
    
    if mode=="single_category":
      columnmap={}
      columnmap["Protein1"]="pep1.accession"
      columnmap["Protein2"]="pep2.accession"
      columnmap["Residue1"]="pep1.xlinked_aa"
      columnmap["Residue2"]="pep2.xlinked_aa"
      columnmap["IDScore"]=None
      columnmap["XLUniqueID"]=None

      ids_map=IMP.pmi.tools.map()
      ids_map.set_map_element(1.0,1.0)

    xl = IMP.pmi.restraints.crosslinking.ISDCrossLinkMS(representation,
                               IMP.pmi.get_data_path("polii_xlinks.csv"),
                               length=21.0,
                               slope=0.01,
                               columnmapping=columnmap,
                               ids_map=ids_map,
                               resolution=1.0,
                               label="XL",
                               csvfile=True)
    xl.add_to_model()
    xl.set_label("XL")
    psi=xl.get_psi(1.0)[0]
    psi.set_scale(0.05)
    sigma=xl.get_sigma(1)[0]
    sigma.set_scale(10.0)
    return xl
        
def setup_crosslinks_beads(representation,mode):
    
    restraints_beads=IMP.pmi.tools.get_random_cross_link_dataset(representation,
                                                number_of_cross_links=100,
                                                resolution=1.0,
                                                ambiguity_probability=0.3,
                                                confidence_score_range=[0,100])
    
    ids_map=IMP.pmi.tools.map()
    ids_map.set_map_element(25.0,0.1)        
    ids_map.set_map_element(75,0.01)   
    
    xl = IMP.pmi.restraints.crosslinking.ISDCrossLinkMS(
        representation,
        restraints_beads,
        21,
        label="XL",
        ids_map=ids_map,
        resolution=1,
        inner_slope=0.01)

    sig = xl.get_sigma(1.0)[0]
    psi1 = xl.get_psi(25.0)[0]        
    psi2 = xl.get_psi(75.0)[0]    
    sig.set_scale(10.0)
    psi1.set_scale(0.1)
    psi2.set_scale(0.01)
    
    return xl,restraints_beads
        




class ISDCrossMSTest(IMP.test.TestCase):
    
    def setUp(self):
        IMP.test.TestCase.setUp(self)    
        self.m = IMP.Model()
        self.rcomplex=init_representation_complex(self.m)  
        self.rbeads=init_representation_beads(self.m)  
        self.xlc=setup_crosslinks_complex(self.rcomplex,"single_category")
        self.xlb,self.restraints_beads=setup_crosslinks_beads(self.rbeads,"single_category")        

    def test_partial_scores_complex(self):
        o=IMP.pmi.output.Output()
        o.write_test("expensive_test_cross_link_ms_restraint.dat", [self.xlc])
        passed=o.test(IMP.pmi.get_data_path("expensive_test_cross_link_ms_restraint.dat"), [self.xlc])
        self.assertEqual(passed, True)
        
        
    def test_restraint_probability_complex(self):
        
        rs=self.xlc.get_restraint()

        
        restraints=[]
        for p in self.xlc.pairs:
            p0 = p[0]
            p1 = p[1]
            prob = p[2].get_probability() 
            resid1 = p[3]
            chain1 = p[4]
            resid2 = p[5]
            chain2 = p[6]
            attribute = p[7]
            d0 = IMP.core.XYZ(p0)
            d1 = IMP.core.XYZ(p1)
            dist=IMP.core.get_distance(d0, d1)
            
            sig1 = self.xlc.get_sigma(p[8])[0]
            sig2 = self.xlc.get_sigma(p[9])[0]
            psi = self.xlc.get_psi(p[10])[0]
            test_prob=get_probability([d0],[d1],[sig1],[sig2],[psi],21.0,0.0)
            restraints.append(p[2])
            
            
            # check that the probability is the same for
            # each cross-link
            self.assertAlmostEqual(prob, test_prob, delta=0.00001)
        
        # check the log_wrapper
        log_wrapper_score=rs.unprotected_evaluate(None)
        test_log_wrapper_score=log_evaluate(restraints)
        self.assertAlmostEqual(log_wrapper_score, test_log_wrapper_score, delta=0.00001)



    def test_internal_data_structure_beads(self):
        ds=self.xlb.pairs
        nxl=0
        for l in self.restraints_beads.split("\n"):
            if l[0]=="#": continue
            t=l.split()
            if len(t)==0: continue
            chain1 = t[0]
            chain2 = t[1]
            res1 =  t[2]
            res2 =  t[3]
            ids =   t[4]
            xlid =  t[5]
            dsres1 = ds[nxl][3]
            dschain1 = ds[nxl][4]
            dsres2 = ds[nxl][5]
            dschain2 = ds[nxl][6]
            dsxlid=    ds[nxl][11]            
            self.assertEqual(chain1,dschain1)
            self.assertEqual(chain2,dschain2)            
            self.assertEqual(res1,dsres1)   
            self.assertEqual(res2,dsres2) 
            self.assertEqual(xlid,dsxlid)             
            nxl+=1            
            

    def test_restraint_probability_beads(self):
        
      
        cross_link_dict={}
        
        # randomize coordinates
        for i in range(100):
          self.rbeads.shuffle_configuration(max_translation=10)
          cross_link_dict={}
          for p in self.xlb.pairs:
              p0 = p[0]
              p1 = p[1]
              prob = p[2].get_probability() 
              resid1 = p[3]
              chain1 = p[4]
              resid2 = p[5]
              chain2 = p[6]
              attribute = p[7]
              xlid=p[11]
              d0 = IMP.core.XYZ(p0)
              d1 = IMP.core.XYZ(p1)
              sig1 = self.xlb.get_sigma(p[8])[0]
              sig2 = self.xlb.get_sigma(p[9])[0]
              psi = self.xlb.get_psi(p[10])[0]
              
              if xlid not in cross_link_dict:
                 cross_link_dict[xlid]=([d0],[d1],[sig1],[sig2],[psi],prob)
              else:
                 cross_link_dict[xlid][0].append(d0)
                 cross_link_dict[xlid][1].append(d1)               
                 cross_link_dict[xlid][2].append(sig1)
                 cross_link_dict[xlid][3].append(sig2)
                 cross_link_dict[xlid][4].append(psi)                 

          for xlid in cross_link_dict:

              test_prob=get_probability(cross_link_dict[xlid][0],
                                             cross_link_dict[xlid][1],
                                             cross_link_dict[xlid][2],
                                             cross_link_dict[xlid][3],
                                             cross_link_dict[xlid][4],21.0,0.01)
              prob=cross_link_dict[xlid][5]

              self.assertAlmostEqual(prob/test_prob,1.0, delta=0.0001)

if __name__ == '__main__':
    IMP.test.main()
