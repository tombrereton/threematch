file_name = ''
file = open(file_name)

for i in range(26):
    file.readline()

s1 = file.readline()

s1 = s1.split(sep='\t')
s1.remove(s1[-1])
