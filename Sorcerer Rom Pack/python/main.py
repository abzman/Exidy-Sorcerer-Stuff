from itertools import permutations, combinations

def handleChoices(c7, c6, c5):
    # create list of 4k pages based on c7
    s = set()
    for elem in c7:
        s.add(elem)
    s.add(15)
    #print(f'Address bits enabled by choice7:')
    #print(s)
    mask = 0
    for elem in s:
        mask |= 1 << (elem - 12)
    pages = []
    for i in range(0,16):
        if i & mask == mask:
            pages.append(i)

    #print(f'Pages enabled:')
    #print(pages)
    min = 16
    for elem in c6:
        if elem < min:
            min = elem
    blocksize = 1<<min
    #print(f'Address bits connected by choice6:')
    #print(c6)
    #print()
    #print('Choice 5:')
    #print(c5)
    # idea - create a mask of bits with ones for bits that are defined by the current option
    results = []
    for page in pages:
        pageaddr = page*0x1000
        for addr in range(pageaddr,pageaddr+0x1000,blocksize):
            # now, go through this page
            # match the page and c6 to a location
            # and then to a particular output of U6
            a = (addr>>c6[0]) & 1
            b = (addr>>c6[1]) & 1
            c = (addr>>c6[2]) & 1
            chan = c*4+b*2+a
            #print(f'{hex(addr)}-{hex(addr+blocksize-1)} -> {chan}')
            if c5 == '5A':
                if chan < 4:
                    results.append(f'{hex(addr)}-{hex(addr + blocksize - 1)} -> ROM{chan+1}')
            elif c5 == '5B':
                if chan == 2 or chan == 3:
                    results.append(f'{hex(addr)}-{hex(addr + blocksize - 1)} -> ROM{chan+1}')
                elif chan == 4 or chan == 5:
                    results.append(f'{hex(addr)}-{hex(addr + blocksize - 1)} -> ROM{chan-3}')
            else:  # c5 == 'None':
                if chan == 2 or chan == 3:
                    results.append(f'{hex(addr)}-{hex(addr + blocksize - 1)} -> ROM{chan+1}')

    if len(results) > 0:
        print('Choices:')
        print(c7, c6, c5)
        print(f'Blocksize:')
        print(blocksize)
        for item in results:
            print(item)
        print()
        return True
    return False

def main():
    inputs7 = [12, 14, 15, 15]
    choice7 = combinations(inputs7, 2)

    #inputs6 = [14, 10, 11, 13, 12]
    inputs6 = [14, 10, 11, 13, 12, 14, 10, 11, 13, 12]
    choice6 = permutations(inputs6, 3)

    inputs5 = ['5A', '5B', 'None']
    choice5 = combinations(inputs5, 1)

    #print(list(choice7))
    #print(list(choice6))
    #print(list(choice5))

    count = 0
    list_choice7 = list(choice7)
    list_choice6 = list(choice6)
    #list_choice6 = [[12, 13, 14], [11, 12, 13], [10, 11, 12]]
    list_choice5 = list(choice5)
    for c7 in list_choice7:
        for c6 in list_choice6:
            for c5 in list_choice5:
                if handleChoices(c7, c6, c5[0]):
                    count += 1

    print(f'Total valid cases: {count}')

if __name__ == '__main__':
    main()





