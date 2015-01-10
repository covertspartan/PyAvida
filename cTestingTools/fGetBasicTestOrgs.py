__author__ = 'covertar'
# return strings containing strings with specific test orgs
# these are based on the sample progrmas from Lenski et al 2003 supplementary materials
# http://myxo.css.msu.edu/papers/nature2003/logic_programs.html


def getNandGenome():
    return 'rucavcccccccccccccccqqcpqbccccccccccccccutycasvab'

def getOrNotGenome():
    return 'rucavcccccccccccccccccqqcppqbccccccccccccutycasvab'

def getAndGenome():
    return 'rucavcccccccccccccccqqcpgfcpqbccccccccccccccutycasvab'

def getOrGenome():
    return 'rucavcccccccccqgfcpaqgfcpicpqbccccccccccccccutycasvab'

def getAndNotGenome():
    return 'rucavcccccccccccccccqqcppgfcpqbccccccccccccccutycasvab'

def getNorGenome():
    return 'rucavcccccccccccccccqgfcpaqgfcpicpgfcpqbcccccccccutycasvab'

def getXorGenome():
    return 'rucavcccccccccccqqcgpipiafpicpqbcccccccccutycasvab'

def getEquGenome():
    return 'rucavcccccccccqqcgpipiafpicpgfcpqbccccccccccccutycasvab'


# organsism encoded with two different functions
# used to make sure input state of cpu is updating correctly
def getNandOrGenome():
    return 'rucavcccccccqqcpqbcccqgfcpaqgfcpicpqbccccutycasvab'