while True :
    inp1 = int(input('tinggi  '))
    inp2 = int(input('lebar   '))
    while True :
        inp = input()
        if 'z' in inp :
            break
        inp = inp.replace('px','')
        inp = inp.replace(';','')
        inp = inp.split(':')
        if( 'width' in inp[0]  or 'left in inp[0] ' or 'right' in inp[0]):
            result = int(inp[1])*100/inp2
            print (inp[0] + ' : '+str(result) + '%;')
        else :
            result = int(inp[1])*100/inp1
            print (inp[0] + ' : '+str(result) + '%;')

