#coding: utf-8
#Python version 2.7
from DataSets import *
from networkx.algorithms import isomorphism
import pylab as plt
from Queue import *
import heapq
from networkx.drawing.nx_agraph import graphviz_layout, to_agraph
import copy

### Define the TREE Structure
class Tree:
    count=0
    def __init__(self,root=None,v0=None,structure=None,parameters=None,height=None,cost=None):
        Tree.count+=1
        self.v0=v0
        self.id= Tree.count
        self.root=root
        self.structure=structure
        self.height=height
        self.cost = cost
        self.parameters=parameters

def belong(T,Ts):
	##This method checks whether a tree T is included in Te
	belong=False
	for tree in Ts:
		if set(tree.structure)==set(T.structure) and tree.root==T.root:
			belong=True
	return belong


def Tree_merge(T1,T2):
	##This method merges two trees rooted at a given node Vop into a new tree
	exist=False
	G1=nx.DiGraph(T1.structure)
	G2=nx.DiGraph(T2.structure)
	Tm = nx.compose(G1,G2)
	for merge in merges:
		if merge.adjacency()==Tm.adjacency():
			exist=True
	if not exist:
		merges.append(Tm)        
		#print("we check here the merged tree::",Tm.adjacency(), Tm.edges(),"end checking")
	param=list()
	for node in Tm.nodes(data=True):
		##put all parameters in a list 
		for att in Tm.node[node[0]]:
			if att!='pos' and att!='w' and att not in param and att in parameters:
				param.append(att)
	###search for the max matching score for each parameter
	som=0
	for att in param:
		max=0
		for node in Tm.nodes(data=True):
			if att in node[1]:
				if node[1][att]>max:
					max=node[1][att]
		som=som+float(max)
	cost=0
	if param:
		cost=1-(som/len(param))
	T=Tree()
	T.structure =Tm.copy()
	if T1.height>T2.height:
		T.height=T1.height
	else:        
		T.height= T2.height
	T.cost=cost
	T.root=T1.root
	T.parameters=param
	q.put((T.cost,T.id))
	if not belong(T,trees):
		trees.append(T)
		qn.put((T.cost,T.id))
	return T

def Tree_grow(G,Te):
	##This method considers all the neighbors of a node u in Te and 
	#grow the tree if any new additional parameters can be brought after
	#the exploration

	##get the structure of the tree to grow "adjacency View"
	S1=Te.structure
	### define the list of leaves, also called 'end nodes'
	leafs=list()
	for el in S1:
		if not S1[el]:### if no outgoing edges exists --> end node
			leafs.append(el)
	for leaf in leafs:
		neighbors=list()
		for node in G.nodes(data=True):
			if node[0] in G.neighbors(leaf) and node[0] not in S1: #verify if node[0] is already contained in the initial tree T 
				Ten=list(Te.parameters)
				T=Tree(Te.root,Te.v0,Te.structure,Ten,Te.height,Te.cost)
				neighbors.append(node[0])
				### grow the tree with the node
				Treeg=nx.DiGraph(S1)
				## add node, its properties and the edge from leaf to the added new node
				Treeg.add_node(node[0])
				attrs = {}
				attrs[node[0]]= node[1]
				nx.set_node_attributes(Treeg,attrs)
				Treeg.add_weighted_edges_from([(leaf,node[0],G[leaf][node[0]]['weight'])])
				attrrs={(leaf,node[0]):{'label':G[leaf][node[0]]['label']}}
				nx.set_edge_attributes(Treeg, attrrs)         
				init=1-T.v0
				som=0
				###compute the matching score of the grown tree
				pt=list(T.parameters)
				for edge in Treeg.edges(data=True):
					p1,p=list(),list()
					### determine the set of parameters pi brought by navigating using the edge ei
					for att in G.node[edge[0]]:
						p1.append(att)
					for att in G.node[edge[1]]:
						if att not in p1:
							p.append(att)
						if att not in pt and att!='pos' and att!='w' and att in parameters:
							pt.append(att)
					if len(p)>0:
						som=som+(1-edge[2]['weight'])*len(p)		
				if pt:
					cost=1-((((1-T.v0)*len(T.parameters))+som)/len(pt))
				T.structure =Treeg
				T.height=T.height+1
				T.cost=cost
				T.root=node[0]
				T.v0=T.v0
				param=T.parameters
				for node in Treeg.nodes(data=True):
					for att in node[1]:
						if att!= 'w' and att!='pos' and att not in param:
							param.append(att)
				q.put((T.cost,T.id))
				if not belong(T,trees):
					trees.append(T)
					qn.put((T.cost,T.id))
	C=G.adjacency()
	return T

Cnodes=list()
merges=list()
for node in nodes:
	###The number of matching parameters in each node (the total number of attriutes except the attribute pos which defines the position of the node inthe graph representation)
	p=len(node[1])-1
	##Check if p contains already a match parameter or not, if it is the case, we proceed to compute the matching score, initialized to 0 when no parameter is considered
	if p != 0:
		match=0
		for att in node[1]:
			if att !='pos':
				if float(node[1][att])==1.0 and node[0] not in Cnodes:
					Cnodes.append(node[0])
				match+=float(node[1][att])
		weight=1-match/p ## This is the dual: we are considering a minimization problem while we are looking for the tree with the maximal matching score
	else:
		weight=1
	G.node[node[0]]['w'] = weight

### compute weights of edges e(u,v)
for edge in G.edges(data=True):
	inn=edge[0]##outgoing node
	out=edge[1]##ingoing node
	p1,p2=[],[]
	for node in G.nodes(data=True):
		## get the set of attributes of edge inn
		if node[0]==inn:
			for att in node[1]:
				p1.append(att)
		## get the set of attributes of edge out
		if node[0]==out:
			outnode=node
			for att in node[1]:
				p2.append(att)

		deff=[]
		if p2:
			for el in p2:
				if el not in p1:
					deff.append(el)
	if deff:
		matchd=0
		for att in deff:
			matchd+=float(outnode[1][att])
		we=1-matchd/len(deff)
		edge[2]['weight']=we

##H: the largest number of nodes which can be traversed to go from a given Vop to any node Vi
H=1
for vop in Vop:
	for vi in G.nodes():
		lg=nx.shortest_path_length(G,source=vop,target=vi)
		if lg > H:
			H=lg-1


### define a priority queue of steiner trees:  With a priority queue, the entries are kept sorted (using the heapq module) and the lowest valued entry is retrieved first. 
q = PriorityQueue()
qc = PriorityQueue()
####list of correponding trees 
trees=list()
## Enqueue: inserts a tree T(v,p,h) into q (a priority queue)
##intialization: T(v,p,0)=wv(v)
##for each node, we create a rooted tree with zero height
for node in G.nodes(data=True):
	##consider only nodes not included in Vop
	if node[1]['w']!=1:
		T=nx.DiGraph()
		#print("create a tree having noeud", node[0], "as a root")
		T.add_node(node[0])
		attrs = {}
		attrs[node[0]]= node[1]
		nx.set_node_attributes(T,attrs)   
		nx.draw(T, with_labels=True)
		filename=str(node[0])+'.png'
		plt.savefig(str(filename))
		tree=Tree()
		tree.root=node[0]
		tree.v0=G.node[node[0]]['w']
		tree.structure =T.copy()
		tree.height=0
		tree.cost=node[1]['w']
		param=list()
		for att in node[1]:
			if att!= 'w' and att!='pos':
				param.append(att)
		tree.parameters=param
		### add the tree to a queue 
		q.put((tree.cost,tree.id))
		qc.put((tree.cost,tree.id))   
		if not belong(tree,trees): 
			trees.append(tree)

### the queue containing non grown trees
qn=PriorityQueue()
i=1
while i< H+1:
	###get the tree with the higher matching score from the priority queue (which should be in the top of the queue)
	while not qc.empty():
		item=qc.get()## get the id of the tree with the higher matching score
		for tr in trees:
			if tr.id==item[1]:
				tree=copy.copy(tr)
		Tree_grow(G,tree)
	qc=copy.copy(qn)

	##****start merging trees****
	##construct a dictionnary with lists of trees having the same root
	root_trees={}
	for root in G.nodes():
		listN=list()
		root_trees[root]=listN		
		for tree in trees:
			if tree.root==root and tree.height>0:
				root_trees[root].append(tree)
	###merge the trees in a list
	import itertools
	combinations_trees=list()
	for list_root in root_trees.values():
		for L in range(2, len(list_root)+1):
			for subset in itertools.combinations(list_root, L):
				if list(subset) not in combinations_trees:
					combinations_trees.append(list(subset))
	for comb in combinations_trees:
		T1=comb[0]
		T2=comb[1]
		comb.remove(T1)
		comb.remove(T2)
		while comb:
			T1=Tree_merge(T1,T2)
			T2=comb[0]
			comb.remove(T2)
		Tree_merge(T1,T2)
	i+=1

#drawing the corresponding graph
plt.axis('off')
edge_labels=nx.draw_networkx_edge_labels(G,pos=nx.spring_layout(G)) 
nx.draw_networkx(G,with_labels=True,node_color='r',node_size=1000)
plt.savefig("schemagraph.png") # save as png
#plt.show() # display graph
print("====================================================================================")
print("=====================The top-k Steiner Trees are the following:=====================")
print("====================================================================================")
k=0
while not q.empty():
	item=q.get()
	for tree in trees:
		if tree.root in Vop and set(parameters).issubset(set(tree.parameters))and tree.id==item[1]:#and set(Cnodes).issubset(set(tree.structure.nodes())):
			k=k+1
			view=""
			i=1
			j=1
			print("\nTree n"+str(k)+" :\n")
			print("-Matching score:  "+str(round(1-tree.cost, 3)))
			print("-Root:  "+str(tree.root))
			print("-Parameters:  "+str(tree.parameters))
			
			###represent in the form of a conjunctive query Q(X) and enumerate constructing nodes
			for el in tree.structure:
				view=view+el+'(o'+str(i)+'),'
				for att in tree.structure.node[el]:
					##we only consider the attributes with non null matching value 
					if att!='pos' and att!='w' and tree.structure.node[el][att]!='0':
						view=view+att+'(o'+str(i)+',p'+str(j)+'),'
						j+=1
				i+=1
			for edge in tree.structure.edges():
				instances=[]
				label=tree.structure[edge[0]][edge[1]]['label']
				###find instances' names in the view
				nodens=[]
				nodens.append(edge[0])
				nodens.append(edge[1])
				relation0=joinR[(nodens[0],nodens[1])][0]
				relation1=joinR[(nodens[0],nodens[1])][1]
				for noden in nodens:
					p1=view.find(noden+'(')
					view1=view[p1::]
					p11=view1.find('(')
					view11=view1[p11+1::]
					p2=view11.find(')')
					viewf=view11[0:p2]
					p0=viewf.find(',')
					if p0==-1:
						instances.append(viewf)
				view=view+label+'('+instances[0]+','+instances[1]+'),'+relation0+'('+instances[0]+',p'+str(j)+'),'+relation1+'('+instances[1]+',p'+str(j+1)+')'
				j+=2
			print("-Service view:  "+str(view))	