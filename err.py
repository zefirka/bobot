while True:
    a = input('Enter number:\n$ ')

    try:
        a = int(a)
        print(a + 10)
        break
    except ValueError as err:
        print('There is ValueError occured: "{}"'.format(err))
        continue
    
