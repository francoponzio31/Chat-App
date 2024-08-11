from utilities.utils import get_template_content
from pathlib import Path


def render_template_to_file(template_filename: str, template_context: dict):
    rendered_content = get_template_content(template_filename, template_context)
    output_file = Path(__file__).resolve().parent.parent / "templates/template_test_output.html"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(rendered_content)
    
    print(f"Template saved in {output_file}")


if __name__ == "__main__":
    
    template_filename = "validate_signup.html"
    template_context = {
        "username": "username",
        "app_client_url": "client_url",
        "verification_token": "test_token"
    }
    render_template_to_file(template_filename, template_context)