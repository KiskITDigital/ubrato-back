curl "http://${TYPESENSE_HOST}:8108/collections/region_index/documents/import?action=create" \
-H "X-TYPESENSE-API-KEY: ${TYPESENSE_API_KEY}" \
-H "Content-Type: text/plain" \
-X POST \
--data-binary @region.jsonl
printf "\n____________________________________________________________\n"

curl -X POST \
-H "Content-Type: application/json" \
-H "X-TYPESENSE-API-KEY: ${TYPESENSE_API_KEY}" \
--data-binary @city.jsonl \
"http://${TYPESENSE_HOST}:8108/collections/city_index/documents/import?action=create"
printf "\n____________________________________________________________\n"

curl -X POST \
-H "Content-Type: application/json" \
-H "X-TYPESENSE-API-KEY: ${TYPESENSE_API_KEY}" \
--data-binary @object_group.jsonl \
"http://${TYPESENSE_HOST}:8108/collections/object_group_index/documents/import?action=create"
printf "\n____________________________________________________________\n"

curl -X POST \
-H "Content-Type: application/json" \
-H "X-TYPESENSE-API-KEY: ${TYPESENSE_API_KEY}" \
--data-binary @object_type.jsonl \
"http://${TYPESENSE_HOST}:8108/collections/object_type_index/documents/import?action=create"
printf "\n____________________________________________________________\n"

curl -X POST \
-H "Content-Type: application/json" \
-H "X-TYPESENSE-API-KEY: ${TYPESENSE_API_KEY}" \
--data-binary @service_group.jsonl \
"http://${TYPESENSE_HOST}:8108/collections/service_group_index/documents/import?action=create"
printf "\n____________________________________________________________\n"

curl -X POST \
-H "Content-Type: application/json" \
-H "X-TYPESENSE-API-KEY: ${TYPESENSE_API_KEY}" \
--data-binary @service_type.jsonl \
"http://${TYPESENSE_HOST}:8108/collections/service_type_index/documents/import?action=create"
printf "\n____________________________________________________________\n"
