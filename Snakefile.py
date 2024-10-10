import os, glob
from snakemake.io import glob_wildcards

# Configurations
proteins = glob_wildcards("data/proteins/{protein}.pdb").protein
ligands = glob_wildcards("data/ligands/{ligand}.sdf").ligand

# Default docking box size
config = {
    "size_x": 40,
    "size_y": 40,
    "size_z": 40,
    "exhaustiveness": 8
}

# Final rule that executes docking for all combinations of proteins and ligands
rule all:
    input:
        expand("output/proteins_prep/{protein}.pdbqt", protein=proteins),
        expand("output/docking/{protein}_{ligand}_log.txt", protein=proteins, ligand=ligands),
        expand("output/docking/{protein}_{ligand}_out.pdbqt", protein=proteins, ligand=ligands)

# Rule to prepare the protein for docking (generating PDBQT)
rule prepare_protein:
    input:
        pdb="data/proteins/{protein}.pdb"
    output:
        pdbqt="output/proteins_prep/{protein}.pdbqt"
    shell:
        """
        python2 FlipbookApp/mfb/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_receptor4.py -r {input.pdb} -o {output.pdbqt} -A hydrogens  -e True -v
        """

# Rule to prepare the ligand for docking (generating PDBQT)
rule prepare_ligand:
    input:
        sdf="data/ligands/{ligand}.sdf"
    output:
        pdbqt="output/ligands_prep/{ligand}.pdbqt"
    shell:
        """
        obabel {input.sdf} -O output/ligands_prep/{wildcards.ligand}.mol2 && python2 FlipbookApp/mfb/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_ligand4.py -l output/ligands_prep/{wildcards.ligand}.mol2  -o {output.pdbqt}
        """

# Rule to determine the grid center coordinates using AutoDockTools
rule get_grid_center:
    input:
        pdb="output/proteins_prep/{protein}.pdbqt",
        mol2= "output/ligands_prep/{ligand}.pdbqt"
    output:
        gpf="output/proteins_gpf/{protein}_{ligand}.gpf"
    shell:
        """
        python2 FlipbookApp/mfb/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_gpf4.py -l {input.mol2} -r {input.pdb} -o {output.gpf}
        """

# Rule to extract center coordinates from the generated GPF file
rule extract_grid_center:
    input:
        gpf="output/proteins_gpf/{protein}_{ligand}.gpf"
    output:
        center="output/proteins_gpf/{protein}_{ligand}_center.txt"
    run:
        # Read the GPF file to extract the grid center
        with open(input.gpf) as f:
            for line in f:
                if line.startswith("gridcenter"):
                    center_coords = line.split()[1:4]  # Extract x, y, z
                    with open(output.center, "w") as out_f:
                        out_f.write(" ".join(center_coords))

# Rule to perform docking with AutoDock Vina using the extracted grid center
rule dock:
    input:
        protein="output/proteins_prep/{protein}.pdbqt",
        ligand="output/ligands_prep/{ligand}.pdbqt",
        center="output/proteins_gpf/{protein}_{ligand}_center.txt"
    output:
        out="output/docking/{protein}_{ligand}_out.pdbqt",
        log="output/docking/{protein}_{ligand}_log.txt"
    params:
        size_x=config["size_x"],
        size_y=config["size_y"],
        size_z=config["size_z"],
        exhaustiveness=config["exhaustiveness"]
    shell:
        """
        vina --receptor {input.protein} --ligand {input.ligand} \
             --center_x $(cat {input.center} | cut -d ' ' -f 1) \
             --center_y $(cat {input.center} | cut -d ' ' -f 2) \
             --center_z $(cat {input.center} | cut -d ' ' -f 3) \
             --size_x {params.size_x} --size_y {params.size_y} --size_z {params.size_z} \
             --out {output.out} --log {output.log} --exhaustiveness {params.exhaustiveness}
        """


