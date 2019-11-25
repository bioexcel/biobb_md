#Usage: . ./template_render.sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
parent_dir="$(dirname $DIR)"
REPOSITORY="$(dirname $parent_dir)"
#read -p "Repository absolute path : " REPOSITORY
echo $REPOSITORY
repo_name=$(basename $REPOSITORY)
echo $repo_name
read -p "Version number ie 0.1.2 : " version
sed "s/{{version}}/${version}/g" $REPOSITORY/$repo_name/docs/README_template.md > $REPOSITORY/$repo_name/docs/source/readme.md
read -p "Version name ie 'April 2019 Release' : " v_name
sed -i "s/{{v_name}}/${v_name}/g" $REPOSITORY/$repo_name/docs/source/readme.md

cp $REPOSITORY/$repo_name/docs/source/readme.md $REPOSITORY/README.md
