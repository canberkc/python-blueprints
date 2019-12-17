from lxml import etree


class EchoTarget(object):

    def __init__(self):
        self.isProcess = False
        self.rule_node_map = {}

    def start(self, tag, attrib):
        if self.isProcess:
            name = etree.QName(tag).localname
            if name == 'ruleNode':
                rule_node = RuleNode(attrib)
                self.rule_node_map.update({rule_node.node_id: rule_node})

        if etree.QName(tag).localname == 'link':
            self.isProcess = True

    def end(self, tag):
        if etree.QName(tag).localname == 'link':
            self.isProcess = False

    def data(self, data):
        if self.isProcess:
            pass

    def comment(self, text):
        if self.isProcess:
            print("comment %s" % text)

    def close(self):
        print("close")
        for e in self.rule_node_map:
            print(e)

        return "closed!"


class RuleNode:
    def __init__(self, attrib):
        for a in attrib:
            if etree.QName(a).localname == 'id':
                self.node_id = attrib[a]
            if etree.QName(a).localname == 'type':
                self.node_type = attrib[a]
            if etree.QName(a).localname == 'label':
                self.label = attrib[a]
