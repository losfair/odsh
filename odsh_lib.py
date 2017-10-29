import odsh_imports
import json

class Engine:
    def __init__(self, inst = None):
        if inst == None:
            self.inst = odsh_imports.lib.oneshell_engine_create()
        else:
            self.inst = inst

    def __del__(self):
        if self.inst != None:
            odsh_imports.lib.oneshell_engine_destroy(self.inst)
            self.inst = None

    def clone(self):
        return Engine(
            odsh_imports.lib.oneshell_engine_clone(
                self.inst
            )
        )

    def eval_block(self, blk):
        if not isinstance(blk, Block):
            raise Exception("An instance of Block is required")

        ret = odsh_imports.lib.oneshell_engine_eval_block(self.inst, blk.inst)
        return ret

class Block:
    def __init__(self, ast):
        self.inst = odsh_imports.lib.oneshell_block_load(
            json.dumps(ast).encode()
        )
        if self.inst == odsh_imports.ffi.NULL:
            self.inst = None
            raise Exception("Unable to load AST")

    def __del__(self):
        if self.inst != None:
            odsh_imports.lib.oneshell_block_destroy(self.inst)
            self.inst = None
