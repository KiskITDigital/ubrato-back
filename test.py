import typesense

client = typesense.Client({
    'api_key': 'xyz',
    'nodes': [
        {
            'host': 'localhost',
            'port': '8108',
            'protocol': 'http'
        },
    ],
    'connection_timeout_seconds': 10
})

print(client.collections['tender_index'].documents.search({
    'q': 'уборка',
    'query_by': 'name',
}))
