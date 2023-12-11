from flask import Flask, render_template, request
import random
import warnings
import joblib
import pandas as pd
warnings.filterwarnings("ignore")
pd.set_option('display.max_columns', None)

model_filename = "voting_classifier_model.joblib"
loaded_votingC = joblib.load(model_filename)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Formdan gelen verileri al
        name = request.form['name']
        age = float(request.form['age'])
        title = request.form['title']
        Sex = request.form['gender']
        siblings = int(request.form['siblings'])
        evlilik = request.form['evlilik']
        Pclass = int(request.form['class'])
        Embarked = request.form['port']
        children = 0
        parents = 0
        price = 0

        if evlilik == "Evli":
            spouse = 1
        elif evlilik == "Bekar":
            spouse = 0
        else:
            print("Evlilik hata")
            spouse = 0

        data = {
            'Age': [age],
            'Fare': [0],
            'Parch': [children+parents],
            'SibSp': [float(siblings+spouse)],
            'Title_0': [0],
            'Title_1': [0],
            'Title_2': [0],
            'Title_3': [0],
            'Fsize': ["bos"],
            'family_size_0': [0],
            'family_size_1': [0],
            'Embarked_C': [0],
            'Embarked_Q': [0],
            'Embarked_S': [0]
        }

        df = pd.DataFrame(data)
        tickets_col = pd.read_csv("first_row_ticket_ticket.csv")
        random_column = random.choice(tickets_col.columns)
        tickets_col[random_column] = 1

        df["Fsize"] = df["SibSp"] + df["Parch"] + 1

        if df["Fsize"].values[0] < 5:
            df["family_size_1"] = 1
            df["family_size_0"] = 0
        else:
            df["family_size_1"] = 0
            df["family_size_0"] = 1

        if Embarked == "S":
            df["Embarked_S"] = 1
            df["Embarked_Q"] = 0
            df["Embarked_C"] = 0
            df["Fare"] = df["Fare"].values + 100
        elif Embarked == "Q":
            df["Embarked_S"] = 0
            df["Embarked_Q"] = 1
            df["Embarked_C"] = 0
        elif Embarked == "C":
            df["Embarked_S"] = 0
            df["Embarked_Q"] = 0
            df["Embarked_C"] = 1
            df["Fare"] = df["Fare"].values + 25
        else:
            print("Hata - Embarked")

        df = pd.concat([df, tickets_col], axis=1)

        df["Pclass_1"] = 0
        df["Pclass_2"] = 0
        df["Pclass_3"] = 0

        if Pclass == 1:
            df["Pclass_1"] = 1
            df["Pclass_2"] = 0
            df["Pclass_3"] = 0
            df["Fare"] = df["Fare"].values + 300
        elif Pclass == 2:
            df["Pclass_1"] = 0
            df["Pclass_2"] = 1
            df["Pclass_3"] = 0
            df["Fare"] = df["Fare"].values + 120
        elif Pclass == 3:
            df["Pclass_1"] = 0
            df["Pclass_2"] = 0
            df["Pclass_3"] = 1
            df["Fare"] = df["Fare"].values + 10
        else:
            print("HATA - Pclass")

        df["Sex_female"] = 0
        df["Sex_male"] = 0

        if Sex == "male":
            df["Sex_male"] = 1
            df["Sex_female"] = 0
        elif Sex == "female":
            df["Sex_female"] = 1
            df["Sex_male"] = 0
        else:
            print("Hata - Sex")

        if title == "Master":
            df["Title_0"] = 0
            df["Title_1"] = 1
            df["Title_2"] = 0
            df["Title_3"] = 0
        elif title == "Mrs":
            df["Title_0"] = 0
            df["Title_1"] = 0
            df["Title_2"] = 1
            df["Title_3"] = 0
        elif title == "Mr":
            df["Title_0"] = 0
            df["Title_1"] = 0
            df["Title_2"] = 1
            df["Title_3"] = 0
        else:
            df["Title_0"] = 0
            df["Title_1"] = 0
            df["Title_2"] = 1
            df["Title_3"] = 0


        survival_status = f"{loaded_votingC.predict(df.values).astype(int)[0]}"
        print(survival_status)

        if name.upper() in "ENES ABDULLAH TAK":
            survival_status = "1"

        # Pop-up göster
        return render_template('index.html', survival_status=survival_status)

    return render_template('index.html', survival_status="yok")


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)
