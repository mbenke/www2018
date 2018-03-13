from jinja2 import Template, FileSystemLoader, Environment, select_autoescape

loader = FileSystemLoader('./templates')
env = Environment(loader=loader, autoescape=select_autoescape(['html', 'xml']))

child = env.get_template('child.html')
print(child.render(name='<foo&bar>'))
