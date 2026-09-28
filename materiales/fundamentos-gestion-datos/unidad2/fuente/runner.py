import ast, io, contextlib, pickle, sqlite3, os, shutil, sys
import pandas as pd
pd.set_option('display.width', 110); pd.set_option('display.max_columns', 20)
from snippets import S
def prep():
    shutil.copy('rutamarket.db', 'work.db')
    c = sqlite3.connect('rutamarket.db'); pd.read_sql_query('SELECT * FROM productos', c).to_csv('productos.csv', index=False); c.close()
def run_all(stop=None):
    prep()
    ns = {}; out = {}
    for k, code in S.items():
        code_exec = code.replace("'rutamarket.db'", "'work.db'")
        tree = ast.parse(code_exec); last = None
        if tree.body and isinstance(tree.body[-1], ast.Expr):
            last = ast.Expression(tree.body.pop().value)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            exec(compile(tree, k, 'exec'), ns)
            val = eval(compile(last, k, 'eval'), ns) if last else None
        out[k] = (buf.getvalue(), val)
        if k == stop: break
    return ns, out
if __name__ == '__main__':
    ns, out = run_all(sys.argv[1] if len(sys.argv) > 1 else None)
    for k, (txt, val) in out.items():
        print('=====', k); print(txt, end='')
        if val is not None: print(val)
    pickle.dump({k: (t, v) for k, (t, v) in out.items()}, open('outputs.pkl', 'wb'))
