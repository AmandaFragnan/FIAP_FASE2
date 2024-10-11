import tkinter as tk
from tkinter import messagebox
import pandas as pd
import json
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text
import requests
from datetime import datetime


# Conectando com o Oracle
def conectar_oracle():
    try:
        engine = create_engine('oracle+oracledb://SYSTEM:1234@localhost:1521/xe')
        conn = engine.connect()
        print("Conexão com o Oracle estabelecida com sucesso!")
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao Oracle: {e}")
        return None


conexao = conectar_oracle()


# Função para calcular custo de produção, utilizando como exemplo R$ 20 por hora de trabalho
def calcular_custo(insumos, horas_trabalho):
    custo_total = sum(insumos.values()) + horas_trabalho * 20
    return custo_total


def registrar_safra(conn, produto, area, insumos, colheita_prevista, custo_total):
    try:
        query = """
        INSERT INTO SAFRAS (PRODUTO, AREA, INSUMOS, COLHEITA_PREVISTA, CUSTO_TOTAL)
        VALUES (:produto, :area, :insumos, TO_DATE(:colheita_prevista, 'DD-MM-YYYY'), :custo_total)
        """
        conn.execute(
            text(query),
            {'produto': produto, 'area': area, 'insumos': insumos, 'colheita_prevista': colheita_prevista,
             'custo_total': custo_total}
        )
        conn.commit()
        print("Safra registrada com sucesso!")
    except Exception as e:
        print(f"Erro ao registrar safra: {e}")


# Obtendo a previsão do tempo para análise
def obter_previsao(cidade, chave_api):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={chave_api}&q={cidade}&days=5&aqi=no&alerts=no"
    try:
        resposta = requests.get(url)
        dados = resposta.json()

        if resposta.status_code == 200:
            print(f"Previsão do tempo em {dados['location']['name']}, {dados['location']['country']}:")
            for dia in dados['forecast']['forecastday']:
                print(f"Data: {dia['date']}")
                print(f"Temperatura Máxima: {dia['day']['maxtemp_c']}°C")
                print(f"Temperatura Mínima: {dia['day']['mintemp_c']}°C")
                print(f"Condições: {dia['day']['condition']['text']}")
                print("----------------------------")
            return dados['forecast']['forecastday']
        else:
            print(f"Erro ao obter os dados: {dados['error']['message']}")
            return None

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return None


class SafraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gerenciamento de Safras")
        self.create_widgets()

        self.produtores = {
            'Produtor A': []
        }

        self.chave_api = "665e3178898f443f85f110605240910"
        self.cidade = "São Paulo"

    def create_widgets(self):

        tk.Label(self.root, text="Produtor").grid(row=0, column=0)
        tk.Label(self.root, text="Produto").grid(row=1, column=0)
        tk.Label(self.root, text="Área Cultivada").grid(row=2, column=0)
        tk.Label(self.root, text="Insumos (Fertilizantes, Pesticidas, Água)").grid(row=3, column=0)
        tk.Label(self.root, text="Horas de Trabalho").grid(row=4, column=0)
        tk.Label(self.root, text="Colheita Prevista (DD-MM-YYYY)").grid(row=5, column=0)

        self.entry_produtor = tk.Entry(self.root)
        self.entry_produto = tk.Entry(self.root)
        self.entry_area = tk.Entry(self.root)
        self.entry_insumos = tk.Entry(self.root)
        self.entry_horas_trabalho = tk.Entry(self.root)
        self.entry_colheita_prevista = tk.Entry(self.root)

        self.entry_produtor.grid(row=0, column=1)
        self.entry_produto.grid(row=1, column=1)
        self.entry_area.grid(row=2, column=1)
        self.entry_insumos.grid(row=3, column=1)
        self.entry_horas_trabalho.grid(row=4, column=1)
        self.entry_colheita_prevista.grid(row=5, column=1)

        tk.Button(self.root, text="Registrar Safra", command=self.registrar_safra).grid(row=6, column=0, columnspan=2)
        tk.Button(self.root, text="Visualizar Gráficos", command=self.visualizar_graficos).grid(row=7, column=0,
                                                                                                columnspan=2)
        tk.Button(self.root, text="Ver Previsão do Tempo", command=self.ver_previsao_tempo).grid(row=8, column=0,
                                                                                                 columnspan=2)
        tk.Button(self.root, text="Salvar Relatório em Texto", command=self.salvar_relatorio_texto).grid(row=9,
                                                                                                         column=0,
                                                                                                         columnspan=2)
        tk.Button(self.root, text="Salvar Relatório em JSON", command=self.salvar_relatorio_json).grid(row=10, column=0,
                                                                                                       columnspan=2)

    def registrar_safra(self):
        produtor = self.entry_produtor.get()
        produto = self.entry_produto.get()

        try:
            area_cultivada = float(self.entry_area.get())
        except ValueError:
            messagebox.showerror("Erro", "A área cultivada deve ser um número.")
            return

        try:
            insumos_list = self.entry_insumos.get().split(',')
            if len(insumos_list) != 3:
                raise ValueError("Três valores devem ser fornecidos para insumos.")
            insumos = {
                'fertilizantes': int(insumos_list[0]),
                'pesticidas': int(insumos_list[1]),
                'agua': int(insumos_list[2])
            }
        except ValueError as e:
            messagebox.showerror("Erro", f"Erro ao processar insumos: {e}")
            return

        try:
            horas_trabalho = int(self.entry_horas_trabalho.get())
        except ValueError:
            messagebox.showerror("Erro", "Horas de trabalho deve ser um número inteiro.")
            return

        colheita_prevista = self.entry_colheita_prevista.get()

        custo_total = calcular_custo(insumos, horas_trabalho)

        try:
            data_colheita = datetime.strptime(colheita_prevista, "%d-%m-%Y")
            if data_colheita < datetime.now():
                messagebox.showerror("Erro", "A data de colheita prevista não pode ser anterior à data atual.")
            return
        except ValueError:
            messagebox.showerror("Erro", "Data de colheita prevista deve estar no formato AAAA-MM-DD.")
            return

        safra = {
            'produto': produto,
            'area_cultivada': area_cultivada,
            'insumos': insumos,
            'custo_total': custo_total,
            'colheita_prevista': colheita_prevista
        }

        if produtor not in self.produtores:
            self.produtores[produtor] = []

        for s in self.produtores[produtor]:
            if s['produto'] == produto:
                s['area_cultivada'] += area_cultivada
                s['custo_total'] += custo_total
                s['insumos']['fertilizantes'] += insumos['fertilizantes']
                s['insumos']['pesticidas'] += insumos['pesticidas']
                s['insumos']['agua'] += insumos['agua']
                break
        else:
            self.produtores[produtor].append(safra)

        # Inserindo as informações ao banco de dados Oracle
        if conexao:
            registrar_safra(conexao, produto, area_cultivada, str(insumos), colheita_prevista, custo_total)

        messagebox.showinfo("Sucesso", "Safra registrada com sucesso!")

    def visualizar_graficos(self):
        produtor = self.entry_produtor.get()
        if produtor in self.produtores:
            df = pd.DataFrame(self.produtores[produtor])
            df['custo_total'] = df['custo_total'].astype(float)

            # Gráfico de Custo por Safra
            plt.figure(figsize=(10, 5))
            df.plot(kind='bar', x='produto', y='custo_total', title="Custo Total por Safra", color='lightblue')
            plt.ylabel("Custo Total")
            plt.grid(axis='y')
            plt.show()

            # Gráfico de Área Cultivada por Produto
            plt.figure(figsize=(10, 5))
            df.plot(kind='bar', x='produto', y='area_cultivada', title="Área Cultivada por Produto", color='lightgreen')
            plt.ylabel("Área Cultivada")
            plt.grid(axis='y')
            plt.show()

            # Gráfico de Dispersão: Custo Total vs. Área Cultivada
            plt.figure(figsize=(10, 5))
            plt.scatter(df['area_cultivada'], df['custo_total'], color='orange')
            plt.title("Custo Total vs. Área Cultivada")
            plt.xlabel("Área Cultivada")
            plt.ylabel("Custo Total")
            plt.grid()
            plt.show()

            if 'colheita_prevista' in df.columns:
                df['colheita_prevista'] = pd.to_datetime(df['colheita_prevista'])
                df.sort_values('colheita_prevista', inplace=True)  # Ordenar por data
                plt.figure(figsize=(10, 5))
                plt.plot(df['colheita_prevista'], df['custo_total'], marker='o', linestyle='-', color='purple')
                plt.title("Evolução do Custo Total ao Longo do Tempo")
                plt.xlabel("Data de Colheita Prevista")
                plt.ylabel("Custo Total")
                plt.xticks(rotation=45)
                plt.grid()
                plt.show()

        else:
            messagebox.showwarning("Atenção", "Nenhuma safra registrada para este produtor.")

    def ver_previsao_tempo(self):
        previsao = obter_previsao(self.cidade, self.chave_api)
        if previsao:
            temperaturas_max = [dia['day']['maxtemp_c'] for dia in previsao]
            temperaturas_min = [dia['day']['mintemp_c'] for dia in previsao]
            datas = [dia['date'] for dia in previsao]

            # Gráfico da Previsão do Tempo
            plt.figure(figsize=(10, 5))
            plt.plot(datas, temperaturas_max, label='Temperatura Máxima (°C)', color='red', marker='o')
            plt.plot(datas, temperaturas_min, label='Temperatura Mínima (°C)', color='blue', marker='o')
            plt.fill_between(datas, temperaturas_max, temperaturas_min, color='gray', alpha=0.2)
            plt.title("Previsão do Tempo")
            plt.xlabel("Data")
            plt.ylabel("Temperatura (°C)")
            plt.xticks(rotation=45)
            plt.legend()
            plt.grid()
            plt.show()

    # Gerando o relatório de analise das informações em arquivo texto
    def salvar_relatorio_texto(self):
        try:
            with open("relatorio_safras_analise.txt", "w", encoding='utf-8') as file:
                for produtor, safras in self.produtores.items():
                    file.write(f"Produtor: {produtor}\n")
                    file.write("Análise das Safras:\n")

                    df = pd.DataFrame(safras)
                    df['area_cultivada'] = pd.to_numeric(df['area_cultivada'], errors='coerce')

                    area_total = df['area_cultivada'].sum()
                    area_media = df['area_cultivada'].mean()
                    file.write(f"  Área Total Cultivada: {area_total} hectares\n")
                    file.write(f"  Área Média Cultivada por Safra: {area_media:.2f} hectares\n")

                    if 'colheita_prevista' in df.columns:
                        df['colheita_prevista'] = pd.to_datetime(df['colheita_prevista'])
                        df.sort_values('colheita_prevista', inplace=True)
                        file.write("  Evolução do Custo ao Longo do Tempo:\n")
                        for index, row in df.iterrows():
                            file.write(
                                f"    Data de Colheita: {row['colheita_prevista'].date()}, Custo Total: R$ {row['custo_total']:.2f}\n")

                    file.write("----------------------------\n")

            messagebox.showinfo("Sucesso", "Relatório com análises salvo em texto com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar relatório: {e}")

    # Gerando o relatório das informações em arquivo json
    def salvar_relatorio_json(self):
        try:
            with open("relatorio_safras.json", "w") as file:
                json.dump(self.produtores, file, indent=4)
                messagebox.showinfo("Sucesso", "Relatório salvo em JSON com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar relatório: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SafraApp(root)
    root.mainloop()
