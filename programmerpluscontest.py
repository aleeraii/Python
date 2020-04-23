def alpha2num(alpha):
    data = {}
    n = 1
    for c in range(97, 123):
        while n < 27:
            data[chr(c)] = n
            n += 1
            break
    rev_alpha = alpha.lower()[::-1]
    final = ""
    res_list = []
    for v in rev_alpha:
        if v in res_list:
            res_list[res_list.index(v)] = None
            res_list.append(v)
            value = data[v] + res_list.index(v)
            final += str(value)
        else:
            res_list.append(v)
            value = data[v] + res_list.index(v)
            final += str(value)
    return final


print(alpha2num("insight"))