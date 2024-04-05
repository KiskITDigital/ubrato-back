apply_migration() {
  local json_file=$1
  echo "Applying migration from $json_file"
  curl -X POST \
    -H "Content-Type: application/json" \
    -H "X-TYPESENSE-API-KEY: ${TYPESENS_API_KEY}" \
    -d "@$json_file" \
    "http://localhost:8108/collections"
}

for file in ./*.json; do
  apply_migration "$file"
done
