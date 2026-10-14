#CONFIGURAÇÃO DO BANCO

import sqlite3

conexao = sqlite3.connect("jobmatch.db")
cursor = conexao.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS candidatos (id INTEGER PRIMARY KEY AUTOINCREMENT,
nome TEXT NOT NULL, cargo TEXT NOT NULL, habilidades TEXT NOT NULL)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS vagas (id INTEGER PRIMARY KEY AUTOINCREMENT,
empresa TEXT NOT NULL, cargo TEXT NOT NULL, salario REAL NOT NULL, habilidades TEXT NOT NULL)""")

conexao.commit()

print("JOBMATCH")
print("Sistema de vagas")

#CARREGAMENTO DOS DADOS

candidatos = []

cursor.execute("SELECT nome, cargo, habilidades FROM candidatos")

for nome, cargo, habilidades in cursor.fetchall():
    candidatos.append({
        "nome": nome,
        "cargo": cargo,
        "habilidades": [h.strip() for h in habilidades.split(",")]})

vagas = []

cursor.execute("SELECT empresa, cargo, salario, habilidades FROM vagas")

for empresa, cargo, salario, habilidades in cursor.fetchall():
   vagas.append({
       "empresa": empresa,
       "cargo": cargo,
       "salario": salario,
       "habilidades": [h.strip() for h in habilidades.split(",")]})

#FUNÇÕES DO SISTEMA

def cadastrar_candidato():
    print("\nCadastro de candidato")

    while True:
        nome = input("Nome: ")
        if nome:
            break
        print("O nome não pode ficar vazio.")

    while True:
        cargo = input("Cargo desejado: ").strip()
        if cargo:
            break
        print("O cargo não pode ficar vazio.")

    while True:
        habilidades = input("Suas habilidades: ").lower().split(",")
        habilidades = [habilidade.strip() for habilidade in habilidades]
        habilidades = list(dict.fromkeys(habilidades))

        if all(habilidades):
            break
        print("Digite pelo menos uma habilidade.")

    cursor.execute("SELECT id FROM candidatos "
        "WHERE nome = ? AND cargo = ? AND habilidades = ?",
                   (nome, cargo, ",".join(habilidades)))

    if cursor.fetchone():
        print("\nEsse candidato já está cadastrado.")
        return


    candidato = {
        "nome": nome,
        "cargo": cargo,
        "habilidades": habilidades
    }
    habilidades_texto = ",".join(habilidades)

    cursor.execute(
        "SELECT id FROM candidatos WHERE nome = ? AND cargo = ? AND  habilidades = ?",
        (nome, cargo, habilidades_texto)
    )

    if cursor.fetchone():
        print("Esse candidato já está cadastrado.")
        return

    cursor.execute(
        "INSERT INTO candidatos (nome, cargo, habilidades) VALUES (?, ?, ?)",
        (nome, cargo, habilidades_texto)
    )
    conexao.commit()

    candidatos.append(candidato)
    print("Candidato cadastrado com sucesso!")

def cadastrar_vaga():
    print("\nCadastro de vaga")

    while True:
        empresa = input("Empresa: ").strip()
        if empresa:
            break
        print("O nome da empresa não pode ficar vazio.")

    while True:
        cargo = input("Cargo: ").strip()
        if cargo:
            break
        print("O cargo não pode ficar vazio.")

    while True:
        try:
            salario = float(input("Salário: ").strip().replace(",", "."))
            if salario > 0:
                break
            print("O salário deve ser maior que zero.")
        except ValueError:
            print("Digite um valor numérico válido.")


    while True:
        habilidades = input("Habilidades exigidas: ").lower().split(",")
        habilidades = [habilidade.strip() for habilidade in habilidades]
        habilidades = list(dict.fromkeys(habilidades))

        if all(habilidades):
           break
        print("Digite pelo menos uma habilidade.")

    cursor.execute(
        "SELECT id FROM vagas WHERE empresa = ? AND cargo = ? AND salario = ? AND habilidades = ?",
    (empresa, cargo, salario, ",".join(habilidades))
    )

    if cursor.fetchone():
        print("\nEssa vaga já está cadastrada.")
        return

    vaga = {
        "empresa" : empresa,
        "cargo" : cargo,
        "salario" : salario,
        "habilidades" : habilidades
    }
    vagas.append(vaga)
    print("\nVaga cadastrada com sucesso!")

    cursor.execute(
        "INSERT INTO vagas (empresa, cargo, salario, habilidades) "
        "VALUES (?, ?, ?, ?)",
        (empresa, cargo, salario, ",".join(habilidades))
    )

    conexao.commit()

def listar_vagas():
    print("\nVagas cadastradas!")

    if len(vagas) == 0:
        print("Nenhuma vaga cadastrada!")
        return

    for vaga in vagas:
        print(f"Empresa: {vaga['empresa']}")
        print(f"Cargo: {vaga['cargo']}")

        salario = f"{vaga['salario']:.2f}".replace(".", ",")
        print(f"Salario: {salario}")

        habilidades = ",".join(vaga["habilidades"])
        print(f"Habilidades: {habilidades.title()}")

        print("-" * 30)

def listar_candidatos():
    print("\nCandidatos cadastrados.")

    if len(candidatos) == 0:
        print("Nenhum candidato cadastrado.")
        return

    for candidato in candidatos:
        print(f"Nome: {candidato['nome']}")
        print(f"Cargo desejado: {candidato['cargo']}")

        habilidades = ",".join(candidato["habilidades"])
        print(f"Habilidades: {habilidades.title()}")

        print("-" * 30)


def calcular_match(habilidades_candidato, habilidades_vaga):
    correspondencias = 0

    for habilidade in habilidades_vaga:
        if habilidade in habilidades_candidato:
            correspondencias += 1

    if len(habilidades_vaga) == 0:
        return 0

    percentual = (correspondencias / len(habilidades_vaga)) * 100
    return percentual

def mostrar_match():
    if len(candidatos) == 0:
        print("\nNenhum candidato cadastrado.")
        return
    if len(vagas) == 0:
        print("\nNenhuma vaga cadastrada.")
        return

    print("\nEscolha o candidato")

    for i, candidato in enumerate(candidatos):
        print(f"{i + 1} - {candidato['nome']}")

    while True:
        try:
            escolha = int(input("Digite o número do candidato: "))
        except ValueError:
            print("Digite apenas um número.")
            continue

        if 1 <= escolha <= len(candidatos):
            candidato = candidatos[escolha - 1]
            break

        print("Opção inválida. Escolha um candidato da lista.")

    print("Escolha a vaga: ")

    for i, vaga in enumerate(vagas):
        print(f"{i + 1} - {vaga['cargo']} - {vaga['empresa']}")

    while True:
        try:
            escolha_vaga = int(input("Digite o número da vaga: "))
        except ValueError:
            print("Digite apenas um número.")
            continue

        if 1 <= escolha_vaga <= len(vagas):
            vaga = vagas[escolha_vaga - 1]
            break

        print("Opção inválida. Escolha uma vaga da lista.")

    resultado = calcular_match(candidato["habilidades"], vaga["habilidades"])
    habilidades_encontradas = []
    habilidades_faltantes = []

    for habilidade in vaga["habilidades"]:
        if habilidade in candidato["habilidades"]:
            habilidades_encontradas.append(habilidade)
        else:
            habilidades_faltantes.append(habilidade)


    print("\nResultado do match")
    print(f"Candidato: {candidato['nome']}")
    print(f"Vaga: {vaga['cargo']}")
    print(f"Empresa: {vaga['empresa']}")
    print(f"Compatibilidade: {resultado:.2f}%")


    print("\nHabilidades encontradas: ")

    for habilidade in habilidades_encontradas:
        print(f" - {habilidade}")

    print("\nHabilidades faltantes: ")
    if habilidades_faltantes:
        for habilidade in habilidades_faltantes:
            print(f" - {habilidade}")
    else:
        print("Nenhuma habilidade faltante.")


while True:
    print("\n1 - Cadastrar candidato")
    print("2 - Cadastrar vaga")
    print("3 - Ver vagas")
    print("4 - Ver candidatos")
    print("5 - Ver Match")
    print("6 - Sair")

    opcao = input("\nEscolha uma opção: ")

    if opcao == "1":
        cadastrar_candidato()

    elif opcao == "2":
        cadastrar_vaga()

    elif opcao == "3":
         listar_vagas()

    elif opcao == "4":
        listar_candidatos()

    elif opcao == "5":
        mostrar_match()

    elif opcao == "6":
        print("\nPrograma encerrado.")
        break

    else:
        print("\nOpção inválida. Escolha uma opção de 1 a 6.")

conexao.close()


