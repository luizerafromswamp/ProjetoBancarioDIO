from abc import ABC, abstractclassmethod,abstractproperty
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.conta = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adcionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __int__(self, nome, cpf, data_de_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_de_nascimento = data_de_nascimento
        self.cpf = cpf

class Conta:
    def __int__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self.agencia = "0001"
        self.cliente = cliente
        self.historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente")

        elif valor > 0:
            self._saldo -= valor
            print("Saque realizado com sucesso!")
            return True

        else:
            print("Operação falhou! O valor informado é inválido.")
            return False


    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Depósito realizado com sucesso")

        else:
            print("Operação falhou!")
            return False

        return True

class ContaCorrente(Conta):
    def __int__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("Operação falhou!")
        elif excedeu_saques:
            print("Operação falhou")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
             Agencia:\t{self.agencia}
             C/C:\t\t{self.numero}
             Titular:\t{self.cliente.nome}
        """

class Historico:
    def __int__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adcionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__clas__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime
                ("%d-%m-%Y %H:%M:%s"),
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adcionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adcionar_transacao(self)











def menu():
    menu = """"
    ==========MENU==========
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Criar Conta
    [5] Criar Cliente
    [6] Listar Contas
    [7] Sair

    => """
    return input(menu)


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

# def filtrar_usuarios(cpf, usuarios):
#     usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
#     return usuarios_filtrados[0] if usuarios_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possui conta!")
        return cliente.contas[0]


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n Cliente não encontrado")
        return
    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado")
        return
    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado")
        return
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    print("\n============EXTRATO=============")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizado transações"
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}\n\tR${transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==================================")


def criar_cliente(clientes):
    cpf = input("Informe seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("Já existe usuario com este CPF")
        return

    nome = input("Informe seu nome: ")
    data_nascimento = input("Informe sua data de nascimento: ")
    endereco = input("Informe seu endereço(Rua - Bairro - Cidade - Estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, endereco=endereco, cpf=cpf)

    clientes.append(cliente)

    print("Usuário criado com sucesso!")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("Conta criada com sucesso!")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)


def main():
    clientes = []
    contas = []


    while True:

        opção = menu()

        if opção == "1":
            depositar(clientes)

        elif opção == "2":
            sacar(clientes)

        elif opção == "3":
            exibir_extrato(clientes)

        elif opção == "4":
            criar_cliente(clientes)

        elif opção == "5":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opção == "6":
            listar_contas(contas)

        elif opção == "7":
            break

        else:
            print("Operação inválida! Selecione a operação desejada")

main()

# LIMITE_DE_SAQUES = 3
# AGENCIA = "0001"
# saldo = 0
# limite = 500
# extrato = ""
# numero_de_saques = 0
# usuarios = []
# contas = []
