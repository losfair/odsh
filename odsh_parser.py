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
        transform_root(ast, blk)

    return blk

def transform_root(node, blk):
    if node.kind == "command":
        blk.append_op(
            odsh_ast.ExecOperation(
                transform_command(node)
            )
        )
    elif node.kind == "list":
        transform_list(node, blk)
    else:
        raise Exception("Unsupported node in root: " + node.kind)

def transform_list(node, blk):
    for child in node.parts:
        if child.kind == "command":
            blk.append_op(
                odsh_ast.ExecOperation(
                    transform_command(child)
                )
            )
        elif child.kind == "operator":
            if_blk = odsh_ast.Block() # 'if'
            else_blk = odsh_ast.Block() # 'else'
            target_blk = None

            ifelse_op = None

            if child.op == "&&":
                target_blk = else_blk
            elif child.op == "||":
                target_blk = if_blk
            else:
                raise Exception("Unsupported operation: " + child.op)

            blk.append_op(
                odsh_ast.IfElseOperation(
                    if_blk,
                    else_blk
                )
            )
            blk = target_blk

def transform_command(node):
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
