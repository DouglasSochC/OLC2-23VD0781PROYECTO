class BaseDatosWrapper:
    def __init__(self, valor):
        self.valor = valor

# Para realizar el analisis
from Parser.parser import parse

# Utilidades
from Parser.tablas.tabla_simbolo import TablaDeSimbolos
from Parser.abstract.retorno import RetornoError

ts_global = TablaDeSimbolos()
base_datos = BaseDatosWrapper("bd1")
instrucciones = parse(
'''
DECLARE @texto_corto NCHAR(1);
DECLARE @texto_largo NVARCHAR(5);
DECLARE @decimal_num DECIMAL;
DECLARE @binario BIT;
DECLARE @bin INT;
DECLARE @num INT;
SET @binario = 1;
SET @bin = 1;
SET @texto_corto = "a";
SET @texto_largo = "abcde";
SET @decimal_num = 1.0;
SET @num = 87;
DECLARE @new_texto_corto_int INT;
DECLARE @new_texto_largo_int INT;
DECLARE @new_decimal_num_int INT;
DECLARE @new_num_decimal DECIMAL;
DECLARE @new_binario_int INT;
DECLARE @new_bin_bit BIT;
DECLARE @new_num_nvarchar NVARCHAR(5);
DECLARE @new_num_nchar NCHAR(5);
SET @new_texto_corto_int = CAST(@texto_corto AS INT);
SET @new_texto_largo_int = CAST(@texto_largo AS INT);
SET @new_decimal_num_int = CAST(@decimal_num AS INT);
SET @new_num_decimal = CAST(@num AS DECIMAL);
SET @new_binario_int = CAST(@binario AS INT);
SET @new_bin_bit = CAST(@bin AS BIT);
SET @new_num_nvarchar = CAST(@num AS NVARCHAR(5));
SET @new_num_nchar = CAST(@num AS NCHAR(5));

''')

# Se revisa que se haya obtenido una instrucciones
if instrucciones is not None:

    if isinstance(instrucciones, str):
        print("SALIDA STRING: {}".format(instrucciones))
    else:
        for instr in instrucciones:
            res = instr.Ejecutar(base_datos, ts_global)
            print("ERROR: {}".format(res.msg) if isinstance(res, RetornoError) else res.msg)
