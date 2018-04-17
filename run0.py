#from MG import *
execfile('MG.py')

print(datetime_str())
wld=World(1000, 1000, 10, 10)
# # agents, # iterations. Each agent: mem_len #, alternative strategies #
wld.run()
print(datetime_str())

subplot(211)
plot(wld.prices_hist)
title('prices')

subplot(223)
hist(wld.mstate_hist, 5)
title('memory state')

subplot(224)
mu, sigma = avg(wld.ACTION_hist), std(wld.ACTION_hist)
n, bins, patches = hist(wld.ACTION_hist, 20, density=True)
norm_curv = (np.sqrt(2*np.pi)*sigma)**(-1) * np.exp(-0.5*(1/sigma*(bins-mu))**2)
plot(bins, norm_curv, 'blue')
title('ACTION state: $\mu=%f, \sigma=%f$'%(mu, sigma))

savefig('run0.jpg')
show()
clf()

savetxt('run0_mstate_hist.txt', array(wld.mstate_hist))
savetxt('run0_wstate_hist.txt', array(wld.wstate_hist))
savetxt('run0_ACTION_hist.txt', array(wld.ACTION_hist))
savetxt('run0_prices_hist.txt', array(wld.prices_hist))
