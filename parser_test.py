import odsh_parser
import odsh_lib
import json

blk = odsh_parser.parse('''
ls / && echo "OK"
ls /niwf3w4y3nxif4 || echo "Failed"
ls / | grep etc
''')

print(json.dumps(blk.build()))

exec_blk = odsh_lib.Block(blk.build())
engine = odsh_lib.Engine()

engine.eval_block(exec_blk)
