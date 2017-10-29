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
    else:
        raise Exception("Unsupported node in root: " + node.kind)

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
