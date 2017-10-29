import odsh_ast
import bashlex

def parse(doc):
    lines = doc.strip().split('\n')
    for i in range(len(lines)):
        lines[i] = lines[i].strip()

    _lines = lines
    lines = []

    for line in _lines:
        if len(line) > 0:
            lines.append(line)

    parts = bashlex.parse('\n'.join(lines))
    blk = odsh_ast.Block()

    for ast in parts:
        transformer = Transformer(blk)
        transformer.transform_node(ast)

    return blk

class Transformer:
    def __init__(self, blk):
        self.blk = blk
            
    def transform_list(self, node):
        for child in node.parts:
            self.transform_node(child)

    def transform_compound(self, node):
        for child in node.list:
            self.transform_node(child)

    def transform_node(self, node):
        if node.kind == "command":
            self.blk.append_op(
                odsh_ast.ExecOperation(
                    self.transform_command(node)
                )
            )
        elif node.kind == "operator":
            if_blk = odsh_ast.Block() # 'if'
            else_blk = odsh_ast.Block() # 'else'
            target_blk = None

            ifelse_op = None

            if node.op == "&&":
                target_blk = else_blk
            elif node.op == "||":
                target_blk = if_blk
            else:
                raise Exception("Unsupported operation: " + node.op)

            self.blk.append_op(
                odsh_ast.IfElseOperation(
                    if_blk,
                    else_blk
                )
            )
            self.blk = target_blk
        elif node.kind == "list":
            self.transform_list(node)
        elif node.kind == "compound":
            self.transform_compound(node)
        elif node.kind == "reservedword":
            pass
        else:
            raise Exception("Unsupported node kind: " + node.kind)

    def transform_command(self, node):
        args = []
        envs = []

        for child in node.parts:
            if child.kind == "word":
                args.append(odsh_ast.StringSource(
                    "Plain",
                    child.word
                ))
            elif child.kind == "assignment":
                env_parts = child.word.split("=")
                env_key = env_parts.pop()
                env_value = '='.join(env_parts)

                envs.append(odsh_ast.EnvInfo(
                    StringSource("Plain", env_key),
                    StringSource("Plain", env_value)
                ))
            else:
                raise Exception("Unsupport node in command: " + child.kind)

        exec_info = odsh_ast.ExecInfo(
            command = args,
            env = envs
        )
        return exec_info
