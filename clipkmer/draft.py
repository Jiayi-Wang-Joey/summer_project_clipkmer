import random
random.seed(10)
s="abcdef123"
xs = ''.join(random.sample(s,len(s)))
print(xs)