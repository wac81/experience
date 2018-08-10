[This code's documentation lives on the grpc.io site.](https://grpc.io/docs/quickstart/python.html)
python -m grpc_tools.protoc -I./ --python_out=. --grpc_python_out=. ./hello.proto