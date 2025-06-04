from vanna.flask import VannaFlaskApp
from data.vanna import vn

app = VannaFlaskApp(vn, 
    allow_llm_to_see_data=True, 
    csv_download=False,
    chart=False
)
app.run()