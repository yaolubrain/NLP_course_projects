def prefix(word):
    if word[0:2] == 're' or word[0:2] == 'in' or word[0:2] == 'un':
        return [word[2:]]
    else
        return []

def suffix(word):
    corr = []
    if word[-3:] == 'ive':
        corr.append(word[:-3] + 'e')
    if word[-3:] == 'ive':
        corr.append(word[:-3])
    if word[-3:] == 'ion':
        corr.append(word[:-3] + 'e')
    if word[-7:] == 'ication':
        corr.append(word[:-7] + 'y')
    if word[-2:] == 'en':
        corr.append(word[:-2])
    if word[-4:] == 'ions':
        corr.append(word[:-4] + 'e')
    if word[-8:] == 'ications':
        corr.append(word[:-8] + 'y')
    if word[-3:] == 'ens':
        corr.append(word[:-3])
    if word[-4:] == 'ieth':
        corr.append(word[:-4] + 'y')
    if word[-3:] == 'ily':
        corr.append(word[:-3] + 'y')
    if word[-2:] == 'ly':
        corr.append(word[:-2])
    if word[-3:] == 'ing':
        corr.append(word[:-3] + 'e')
    if word[-3:] == 'ing':
        corr.append(word[:-3])
    if word[-4:] == 'ings':
        corr.append(word[:-4] + 'e')
    if word[-4:] == 'ings':
        corr.append(word[:-4])
    if word[-2:] == 'ed':
        corr.append(word[:-2] + 'e')
    if word[-3:] == 'ied' and word[-5] not in 'aeiou':
        corr.append(word[:-3] + 'y')
    if word[-4:] == 'ed':
        corr.append(word[:-4])
    if word[-3:] == 'yed':
        corr.append(word[:-3] + 'y')
    if word[-3:] == 'est':
        corr.append(word[:-3] + 'e')
    if word[-4:] == 'iest' and word[-5] not in 'aeiou':
        corr.append(word[:-4] + 'y')
    if word[-4:] == 'yest' and word[-5] in 'aeiou':
        corr.append(word[:-4] + 'y')
    if word[-3:] == 'est' and word[-4] not in 'ey':
        corr.append(word[:-3] + 'e')
    if word[-2:] == 'er':
        corr.append(word[:-2] + 'e')
    if word[-3:] == 'ier' and word[-4] not in 'aeiou':
        corr.append(word[:-3] + 'y')
    if word[-3:] == 'yer' and [word[-4] in 'aeiou':
        corr.append(word[:-3] + 'y')
    if word[-2:] == 'er' and word[-3] not in 'ey':
        corr.append(word[:-2])
    if word[-3:] == 'ers':
        corr.append(word[:-3] + 'e')
    if word[-4:] == 'iers' and word[-5] not in 'aeiou':
        corr.append(word[:-4] + 'y')
    if word[-4:] == 'yers' and [word[-5] in 'aeiou':
        corr.append(word[:-4] + 'y')
    if word[-3:] == 'ers' and word[-4] not in 'ey':
        corr.append(word[:-3])
    if word[-3:] == 'ies' and word[-4] not in 'aeiou':
        corr.append(word[:-3] + 'y')
    if word[-2:] == 'ys' and word[-3] in 'aeiou':
        corr.append(word[:-2] + 'y')
    if word[-2:] == 'es' and (word[-4:-2] == 'sh' or word[-4:-2] == 'ch' or word[-4:-2] == 'th'):
        corr.append(word[:-2])
    if word[-2:] == 'hs' and word[-3] not in 'sct':
        corr.append(word[:-2] + 'h')
    if word[-2:] == 'es' and word[-3] in 'sxz':
        corr.append(word[:-2])
    if word[-1:] == 's' and word[-2] not in 'SXZHY':
        corr.append(word[:-1])
    if word[-5:] == 'iness' and word[-6] not in 'aeiou':
        corr.append(word[:-5] + 'y')
    if word[-5:] == 'yness' and word[-6] in 'aeiou':
        corr.append(word[:-5] + 'y')
    if word[-4:] == 'ness' and word[-5] != 'y':
        corr.append(word[:-4])
    if word[-2:] == '\'s':
        corr.append(word[:-2]) 

    return corr

def correct(word):
    return list(set(prefix(word) + suffix(word))) 







    
