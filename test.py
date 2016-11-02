test = ['123', '343','dsdf', 'sdfs']
for i in test:
        j = test.index(i)
        for k in test[j+1:]:
                print(k)
