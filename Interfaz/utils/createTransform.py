import xml.etree.ElementTree as ET

def create_table_sql(xml_file):
    # Parsear el archivo XML
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Obtener el nombre de la tabla
    table_name = root.tag

    # Iniciar la instrucción CREATE TABLE
    create_table_statement = f"CREATE TABLE {table_name} (\n"

    # Iterar sobre los elementos 'campo' bajo la etiqueta 'estructura'
    for i, campo_element in enumerate(root.find('.//estructura').findall('campo')):
        campo_name = campo_element.attrib['name']
        campo_type = campo_element.attrib['type']
        campo_length = campo_element.attrib.get('length', '')
        campo_not_null = 'NOT NULL' if campo_element.attrib.get('not_null') is not None else ''
        campo_pk = 'PRIMARY KEY' if campo_element.attrib.get('pk') is not None else ''
        fk_table = campo_element.attrib.get('fk_table')
        fk_attribute = campo_element.attrib.get('fk_attribute')

        # Construir la parte de la columna en la instrucción CREATE TABLE
        column_definition = f"{campo_name} {campo_type}{f'({campo_length})' if campo_length else ''} {campo_not_null} {campo_pk}"

        # Agregar claves foráneas si existen
        if fk_table and fk_attribute:
            column_definition += f"REFERENCES {fk_table}({fk_attribute})"

        # Agregar coma si no es la última columna
        if i < len(root.find('.//estructura').findall('campo')) - 1:
            column_definition += ', '

        create_table_statement += '\t'+column_definition+'\n'

    # Agregar el cierre de paréntesis
    create_table_statement += '\n);\n'

    return create_table_statement