import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# Git Test

def carregar_arquivo():
    """Carrega um arquivo CSV ou JSON baseado no caminho fornecido pelo usuário."""
    while True:
        caminho = input("Digite o caminho completo do arquivo .csv ou .json: ").strip()
        
        try:
            if caminho.endswith('.csv'):
                df = pd.read_csv(caminho)
                print(f"Arquivo CSV carregado com sucesso! ({len(df)} registros)")
                return df
            elif caminho.endswith('.json'):
                df = pd.read_json(caminho)
                print(f"Arquivo JSON carregado com sucesso! ({len(df)} registros)")
                return df
            else:
                print("Formato inválido! Use apenas arquivos .csv ou .json.")
        except FileNotFoundError:
            print("Arquivo não encontrado. Verifique o caminho e tente novamente.")
        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")
            print("Tente novamente.")


def exibir_resumo_estatistico(df):
    """Exibe um resumo estatístico dos dados carregados."""
    if df is None or df.empty:
        print("Nenhum dado disponível para análise.")
        return

    print('\n--- Resumo Estatístico dos Dados ---\n')
    total_registros = len(df)
    print(f"Quantidade total de registros: {total_registros}")

    # Verifica e analisa cada coluna se existir
    colunas_verificar = ['Gender', 'Parent_Education_Level', 'Attendance (%)']
    
    for coluna in colunas_verificar:
        if coluna in df.columns:
            if coluna == 'Gender':
                homens = (df['Gender'] == 'Male').sum()
                mulheres = (df['Gender'] == 'Female').sum()
                print(f"\nDistribuição por gênero:\n- Homens: {homens}\n- Mulheres: {mulheres}")
            elif coluna == 'Parent_Education_Level':
                nulos = df['Parent_Education_Level'].isna().sum()
                print(f"\nRegistros sem dados sobre educação dos pais: {nulos}")
            elif coluna == 'Attendance (%)':
                print(f"\nMédia de frequência: {df['Attendance (%)'].mean():.1f}%")
        else:
            print(f"\nAviso: Coluna '{coluna}' não encontrada no dataset.")


def limpar_dados(df):
    """Realiza a limpeza dos dados."""
    if df is None or df.empty:
        print("Nenhum dado para limpar.")
        return df

    print("\n--- Iniciando limpeza dos dados ---")
    original_size = len(df)

    # Limpeza da educação dos pais
    if 'Parent_Education_Level' in df.columns:
        df = df.dropna(subset=['Parent_Education_Level'])
        print(f"Removidos {original_size - len(df)} registros sem educação dos pais")

    # Preenchimento de Attendance
    if 'Attendance (%)' in df.columns:
        median_att = df['Attendance (%)'].median()
        df['Attendance (%)'] = df['Attendance (%)'].fillna(median_att)
        print(f"Valores nulos em Attendance preenchidos com mediana: {median_att}")

    print(f"--- Limpeza concluída. Registros restantes: {len(df)} ---")
    return df


def consultar_dados(df):
    """Permite consultar estatísticas de colunas numéricas."""
    if df is None or df.empty:
        print("Nenhum dado disponível para consulta.")
        return

    numericas = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if not numericas:
        print("Nenhuma coluna numérica disponível.")
        return

    print("\nColunas numéricas disponíveis:")
    for i, col in enumerate(numericas, 1):
        print(f"{i}. {col}")

    while True:
        escolha = input("\nDigite o número da coluna ou 'sair': ")
        
        if escolha.lower() == 'sair':
            break
            
        try:
            idx = int(escolha) - 1
            if 0 <= idx < len(numericas):
                col = numericas[idx]
                print(f"\nEstatísticas de '{col}':")
                print(f"- Média: {df[col].mean():.2f}")
                print(f"- Mediana: {df[col].median():.2f}")
                print(f"- Desvio Padrão: {df[col].std():.2f}")
                
                moda = df[col].mode()
                if len(moda) < len(df[col]):
                    print(f"- Moda: {', '.join(map(str, moda.tolist()))}")
            else:
                print("Número inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Use números ou 'sair'.")


def gerar_graficos(df):
    """Gera gráficos para visualização dos dados."""
    if df is None or df.empty:
        print("Nenhum dado disponível para gráficos.")
        return

    # Gráfico de dispersão: sono vs nota
    if all(col in df.columns for col in ['Sleep_Hours_per_Night', 'Final_Score']):
        plt.figure(figsize=(10, 6))
        plt.scatter(df['Sleep_Hours_per_Night'], df['Final_Score'], alpha=0.5)
        plt.title('Relação entre Horas de Sono e Nota Final')
        plt.xlabel('Horas de Sono por Noite')
        plt.ylabel('Nota Final')
        plt.grid(True)
        plt.show()
    else:
        print("\nDados insuficientes para gerar gráfico de Sono vs Nota.")

    # Gráfico de barras: idade vs nota média
    if all(col in df.columns for col in ['Age', 'Midterm_Score']):
        df['Faixa Etária'] = pd.cut(df['Age'], 
                                   bins=[0, 17, 21, 24, 100],
                                   labels=['<18', '18-21', '22-24', '25+'])
        
        age_score = df.groupby('Faixa Etária')['Midterm_Score'].mean()
        
        plt.figure(figsize=(10, 6))
        age_score.plot(kind='bar', color='skyblue')
        plt.title('Média de Notas por Faixa Etária')
        plt.xlabel('Faixa Etária')
        plt.ylabel('Média da Nota')
        plt.xticks(rotation=45)
        plt.grid(axis='y')
        plt.show()
    else:
        print("\nDados insuficientes para gerar gráfico de Idade vs Nota.")


def main():
    """Função principal que orquestra a execução do programa."""
    print("=== Análise de Dados de Estudantes ===")
    
    df = carregar_arquivo()
    if df is not None:
        exibir_resumo_estatistico(df)
        df = limpar_dados(df)
        
        while True:
            print("\nMenu Principal:")
            print("1. Consultar estatísticas")
            print("2. Gerar gráficos")
            print("3. Sair")
            
            opcao = input("Escolha uma opção: ")
            
            if opcao == '1':
                consultar_dados(df)
            elif opcao == '2':
                gerar_graficos(df)
            elif opcao == '3':
                print("Encerrando o programa...")
                break
            else:
                print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()