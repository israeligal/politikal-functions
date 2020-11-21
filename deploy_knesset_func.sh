
PROJECT_PATH=/Users/galisr/myprojects/politikal-server/politikal-functions
cd "$PROJECT_PATH" || exit

rm func.zip

cd "$PROJECT_PATH"/venv/lib/python3.6/site-packages || exit

# replace lxml with precompiled lxml, zip and bring back original lxml
mv lxml ..

cp -R "$PROJECT_PATH"/precompiled_lxml/ ./lxml

zip -r9 "$PROJECT_PATH"/func.zip .

rm -r lxml

mv ../lxml .

cd "$PROJECT_PATH"/knesset_search || exit

zip -r9 "$PROJECT_PATH"/func.zip .

cd "$PROJECT_PATH" || exit

aws lambda update-function-code --function-name knesset-search --zip-file fileb://func.zip  --profile politikal
