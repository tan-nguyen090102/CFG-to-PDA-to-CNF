"""Module to convert CFG to PDA"""
from cfg_to_cnf import CFGToCNF
from cfg_to_pda import CFGToPDA

pda_conversion = CFGToPDA("test_pda.txt")
cnf_conversion = CFGToCNF("test_cnf.txt")

if __name__ == "__main__":
    # Convert CFG to PDA
    # productions = pda_conversion.storing_cfg()
    # nodes = pda_conversion.storing_pda(production_list=productions)
    # pda_conversion.graphing_pda(node_list=nodes)

    # Convert CFG to CNF
    productions = cnf_conversion.storing_cfg()
    cnf_list = cnf_conversion.convert_to_cnf(production_list=productions)
    cnf_conversion.printing_cnf(cnf_list=cnf_list)
