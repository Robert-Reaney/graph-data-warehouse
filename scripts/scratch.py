data = NeoData("neo4j:/localhost")
result = data.test_ubo('161690')
result

netx = data.cypher_to_netx(result)
cyto = data.netx_to_dash(netx)

netx.nodes.values()
dir(netx)
list(result.nodes)


list(netx.nodes.data())

node = nx.readwrite.json_graph.cytoscape_data(netx)['elements']['nodes'][0]

{'data': 
 {'id': node['data']['properties']['id'], 
  'label': node['properties']['name'], 
  'classes': ' '.join([x.lower() for x in node['data']['labels']])
  }
}

[{'data': {'id': '161690', 'label': 'L3Harris Surveillance Solutions', 'classes': 'company'}}, {'data': {'id': 'NaEqr4QTS4J3Jjo4Rud4uw', 'label': 'EXELIS INC.', 'classes': 'entity'}}, {'data': {'id': 'dGASOn691mmM-RwoLkc7Ng', 'label': 'Flynn Ryan F.', 'classes': 'entity'}}, 
 
 {'data': {'type': 'IS_MATCH', 'properties': {}, 'source': '161690', 'target': 'NaEqr4QTS4J3Jjo4Rud4uw', 'key': 0}}
 
 , {'data': {'type': 'HAS_UBO', 'properties': {}, 'source': 'NaEqr4QTS4J3Jjo4Rud4uw', 'target': 'dGASOn691mmM-RwoLkc7Ng', 'key': 0}}]

[{'data': {'id': '161690', 'label': 'L3Harris Surveillance Solutions'}, 'classes': 'company'}, 
 {'data': {'id': 'NaEqr4QTS4J3Jjo4Rud4uw', 'label': 'EXELIS INC.'}, 'classes': 'entity'},
   {'data': {'id': 'dGASOn691mmM-RwoLkc7Ng', 'label': 'Flynn Ryan F.'}, 'classes': 'entity'}, 
   
   {'data': {'source': '161690', 'target': 'NaEqr4QTS4J3Jjo4Rud4uw', 'label': 'IS_MATCH'}}, {'data': {'source': 'NaEqr4QTS4J3Jjo4Rud4uw', 'target': 'dGASOn691mmM-RwoLkc7Ng', 'label': 'HAS_UBO'}}]