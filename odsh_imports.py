import cffi

ffi = cffi.FFI()
ffi.cdef('''
void * oneshell_engine_create();
void oneshell_engine_destroy(void *eng);
void * oneshell_engine_clone(void *eng);
void * oneshell_block_load(const char *ast);
void oneshell_block_destroy(void *blk);
int oneshell_engine_eval_block(void *eng, void *blk);
''')

lib = ffi.dlopen("liboneshell.so")
