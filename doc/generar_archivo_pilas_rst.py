# -*- encoding: utf-8 -*-
# Genera el contenido del archivo pilas.rst que describe
# toda la api de pilas y se agrega al manual como anexo.

import os


content = [
"Referencia del módulo Pilas",
"===========================",
"",
"Aquí encontrarás la documentación técnica del toda la biblioteca",
"pilas, puedes usar esta sección para profundizar tus conocimientos",
"o simplemente como referencia ante cualquier duda.",
"",
"",
".. automodule:: pilas",
"    :members:",
"",
"",
]



for x in os.walk("../pilas"):

    for filename in x[2]:
        if filename.endswith(".py") and not filename.startswith("__"):
            fullname = x[0] + '/' + filename[:-3]
            
            fullname = fullname.replace("../", "")
            fullname = fullname.replace("/", ".")

            if "test" not in fullname and "__" not in fullname and "rope" not in fullname:
                title = "Módulo " + fullname
                content.append(title)
                content.append("-" * (len(title) - 1))

                content.append("")
                content.append(".. automodule:: " + fullname)
                content.append("    :members:")
                content.append("")
                content.append("")



print "Actualizando el archivo 'source/pilas.rst'"
archivo = open("source/pilas.rst", "wt")
archivo.write("\n".join(content))
archivo.close()
