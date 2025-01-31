from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitlife.db'
db = SQLAlchemy(app)

# Modelo para armazenar informações do usuário
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    days_available = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.name}>'

# Rota principal (coleta de informações do usuário)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Coleta os dados do formulário
        name = request.form['name']
        age = request.form['age']
        days_available = request.form['days_available']

        # Cria um novo usuário no banco de dados
        new_user = User(name=name, age=age, days_available=days_available)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('workout', user_id=new_user.id))
        except Exception as e:
            return f'Houve um erro ao salvar os dados: {str(e)}'
    else:
        return render_template('index.html')

# Rota para exibir o treino gerado
@app.route('/workout/<int:user_id>')
def workout(user_id):
    user = User.query.get_or_404(user_id)
    
    # Lógica para gerar o treino com base nos dias disponíveis
    workout_plan = generate_workout(user.days_available)
    
    return render_template('workout.html', user=user, workout_plan=workout_plan)

# Função para gerar o treino (exemplo simples)
def generate_workout(days_available):
    # Exemplo de lógica para gerar treinos
    if days_available == 1:
        return ["Treino Full Body"]
    elif days_available == 2:
        return ["Treino A: Superior", "Treino B: Inferior"]
    elif days_available == 3:
        return ["Treino A: Peito e Tríceps", "Treino B: Costas e Bíceps", "Treino C: Pernas"]
    else:
        return ["Treino Personalizado com base nos dias disponíveis"]

# Cria o banco de dados e as tabelas (se não existirem)
with app.app_context():
    db.create_all()

# Executa o aplicativo
if __name__ == '__main__':
    app.run(debug=True)