class FilterModule(object):

    def filters(self):
        return { 
            "codify": self.do_codify,
            "root_partitions": self.do_find_root_partitions
        }

    def do_codify(self, content, endline='\n'):
        return '[code]<pre>' + content.replace(endline,'<br>') + '</pre>[/code]'
    
    def do_find_root_partitions(self, devices):
        root_devs = []
        for dev in devices.keys():
            partitions = devices[dev].get('partitions', {})
            for part in partitions.keys():
                if 'root' in partitions[part].get('labels', []):
                    root_devs.append({"dev": dev, "part": part, "num": dev.replace(part, "")})
        return root_devs