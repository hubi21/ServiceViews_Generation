# ServiceViews_Generation
Implementation of our solution to automatically generate services' views given their description (we only consider I/O parameters). The generated views are expressed as conjunctive queries over the relations in the local data source schema. 

Given a schema graph Gs, a set of service parameters’ matchings Vi and a set of service operation matchings Vop, our code outputs the top-k minimum cost
connected trees that contain all the nodes.

We implement a dynamic programming solution by taking the heights, h, of trees as stages, and find the top-k Steiner trees by expanding the trees with height h=0,1,2, . . . ,H until k optimal trees are found. 


The main file is: Views_Specif.py

We consider the data source and the data service operation defined in the file datasets.py for the validation of our algorithm. The data source is represented using a node/edge-weighted graph, depicting the schema such that the weights of the nodes represent an aggregated matching score on the node attributes. The weight associated to each node reflects the score by which a node is too far to match the data service parameters: the smaller the score, the higher the probability that the corresponding node Vi is relevant for the service view description. Those matchings have been automatically computed by COMA++, a schema matching tool. Then, our algorithm study finding the top-k minimum cost connected trees that contain all service parameters at least once in the graph. We do so by exploring Steiner trees.
