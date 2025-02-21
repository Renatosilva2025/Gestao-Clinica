ProjetosII- PD Itabira

Clínica de estética prime LTDA Autores: Scárlath Eduarda, Lucas De Souza Martins, Renato de Almeida Silva, Ramon Godoi

Objetivos do projeto: Criar um sistema de login especificamente funcionários da clínica contendo: 
Nome do paciente. CPF Procedimentos Horários criação e logins de contas para pacientes 
Criar um sistema de login para pacientes recorrentes (feito por um funcionario) para poderem:
olhar horários vagos marcar horários tirar dúvidas com profissionais
Criação das páginas para: logins de contas horários e procedimentos


### Documentação Sistema de Clinica de Estetica Prime - Projetos II 


Este é um aplicativo web Flask para gerenciamento de uma clínica de estética Prime. 

Principais componentes:

Estrutura Principal:
app.py: Inicializa o aplicativo Flask, banco de dados e gerenciador de login
models.py: Define os modelos do banco de dados (Usuário, Cliente, Profissional, Procedimento, Agendamento)
routes.py: Contém todas as rotas para diferentes páginas/funcionalidades
main.py: Ponto de entrada que executa o servidor Flask
Funcionalidades Principais:
Autenticação de usuários com criação de usuário admin
Gerenciamento de clientes (adicionar/editar/excluir)
Gerenciamento de profissionais
Gerenciamento de procedimentos/serviços
Sistema de agendamentos
Painel com estatísticas
Banco de Dados:
Usa SQLAlchemy com banco SQLite
Modelos incluem relacionamentos entre agendamentos, clientes, profissionais e procedimentos
Autenticação:
Flask-Login para gerenciar sessões de usuário
Senhas são criptografadas para segurança
Usuário admin é criado automaticamente no início
Rotas:
/login: Autenticação de usuários
/dashboard: Visão geral e estatísticas
/clients, /professionals, /procedures: Operações CRUD
/appointments: Sistema de agendamentos
Endpoints API para obtenção de dados
O aplicativo vai rodaro na porta 5000 

autenticação

usuário: admin@prime.com
senha :@Admin123
