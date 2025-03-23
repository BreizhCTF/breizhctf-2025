from ast import literal_eval

# Matrice générée avec la fonction:
# `random_matrix(Zn, k, l)`
def get_a(p):
    f = open(p, "r")
    A = f.read() ; f.close()

    return literal_eval(A)

