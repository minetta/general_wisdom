#from MG import *
execfile('MG.py')

print(datetime_str())
wld=World(10000,100,15,100)
wld.run()
print(datetime_str())

plot(wld.mem_hist)
show()
