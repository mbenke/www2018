from jinja2 import Template, FileSystemLoader, Environment, select_autoescape

loader = FileSystemLoader('./templates')
env = Environment(loader=loader, autoescape=select_autoescape(['html', 'xml']))

hello = env.get_template('hello.html')
print(hello.render(name='<foo&bar>'))
