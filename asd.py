f = open("years.txt", "r")
a = []
for i in range(6):
    a.append(int(f.readline()))
print(a)

