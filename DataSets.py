import networkx as nx

###An example of a schema graph::: (the same in the paper)
G=nx.DiGraph()
G.add_node('Book',pos=(0,0))
G.node['Book']['id'] = '0'
G.node['Book']['title'] = '1'
G.node['Book']['isbn13'] = '1'
G.node['Book']['isbn10'] = '1'
G.node['Book']['topic'] = '0'
G.node['Book']['seller'] = '0'
G.node['Book']['author'] = '0'
G.node['Book']['publisher'] = '0'
G.node['Book']['publication_date'] = '0'
G.node['Book']['price'] = '1'
G.node['Book']['available_quantity'] = '1'
G.add_node('Person',pos=(0,1))
G.node['Person']['id'] = '0'
G.node['Person']['name'] = '1'
G.node['Person']['birth_date'] = '0'
G.node['Person']['profession'] = '0'
G.node['Person']['email'] = '0'
G.node['Person']['nationality'] = '0'
G.node['Person']['spouse'] = '0'
G.add_node('Author',pos=(1,0))
G.node['Author']['id'] = '0'
G.node['Author']['genre'] = '0'
G.add_node('Actor',pos=(1,1))
G.node['Actor']['id'] = '0'
G.node['Actor']['genre'] = '0'
G.add_node('Conference',pos=(0,2))
G.node['Conference']['id'] = '0'
G.node['Conference']['name'] = '0'
G.node['Conference']['location'] = '0'
G.node['Conference']['start_date'] = '0'
G.node['Conference']['end_date'] = '0'
G.add_node('Publisher',pos=(2,0))
G.node['Publisher']['id'] = '0'
G.node['Publisher']['country'] = '0'
G.node['Publisher']['founder'] = '0'
G.node['Publisher']['publication_types'] = '0'
G.node['Publisher']['country'] = '0'
G.node['Publisher']['foundation_date'] = '0'
G.add_node('Researcher',pos=(1,2))
G.node['Researcher']['id'] = '0'
G.node['Researcher']['email'] = '0'
G.add_node('Award',pos=(2,1))
G.node['Award']['id'] = '0'
G.node['Award']['name'] = '0'
G.add_node('Movie',pos=(0,3))
G.node['Movie']['id'] = '0'
G.node['Movie']['title'] = '0'
G.node['Movie']['director'] = '0'
G.node['Movie']['genre'] = '0'
G.node['Movie']['rating'] = '0'
G.node['Movie']['budget'] = '0'
G.node['Movie']['nomination'] = '0'
G.node['Movie']['release_date'] = '0'
G.node['Movie']['box_office'] = '0'
G.node['Movie']['country'] = '0'
G.add_node('Seller',pos=(3,1))
G.node['Seller']['id'] = '0'
G.node['Seller']['name'] = '1'
G.node['Seller']['country'] = '1'
G.node['Seller']['rating'] = '1'
G.node['Seller']['phone'] = '0'
G.node['Seller']['description'] = '0'

G.add_weighted_edges_from([('Book','Movie',1)])
G.add_weighted_edges_from([('Book','Seller',1)])
G.add_weighted_edges_from([('Movie','Seller',1)])
G.add_weighted_edges_from([('Book','Award',1)])
G.add_weighted_edges_from([('Book','Publisher',1)])
G.add_weighted_edges_from([('Book','Author',1)])
G.add_weighted_edges_from([('Person','Publisher',1)])
G.add_weighted_edges_from([('Award','Conference',1)])
G.add_weighted_edges_from([('Award','Movie',1)])
G.add_weighted_edges_from([('Award','Author',1)])
G.add_weighted_edges_from([('Person','Author',1)])
G.add_weighted_edges_from([('Person','Researcher',1)])
G.add_weighted_edges_from([('Movie','Actor',1)])
G.add_weighted_edges_from([('Person','Actor',1)])
G.add_weighted_edges_from([('Author','Researcher',1)])
G.add_weighted_edges_from([('Movie','Book',1)])
G.add_weighted_edges_from([('Seller','Book',1)])
G.add_weighted_edges_from([('Seller','Movie',1)])
G.add_weighted_edges_from([('Movie','Award',1)])
G.add_weighted_edges_from([('Award','Book',1)])
G.add_weighted_edges_from([('Publisher','Book',1)])
G.add_weighted_edges_from([('Author','Book',1)])
G.add_weighted_edges_from([('Publisher','Person',1)])
G.add_weighted_edges_from([('Conference','Award',1)])
G.add_weighted_edges_from([('Author','Award',1)])
G.add_weighted_edges_from([('Author','Person',1)])
G.add_weighted_edges_from([('Researcher','Person',1)])
G.add_weighted_edges_from([('Actor','Movie',1)])
G.add_weighted_edges_from([('Researcher','Author',1)])
G.add_weighted_edges_from([('Actor','Person',1)])

###define a relation label on the edges between different nodes in order to be able to express the relationship in the conjunctive query
attrs = {('Book','Movie'): {'label': 'made_into'},('Movie','Book'): {'label': 'based_on'},('Book','Seller'): {'label': 'available in'},('Movie','Seller'): {'label': 'available in'},('Seller','Book'): {'label': 'have'},('Seller','Movie'): {'label': 'have'},('Author','Book'): {'label': 'wrote'},('Book','Author'): {'label': 'written_by'},('Book','Publisher'): {'label': 'published_by'},('Publisher','Book'): {'label': 'published'},('Person','Author'): {'label': 'works_as'},('Person','Actor'): {'label': 'works_as'},('Person','Publisher'): {'label': 'works_as'},('Actor','Person'): {'label': 'is'},('Actor','Movie'): {'label': 'starred_in'},('Movie','Actor'): {'label': 'actors'},('Author','Person'): {'label': 'is'},('Author','Researcher'): {'label': 'is also'},('Author','Award'): {'label': 'got'},('Person','Researcher'): {'label': 'is'},('Publisher','Person'): {'label': 'is'},('Book','Award'): {'label': 'got'}}
nx.set_edge_attributes(G, attrs)


### Nodes representing a service opertaion example
Vop=[]
for node in G.nodes():
	if node=='Author' or node=='Book':
		Vop.append(node)
###The set of parameters we're looking for
parameters=list()
parameters.append('title')
parameters.append('isbn10')
parameters.append('isbn13')
parameters.append('name')
parameters.append('available_quantity')
parameters.append('price')
parameters.append('seller')
parameters.append('author')
parameters.append('publisher')
parameters.append('country')
parameters.append('rating')
#### the list of join relations::
joinR={}
joinR[('Book','Publisher')]=('publisher','id')
joinR[('Book','Seller')]=('seller','id')
joinR[('Book','Author')]=('author','id')
joinR[('Publisher','Person')]=('id','id')
joinR[('Author','Person')]=('id','id')
joinR[('Researcher','Person')]=('id','id')
joinR[('Actor','Person')]=('id','id')
joinR[('Publisher','Book')]=('id','publisher')
joinR[('Seller','Book')]=('id','seller')
joinR[('Author','Book')]=('id','author')
joinR[('Person','Publisher',)]=('id','id')
joinR[('Person','Author')]=('id','id')
joinR[('Person','Researcher')]=('id','id')
joinR[('Person','Actor')]=('id','id')

nodes=G.nodes(data=True)