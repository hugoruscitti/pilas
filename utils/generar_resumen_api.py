# -*- encoding: utf-8 -*-
# Genera el contenido del archivo pilas.rst que describe
# toda la api de pilas y se agrega al manual como anexo.

import os
import re


content = []

for x in os.walk("../pilas"):

    for filename in x[2]:
        if filename.endswith(".py") and not filename.startswith("__"):
            fullname = x[0] + '/' + filename[:-3]
            
            fullname = fullname.replace("../", "")
            fullname = fullname.replace("/", ".")

            if "test" not in fullname and "__" not in fullname and "rope" not in fullname and "cargador" not in fullname:
                title = fullname
                content.append(title)
                content.append("-" * len(title))

                content.append("")
                content.append("")

                archivo = open(os.path.join(x[0], filename), "rt")

                contenido = archivo.readlines()

                for linea in contenido:
                    class_name = re.match("class (.+)\((\S*)\):", linea)

                    if class_name:
                        content.append("")
                        content.append("")
                        content.append("class **%s** (%s)" %(class_name.group(1), class_name.group(2)))
                        content.append("")

                    method = re.match("\s*def (.+)\((\S+)\):", linea)

                    if method:
                        argumentos = method.group(2).replace("*", "x")
                        argumentos = argumentos.replace("self", "")
                        content.append("- **%s** (%s)" %(method.group(1), argumentos))
                        
                        

                archivo.close()
                content.append("")



print('\n'.join(content))
print("Actualizando el archivo 'resumen_api.rst")
archivo = open("resumen_api.rst", "wt")
archivo.write("\n".join(content))
archivo.close()
