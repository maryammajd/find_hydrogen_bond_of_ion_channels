This script needs installation of GROMACS software.

To find the hydrogen bonds formed in an MD simulation, we need to have some files as the input. First, copy the .gro file of the model in the input folder and change the name to source_model.gro (you can download the pdb file of the protein and convert it to gro file using GROMACS). 
Then, create a csv file containing data about the simulations you want to derive the hydrogen bonds of.Each line contains the data about one simulation. The first line should contain the source simulation.
 Pay attention that the file should have the following format. 
simulation_name, color_for_plot,complete_directory_of_the_sim, caption_to_be_used_in_plot_legends,

Then, you need to find the residues that make the voltage sensing domains(VSD) or the pore domain for your specific protein from the literature. Using this data, you can now make an index file for each vsd and separating each helix. You can use GROMACS feature "gmx make_ndx" for this step, but you need to have the residue numbers that make each helix. save the files as #NAME.ndx. 

Then, run the bash files from number 1 to number 4 to find all the H-bonds and save and plot them.
ATTENTION: you may need extra files for running each step. They are mentioned in the code itself.
