from Main import main
summ = 0
for x in range(10000):
    summ += main()
print(summ/10000)