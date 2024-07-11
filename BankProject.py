def menu():
    menu = """"
    ==========MENU==========
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Nova Conta
    [5] Novo Usuário
    [6] Sair

    => """
    return input(menu)

def depositar(saldo, valor, extrato):
    if valor > 0:
            saldo += valor
            extrato += f"Deposito: R$ {valor:.2f}\n"
    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato

def saque(*, saldo, valor, extrato, limite, numero_de_saques, limite_de_saques):

    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_de_saques >= limite_de_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente")

    elif excedeu_limite:
        print("Operação falhou! O limite do saldo excede o limite!")

    elif excedeu_saques:
        print("Operação falhou! Numero máximo de saques excedido!")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_de_saques += 1
        print("Saque realizado com sucesso!")

    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
    print("\n========== EXTRATO ==========")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\n Saldo: R$ {saldo:.2f}")
    print("===============================")
    return saldo, extrato

def novo_usuario(usarios):
    cpf = input("Informe seu CPF: ")
    usuario = filtrar_usuarios(cpf,usarios)

    if usuario:
        print("Já existe usuario com este CPF")
        return
    nome = input("Informe seu nome: ")
    data_nascimento = input("Informe sua data de nascimento: ")
    endereco = input("Informe seu endereço(Rua - Bairro - Cidade - Estado): ")

    usarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("Usuário criado com sucesso!")

def filtrar_usuarios(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuarios(cpf,usuarios)

    if usuario:
        print("Conta criada com sucesso!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("Usuário não encontrado, criação de conta cancelada!")

def main():
    LIMITE_DE_SAQUES = 3
    AGENCIA = "0001"
    saldo = 0
    limite = 500
    extrato = ""
    numero_de_saques = 0
    usuarios = []
    contas = []

    while True:

        opção = menu()

        if opção == "1":
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato)


        elif opção == "2":
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato = saque(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_de_saques=numero_de_saques,
                limite_de_saques=LIMITE_DE_SAQUES)


        elif opção == "3":
            exibir_extrato(saldo, extrato=extrato)

        elif opção == "4":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)


        elif opção == "5":

            novo_usuario(usuarios)

        elif opção == "6":
            break

        else:
            print("Operação inválida! Selecione a operação desejada")

main()




