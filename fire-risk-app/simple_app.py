from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    # Provide dummy values for testing
    month = "2025-05"
    readable_month = "May 2025"
    pred_map_url = "https://via.placeholder.com/800x600?text=Predicted+Map"
    true_map_url = "https://via.placeholder.com/800x600?text=True+Map"

    if request.method == "POST":
        selected_month = request.form.get("month")
        if selected_month:
            month = selected_month
            # Dummy transformation: e.g., 2025-05 → "May 2025"
            year, month_num = selected_month.split("-")
            readable_month = f"{month_name(int(month_num))} {year}"

    return render_template(
        "index.html",
        month=month,
        readable_month=readable_month,
        pred_map_url=pred_map_url,
        true_map_url=true_map_url
    )

# Helper for month name
def month_name(num):
    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    return months[num - 1]

if __name__ == "__main__":
    app.run(debug=True)