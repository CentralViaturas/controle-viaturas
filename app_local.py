import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json


class Viatura:
    def __init__(self, placa, modelo, cor):
        self.placa = placa
        self.modelo = modelo
        self.cor = cor
        self.estado = "Dentro"  # Estado inicial: Dentro
        self.motorista = None

    def registrar_saida(self, motorista):
        """Registra a saída da viatura com o motorista informado."""
        self.motorista = motorista
        self.estado = "Fora"
        hora_saida = datetime.now()
        messagebox.showinfo("Saída Registrada", f"Viatura {self.placa} saiu com motorista {self.motorista}.")
        self.salvar_dados("Saída", hora_saida)

    def registrar_entrada(self):
        """Registra a entrada da viatura."""
        self.estado = "Dentro"
        hora_entrada = datetime.now()
        messagebox.showinfo("Entrada Registrada", f"Viatura {self.placa} entrou com motorista {self.motorista}.")
        self.salvar_dados("Entrada", hora_entrada)

    def reservar(self, motorista):
        """Reserva a viatura com o motorista informado."""
        self.motorista = motorista
        self.estado = "Reservada"
        messagebox.showinfo("Reservada", f"Viatura {self.placa} está reservada com motorista {self.motorista}.")
        self.salvar_dados("Reservada", datetime.now())

    def salvar_dados(self, tipo_movimentacao, hora_movimentacao):
        """Salva os dados da viatura no Google Sheets."""
        try:
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
            client = gspread.authorize(creds)
            sheet = client.open("Controle de Viaturas").sheet1

            nova_linha = [
                self.placa,
                self.modelo,
                self.cor,
                self.motorista if self.motorista else "N/A",
                tipo_movimentacao,
                hora_movimentacao.strftime("%Y-%m-%d %H:%M:%S"),
                self.estado
            ]

            sheet.append_row(nova_linha)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar dados no Google Sheets: {e}")


def salvar_estado_viaturas(viaturas, arquivo="estado_viaturas.json"):
    """Salva o estado das viaturas em um arquivo JSON."""
    estado = []
    for viatura in viaturas:
        estado.append({
            "placa": viatura.placa,
            "modelo": viatura.modelo,
            "cor": viatura.cor,
            "estado": viatura.estado,
            "motorista": viatura.motorista
        })
    with open(arquivo, "w") as f:
        json.dump(estado, f)


def carregar_estado_viaturas(arquivo="estado_viaturas.json"):
    """Carrega o estado das viaturas de um arquivo JSON."""
    try:
        with open(arquivo, "r") as f:
            estado = json.load(f)
        return estado
    except FileNotFoundError:
        return None


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle de Viaturas")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f0f0")

        # Configuração do Canvas e barra de rolagem
        self.canvas = tk.Canvas(root, borderwidth=0, bg="#f0f0f0", highlightthickness=0)
        self.frame = tk.Frame(self.canvas, bg="#f0f0f0")
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Posicionamento do Canvas e Scrollbar
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        # Configuração do frame para ajustar o tamanho
        self.frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Título
        titulo = tk.Label(self.frame, text="Controle de Viaturas", font=("Helvetica", 20, "bold"), bg="#f0f0f0")
        titulo.grid(row=0, column=0, columnspan=6, pady=20)

        # Botões de adicionar e editar viaturas
        btn_adicionar = tk.Button(self.frame, text="Adicionar Viatura", command=self.adicionar_viatura, bg="#2196F3", fg="white", font=("Helvetica", 12, "bold"))
        btn_adicionar.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        btn_editar = tk.Button(self.frame, text="Editar Viatura", command=self.editar_viatura, bg="#FF9800", fg="white", font=("Helvetica", 12, "bold"))
        btn_editar.grid(row=1, column=2, padx=10, pady=10, columnspan=2)

        # Lista de viaturas pré-cadastradas
        self.viaturas = [
            Viatura("QZW-1G12", "CCOL", "AZUL"),
            Viatura("TAB-3G69", "CCOL", "CINZA"),
            Viatura("QZW-1E02", "PMT", "PRETO"),
            Viatura("TAF-8I68", "TI", "CINZA"),
            Viatura("TAF-8I58", "COE", "BRANCO"),
            Viatura("QZW-1E22", "D3", "PRETO"),
            Viatura("QZQ-8H99", "EVOE", "BRANCO"),
            Viatura("QZB-4B22", "UGE", "PRATA"),
            Viatura("QZY-5E82", "CCI", "BRANCO"),
            Viatura("QZQ-8I09", "SPI", "BRANCO"),
            Viatura("QZR-2C59", "SPI", "BRANCO"),
            Viatura("QZW-1D62", "D9", "PRATA"),
            Viatura("QZY-5E12", "D9", "CINZA"),
            Viatura("QZY-5D72", "COMSOC", "VERMELHO"),
            Viatura("QZY-6E12", "PTRIG", "PRATA"),
            Viatura("QZQ-8H79", "CSA", "BRANCO"),
            Viatura("QZX-1F42", "CCOL", "BRANCO"),
            Viatura("QZT-3I89", "ASSJUR", "BRANCO"),
            Viatura("QZT-7D89", "CCE", "BRANCO"),
            Viatura("QZY-5D92", "CCA", "CINZA"),
            Viatura("TAA-3G29", "S4", "PRETO"),
            Viatura("QZA-7E61", "D2", "PRETO"),
            Viatura("QZY-6B91", "EVOE", "VERMELHO"),
            Viatura("QZS-8F79", "UGE", "BRANCO"),
            Viatura("QZT-3I59", "DEST.ENG", "PRETO"),
            Viatura("QZT-7E29", "DEST.ENG", "BRANCO"),
            Viatura("QZY-6E22", "CAPELA", "PRETO"),
            Viatura("QZP-6D85", "BASE", "BRANCO"),
            Viatura("QZW-0B65", "RANCHO", "BRANCO"),
            Viatura("QZG-1D65", "CSA", "BRANCO"),
            Viatura("PHZ-0G41", "CCA", "BRANCO"),
            Viatura("PHZ-0H31", "CCA", "BRANCO"),
            Viatura("QZP-6E95", "PRA", "BRANCO"),
            Viatura("QZP-2F16", "CENTRAL", "BRANCO"),
            Viatura("QZC-5H15", "SUB CMT FT", "BRANCO"),
            Viatura("QZI-2J15", "CMT CONT", "BRANCO"),
            Viatura("QZD-6H35", "CMT FT", "BRANCO"),
            Viatura("QZH-9F85", "D2", "BRANCO"),
            Viatura("QZW-0C75", "IFOOD", "BRANCO"),
            Viatura("QZW-0B85", "CENTRAL", "BRANCO"),
            Viatura("QZE-5J65", "CCI", "BRANCO"),
        ]

        # Carregar o estado das viaturas, se existir
        estado_salvo = carregar_estado_viaturas()
        if estado_salvo:
            for viatura, estado in zip(self.viaturas, estado_salvo):
                viatura.estado = estado["estado"]
                viatura.motorista = estado["motorista"]

        self.botoes = []
        self.criar_botoes()

        # Salvar o estado ao fechar a janela
        self.root.protocol("WM_DELETE_WINDOW", self.ao_fechar)

    def criar_botoes(self):
        """Cria os botões para cada viatura."""
        for i, viatura in enumerate(self.viaturas):
            botao = tk.Button(self.frame, text=f"{viatura.placa}\n{viatura.modelo}\n{viatura.cor}",
                              bg=self.obter_cor_estado(viatura.estado),
                              fg="black", width=15, height=4, font=("Helvetica", 10, "bold"),
                              relief="flat", activebackground="#45a049",
                              command=lambda v=viatura: self.alterar_estado(v))
            botao.grid(row=(i // 6) + 2, column=i % 6, padx=10, pady=10)
            self.botoes.append(botao)

    def obter_cor_estado(self, estado):
        """Retorna a cor correspondente ao estado da viatura."""
        if estado == "Dentro":
            return "#4CAF50"  # Verde
        elif estado == "Fora":
            return "#f44336"  # Vermelho
        elif estado == "Reservada":
            return "#FFEB3B"  # Amarelo

    def alterar_estado(self, viatura):
        """Altera o estado da viatura (Dentro/Fora/Reservada)."""
        try:
            if viatura.estado == "Dentro":
                resposta = messagebox.askyesno("Escolha uma opção", "Deseja registrar saída? (Sim para Saída, Não para Reservar)")
                if resposta:
                    motorista = self.obter_motorista()
                    if motorista:
                        viatura.registrar_saida(motorista)
                else:
                    motorista = self.obter_motorista()
                    if motorista:
                        viatura.reservar(motorista)
            elif viatura.estado == "Fora":
                viatura.registrar_entrada()
            elif viatura.estado == "Reservada":
                viatura.registrar_entrada()
            self.atualizar_botoes()
            salvar_estado_viaturas(self.viaturas)  # Salva o estado após cada alteração
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    def obter_motorista(self):
        """Solicita o nome do motorista ao usuário."""
        motorista = simpledialog.askstring("Motorista", "Digite o nome do motorista:", parent=self.root)
        return motorista

    def atualizar_botoes(self):
        """Atualiza as cores dos botões com base no estado da viatura."""
        for botao, viatura in zip(self.botoes, self.viaturas):
            botao.config(bg=self.obter_cor_estado(viatura.estado))

    def adicionar_viatura(self):
        """Adiciona uma nova viatura à lista."""
        placa = simpledialog.askstring("Adicionar Viatura", "Digite a placa da viatura:", parent=self.root)
        modelo = simpledialog.askstring("Adicionar Viatura", "Digite o modelo da viatura:", parent=self.root)
        cor = simpledialog.askstring("Adicionar Viatura", "Digite a cor da viatura:", parent=self.root)
        if placa and modelo and cor:
            nova_viatura = Viatura(placa, modelo, cor)
            self.viaturas.append(nova_viatura)
            self.criar_botoes()
            salvar_estado_viaturas(self.viaturas)  # Salva o estado após adicionar uma viatura

    def editar_viatura(self):
        """Edita uma viatura existente."""
        placas = [viatura.placa for viatura in self.viaturas]
        placa = simpledialog.askstring("Editar Viatura", "Digite a placa da viatura que deseja editar:", parent=self.root)
        if placa in placas:
            index = placas.index(placa)
            viatura = self.viaturas[index]
            novo_modelo = simpledialog.askstring("Editar Viatura", "Digite o novo modelo da viatura:", parent=self.root, initialvalue=viatura.modelo)
            nova_cor = simpledialog.askstring("Editar Viatura", "Digite a nova cor da viatura:", parent=self.root, initialvalue=viatura.cor)
            if novo_modelo and nova_cor:
                viatura.modelo = novo_modelo
                viatura.cor = nova_cor
                self.criar_botoes()
                salvar_estado_viaturas(self.viaturas)  # Salva o estado após editar uma viatura
        else:
            messagebox.showerror("Erro", "Viatura não encontrada.")

    def ao_fechar(self):
        """Salva o estado das viaturas ao fechar o programa."""
        salvar_estado_viaturas(self.viaturas)
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()