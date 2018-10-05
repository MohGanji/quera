from bs4 import BeautifulSoup

class HTMLParser:
    def __init__(self, html_doc):
        self.html_doc = html_doc
        self.soup = BeautifulSoup(html_doc, 'html.parser')
        pass

    def set_html_doc(self, html_doc):
        self.html_doc = html_doc
        self.soup = BeautifulSoup(self.html_doc, 'html.parser')

    def find_first(self, output_arg, **finding_args):
        pass

    def find_all(self, n, output_arg, **finding_args):
        # id = finding_args.get('id')
        string = finding_args['string']
        name = finding_args['name']
        res = self.soup.find_all(name, string, finding_args)
        print(res)
        res = [tag.get('id') if tag.get('id') else '' for tag in res]
        return res if len(res) < n else res[:n]

    def find_parent(self, output_arg, **finding_args):
        pass

    def find_grandparent(self, n, output_arg, **finding_args):
        pass

    def remove_comment(self, **finding_args):
        pass

    def remove_all_comments(self):
        pass

    def remove_tag(self, **finding_args):
        pass

parser = HTMLParser("<a id='link'>some text</a>")
doc = '<b id="1">first</b> <b id="2">second</b> <b>third</b>'
parser.set_html_doc(doc)
print(parser.find_all(5, "id", name='b', string="second"))