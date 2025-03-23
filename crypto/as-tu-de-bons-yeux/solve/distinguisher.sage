load("parameters.sage")

def is_in_bound(u):
    return all([-RING_RANK*eta <= uu <= RING_RANK*eta for uu in u.lift_centered()])

def solve_lwe(A, t):
    Ik = identity_matrix(k)
    L  = block_matrix(ZZ, [ [A, Ik, Matrix(-t).T, q*Ik] ])

    kerL  = L.right_kernel().matrix()
    bkzed = kerL.BKZ()

    for r in bkzed.rows():
        res = r[l+k]
        sign_res = sign(res)
        
        if abs(res) != 1:
            continue
        
        s = vector(Fq, [sign_res*i for i in r[:l]])
        e = vector(Fq, [sign_res*j for j in r[l:l+k]])

        if t != A*s + e:
            continue

        if not is_in_bound(e) and not is_in_bound(s):
            continue

        return e,s

    return False

# Appelons phi le morphisme allant vers Z_q
def phi_vec(u):
    return vector(Fq, [sum(list(P)) for P in u])

def phi_mat(A):
    return Matrix(Fq, [phi_vec(u) for u in A])

def to_lwe(A, t):
    return phi_mat(A), phi_vec(t)

def distinguish(A, t):
    A, t = to_lwe(A, t)
    res = solve_lwe(A, t)

    if res != False:
        return True
    else:
        return res

