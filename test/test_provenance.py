import IMP
import IMP.test
import IMP.pmi.macros
import IMP.pmi.tools

class Tests(IMP.test.TestCase):
    def get_all_provenance(self, h):
        def get_subclass(p):
            for c in (IMP.core.StructureProvenance, IMP.core.SampleProvenance,
                      IMP.core.CombineProvenance, IMP.core.FilterProvenance,
                      IMP.core.ClusterProvenance):
                if c.get_is_setup(p):
                    return c(p)
            raise TypeError("Unknown provenance type", p)
        if IMP.core.Provenanced.get_is_setup(h):
            prov = IMP.core.Provenanced(h).get_provenance()
            while prov:
                yield get_subclass(prov)
                prov = prov.get_previous()

    def make_representation(self):
        pdbfile = self.get_input_file_name("nonbond.pdb")
        fastafile = self.get_input_file_name("nonbond.fasta")
        fastids = IMP.pmi.tools.get_ids_from_fasta_file(fastafile)

        m = IMP.Model()
        r = IMP.pmi.representation.Representation(m)

        r.create_component("A", color=0.)
        r.add_component_sequence("A", fastafile, id=fastids[0])
        r.autobuild_model("A", pdbfile, "A", resrange=(12,12),
                          resolutions=[1, 10], missingbeadsize=1)
        return m, r

    def test_pdb_provenance(self):
        """Make sure that provenance info is added for each input PDB file"""
        m, r = self.make_representation()
        pdb_frags = [f for f in IMP.pmi.tools.select(r, resolution=1)
                     if 'pdb' in f.get_name()]
        parent = pdb_frags[0].get_parent()
        prov = list(self.get_all_provenance(parent))
        self.assertEqual(len(prov), 1)
        self.assertEqual(prov[0].get_filename(),
                         self.get_input_file_name("nonbond.pdb"))
        self.assertEqual(prov[0].get_chain_id(), 'A')
        self.assertEqual(prov[0].get_start_residue_index(), 12)

if __name__ == '__main__':
    IMP.test.main()
