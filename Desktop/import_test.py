import importlib, sys
sys.path.insert(0, 'C:/Programas/Inova Edu/Desktop')
try:
    importlib.import_module('views.Aluno_e_Professor.eventos')
    print('IMPORT_OK')
except Exception as e:
    print('IMPORT_FAIL', e)
