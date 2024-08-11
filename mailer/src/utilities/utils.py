from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def get_template_content(template_filename:str, context:dict) -> str: 
    base_path = Path(__file__).resolve().parent.parent / "templates/"
    jinja_env = Environment(loader=FileSystemLoader(base_path))
    template = jinja_env.get_template(template_filename)
    return template.render(context)