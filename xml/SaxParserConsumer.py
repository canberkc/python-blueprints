from lxml import etree
from . import SaxParserUtil


def main():
    template_folder = 'taxonoomy_source/file_location/'
    rend_folder = template_folder + 'table_name-rend.xml'

    parser = etree.XMLParser(target=SaxParserUtil.EchoTarget())
    result = etree.parse(rend_folder, parser)
    print(result)


if __name__ == "__main__":
    main()
