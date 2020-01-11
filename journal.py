y = 2019
m = 1
d = 1    

while True:
    filename = str(y) + '-'

    if (d > 31):
        m += 1
        d = 1

    if (m > 12):
        break

    if (m < 10):
        filename += '0' + str(m)
    else:
        filename += str(m)
    
    filename += '-'

    if (d < 10):
        filename += '0' + str(d)
    else:
        filename += str(d)

    filename += '.txt'

    try:
        with open(filename) as file_object:
            contents = file_object.read().strip()
        with open('2019 Journal.txt', 'a') as output:
            output.write(contents + '\n\n\n\n')
    except FileNotFoundError:
        pass
    
    d += 1
