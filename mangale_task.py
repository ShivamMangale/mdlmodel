class Grid():
	def __init__(self,gamma,be):#changed al to be
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
			diff=abs(float(self.util_1[s])-float(self.util_0[s]))
			if (diff>=max_val):
				max_val=diff
		print(max_val)
		if (max_val<=self.be):
			return True
		else:
			return False

class iters():
	def __init__(self,grid,cost_d,cost_r,cost_s,in_val):#changed order of grid
		stamina=[0,1,2]
		arrows=[0,1,2,3]
		health_MD=[0,1,2,3,4]
		
		grid.states = [(h,a,s) for h in health_MD for a in arrows for s in stamina] #order fixed
		self.cost_s=cost_s#cost of shooting
		self.cost_d=cost_d
		self.cost_r=cost_r

		for state in grid.states:
			grid.util_0[state] = float(0)
			grid.util_1[state] = float(0)
			# if state[2]==0:#health value
			# 	grid.util_0[state] = float(10)

	def action_vals(self,state,grid,in_val):
		s_val=0
		r_val=0#recharge
		d_val=0#dodge
		h= state[0]
		a= state[1]
		s= state[2]
		
		if s in [1,2] and a in [1,2,3] and h in [1,2,3,4]:
			s_val = ((0.5)*float(grid.util_1[(h,a-1,s-1)]) + (0.5)*float(grid.util_1[(h-1,a-1,s-1)]))

		if s in [0,1]:
			r_val = ((0.8)*float(grid.util_1[(h,a,s+1)]) + (0.2)*float(grid.util_1[(h,a,s)]))
		

		if s == 2:
			if a==3:
				d_val = float(((0.8)*float(grid.util_1[(h,a,1)]) + (0.2)*float(grid.util_1[(h,a,0)])))
			else:
				d_val = float(float(0.8*0.8)*float(grid.util_1[(h,a+1,1)]) + float(0.8*0.2)*float(grid.util_1[(h,a,1)]) + float(0.2*0.8)*float(grid.util_1[(h,a+1,0)]) + float(0.2*0.2)*float(grid.util_1[(h,a,0)]))
		if s == 1:
			if a==3:
				d_val = float(grid.util_1[(h,a,0)])
			else:
				d_val = float(float(0.8)*float(grid.util_1[(h,a+1,0)]) + float(0.2)*float(grid.util_1[(h,a,0)]))

		return s_val,r_val,d_val

	def maximum(self,a, b, c): 
		list = [a,b,c] 
		return max(list)

	def choose_action(self,state,grid,in_val):
		ret_ac = 10
		s_val,r_val,d_val = self.action_vals(state,grid,1)
		s_val = self.cost_s + grid.gamma*s_val
		r_val = self.cost_r + grid.gamma*r_val
		d_val = self.cost_d + grid.gamma*d_val

		if s_val == self.maximum(s_val,r_val,d_val):
			ret_ac=1
			val = s_val
		elif r_val == self.maximum(s_val,r_val,d_val):
			ret_ac=2
			val = r_val
		else:
			ret_ac=3
			val = d_val

		return ret_ac, val

	def update_utils(self,grid,in_val):
		for state in grid.states:
			# s_val,r_val,d_val = self.action_vals(state,grid,1)
			action = ''
			ac, val = self.choose_action(state,grid,1)
			h= state[0]
			a= state[1]
			s= state[2]
			if ac==1:
				action='SHOOT'
			elif ac==2:
				action='RECHARGE'
			elif ac==3:
				action='DODGE'
			# val = float(max(self.cost_s + grid.gamma*s_val,self.cost_r + grid.gamma*r_val,self.cost_d + grid.gamma*d_val))
			if h==1 and ac==1:
				val += float(10)
				# action = '-1'
			if h==0:
				val = 0
				action = '-1'

			
		
			grid.action[state] = action
			grid.util_0[state] = val


			print('('+str(int(h))+','+str(a)+','+str(int(s))+'):'+str(action)+'=['+str(round(grid.util_0[state],3))+']')
		pass

if __name__=="__main__":
        #filename = open("path")
	# print("dsljbo", file = filename)
	stepcost = -20#update
	grid = Grid(gamma=0.99,be=0.001)#changed al to be
	it = iters(grid,cost_s=stepcost,cost_d=stepcost,cost_r=stepcost,in_val = 0)#in_val wasn't added. put dummy. recheck
	i=0
	# print('Gamma = '+str(mdp.gamma)+'\tDelta = '+str(mdp.delta))
	print('iteration='+str(i))
	grid.update_util()
	it.update_utils(grid,1)
	i += 1
	while(grid.check_converged()==False):
		print('iteration='+str(i))

		#uncommet for viewing update values tag:A
		# print("State\t\tDV\tSV\tRV\tU\tVal")
		grid.update_util()
		it.update_utils(grid,1)
		i+=1
	pass