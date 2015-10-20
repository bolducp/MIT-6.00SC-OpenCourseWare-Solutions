T = (0.1, 0.1)
x = 0.0
def print_i(T, x):
    i = 6
    print i
    for i in range(len(T)):
        for j in T:
            x += i + j
            print x
    print i
    print j

"""assumes v1 and v2 are lists of ints.
 Returns a list containing the pointwise sum of
 the elements in v1 and v2. For example,
 addVectors([4,5], [1,2,3]) returns [5,7,3],and
 addVectors([], []) returns []. Does not modify inputs."""

def addVectors(v1, v2):
    if len(v1) > len(v2):
        result = v1
        other = v2
    else:
        result = v2
        other = v1
    for i in range(len(other)):
        result[i] += other[i]
    return result


a = [3, 2, 4]
b = [1, 2, 0, 0]
print addVectors(a, b)