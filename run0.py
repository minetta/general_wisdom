#from MG import *
execfile('MG.py')

print(datetime_str())
wld=World(1000,1000,10,10)
# 1K agents, 1K iterations, mem_len 10, 10 alternative strategies each agent
wld.run()
print(datetime_str())

subplot(411)
plot(wld.prices_hist)
title('prices')

subplot(412)
plot(wld.wstate_hist)
title('win state')

subplot(413)
plot(wld.ACTION_hist)
title('ACTION state')

subplot(414)
plot(wld.mstate_hist)
title('memory state')
show()
