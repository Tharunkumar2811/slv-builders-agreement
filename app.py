from flask import Flask, render_template, request, send_file
from docxtpl import DocxTemplate
from datetime import datetime
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


# ADD STEP 3 HERE
@app.route("/generate", methods=["POST"])
def generate():

    client_name = request.form["client_name"]
    property_address = request.form["property_address"]

    sqft = float(request.form["sqft"])
    floors = int(request.form["floors"])
    rate = float(request.form["rate"])

    total_area = sqft * floors
    total_cost = total_area * rate
    agreement_date = datetime.now().strftime("%d %B %Y")

    template_path = os.path.join(
    os.path.dirname(__file__),
    "agreement_template.docx"
)

    doc = DocxTemplate(template_path)

    floor_cost = sqft * rate

    context = {
    "CLIENT_NAME": client_name,
    "PROPERTY_ADDRESS": property_address,
    "RATE": f"{rate:,.0f}",
    "SQFT_PER_FLOOR": f"{sqft:,.0f}",
    "TOTAL_AREA": f"{total_area:,.0f}",
    "TOTAL_COST": f"{total_cost:,.0f}",
    "FLOORS": floors,
    "AGREEMENT_DATE": agreement_date,
    "FLOOR_COST": f"{floor_cost:,.0f}"
    }
    

    doc.render(context)

    output_dir = os.path.join(
    os.path.dirname(__file__),
    "output"
)

    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(
    output_dir,
    f"Construction_Agreement_{client_name}.docx"
)

    doc.save(output_file)

    return send_file(
        output_file,
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )