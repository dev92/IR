__author__ = 'Dev'


def setup_index(client):
    client.indices.delete(index=["ir-hw3"],ignore=404)
    client.indices.create(index="ir-hw3", body={
            "settings": {
                "index": {
                    "store": {
                        "type": "default"
                    },
                    "number_of_shards": 1,
                    "number_of_replicas": 0
                },
                "analysis": {
                    "analyzer": {
                        "my_english": {
                            "type": "english",
                            "stopwords_path": "stoplist.txt"
                        }
                    }

                }
            }
        })
    client.indices.put_mapping(index="ir-hw3",doc_type="documents",body={
  "documents": {
    "properties": {
      "clean_text": {
        "type": "string",
        "store": True,
        "index": "analyzed",
        "term_vector": "with_positions_offsets_payloads",
        "analyzer": "my_english"
      },
      "raw_html":{
        "type": "string",
        "store": True,
        "index": "no"
      },
      "outlinks":{
          "type":"string",
          "store":True,
          "index":"not_analyzed"
      },
      "inlinks":{
          "type":"string",
          "store":True,
          "index":"not_analyzed"
      }
    }
  }
})
    print "Index Setup"


def setup_commonindex(client):
    client.indices.create(index="basketball", body={
            "settings": {
                "index": {
                    "store": {
                        "type": "default"
                    },
                    "number_of_shards": 1,
                    "number_of_replicas": 0
                },
                "analysis": {
                    "analyzer": {
                        "my_english": {
                            "type": "english",
                            "stopwords_path": "stoplist.txt"
                        }
                    }

                }
            }
        })
    client.indices.put_mapping(index="basketball",doc_type="page",body={
  "page": {
    "properties": {
      "clean_text": {
        "type": "string",
        "store": True,
        "index": "analyzed",
        "term_vector": "with_positions_offsets_payloads",
        "analyzer": "my_english"
      },
      "raw_html":{
        "type": "string",
        "store": True,
        "index": "no"
      },
      "outlinks":{
          "type":"string",
          "store":True,
          "index":"not_analyzed"
      },
      "inlinks":{
          "type":"string",
          "store":True,
          "index":"not_analyzed"
      }
    }
  }
})
    print "Common Index Setup"


