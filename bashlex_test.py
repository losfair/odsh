import bashlex
import json

parts = bashlex.parse('''
ls /
echo "Hello world!" && true
ls / | grep etc | true
ENV="aaa=b" exit
'''.strip())
for ast in parts:
    print(ast.kind)
    print(ast.parts)
