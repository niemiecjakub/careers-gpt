import os
import tempfile
import subprocess
from jinja2 import Environment, FileSystemLoader
from models import CvDocument

class LatexService:
    def __init__(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.output_path = os.path.normpath(os.path.join(self.dir_path, '..', 'resources', 'output'))
        os.makedirs(self.output_path, exist_ok=True)
        self.xelatex_render_command = ["xelatex", "-interaction=nonstopmode"]
    
    def generate_latex(self, template_name: str, cv: CvDocument) -> str:
        template_path = os.path.normpath(os.path.join(self.dir_path, '..', 'resources'))
        
        env = Environment(
            loader=FileSystemLoader(template_path),
            autoescape=False,
            comment_start_string="###"
        )

        template = env.get_template(f"{template_name}/cv_doc.jinja")     
        return template.render(**cv.model_dump())
        
       
    def render_pdf_file(self, rendered_tex: str, file_name: str) -> None:
        with tempfile.TemporaryDirectory() as tmpdirname:
            tex_path = os.path.join(tmpdirname, f"{file_name}.tex")
            with open(tex_path, "w", encoding="utf-8") as f:
                f.write(rendered_tex)

            render_command = self.xelatex_render_command + [f"{file_name}.tex"] 
            subprocess.run(render_command, cwd=tmpdirname, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            pdf_path = os.path.join(tmpdirname, f"{file_name}.pdf")
            with open(pdf_path, "rb") as f:
                pdf_data = f.read()

            output_pdf_path = os.path.join(self.output_path, f'{file_name}.pdf')
            with open(output_pdf_path, "wb") as f:
                f.write(pdf_data)

            print(f"PDF file generated successfully at {output_pdf_path}")
           
             
    def render_tex_file(self, rendered_tex: str, fileName: str) -> None:
        output_tex_path = os.path.normpath(os.path.join(self.output_path, f'{fileName}.tex'))
        with open(output_tex_path, "w", encoding="utf-8") as f:
            f.write(rendered_tex)
            
        print(f"LaTeX file rendered successfully at {output_tex_path}")
        