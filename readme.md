# 📊 Teams Attendance Pipeline

This project automates the processing of attendance reports exported from Microsoft Teams. It cleans the raw file, filters participants based on a minimum stay duration, and generates a consolidated final report.

## 📁 Project Structure

* `data/raw/`: Original CSV files exported from Teams.
* `data/processed/`: Intermediate files with the extracted participant section.
* `data/final/`: Final reports with Name and formatted Duration.
* `main.py`: Main script that executes the entire pipeline.
* `cleaning.py`: Initial extraction and cleaning logic.
* `filtrar_participantes.py`: Business rules and time filtering (>30min).

## 🚀 How to Run

1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`.
3. Install dependencies: `pip install -r requirements.txt`.
4. Place the exported Teams file in `data/raw/`.
5. Run the command:
    ```bash
    python main.py
    ```

## 🛠️ Technologies Used
* Python 3.x
* Pandas (Data processing)
* Regex (Time string handling)

## ⚖️ LGPD & Privacy
This project was designed not to version sensitive data. The `.gitignore` file is configured to ignore the `data/` folder, ensuring that participant names are not sent to the repository.