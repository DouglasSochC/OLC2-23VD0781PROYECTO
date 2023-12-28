import xml.etree.ElementTree as ET

def generate_create_procedure(xml_data):
    # Parsear el XML
    tree = ET.parse(xml_data)
    root = tree.getroot()

    # Obtener el nombre de la tabla
    proc_name = root.tag


    # Extraer información de la estructura
    structure = []
    for campo in root.find('estructura'):
        field_info = {
            'name': campo.get('name'),
            'type': campo.get('type'),
        }
        if campo.get('length'):
            field_info['length'] = campo.get('length')
        structure.append(field_info)

    # Extraer la query
    query = root.find('query').text.strip()

    # Comenzar la construcción del script
    script = f"CREATE PROCEDURE {proc_name}"

    # Agregar parámetros
    script += "(" + ', '.join([f"{field['name']} {field['type']}" + (f"({field['length']})" if 'length' in field else '') for field in structure]) + ")"

    # Agregar la declaración de la query
    script += "\nAS\nBEGIN\n"

    # Agregar el contenido de la query
    script += "\t" + query + "\n"

    # Finalizar el script
    script += "END;\n"

    return script