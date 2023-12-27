import xml.etree.ElementTree as ET

def xml_to_insert_statements(xml_file):
    # Parsear el archivo XML
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Obtener el nombre de la tabla
    table_name = root.tag

    # Lista para almacenar las sentencias INSERT
    insert_statements = []

    # Iterar sobre los elementos 'fila' bajo la etiqueta 'registros'
    for fila_element in root.find('.//registros').findall('fila'):
        # Construir la sentencia INSERT
        columns_list = []
        values_list = []

        for campo_element in fila_element:
            campo_name = campo_element.tag
            campo_value = campo_element.text

            # Obtener el tipo de dato del campo
            campo_type = root.find(f".//estructura/campo[@name='{campo_name}']").attrib['type']

            # Determinar si agregar comillas o no
            if campo_type.lower() in ['nvarchar','date', 'datetime' ,'nchar', 'varchar', 'char', 'text']:
                campo_value = f"'{campo_value}'"

            columns_list.append(campo_name)
            values_list.append(campo_value)

        columns_str = ', '.join(columns_list)
        values_str = ', '.join(values_list)

        insert_statement = f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str});"
        insert_statements.append(insert_statement)

    return insert_statements