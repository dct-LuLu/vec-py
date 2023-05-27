

# print(int((4**(PROFONDEUR + 1) - 1) / 3))
# print()
# print(int((4**(PROFONDEUR - 3) - 1) / 3))
# print(int((4**(PROFONDEUR - 2) - 1) / 3))
# print(int((4**(PROFONDEUR - 1) - 1) / 3))
# print(int((4**(PROFONDEUR) - 1) / 3))

# print(4 * 5**(PROFONDEUR - 3) + 1)

# print()

# tab = '\t'

# for i in range(int((4**(PROFONDEUR + 1) - 1) / 3) - 1):
#     a = i
#     b = []

#     for j in range(PROFONDEUR - 1):
#         calcul = int((4**(PROFONDEUR - j) - 1) / 3)

#         b.append(a // (calcul))

#         if a % calcul == 0:
#             print(tab * j, i, b)
#             break

#         a = a % calcul - 1
#     else:
#         b.append(a)
#         print(tab * PROFONDEUR, i, b)


# def foo(n):
#     tab = []

#     for j in range(PROFONDEUR - 1):
#         calcul = int((4**(PROFONDEUR - j) - 1) / 3)

#         tab.append(n // (calcul))

#         if n % calcul == 0:
#             break

#         n = n % calcul - 1
#     else:
#         tab.append(n)

#     return tab

# print(foo(340))

    # if i % (4 * 5**(PROFONDEUR - 2) + 1) == 0:
    #     print('\t', i)
    # else:
    #     a = i % (4 * 5**(PROFONDEUR - 2) + 1)
    #     if a % (4 * 5**(PROFONDEUR - 3) + 1) == 1:
    #         print('\t\t', i)

    # if i % (4 * 5 ** (PROFONDEUR - 1) + 1) == 0:
    #     print("1:", i)
    # elif i % (4 * 5 ** (PROFONDEUR - 2) + 1) == 0:
    #     print("\t2:", i)
    # else:
    #     print("\t\t3:", i)


PROFONDEUR =  6

def foo(n):
    tab = []

    for j in range(PROFONDEUR - 1):
        calcul = int((4**(PROFONDEUR - j) - 1) / 3)

        tab.append(n // (calcul))

        if n % calcul == 0:
            break

        n = n % calcul - 1
    else:
        tab.append(n)

    return tab

dict = {}

# tab = foo(0)
# dict[tuple(tab)] = 1

# tab = foo(1)
# dict[tuple(tab)] = dict[tuple(tab[1:])]

for i in range(50):
    dict[i] = 1



print(dict)


