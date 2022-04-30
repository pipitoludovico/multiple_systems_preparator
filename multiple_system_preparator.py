import os
import sys


def main():
    initial = os.getcwd()
    for subdir, dirs, files in os.walk(sys.argv[1]):
        for f in files:

            if f.endswith(".pdb") and f != "receptor.pdb":
                os.system(f"pdb_seg -X {f} > {f.replace('.pdb', '')}_2.pdb")
                os.system(f"rm {f}")
                os.system(f"mv {f.replace('.pdb', '')}_2.pdb {f}")

                sys_builder = ["package require psfgen\n"
                               "resetpsf\n"
                               f"readpsf receptor.psf\n"
                               f"readpsf {f.replace('.pdb', '')}.psf\n"
                               "coordpdb receptor.pdb\n"
                               f"coordpdb {f.replace('.pdb', '')}.pdb\n"
                               "writepsf all.psf\n"
                               "writepdb all.pdb\n"
                               'puts "merging complete!!!"\n'
                               'quit']

                config_file = open(f"{sys.argv[1]}{f.replace('.pdb', '')}/structure_merger.tcl", "w")

                for line in sys_builder:
                    config_file.write(line)
                config_file.close()

                sys_prep = ["package require autoionize\n"
                            "package require solvate\n\n"
                            "solvate all.psf all.pdb -t 10 -o solvate\n"
                            "autoionize -psf solvate.psf -pdb solvate.pdb -o ionized -sc 0.154\n"
                            "quit"]

                sys_prep_inp = open(f"{sys.argv[1]}{f.replace('.pdb', '')}/solv_and_ionize.tcl", "w")
                for line in sys_prep:
                    sys_prep_inp.write(line)
                sys_prep_inp.close()

                os.chdir(f"{sys.argv[1]}{f.replace('.pdb', '')}")
                os.system("vmd -dispdev text -e structure_merger.tcl")
                os.system("vmd -dispdev text -e solv_and_ionize.tcl")
                os.system("rm all.*")
                os.system("rm *.tcl")
                os.system("rm solvate.*")
                os.chdir(initial)


if __name__ == '__main__':
    main()
