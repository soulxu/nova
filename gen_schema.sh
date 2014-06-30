# fetch schema for each version.
# In future we can support return jsonschema for each version

schemas_path="nova/api/openstack/compute/schemas/v3"
schemas_commits=`git log --grep="@schema" --oneline |cut -d " " -f 1`

for commit in $schemas_commits; do
  schema_note=`git show ${commit}|grep -m 1 @schema`
  extension=`echo $schema_note|cut -d : -f 2`
  version=`echo $schema_note|cut -d : -f 3|sed  "s/\./\_/"`
  schema_file="${schemas_path}/${extension}.py"
  git checkout $commit $schema_file
  cp $schema_file "${schemas_path}/${extension}_${version}.py"
  git checkout -f
done

