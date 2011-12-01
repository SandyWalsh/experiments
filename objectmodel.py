import jinja2


def cmd(collection, verb, parameters, url, body):
    return dict(collection=collection, verb=verb, parameters=parameters,
                url=url, body=body)


def p(name):
    return dict(name=name)


CMDS = [
    cmd('servers', 'find', [p('uuid'),],
        'http://{{management_url}}/{{collection}}/{{verb}}',
        """
{
   "uuid": "{{uuid}}"
}
        """),

]


class VerbCallable(object):
    def __init__(self, connection, cmd):
        self.connection = connection
        self.cmd = cmd

    def __call__(self, *args):
       self.connection._execute(self.cmd, args)


class Connection(object):
    def __init__(self, auth_url):
        self.context = dict(auth_url=auth_url,
            management_url='192.168.1.100:8000',
            collection=None)

        self.cmds = CMDS

        self.collections = set()
        for cmd in self.cmds:
            self.collections.add(cmd['collection'])

    def __getattr__(self, name):
        # Have we already defined the collection?
        collection = self.context['collection']
        if collection:
            # Yes, find the verb ...
            for cmd in self.cmds:
                if cmd['verb'] == name:
                    return VerbCallable(self, cmd)
            raise Exception("Unknown method '%s' on '%s' collection" %
                (name, collection))

        if name in self.collections:
            self.context['collection'] = name
        else:
            raise Exception("Unknown collection '%s'" % name)

        return self

    def _execute(self, cmd, args):
        verb = cmd['verb']
        print "%s.%s(%s)" % (self.context['collection'],
                             verb, ",".join(args))

        params = cmd['parameters']
        if len(args) != len(params):
            raise Exception("Expected %d params, got %d" %
                            (len(params), len(args)))
        tuples = zip(params, args)
        for param, value in tuples:
            self.context[param['name']]=value

        self.context['verb'] = verb

        url_template = jinja2.Template(cmd['url'])
        url = url_template.render(self.context)
        body_template = jinja2.Template(cmd['body'])
        body = body_template.render(self.context)

        print "URL=", url
        print "BODY=", body


class Novaclient(object):
    def bind(self, auth_url):
        return Connection(auth_url)


if __name__=='__main__':
    c = Novaclient().bind("http://myauthurl.com:1234")
    c.servers.find('myuuid')
