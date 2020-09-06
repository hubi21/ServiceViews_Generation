# ServiceViews_Generation
Implementation of our solution to automatically generate services' views given their description (we only consider I/O parameters). The generated views are expressed as conjunctive queries over the relations in the local data source schema. The first step relies on the matching results computed by COMA++ between the schema of the local data source and the input/output parameters of the data service. Using the matching obtained in the first step, the second step automatically creates a node/edge-weighted graph, depicting the schema of the local data source such that the weights of the nodes represent an aggregated matching score on the node attributes. Then, we study finding the top-k minimum cost connected trees that contain all service parameters at least once in the graph. We do so by exploring Steiner trees.

Our main aim is to find the top-k Steiner trees interconnecting service parameters (defined within the schema graph' nodes). The weight associated to each node reflects the score by which a node is too far to match the data service parameters: the smaller the score, the higher the probability that the corresponding node Vi is relevant for the service view description.

We implement a dynamic programming solution by taking the heights, h, of trees as stages, and find the top-k Steiner trees by expanding the trees with height h=0,1,2, . . . ,H until k optimal trees are found. 

Given a schema graph GS, a set of service parameters’ matchings Vi and a set of service operation matchings Vop, our code outputs the top-k minimum cost
connected trees that contain all the nodes.
