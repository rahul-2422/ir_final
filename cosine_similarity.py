import math

def cosine_similarity(vectA, vectB):
    a_mag = math.sqrt(sum([value * value for value in vectA]))
    b_mag = math.sqrt(sum([value * value for value in vectB]))

    dot_product = 0

    for i in zip(vectA, vectB):
        a,b = i
        dot_product += ( a * b )

    similarity = dot_product / ( a_mag * b_mag )

    return similarity