class Grid():
	def __init__(self,al,gamma):
		self.states=[]
		self.util_0={}#t+1 vals
		self.util_1={}#t vals
		self.action={}#for policy
		
		self.be=be#BellmanError
		self.gamma=gamma

	def update_util(self):
		for s in self.states:
			self.util_1[s] = self.util_0[s]

	def check_converged(self):
		max_val = float(0.00)
		for s in self.states:
			diff=abs(self.util_1[s]-self.util_0[s])
			if (diff>=max_val):
				max_val=diff

		if (max_val<=self.be):
			return True
		else:
			return False

class iters():
	def __init__(self,cost_d,cost_r,cost_s,grid,in_val):
		stamina=[0,50,100]
		arrows=[0,1,2,3]
		health_MD=[0,25,50,75,100]
		
		grid.states = [(s,a,h) for s in stamina for a in arrows for h in health_MD] #order fixed
		self.cost_s=cost_s#cost of shooting
		self.cost_d=cost_d
		self.cost_r=cost_r

    	for state in grid.states:
    		grid.util_0[state] = float(0)
    		grid.util_1[state] = float(0)
    		if state[2]==0:#health value
    			grid.util_0[state] = float(10)

    def action_vals(self,state,grid,in_val):
    	s_val=0
    	r_val=0#recharge
    	d_val=0#dodge
    	s= state[0]
    	a= state[1]
    	h= state[2]
    	
    	if state[0] in [50,100] and state[1] in [1,2,3] and state[2] in [25,50,75,100]:
    		s_val = ((0.5)*float(grid.util_1[(s-50,a-1,h)]) + (0.5)*float(grid.util_1[(s-50,a-1,h-25)]))
    	
    	if state[0] in [0,50]:
    		r_val = ((0.8)*float(grid.util_1[(s+50,a,h)]) + (0.2)*float(grid.util_1[(s,a,h)]))
    	

    	if state[0] == 100:
    		if a==3:
    			d_val = float(((0.8)*float(grid.util_1[(50,a,h)]) + (0.2)*float(grid.util_1[(0,a,h)])))
    		else:
    			d_val = float(float(0.8*0.8)*float(grid.util_1[(50,a+1,h)]) + float(0.8*0.2)*float(grid.util_1[(50,a,h)]) + float(0.2*0.8)*float(grid.util_1[(0,a+1,h)]) + float(0.2*0.2)*float(grid.util_1[(0,a,h)]))
    	if s == 50:
    		if a==3:
    			d_val = float(grid.util_1[(0,a,h)])
    		else:
    			d_val = float(float(0.8)*float(grid.util_1[(0,a+1,h)]) + float(0.2)*float(grid.util_1[(0,a,h)]))

    	return s_val,r_val,d_val

    def maximum(a, b, c): 
    	list = [a,b,c] 
    	return max(list)

    def choose_action(self,state,grid,in_val):
    	ret_ac = 10
    	s_val,r_val,d_val = action_vals(state,grid,1)
    	s_val += self.cost_s
    	r_val += self.cost_r
    	d_val += self.cost_d

    	if s_val == maximum(s_val,r_val,d_val):
    		ret_ac=1
    	elif r_val == maximum(s_val,r_val,d_val):
    		ret_ac=2
    	else:
    		ret_ac=3

    	return ret_ac

    def update_utils(self,grid,in_val):
    	for state in grid.states:
	    	s_val,r_val,d_val = action_vals(state,grid,1)
	    	action = ''
	    	ac = choose_action(state,grid,1)
	    	s= state[0]
	    	a= state[1]
	    	h= state[2]

	    	val = float(max(self.cost_s + grid.gamma*s_val,self.cost_r + grid.gamma*r_val,self.cost_d + grid.gamma*d_val))
		    if state[2]==0:
		    	val = float(10)
		    	action = '-1'

		    if ac==1:
	    		action='SHOOT'
	    	elif ac==2:
	    		action='RECHARGE'
	    	elif ac==3:
	    		action='DODGE'
	    
		    grid.action[state] = action
		    grid.util_0[state] = val


		    print('('+str(int(s/50))+','+str(a)+','+str(int(h/25))+'):'+str(action)+'=['+str(round(grid.util_0[state],3))+']')
		pass

if __name__=="__main__":
  grid = Grid(gamma=0.99,al=0.001)
  it = iters(gird,cost_s=-10,cost_d=-10,cost_r=-10)
  i=1
  # print('Gamma = '+str(mdp.gamma)+'\tDelta = '+str(mdp.delta))
  while(grid.check_converged()==False):
    print('iteration='+str(i))

    #uncommet for viewing update values tag:A
    # print("State\t\tDV\tSV\tRV\tU\tVal")
    grid.update_util()
    it.update_utils(grid,1)
    i+=1
    pass


    