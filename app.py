from flask import Flask, request, render_template, send_file
import cv2
import os
import time
from main import load_model, detect_waste

app = Flask(__name__)
model = load_model()
os.makedirs("output", exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" in request.files:
            file = request.files["file"]
            if file.filename:
                timestamp = int(time.time())
                uploaded_filename = f"uploaded_image_{timestamp}.jpg"
                classified_filename = f"classified_output_{timestamp}.jpg"

                image_path = os.path.join("output", uploaded_filename)
                output_path = os.path.join("output", classified_filename)

                file.save(image_path)
                image = cv2.imread(image_path)

                if image is None:
                    return "Error: Invalid image", 400

                output_image, detection_count = detect_waste(image, model)

                if detection_count == 0:
                    return "No waste items detected. Try a different image.", 200

                cv2.imwrite(output_path, output_image)

                abs_output_path = os.path.abspath(output_path)
                return send_file(abs_output_path, mimetype="image/jpeg")
    return render_template("index.html")

@app.route("/webcam")
def webcam():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return "Error: Could not access webcam", 500

    print("[INFO] Starting webcam detection...")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        output_frame, _ = detect_waste(frame, model)
        cv2.imshow("Smart Waste Sorter - Webcam", output_frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return "Webcam session ended"

if __name__ == "__main__":
    app.run(debug=True)
