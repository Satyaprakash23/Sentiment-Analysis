from flask import Flask,render_template,request
import joblib
import re

app=Flask(__name__)

def preprocess_text(text):

    text = str(text)

    # Remove 'READ MORE' if found
    text = text.replace('READ MORE', '')

    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)

    # Remove punctuation and special characters
    text = re.sub(r'[^\w\s]', '', text)

    text = re.sub(r':\)|:\(|:\D|:\S', '', text)

    # Convert text to lowercase
    text = text.lower()

    return text


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/prediction',methods=['get','post'])
def prediction():
    review_text=request.form.get("Review Text")
    text_clean= preprocess_text(review_text)

    loaded_model = joblib.load('model/best_model.pkl')

    prediction = loaded_model.predict([text_clean])
    sentiment = "Positive 😊" if prediction =='Positive' else "Negative ☹️" 
    return render_template("output.html",predictions=prediction,sentiment=sentiment)


if __name__=="__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)