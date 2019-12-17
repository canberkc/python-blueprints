from xml.etree import ElementTree as ET
import json
import os


main_dict = {}
main_array = []

row_position_dic = {}
col_position_dic = {}


def start_process(file_path, result_path):
    problem_pages = []
    file_list = generate_file_list(file_path)

    for xml_file in file_list:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        blocks_array = []
        for child in root:
            if child.tag == 'blocks':
                handle_blocks(child, blocks_array, problem_pages, xml_file)
                text_form = json.dumps(blocks_array)
                write_to_file(result_path + '/' + change_file_name(xml_file), text_form)
                print(text_form)

    print(problem_pages)


def generate_file_list(path):
    os.chdir(path)
    file_list = os.listdir('.')
    return file_list


def handle_blocks(element, blocks_array, problem_pages, current_file):
    block_nr = 0
    for block in element:
        block_nr += 1
        block_dict = {}
        block_dict.update({'block': block_nr})
        block_dict.update({'id': block.attrib['id']})
        block_dict.update({'paging': block.attrib['paging']})
        block_dict.update({'x': block.attrib['x']})
        block_dict.update({'y': block.attrib['y']})
        block_dict.update({'caption': block.attrib['caption']})
        block_dict.update({'pages': []})
        block_dict.update({'filters': []})
        blocks_array.append(block_dict)
        handle_block(block, block_dict, problem_pages, current_file)


def handle_block(block_element, block_dict, problem_pages, current_file):
    for child in block_element:
        if child.tag == 'pages':
            handle_pages(child, block_dict)
        if child.tag == 'filters':
            handle_filters(child, block_dict)
        else:
            problem_pages.append(current_file)
            break


def handle_filters(element, block_dict):
    for child in element:
        filter_dict = {}
        filter_dict.update({'field': child.attrib['field']})
        filter_dict.update({'description': child.attrib['description']})
        filter_dict.update({'forceSelection': child.attrib['forceSelection']})
        block_dict['filters'].append(filter_dict)


def handle_pages(element, bl_dict):
    page_nr = 0
    for child in element:
        page_nr += 1
        page_dict = {}
        page_dict.update({'page_id': page_nr})
        page_dict.update({'allrows': child.attrib['allrows']})
        page_dict.update({'rows': child.attrib['rows']})
        page_dict.update({'allcols': child.attrib['allcols']})
        page_dict.update({'cols': child.attrib['cols']})
        bl_dict['pages'].append(page_dict)
        handle_page(child, page_dict)


def handle_page(item, p_dict):
    p_dict.update({'rows': []})
    p_dict.update({'cols': []})
    p_dict.update({'cells': []})
    for child in item:
        # print(child.tag, child.attrib)

        if child.tag == 'rows':
            handle_rows(child, p_dict['rows'])

        if child.tag == 'cols':
            handle_cols(child, p_dict['cols'])

        if child.tag == 'cells':
            handle_cells(child, p_dict['cells'])


def handle_cols(item, col_array):
    for child in item:
        c_dict = {}
        c_dict.update({'name': child.attrib['name']})
        c_dict.update({'width': child.attrib['width']})

        if 'official' in child.attrib:
            c_dict.update({'official': child.attrib['official']})

        c_dict.update({'pos': child.attrib['pos']})

        col_position_dic.update({child.attrib['name']: child.attrib['pos']})
        col_array.append(c_dict)


def handle_rows(item, row_array):
    for child in item:
        r_dict = {}
        r_dict.update({'name': child.attrib['name']})

        if 'height' in child.attrib:
            r_dict.update({'height': child.attrib['height']})

        if 'official' in child.attrib:
            r_dict.update({'official': child.attrib['official']})

        r_dict.update({'pos': child.attrib['pos']})

        row_position_dic.update({child.attrib['name']: child.attrib['pos']})
        row_array.append(r_dict)


def handle_cells(item, cell_array):
    for child in item:
        cell_dict = {}
        cell_dict.update({'style': {}})
        cell_dict.update({'rowname': child.attrib['rowname']})
        cell_dict.update({'colname': child.attrib['colname']})

        cell_dict.update({'rowpos': row_position_dic[child.attrib['rowname']]})
        cell_dict.update({'colpos': col_position_dic[child.attrib['colname']]})

        if 'backcolor' in child.attrib:
            cell_dict.update({'backcolor': child.attrib['backcolor']})

        if 'forecolor' in child.attrib:
            cell_dict.update({'forecolor': child.attrib['forecolor']})

        if 'halign' in child.attrib:
            cell_dict.update({'halign': child.attrib['halign']})
        if 'valign' in child.attrib:
            cell_dict.update({'valign': child.attrib['valign']})
        if 'type' in child.attrib:
            cell_dict.update({'type': child.attrib['type']})
        if 'format' in child.attrib:
            cell_dict.update({'format': child.attrib['format']})
        if 'rowspan' in child.attrib:
            cell_dict.update({'rowspan': child.attrib['rowspan']})
        if 'colspan' in child.attrib:
            cell_dict.update({'colspan': child.attrib['colspan']})

        cell_array.append(cell_dict)
        handle_style(child, cell_dict['style'])


def handle_style(item, style_dict):
    style_dict.update({'font': {}})
    style_dict.update({'border': []})
    for child in item:
        if child.tag == 'text':
            style_dict.update({'text': child.text})

        if child.tag == 'font':
            handle_font(child, style_dict['font'])

        if child.tag == 'border':
            handle_border(child, style_dict['border'])


def handle_border(item, border_array):
    border_dict = {}
    border_dict.update({'type': item.attrib['type']})

    if 'width' in item.attrib:
        border_dict.update({'width': item.attrib['width']})

    if 'style' in item.attrib:
        border_dict.update({'style': item.attrib['style']})

    border_array.append(border_dict)


def handle_font(item, font_dict):
    font_dict.update({'family': item.attrib['family']})
    font_dict.update({'size': item.attrib['size'] + 'px'})

    if 'bold' in item.attrib:
        font_dict.update({'bold': item.attrib['bold']})

    if 'italic' in item.attrib:
        font_dict.update({'italic': item.attrib['italic']})

    if 'underline' in item.attrib:
        font_dict.update({'underline': item.attrib['underline']})

    if 'strikethrough' in item.attrib:
        font_dict.update({'strikethrough': item.attrib['strikethrough']})


def change_file_name(file_name):
    new_name = file_name[:-4] + '.json'
    return new_name


def write_to_file(file_destination, content):
    with open(file_destination, 'w') as file:
        file.write(content)


def main():
    file_path = 'source_path'
    result_path = 'result_path'
    start_process(file_path, result_path)


if __name__ == "__main__":
    main()







