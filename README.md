# 🌾 Smart Farmer — AI-Powered Crop Recommendation System

A supervised machine learning project that recommends the best crop to plant based on soil chemistry: **Nitrogen (N), Phosphorus (P), Potassium (K), and pH level**.

Combines **Python (scikit-learn)** for ML classification with **Prolog** for expert-system-style knowledge reasoning.

---

## 📁 Repository Structure

```
smart-farmer/
│
├── data/
│   └── crop_recommendation.csv       # Dataset (download from Kaggle)
│
├── models/
│   └── crop_model.pkl                # Saved trained model (auto-generated)
│
├── prolog/
│   └── crop_rules.pl                 # Prolog expert system rules
│
├── src/
│   ├── preprocess.py                 # Data loading and preprocessing
│   ├── train.py                      # Model training (Decision Tree + Random Forest)
│   ├── evaluate.py                   # Model evaluation and metrics
│   ├── predict.py                    # Predict crop from user input
│   └── visualize.py                  # Joint distributions and decision tree plots
│
├── notebooks/
│   └── smart_farmer_analysis.ipynb   # Full Jupyter walkthrough
│
├── requirements.txt                  # Python dependencies
└── README.md
```

---

## 🚀 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/smart-farmer.git
cd smart-farmer
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Download the Dataset
- Go to: https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset
- Download `Crop_recommendation.csv`
- Rename it to `crop_recommendation.csv` and place it inside the `data/` folder

### 4. Train the Model
```bash
python src/train.py
```

### 5. Evaluate the Model
```bash
python src/evaluate.py
```

### 6. Make a Prediction
```bash
python src/predict.py
```

### 7. Run Visualizations
```bash
python src/visualize.py
```

---

## 🧠 Prolog Expert System

Install SWI-Prolog from: https://www.swi-prolog.org/Download.html

Then run:
```bash
swipl prolog/crop_rules.pl
```

Inside the Prolog shell:
```prolog
?- recommend_crop(high, medium, high, neutral, Crop).
?- suitable_soil(rice, SoilType).
?- halt.
```

---

## 📊 Where to Test / Run the Code

| Platform | How |
|---|---|
| **Google Colab** | Upload the `.ipynb` notebook, upload the CSV — run everything free in browser |
| **Kaggle Notebooks** | Fork the dataset and write code directly on Kaggle |
| **VS Code (local)** | Install Python + extensions, run `.py` files from terminal |
| **Jupyter Notebook** | `pip install notebook`, then `jupyter notebook` |
| **SWI-Prolog** | For the Prolog expert system only |

---

## 📚 Course Concepts Demonstrated

| Concept | Where Used |
|---|---|
| Supervised Learning (CO4) | `train.py` — Decision Tree & Random Forest |
| Classification | Predicting crop labels from soil features |
| Joint Distributions (CO3) | `visualize.py` — pairplot and correlation heatmap |
| Decision Trees | `train.py` + `visualize.py` — tree structure exported |
| Expert Systems / Logic | `prolog/crop_rules.pl` |
| Model Evaluation | `evaluate.py` — accuracy, confusion matrix, classification report |

---

## 🌱 Crops Covered
Rice, Maize, Chickpea, Kidney Beans, Pigeon Peas, Moth Beans, Mung Bean, Blackgram, Lentil, Pomegranate, Banana, Mango, Grapes, Watermelon, Muskmelon, Apple, Orange, Papaya, Coconut, Cotton, Jute, Coffee
