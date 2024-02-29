class FilterModule(object):

    def filters(self):
        return { "codify": self.do_codify }

    def do_codify(self, content, endline='\n'):
        return '[code]<pre>' + content.replace(endline,'<br>') + '</pre>[/code]'