from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, login_manager, logger
from models import User, Client, Professional, Procedure, Appointment
from datetime import datetime, timedelta

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        logger.debug(f"Tentativa de login para email: {email}")

        if not email or not password:
            flash('Por favor, preencha todos os campos')
            return render_template('login.html')

        user = User.query.filter_by(email=email).first()

        if user is None:
            logger.debug(f"Usuário não encontrado para email: {email}")
            flash('Email ou senha inválidos')
            return render_template('login.html')

        if not user.check_password(password):
            logger.debug(f"Senha inválida para email: {email}")
            flash('Email ou senha inválidos')
            return render_template('login.html')

        login_user(user)
        logger.info(f"Login bem-sucedido para usuário: {email}")
        return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    today = datetime.now().date()
    today_appointments = Appointment.query.filter(
        db.func.date(Appointment.date_time) == today
    ).count()

    total_clients = Client.query.count()
    total_professionals = Professional.query.count()
    total_procedures = Procedure.query.count()

    return render_template('dashboard.html',
                         today_appointments=today_appointments,
                         total_clients=total_clients,
                         total_professionals=total_professionals,
                         total_procedures=total_procedures)

# Rotas para Clientes
@app.route('/clients')
@login_required
def clients():
    clients = Client.query.all()
    return render_template('clients.html', clients=clients)

@app.route('/clients/add', methods=['POST'])
@login_required
def add_client():
    try:
        data = request.form
        if not all([data.get('name'), data.get('email'), data.get('phone'), data.get('cpf')]):
            flash('Todos os campos são obrigatórios', 'error')
            return redirect(url_for('clients'))

        # Verifica se já existe cliente com mesmo email ou CPF
        existing_client = Client.query.filter(
            (Client.email == data['email']) | (Client.cpf == data['cpf'])
        ).first()
        
        if existing_client:
            flash('Já existe um cliente com este email ou CPF', 'error')
            return redirect(url_for('clients'))

        client = Client(
            name=data['name'].strip(),
            email=data['email'].strip(),
            phone=data['phone'].strip(),
            cpf=data['cpf'].strip()
        )
        db.session.add(client)
        db.session.commit()
        flash('Cliente adicionado com sucesso!', 'success')
    except Exception as e:
        logger.error(f"Erro ao adicionar cliente: {str(e)}")
        db.session.rollback()
        flash('Erro ao adicionar cliente. Verifique se os dados estão corretos.', 'error')
    return redirect(url_for('clients'))

# API routes para buscar dados
@app.route('/api/clients/<int:id>')
@login_required
def get_client(id):
    client = Client.query.get_or_404(id)
    return jsonify({
        'name': client.name,
        'email': client.email,
        'phone': client.phone,
        'cpf': client.cpf
    })

@app.route('/api/professionals/<int:id>')
@login_required
def get_professional(id):
    professional = Professional.query.get_or_404(id)
    return jsonify({
        'name': professional.name,
        'specialty': professional.specialty,
        'professional_id': professional.professional_id,
        'email': professional.email,
        'phone': professional.phone
    })

@app.route('/api/procedures/<int:id>')
@login_required
def get_procedure(id):
    procedure = Procedure.query.get_or_404(id)
    return jsonify({
        'name': procedure.name,
        'description': procedure.description,
        'duration': procedure.duration,
        'price': procedure.price
    })

@app.route('/api/appointments/<int:id>')
@login_required
def get_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    return jsonify({
        'date_time': appointment.date_time.isoformat(),
        'client_id': appointment.client_id,
        'professional_id': appointment.professional_id,
        'procedure_id': appointment.procedure_id,
        'status': appointment.status
    })

# Rotas de edição
@app.route('/clients/<int:id>/edit', methods=['POST'])
@login_required
def edit_client(id):
    client = Client.query.get_or_404(id)
    try:
        if not all([request.form.get('name'), request.form.get('email'), 
                   request.form.get('phone'), request.form.get('cpf')]):
            raise ValueError("Todos os campos são obrigatórios")

        client.name = request.form['name']
        client.email = request.form['email']
        client.phone = request.form['phone']
        client.cpf = request.form['cpf']
        db.session.commit()
        flash('Cliente atualizado com sucesso!')
    except Exception as e:
        logger.error(f"Erro ao atualizar cliente: {str(e)}")
        db.session.rollback()
        flash('Erro ao atualizar cliente')
    return redirect(url_for('clients'))

@app.route('/professionals/<int:id>/edit', methods=['POST'])
@login_required
def edit_professional(id):
    professional = Professional.query.get_or_404(id)
    try:
        if not all([request.form.get('name'), request.form.get('specialty'),
                   request.form.get('email'), request.form.get('phone'),
                   request.form.get('professional_id')]):
            raise ValueError("Todos os campos são obrigatórios")

        professional.name = request.form['name']
        professional.specialty = request.form['specialty']
        professional.professional_id = request.form['professional_id']
        professional.email = request.form['email']
        professional.phone = request.form['phone']
        db.session.commit()
        flash('Profissional atualizado com sucesso!')
    except Exception as e:
        logger.error(f"Erro ao atualizar profissional: {str(e)}")
        db.session.rollback()
        flash('Erro ao atualizar profissional')
    return redirect(url_for('professionals'))

@app.route('/procedures/<int:id>/edit', methods=['POST'])
@login_required
def edit_procedure(id):
    procedure = Procedure.query.get_or_404(id)
    try:
        if not all([request.form.get('name'), request.form.get('description'), 
                   request.form.get('duration'), request.form.get('price')]):
            raise ValueError("Todos os campos são obrigatórios")

        procedure.name = request.form['name']
        procedure.description = request.form['description']
        procedure.duration = int(request.form['duration'])
        procedure.price = float(request.form['price'])
        db.session.commit()
        flash('Procedimento atualizado com sucesso!')
    except Exception as e:
        logger.error(f"Erro ao atualizar procedimento: {str(e)}")
        db.session.rollback()
        flash('Erro ao atualizar procedimento')
    return redirect(url_for('procedures'))

# Rotas de exclusão
@app.route('/clients/<int:id>/delete', methods=['POST'])
@login_required
def delete_client(id):
    client = Client.query.get_or_404(id)
    try:
        db.session.delete(client)
        db.session.commit()
        flash('Cliente excluído com sucesso!')
    except Exception as e:
        logger.error(f"Erro ao excluir cliente: {str(e)}")
        db.session.rollback()
        flash('Erro ao excluir cliente')
    return redirect(url_for('clients'))

@app.route('/professionals/<int:id>/delete', methods=['POST'])
@login_required
def delete_professional(id):
    professional = Professional.query.get_or_404(id)
    try:
        db.session.delete(professional)
        db.session.commit()
        flash('Profissional excluído com sucesso!')
    except Exception as e:
        logger.error(f"Erro ao excluir profissional: {str(e)}")
        db.session.rollback()
        flash('Erro ao excluir profissional')
    return redirect(url_for('professionals'))

@app.route('/procedures/<int:id>/delete', methods=['POST'])
@login_required
def delete_procedure(id):
    procedure = Procedure.query.get_or_404(id)
    try:
        db.session.delete(procedure)
        db.session.commit()
        flash('Procedimento excluído com sucesso!')
    except Exception as e:
        logger.error(f"Erro ao excluir procedimento: {str(e)}")
        db.session.rollback()
        flash('Erro ao excluir procedimento')
    return redirect(url_for('procedures'))

# Rotas para Profissionais
@app.route('/professionals')
@login_required
def professionals():
    professionals = Professional.query.all()
    return render_template('professionals.html', professionals=professionals)

@app.route('/professionals/add', methods=['POST'])
@login_required
def add_professional():
    try:
        data = request.form
        if not all([data.get('name'), data.get('specialty'), data.get('professional_id'), data.get('email'), data.get('phone')]):
            flash('Todos os campos são obrigatórios')
            return redirect(url_for('professionals'))
        professional = Professional(
            name=data['name'],
            specialty=data['specialty'],
            professional_id=data['professional_id'],
            email=data['email'],
            phone=data['phone']
        )
        db.session.add(professional)
        db.session.commit()
        flash('Profissional adicionado com sucesso!')
    except Exception as e:
        logger.error(f"Erro ao adicionar profissional: {str(e)}")
        db.session.rollback()
        flash('Erro ao adicionar profissional')
    return redirect(url_for('professionals'))

# Rotas para Procedimentos
@app.route('/procedures')
@login_required
def procedures():
    procedures = Procedure.query.all()
    return render_template('procedures.html', procedures=procedures)

@app.route('/procedures/add', methods=['POST'])
@login_required
def add_procedure():
    try:
        data = request.form
        if not all([data.get('name'), data.get('description'), data.get('duration'), data.get('price')]):
            flash('Todos os campos são obrigatórios')
            return redirect(url_for('procedures'))

        procedure = Procedure(
            name=data['name'],
            description=data['description'],
            duration=int(data['duration']),
            price=float(data['price'])
        )
        db.session.add(procedure)
        db.session.commit()
        flash('Procedimento adicionado com sucesso!')
    except Exception as e:
        logger.error(f"Erro ao adicionar procedimento: {str(e)}")
        db.session.rollback()
        flash('Erro ao adicionar procedimento')
    return redirect(url_for('procedures'))

# Rotas para Agendamentos
@app.route('/appointments')
@login_required
def appointments():
    appointments = Appointment.query.all()
    clients = Client.query.all()
    professionals = Professional.query.all()
    procedures = Procedure.query.all()
    return render_template('appointments.html',
                         appointments=appointments,
                         clients=clients,
                         professionals=professionals,
                         procedures=procedures)

@app.route('/appointments/<int:id>/edit', methods=['POST'])
@login_required
def edit_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    try:
        if not all([request.form.get('date'), request.form.get('time'), 
                   request.form.get('client_id'), request.form.get('professional_id'),
                   request.form.get('procedure_id'), request.form.get('status')]):
            raise ValueError("Todos os campos são obrigatórios")
            
        date_time = datetime.strptime(f"{request.form['date']} {request.form['time']}", '%Y-%m-%d %H:%M')
        
        # Verificar conflito de horário
        conflict = Appointment.query.filter(
            Appointment.professional_id == request.form['professional_id'],
            Appointment.date_time == date_time,
            Appointment.id != id
        ).first()
        
        if conflict:
            raise ValueError("Já existe um agendamento neste horário")
            
        appointment.date_time = date_time
        appointment.client_id = request.form['client_id']
        appointment.professional_id = request.form['professional_id']
        appointment.procedure_id = request.form['procedure_id']
        appointment.status = request.form['status']
        
        db.session.commit()
        flash('Agendamento atualizado com sucesso!')
    except Exception as e:
        logger.error(f"Erro ao atualizar agendamento: {str(e)}")
        db.session.rollback()
        flash('Erro ao atualizar agendamento')
    return redirect(url_for('appointments'))

@app.route('/appointments/<int:id>/delete', methods=['POST'])
@login_required
def delete_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    try:
        db.session.delete(appointment)
        db.session.commit()
        flash('Agendamento excluído com sucesso!')
    except Exception as e:
        logger.error(f"Erro ao excluir agendamento: {str(e)}")
        db.session.rollback()
        flash('Erro ao excluir agendamento')
    return redirect(url_for('appointments'))

@app.route('/appointments/add', methods=['POST'])
@login_required
def add_appointment():
    data = request.form
    try:
        if not all([data.get('date'), data.get('time'), data.get('client_id'), 
                   data.get('professional_id'), data.get('procedure_id')]):
            raise ValueError("Todos os campos são obrigatórios")
            
        date_time = datetime.strptime(f"{data['date']} {data['time']}", '%Y-%m-%d %H:%M')
        
        # Verificar se já existe agendamento no mesmo horário
        existing_appointment = Appointment.query.filter_by(
            date_time=date_time,
            professional_id=data['professional_id']
        ).first()
        
        if existing_appointment:
            raise ValueError("Já existe um agendamento neste horário")
            
        appointment = Appointment(
            date_time=date_time,
            client_id=data['client_id'],
            professional_id=data['professional_id'],
            procedure_id=data['procedure_id']
        )
        db.session.add(appointment)
        db.session.commit()
        flash('Agendamento realizado com sucesso!')
    except ValueError as e:
        logger.error(f"Erro de validação: {str(e)}")
        flash(str(e))
        db.session.rollback()
    except Exception as e:
        logger.error(f"Erro ao realizar agendamento: {str(e)}")
        db.session.rollback()
        flash('Erro ao realizar agendamento')
    return redirect(url_for('appointments'))