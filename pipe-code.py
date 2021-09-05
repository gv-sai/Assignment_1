# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 00:17:37 2010

@author: pc

"""

 

#%%
f=open("pipe_instructions_2",'r') # didnot work for file name= instructions2
inst=f.readlines()

for x in range(0,len(inst)):
    
    inst[x]=inst[x].split()
    inst[x]+=inst[x].pop().strip().split(',')
    
print(inst)


#%%
#inst=[['load', 'r1', 'm1'], ['load', 'r2', 'm2'], ['add', 'r3', 'r1', 'r2'], ['mul', 'r3', 'r1', 'r2'], ['store', 'm1', 'r1']]
# inst has been read from the file 
rw=dict()
rw['load']=[3,4,4]
rw['store']=[1,3,2]    #wrt clockvlaue os stage 1 and now wrt stage
rw['add']=[1,4,3]
rw['sub']=[1,4,3]
rw['mul']=[1,4,3]
rw['jnz']=[1,-1,2]
rw['bne']=[1,-1,2] # as the branch result is known in s3.
print(rw)
c=1
k=0
s=0
p=0

problems=list()

#%%

def read(start_cycle,reads):
    global k
    
    
    if ic<1 :
        problems.insert(ic,[[-1,-1]])  
        return
    for i in range(ic-1,-1,-1):
        if i<0 or c-o[i][0]>4 :
            break
    
        if o[i][2] in list(reads) and i>=0 :
            k=o[i][3]
            problems.insert(ic,[[k,i]])
            return
        #i=i-1
       
        
            
    problems.insert(ic,[[-1,-1]])     
 
#%%
def write(start_cycle,writes) :
    global p
    global s
    if ic<1:
       problems[ic].append([-1,-1])
       problems[ic].append([-1,-1])
       return
    #i=ic-1
    #s=list(o[i])[0]
   # start_cycle-=s      recently commented
    r=-1
    ri=-1
    w=-1
    wi=-1
    for i in range(ic-1,-1,-1) : #and i>=0 
        if i<0 or c-o[i][0]>4:
            break
        if writes in list(o[i][5]) and o[i][6]>r:
            r=o[i][6]
            ri=i
             
        if o[i][2]== writes and o[i][4]>w:
            w=o[i][4]
            wi=i
        #i=i-1
    p=w+1
    s=r+1 
    problems[ic].append([r,ri])
    problems[ic].append([w,wi])
  
  
  #%%
o=list()
d=list()
ip=0;# instruction pointer
ic=0;

while (ip<len(inst)):
    k=0
    s=0
    p=0
    d=inst[ip]
    if d[0] in ['bne','jnz']:
        
        if d[0]=='bne':
            d.insert(1,[d.pop(1),d.pop(1)])
        m=c+rw.get(d[0])[0]
        read(c,d[1])
        problems[ic].append([-1,-1])
        problems[ic].append([-1,-1])
         
        max=0
        if m<k :
            max=k-m
            problems[ic].append(0)
        problems[ic].append(max)
        c+=max
        o.insert(ic,[c,d[0],-1,rw.get(d[0])[2]+c,-1,d[1],m+max])
        c+=rw.get(d[0])[2]
        
        ic+=1
        ip=int(d[2])
    else :
        if d[0] in ['add','mul','sub']:
            d.append([d.pop(2),d.pop(2)])
        m=c+rw.get(d[0])[0]
        w=c+rw.get(d[0])[1] 
    
        read(c,d[2])
        write(c,d[1])
   
        dum=list() # temporary vraiables
        max=0
        dum.append(k-m)
        dum.append(s-w)
        dum.append(p-w)
        if dum[1]>dum[0] and dum[1]>dum[2]:
           max=1
        elif dum[2]>dum[0]:
            max=2
        if dum[max]< 0 :
            dum[max]=0
   
        problems[ic].append(max)
        max=dum[max]    
    
     
        c+=max
        o.insert(ic,[c,d[0],d[1],rw.get(d[0])[2]+c,w+max,d[2],m+max])
        problems[ic].append(max)
        c+=1
  
        ic+=1
        ip+=1
        
        
        
    
    
    
    
    
    #%%
   # print_output()
   
    
    
   
#%%
 # def print_output():
 #   print("cycle\topcode\twrites\twrite_available_from\twrites_at\treads\treads_at\tno_of_stalls\toperand_forwarding_from")
       
