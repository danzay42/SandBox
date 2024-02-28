```shell

# include response headers
curl -i https://example.com/

# verbose mod
curl -v https://example.com/

# set headers
curl https://example.com/ -H "MyHeader: val"
# remove headers
curl https://example.com/ -H "MyHeader:"

# authorization
curl -u login:pass https://example.com/

# send plain data
curl https://example.com/ -d "plain text"
# send data
curl https://example.com/ -d 'key=val'
# send json
curl https://example.com/ -d '{"key": "val"}'
# send file
curl https://example.com/ -d @file
# send file
curl https://example.com/ -T file

# forse use special method
curl -X METHOD https://example.com/

# tls ignore
curl -k https://example.com/

# compile specific curl command
curl https://example.com/ --libcurl code.c
gcc code.c -lcurl -o ./request

```