import openai
from flask import Flask, render_template, request
from dotenv import dotenv_values
import json

config = dotenv_values('.env');
openai.api_key = config["OPENAI_API_KEY"]


app = Flask(__name__,
    template_folder = "templates"            
)

def get_colors(msg):
    prompt = f"""
    You are a color pallette generating assistant that responds to text prompts for color palettes
    You should generate color palettes that fit the theme, mood, or instructions in the prompt.
    The palettes should be between 2 and 8 colors.
    
    Q : Convert the following verbal description of a color palette into a list of colors: The Mediterranean Sea
    A: ["#9AB2B2","#F2D7EE","#F28B9A","#B2DEA2","#7884B8","#E1D6E1","#EDE9BC"]
    
    Q : Convert the following verbal description of a color palette into a list of colors: sages, nature, earth
    A: ["#708D23", "#B8CD2D", "#F8F8F8", "#3F6E6B", "#737581"]
    
    Q: Convert the following verbal description of a color palette into a list of colors: ocean tones
    A: ["#4C5866", "#7395AE", "#A3CED1", "#5D8EA6", "#D4D0C8"]
    
    
    Desired Format : a JSON array of hexadecimal color codes (should be one line of  array format)
    
    Q: Convert the following verbal description of a color palette into a list of colors: {msg}
    A:
    """
    
    reponse = openai.Completion.create(
        prompt = prompt,
        model = "gpt-3.5-turbo-instruct",
        max_tokens=200,
        stop="11."
    )
    
    colors = json.loads(reponse["choices"][0]["text"])
    return colors
    
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/palette", methods=["POST"])
def prompt_to_palette():
    app.logger.info("HIT THE POST REQUEST ROUTE!!")
    query = request.form.get("query")
    colors = get_colors(query)
    return {"colors": colors}

if __name__ == "__main__":
    app.run(debug=True)