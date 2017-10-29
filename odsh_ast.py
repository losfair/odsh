class Block:
    def __init__(self):
        self.ops = []

    def build(self):
        ret = {
            "ops": []
        }
        for op in self.ops:
            ret["ops"].append(op.build())
        return ret

    def append_op(self, op):
        self.ops.append(op)

class ExecOperation:
    def __init__(self, info):
        self.info = info

    def build(self):
        return {
            "Exec": self.info.build()
        }

class ParallelExecOperation:
    def __init__(self, info):
        self.info = info

    def build(self):
        ret = {
            "ParallelExec": []
        }
        for item in self.info:
            ret["ParallelExec"].append(item.build())
        return ret

class IfElseOperation:
    def __init__(self, if_blk, else_blk):
        if (not isinstance(if_blk, Block)) or (not isinstance(else_blk, Block)):
            raise Exception("if_blk and else_blk must be of Block type")

        self.if_blk = if_blk
        self.else_blk = else_blk

    def build(self):
        return {
            "IfElse": [
                self.if_blk.build(),
                self.else_blk.build()
            ]
        }

class ExecInfo:
    def __init__(self, command = [], env = [], stdin = None, stdout = None):
        if len(command) == 0:
            raise Exception("Command must not be empty")

        for p in command:
            if not isinstance(p, StringSource):
                raise Exception("Command parts must be of StringSource type")

        for p in env:
            if not isinstance(p, EnvInfo):
                raise Exception("Env parts must be of EnvInfo type")

        self.command = command
        self.env = env
        self.stdin = StdioConfig.inherit() if stdin == None else stdin
        self.stdout = StdioConfig.inherit() if stdout == None else stdout

    def build(self):
        return {
            "command": list(map(lambda v: v.build(), self.command)),
            "env": self.env,
            "stdin": self.stdin.build(),
            "stdout": self.stdout.build()
        }

class EnvInfo:
    def __init__(self, key, value):
        if not isinstance(key, StringSource):
            raise Exception("Key must be a StringSource")

        if not isinstance(value, StringSource):
            raise Exception("Value must be a StringSource")

        self.key = key
        self.value = value

    def build(self):
        return {
            "key": self.key.build(),
            "value": self.value.build()
        }

class StringSource:
    def __init__(self, kind = "Plain", value = ""):
        if kind == "Plain":
            self.info = {
                "Plain": value
            }
        elif kind == "GlobalVariable":
            self.info = {
                "GlobalVariable": value
            }
        elif kind == "LocalVariable":
            self.info = {
                "LocalVariable": value
            }
        elif kind == "Join":
            self.info = {
                "Join": []
            }
            for item in value:
                self.info["Join"].append(item.build())
        else:
            raise Exception("Unknown StringSource kind: " + kind)

    def build(self):
        return self.info

class StdioConfig:
    def __init__(self, kind = "Inherit", pipe_name = None):
        if kind == "Inherit":
            self.info = "Inherit"
        elif kind == "Pipe":
            if pipe_name == None:
                raise Exception("pipe_name must not be None")

            self.info = {
                "Pipe": pipe_name
            }
        else:
            raise Exception("Unknown kind")

    def build(self):
        return self.info

    @staticmethod
    def inherit():
        return StdioConfig("Inherit")

    @staticmethod
    def pipe(name):
        return StdioConfig("Pipe", pipe_name = name)
