from flask import Flask, render_template, jsonify
import pandas as pd

app = Flask(__name__)


PROBE_DATA = pd.read_csv('PROBE/subj1_series1_events.csv')
XGBOOST_DATA = pd.read_csv('XGBoost/subj_series9_events.csv')
LTSM_DATA = pd.read_csv('LTSM/subj_series9_events.csv')
CNN_DATA = pd.read_csv('CNN/subj_series9_events.csv')

# Выводим данные в консоль для проверки
print("PROBE_DATA:")
print(PROBE_DATA.head())  # Выводим первые несколько строк данных PROBE
print("\nXGBOOST_DATA:")
print(XGBOOST_DATA.head())  # Выводим первые несколько строк данных XGBOOST
print("\nLTSM_DATA:")
print(LTSM_DATA.head())  # Выводим первые несколько строк данных LTSM
print("\nCNN_DATA:")
print(CNN_DATA.head())  # Выводим первые несколько строк данных CNN

@app.route('/')
def index():
    # Отображение основной страницы
    return render_template('index.html')


@app.route('/data/<int:id_num>')
def get_data(id_num):
    # Получение данных по id_num и отправка их на клиент
    probe_event = PROBE_DATA.iloc[id_num].to_dict() if id_num < len(PROBE_DATA) else {}
    xgboost_event = XGBOOST_DATA.iloc[id_num].to_dict() if id_num < len(XGBOOST_DATA) else {}
    ltsm_event = LTSM_DATA.iloc[id_num].to_dict() if id_num < len(LTSM_DATA) else {}
    cnn_event = CNN_DATA.iloc[id_num].to_dict() if id_num < len(CNN_DATA) else {}

    return jsonify({
        'probe': probe_event,
        'xgboost': xgboost_event,
        'ltsm': ltsm_event,
        'cnn': cnn_event,
        'id_num': id_num
    })

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/get_data_by_time_frame')
def get_data_by_time_frame():
    time_frame = request.args.get('time_frame')

    # Получение данных для конкретного time frame
    probe_data = PROBE_DATA[PROBE_DATA['id'].str.contains(time_frame)].to_dict(orient='records')
    xgboost_data = XGBOOST_DATA[XGBOOST_DATA['id'].str.contains(time_frame)].to_dict(orient='records')
    ltsm_data = LTSM_DATA[LTSM_DATA['id'].str.contains(time_frame)].to_dict(orient='records')
    cnn_data = CNN_DATA[CNN_DATA['id'].str.contains(time_frame)].to_dict(orient='records')

    # Формирование ответа
    data = {
        'probe': probe_data,
        'xgboost': xgboost_data,
        'ltsm': ltsm_data,
        'cnn': cnn_data,
    }

    return jsonify(data)
