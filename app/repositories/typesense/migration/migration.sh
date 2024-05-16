apply_migration() {
  local json_file=$1
  printf "Applying migration from $json_file\n"
  curl -X POST \
    -H "Content-Type: application/json" \
    -H "X-TYPESENSE-API-KEY: ${TYPESENSE_API_KEY}" \
    -d "@$json_file" \
    "http://${TYPESENSE_HOST}:8108/collections"
  printf "\n____________________________________________________________\n"
}

ls *.json | sort -n | while read -r file; do
  apply_migration "$file"
done

cd data && TYPESENSE_HOST=${TYPESENSE_HOST} TYPESENSE_API_KEY=${TYPESENSE_API_KEY} sh ./migration.sh
