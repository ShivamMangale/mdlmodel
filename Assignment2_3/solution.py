import os
import numpy 
import cvxpy
import json

cpy=cvxpy
npy=numpy

x = cpy.Variable(4*60)
A = npy.zeros(shape=(4*60,60))
R = npy.zeros(4*60)
alpha = npy.zeros(60)
alpha[60-1] = 1 #START POSITION FOR LERO
constraints = [x >= 0]
impossible = []
policy = []
ac_d='DODGE'
ac_r='RECHARGE'
ac_s='SHOOT'
ac_t='NOOP'

def update_shoot(h,arrow,s):
	mul=(12*h+3*arrow+s)
	if h*s*arrow==0:
		constraints.append(x[4*mul]==0)
		impossible.append(4*mul)
	else:
		A[4*mul][mul]=1
		A[4*mul][(h*12)+((arrow-1)*3)+(s-1)]=-0.5
		A[4*mul][((h-1)*12)+((arrow-1)*3)+(s-1)]=-0.5

def update_dodge(h,arrow,s):
	mul=4*(12*h+3*arrow+s)+1
	if s*h== 0:
		constraints.append(x[mul]==0)
		impossible.append(mul)
	elif s==1:
		if arrow>=3:
			A[mul][(h*12)+(arrow*3)+(s-1)]=-1
			A[mul][(h*12)+(arrow*3)+s]=1			
		else:
			A[mul][(h*12)+(arrow*3)+(s-1)] = -0.2
			A[mul][(h*12)+(arrow*3)+s] = 1
			A[mul][(h*12)+((arrow+1)*3)+(s-1)] = -0.8
	else:
		if arrow>=3:
			A[mul][(h*12)+(arrow*3)+(s-2)] = -0.2
			A[mul][(h*12)+(arrow*3)+(s-1)] = -0.8
			A[mul][(h*12)+(arrow*3)+s] = 1			
		else:
			#A[(h*48)+(arrow*12)+(s*4)+1][(h*12)+(arrow*3)+(s-2)] = -0.04
			A[(h*48)+(arrow*12)+(s*4)+1][(h*12)+(arrow*3)+(s-2)] = -0.04
			A[mul][(h*12)+(arrow*3)+(s-1)] = -0.16
			A[mul][(h*12)+(arrow*3)+s] = 1
			A[mul][(h*12)+((arrow+1)*3)+(s-2)] = -0.16
			A[mul][(h*12)+((arrow+1)*3)+(s-1)] = -0.64
			
def update_recharge(h,arrow,s):
	mul=4*(12*h+3*arrow+s)+2
	if h==0:
		constraints.append(x[mul]==0)
		impossible.append(mul)
	elif s==2:
		constraints.append(x[mul]==0)
		impossible.append(mul)
	else:
		A[mul][(h*12)+(arrow*3)+(s+1)]=-0.8
		A[mul][(h*12)+(arrow*3)+s]=0.8	

def update_term(h,arrow,s):
	mul=4*(12*h+3*arrow+s)+3
	if h==0:
		A[mul][(h*12)+(arrow*3)+s] = 1
	else:
		constraints.append(x[mul] == 0)
		impossible.append(mul)	

def solve():
	constraints.append(A.T@x == alpha)
	objective = cpy.Maximize(x@R.T)
	problem = cpy.Problem(objective, constraints)
	problem.solve()
	return problem

def get_arrays():
	for h in range(0,5):
		for arrow in range(0,4):
			for s in range(0,3):
				for act in range(0,4):
					if act == 0:#SHOOT
						update_shoot(h,arrow,s)
					elif act == 1:
						update_dodge(h,arrow,s)
					elif act == 2:
						update_recharge(h,arrow,s)
					else:
						update_term(h,arrow,s)

def create_policy(x):
	for h in range(0,5):
		for arrow in range(0,4):
			for s in range(0,3):
				pos = []
				curr = 4
				curr *= (12*h+3*arrow+s)
				pos.append([h,arrow, s])
				if h>0:
					if s==0:
						pos.append(ac_r)#RECHARGE
					elif s==2:
						if x[curr] < x[curr+2]:
							pos.append(ac_d)#DODGE
						else:
							pos.append(ac_s)#SHOOT
					elif arrow==0:
						if s==2 or x[curr+1]>=x[curr+2] :
							pos.append(ac_d)#DODGE
						else:
							pos.append(ac_r)#RECHARGE
					else:
						if x[curr+1] <= x[curr] and x[curr+2] <= x[curr]:
							pos.append(ac_s)#SHOOT
						elif x[curr] <+ x[curr+1] and x[curr+2] <+ x[curr+1]:
							pos.append(ac_d)
						else:
							pos.append(ac_r)
				else:
					pos.append(ac_t)#TERMINAL
				policy.append(pos)
	print(policy)
	return policy

for i in range(48, 240):
	R[i]=-20

pol = [] #FORPOLICYCREATION
A_mod = []
R_mod = []
x_mod = []

get_arrays()
problem = solve()
	
for i in range(4*60):
	pol.append(x[i].value)
	if i not in impossible:
		R_mod.append(R[i])
		A_mod.append(list(A[i]))
		x_mod.append(x[i].value)

policy = create_policy(pol)
final={
	"a":list(A_mod),
	"r":list(R_mod),
	"alpha":list(alpha),
	"x":list(x_mod),
	"policy":policy,
	"objective":problem.value
}

if not os.path.exists("outputs"):
    os.mkdir("outputs")
file="outputs/output.json"
f = open(file,'w')
json.dump(final,f)

