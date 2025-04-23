import os
import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess

# --- Configurações ---
USERNAME = "admin"
PASSWORD = "1234"
TEMPO_ESTILO = 10
LARGURA_BOTOES = 35
COR_FUNDO = "#2e2e2e"
COR_BOTOES = "#4CAF50"
COR_BOTOES_HOVER = "#45a049"
COR_TEXTO = "white"
COR_BORDA = "#616161"

# Função para mostrar mensagens de sucesso
def mostrar_mensagem(titulo, mensagem):
    messagebox.showinfo(titulo, mensagem)

# --- Funções de otimização ---
def limpar_temporarios():
    os.system("del /s /f /q %temp%\\* >nul 2>&1")
    os.system("del /s /f /q C:\\Windows\\Temp\\* >nul 2>&1")
    mostrar_mensagem("Sucesso", "Arquivos temporários limpos!")

def set_prioridade():
    caminho = filedialog.askopenfilename(title="Selecionar Executável do Jogo", filetypes=[("Executáveis", "*.exe")])
    if caminho:
        nome = os.path.basename(caminho)
        try:
            subprocess.call(f'wmic process where name="{nome}" CALL setpriority 128', shell=True)
            mostrar_mensagem("Feito", f"A prioridade do processo '{nome}' foi definida como alta.\nObs: o jogo precisa estar aberto.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao definir prioridade: {e}")

def otimizar_energia():
    os.system("powercfg -setactive SCHEME_MIN")
    mostrar_mensagem("Feito", "Plano de energia ajustado para alto desempenho.")

def desativar_visuais():
    os.system('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" /v VisualFXSetting /t REG_DWORD /d 2 /f')
    mostrar_mensagem("Feito", "Efeitos visuais desativados.")

def baixar_otimizacoes():
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    pasta = os.path.join(desktop, "fpsboost")
    os.makedirs(pasta, exist_ok=True)

    arquivos = {
        "desativar-telemetria.reg": """Windows Registry Editor Version 5.00
[HKEY_LOCAL_MACHINE\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection]
"AllowTelemetry"=dword:00000000""",
        "limpeza-disco.bat": """@echo off
cleanmgr /sagerun:1
pause""",
        "otimizacoes.txt": """Dicas:
- Use plano de energia alto desempenho
- Desative inicialização de apps
- Atualize drivers de vídeo"""
    }

    for nome, conteudo in arquivos.items():
        with open(os.path.join(pasta, nome), "w") as f:
            f.write(conteudo)

    mostrar_mensagem("Download Concluído", f"Arquivos criados na pasta:\n{pasta}")

# --- Estilo dos Botões ---
def criar_botao(painel, texto, comando):
    botao = tk.Button(painel, text=texto, command=comando, width=LARGURA_BOTOES, height=2,
                      bg=COR_BOTOES, fg=COR_TEXTO, relief="flat", font=("Helvetica", 12, "bold"),
                      activebackground=COR_BOTOES_HOVER, bd=2, highlightthickness=1, highlightbackground=COR_BORDA)
    
    # Efeito hover nos botões
    def on_enter(event):
        botao.config(bg=COR_BOTOES_HOVER)
    
    def on_leave(event):
        botao.config(bg=COR_BOTOES)
    
    botao.bind("<Enter>", on_enter)
    botao.bind("<Leave>", on_leave)
    
    botao.pack(pady=TEMPO_ESTILO)

# --- Painel Principal ---
def abrir_painel():
    painel = tk.Tk()
    painel.title("FPS Boost - Otimização de Sistema")
    painel.geometry("500x450")
    painel.configure(bg=COR_FUNDO)

    # Cabeçalho
    tk.Label(painel, text="FPS Boost - Painel de Otimização", fg=COR_TEXTO, bg=COR_FUNDO, font=("Helvetica", 16, "bold")).pack(pady=20)

    # Botões
    botoes = [
        ("🧹 Limpar Arquivos Temporários", limpar_temporarios),
        ("🎯 Aumentar Prioridade de Jogo", set_prioridade),
        ("⚡ Otimizar Plano de Energia", otimizar_energia),
        ("🎨 Desativar Efeitos Visuais", desativar_visuais),
        ("📥 Baixar Otimizações", baixar_otimizacoes)
    ]
    
    for texto, comando in botoes:
        criar_botao(painel, texto, comando)

    painel.mainloop()

# --- Tela de Login ---
def login():
    user = usuario.get()
    pw = senha.get()
    if user == USERNAME and pw == PASSWORD:
        login_janela.destroy()
        abrir_painel()
    else:
        messagebox.showerror("Erro", "Usuário ou senha inválidos!")

# --- Interface de Login ---
login_janela = tk.Tk()
login_janela.title("Login FPS Boost")
login_janela.geometry("300x200")
login_janela.configure(bg=COR_FUNDO)

tk.Label(login_janela, text="Usuário:", bg=COR_FUNDO, fg=COR_TEXTO, font=("Helvetica", 12)).pack(pady=5)
usuario = tk.Entry(login_janela, font=("Helvetica", 12))
usuario.pack()

tk.Label(login_janela, text="Senha:", bg=COR_FUNDO, fg=COR_TEXTO, font=("Helvetica", 12)).pack(pady=5)
senha = tk.Entry(login_janela, show="*", font=("Helvetica", 12))
senha.pack()

tk.Button(login_janela, text="Entrar", command=login, width=20, height=2, bg=COR_BOTOES, fg=COR_TEXTO,
          relief="flat", font=("Helvetica", 12, "bold"), activebackground=COR_BOTOES_HOVER).pack(pady=20)

login_janela.mainloop()
