create tweet graph
```
LET likesEdgeDefinition = {
  "collection": "likes",
  "from": ["users"],
  "to": ["tweets"]
}

LET wroteEdgeDefinition = {
  "collection": "wrote",
  "from": ["users"],
  "to": ["tweets"]
}

LET fanOutEdgeDefinition = {
  "collection": "cache",
  "from": ["users"],
  "to": ["tweets"]
}

LET followsEdgeDefinition = {
  "collection": "follows",
  "from": ["users"],
  "to": ["users"]
}

INSERT {
  "_key": "TwitterGraph",
  "edgeDefinitions": [likesEdgeDefinition, wroteEdgeDefinition, fanOutEdgeDefinition, followsEdgeDefinition]
} INTO _graphs
```

add indexes for performance
```
db.follows.ensureIndex({ type: "hash", fields: ["_from", "_to"] });
```
```
db.wrote.ensureIndex({ type: "hash", fields: ["_from", "_to"] });
```

delete collection
```
db._useDatabase('twitter2'); const collections = db._collections(); collections.forEach(function(collection) {
  try {
    collection.truncate();
  } catch (err) {
    console.error('Failed to truncate collection', collection.name());
  }
});
```