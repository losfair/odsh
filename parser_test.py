import odsh_parser
import odsh_lib
import json

blk = odsh_parser.parse('''
ls /

''')

print(json.dumps(blk.build()))

exec_blk = odsh_lib.Block(blk.build())
engine = odsh_lib.Engine()

engine.eval_block(exec_blk)
