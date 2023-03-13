from tkinter import *
import tkinter as tk
from tkcalendar import Calendar, DateEntry
from tkinter import ttk
from tkinter.font import BOLD, Font
from tkinter import Scrollbar
import sqlite3

janela = Tk()

my_font = Font(size="32", weight=BOLD)

class Funcs():
    def Limpar_Tela(self):
        self.busca_C_entry.delete(0, END)
        self.nome_C_entry.delete(0, END)
        self.entry_tel.delete(0, END)
        self.entry_dataS.delete(0, END)
        self.entry_dataE.delete(0, END)

    def conecta_db(self):
        self.conn = sqlite3.connect("clientes.db")
        self.cursor = self.conn.cursor();

    def desconecta_db(self):
        self.conn.close(); print("Desconectando ao banco de dados")

    def criaTabelas(self):
        self.conecta_db(); print("Conectando ao banco de Dados...")
        # Criando tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes(
                codigo_cli INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_cliente CHAR(40) NOT NULL,
                telefone INTEGER(20),
                data_entrada DATE(50),
                data_saida DATE(50)
            );
        """)
        self.conn.commit(); print("Banco de dados criado")
        self.desconecta_db()
        self.Limpar_Tela()


    def variaveis(self):
        self.codigo_cli = self.busca_C_entry.get()
        self.nome = self.nome_C_entry.get()
        self.telefone = self.entry_tel.get()
        self.dataE = self.calendario1.get_date()
        self.dataS = self.calendario2.get_date()

    def add_cliente(self):
        self.variaveis()
        self.conecta_db()
        
        self.cursor.execute(""" INSERT INTO clientes (nome_cliente, telefone, data_entrada, data_saida)
            VALUES (?, ?, ?, ?)""", (self.nome, self.telefone, self.dataE, self.dataS))
        self.conn.commit()
        self.desconecta_db()
        self.select_lista()

        self.Limpar_Tela()
    
    def select_lista(self):
        self.listaCl.delete(*self.listaCl.get_children())
        self.conecta_db()
        lista = self.cursor.execute(""" SELECT codigo_cli, nome_cliente, telefone, data_entrada, data_saida FROM clientes ORDER BY nome_cliente ASC; """)
        for i in lista:
            self.listaCl.insert("", END, values=i)
        self.desconecta_db()
        
    def fechar_calendario(self):
        self.calendario1.destroy()
        self.calDataE.destroy()
        self.btn_fecharC1.destroy()

    def calendarioE(self):
        self.calendario1 = Calendar(self.frame_f, fg= "gray", bg= "3E3E3F", locale="pt_br")
        self.calendario1.place(relx=0.6, rely= 0.3)
        self.calDataE = Button(self.frame_f, text="Inserir Data", command= self.print_calE)

        self.calDataE.place(relx=0.46, rely= 0.37, width= 90)
        self.btn_fecharC1 = Button(self.aba1, text="X", command= self.fechar_calendario)
        self.btn_fecharC1.place(relx= 0.92, rely=0.1)

    def fechar_calendario2(self):
        self.calendario2.destroy()
        self.calDataS.destroy()
        self.btn_fecharC2.destroy()

    def calendarioS(self):
        self.calendario2 = Calendar(self.frame_f, fg= "gray", bg= "3E3E3F", locale="pt_br")
        self.calendario2.place(relx=0.6, rely= 0.3)
        self.calDataS = Button(self.frame_f, text="Inserir Data", command= self.print_calS)
        self.btn_fecharC2 = Button(self.aba1, text="X", command= self.fechar_calendario2)
        self.btn_fecharC2.place(relx= 0.95, rely=0.1)
        self.calDataS.place(relx=0.46, rely= 0.75, width= 90)

    
    def print_calE(self):
        dateEntrada = self.calendario1.get_date()
        self.calendario1.destroy()
        self.entry_dataE.delete(0, END)
        self.entry_dataE.insert(END, dateEntrada)
        self.calDataE.destroy()


    def print_calS(self):
        dateSaida = self.calendario2.get_date()
        self.calendario2.destroy()
        self.entry_dataS.delete(0, END)
        self.entry_dataS.insert(END, dateSaida)
        self.calDataS.destroy()

    def quandoDuploClique(self, event):
        self.Limpar_Tela()
        self.listaCl.selection()

        for n in self.listaCl.selection():
            col1, col2, col3, col4, col5 = self.listaCl.item(n, 'values')
            self.busca_C_entry.insert(END, col1)
            self.nome_C_entry.insert(END, col2)
            self.entry_tel.insert(END, col3)
            self.entry_dataE.insert(END, col4)
            self.entry_dataS.insert(END, col5)
    
    def deleta_cliente(self):
        self.variaveis()
        self.conecta_db()
        self.cursor.execute("""DELETE FROM clientes WHERE codigo_cli = ? """, (self.codigo_cli,))
        self.conn.commit()
        self.desconecta_db()
        self.Limpar_Tela()
        self.select_lista()

    def buscar_cliente(self):
        self.conecta_db()
        self.listaCl.delete(*self.listaCl.get_children())
        
        self.nome_C_entry.insert(END, '%')
        nome = self.nome_C_entry.get()
        self.cursor.execute(""" SELECT codigo_cli, nome_cliente, telefone, data_entrada, data_saida FROM clientes WHERE nome_cliente LIKE '%s' ORDER BY nome_cliente ASC""" % nome)
        buscaenomeCli = self.cursor.fetchall()
        for i in buscaenomeCli:
            self.listaCl.insert("", END, values=i)
        self.Limpar_Tela()
        self.desconecta_db()
        print(buscaenomeCli)

    def alterar_cliente(self):
        self.variaveis()
        self.conecta_db()
        self.cursor.execute(""" UPDATE clientes SET nome_cliente = ?, telefone = ?, data_entrada = ?, data_saida = ?  WHERE codigo_cli = ? """, (self.nome, self.telefone, self.dataE, self.dataS, self.codigo_cli))
        self.conn.commit()
        self.desconecta_db()
        self.select_lista()
        self.Limpar_Tela()

    def menus(self):
        menubar = Menu(self.janela)
        self.janela.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit(): self.janela.destroy()

        menubar.add_cascade(label= "Opções", menu= filemenu)
        menubar.add_cascade(label= "Sobre", menu= filemenu2)

        filemenu.add_command(label= "Sair", command= Quit)
        filemenu2.add_command(label= "Abrir Orçamentos")

class Application(Funcs):
    # Definindo a inicialização das funções
    def __init__(self):
        self.janela = janela
        self.tela()
        self.frames_da_tela()
        self.criando_btns()
        self.outros_widgets()
        self.criaTabelas()
        self.lista_frameS()
        self.menus()
        self.widgets_frame_t()
        janela.mainloop()

    # Definindo as configs da tela
    def tela(self):
        self.janela.title("Cadastro de Clientes")
        self.janela.configure(bg='gray')
        self.janela.geometry("1800x900")
        self.janela.resizable(False, False)

    # Defindo os 2 frames da tela
    def frames_da_tela(self):
        self.frame_f = Frame(self.janela, bd= 4, bg="#3E3E3F", highlightbackground='#000000', highlightthickness= 0.5)
        self.frame_f.place(relx= 0.02, rely= 0.02, relheight= 0.28, relwidth= 0.38)
        
        self.frame_s = Frame(self.janela, bd= 4, bg="#3E3E3F", highlightbackground='#000000', highlightthickness= 0.5)
        self.frame_s.place(relx= 0.02, rely=0.35, relheight= 0.28, relwidth= 0.38)

        self.frame_t = Frame(self.janela, bd= 4, bg="#3E3E3F", highlightbackground='#000000', highlightthickness= 0.5)
        self.frame_t.place(relx= 0.5, rely=0.01, relheight= 0.98, relwidth=0.45)


    def criando_btns(self):
        self.aba = ttk.Notebook(self.frame_f)
        self.aba1 = Frame(self.aba)

        self.aba1.configure(background= "#3E3E3F")

        self.aba.add(self.aba1, text= "Dados do CLiente")

        self.aba.place(relx=0, rely=0, relwidth=0.98, relheight=0.90)

        # Botão limpar
        self.btn_limpar = Button(self.aba1, text="Limpar", bd=3, bg="#4D9428", fg="black", command= self.Limpar_Tela)
        self.btn_limpar.place(relx= 0.3, rely= 0.1, relwidth= 0.1, relheight= 0.15)
        
        # Botão Buscar
        self.btn_buscar = Button(self.aba1, text="Buscar", bd=3, bg="#4D9428", fg="black", command= self.buscar_cliente)
        self.btn_buscar.place(relx= 0.5, rely= 0.1, relwidth= 0.1, relheight= 0.15)
        
        # Botão Novo
        self.btn_novo = Button(self.aba1, text="Novo", bd=3, bg="#4D9428", fg="black", command= self.add_cliente)
        self.btn_novo.place(relx= 0.6, rely= 0.1, relwidth= 0.1, relheight= 0.15)
        
        # Botão Alterar
        self.btn_alterar = Button(self.aba1, text="Alterar", bd=3, bg="#4D9428", fg="black", command= self.alterar_cliente)
        self.btn_alterar.place(relx= 0.7, rely= 0.1, relwidth=0.1, relheight= 0.15)
        
        # Botão Apagar
        self.btn_apagar = Button(self.aba1, text="Apagar", bd=3, bg="#4D9428", fg="black", command= self.deleta_cliente)
        self.btn_apagar.place(relx= 0.8, rely= 0.1, relwidth= 0.1, relheight= 0.15)

        # Calendario data de Entrada
        self.btn_calendario = Button(self.aba1, text= "Data de Entrada", command= self.calendarioE)
        self.btn_calendario.place(rely= 0.5, relx= 0.47)
        self.entry_dataE = Entry(self.aba1, width= 12)
        self.entry_dataE.place(relx= 0.64, rely= 0.51)


        # Calendario data de Saida
        self.btn_calendario = Button(self.aba1, text= "Data de Entrada", command= self.calendarioS)
        self.btn_calendario.place(rely= 0.7, relx= 0.47)
        self.entry_dataS = Entry(self.aba1, width= 12)
        self.entry_dataS.place(relx= 0.64, rely= 0.7)

    def outros_widgets(self):

        # Criando Label e Entrada da Busca do nome do Cliente
        self.lb_busca_C = Label(self.aba1, bg="#3E3E3F", text="Buscar por Cliente:", foreground='white')
        self.lb_busca_C.place(relx= 0.05, rely= 0.08)

        self.busca_C_entry = Entry(self.aba1)
        self.busca_C_entry.place(relx= 0.05, rely= 0.16, relwidth= 0.127)
        
        # Criando Label e Entrada do nome do Cliente
        self.lb_nome_C = Label(self.aba1, bg="#3E3E3F",text="Nome do Cliente:", foreground='white')
        self.lb_nome_C.place(relx= 0.05, rely= 0.35)

        self.nome_C_entry = Entry(self.aba1)
        self.nome_C_entry.place(relx= 0.05, rely= 0.45, relwidth= 0.35)
        
        # Criando Label e Entrada do Telefone
        self.lb_tel = Label(self.aba1, text="Telefone:", bg="#3E3E3F", foreground='white')
        self.lb_tel.place(relx= 0.05, rely= 0.55)

        self.entry_tel = Entry(self.aba1)
        self.entry_tel.place(relx= 0.05, rely= 0.65)

    def add_lin(self):
        # Adicionando label e entrys da Descrição
        self.y_coord = 10
        self.entry = Entry(self.frame_t)
        self.entry.place(relx=0.28, y=self.y_coord, relwidth=0.05)
        self.y_coord += 1
        # Adicionando label e entrys da Descrição
        self.entry = Entry(self.frame_t)
        self.entry.place(relx=0.43, y=self.y_coord)
        self.y_coord += 2  
        # Adicionando label e entrys da Descrição
        self.entry = Entry(self.frame_t)
        self.entry.place(relx=0.72, y=self.y_coord, relwidth=0.05)
        self.y_coord += 3

    def widgets_frame_t(self):
        # Criando Label Orçamento
        self.lb_orca = Label(self.frame_t, text="Orçamento", bg="#3E3E3F", foreground='white', font=my_font)
        self.lb_orca.place(relx=0.37, rely=0.0)

        # Criando label e Entry da Quantidade
        self.lb_Qnt = Label(self.frame_t, text="Qnt.", bg="#3E3E3F", foreground='white')
        self.lb_Qnt.place(relx=0.28, rely=0.08)

        self.entry_Qnt = Entry(self.frame_t)
        self.entry_Qnt.place(relx=0.28, rely=0.1, relwidth=0.05)

        # Criando label e Entry da Descrição
        self.lb_desc = Label(self.frame_t, text="Descrição", bg="#3E3E3F", foreground='white')
        self.lb_desc.place(relx=0.43, rely=0.08)

        self.entry_desc = Entry(self.frame_t)
        self.entry_desc.place(relx=0.43, rely=0.1)

        # Criando label e Entry da Valor
        self.lb_desc = Label(self.frame_t, text="Valor", bg="#3E3E3F", foreground='white')
        self.lb_desc.place(relx=0.72, rely=0.08)

        self.entry_desc = Entry(self.frame_t)
        self.entry_desc.place(relx=0.715, rely=0.1, relwidth=0.05)

        # Criando os botões Adicionar e Deletar

        self.btn_Add = Button(self.frame_t, text="Adicionar", command=self.add_lin)
        self.btn_Add.place(relx=0.55, rely=0.95)

        self.btn_Delete = Button(self.frame_t, text="Deletar")
        self.btn_Delete.place(relx=0.7, rely=0.95)


    def lista_frameS(self):
        self.listaCl = ttk.Treeview(self.frame_s, height= 3, column=("col1", "col2", "col3", "col4", "col5"))
        self.listaCl.heading('#0', text="")
        self.listaCl.heading('#1', text="Codigo")
        self.listaCl.heading('#2', text="Nomo do Cliente")
        self.listaCl.heading('#3', text="Telefone")
        self.listaCl.heading('#4', text="Data de Entrada")
        self.listaCl.heading('#5', text="Data de Saida")

        self.listaCl.column("#0", width=1, stretch=NO)
        self.listaCl.column('#1', width= 50)
        self.listaCl.column("#2", width=200)
        self.listaCl.column("#3", width=125)
        self.listaCl.column("#4", width=125)
        self.listaCl.column("#5", width=125)

        self.listaCl.place(relx= 0.01, rely= 0.1, relheight= 0.85, relwidth= 0.95)

        self.scroolLista = Scrollbar(self.listaCl, orient='vertical')
        self.listaCl.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx= 0.96, rely= 0.1, relwidth= 0.04, relheight= 0.95)
        self.listaCl.bind("<Double-1>", self.quandoDuploClique)
        self.select_lista()

Application()