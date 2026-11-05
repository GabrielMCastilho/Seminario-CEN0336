import random
import os
import json
import time
from datetime import datetime

# 1. Parâmetros fixos do sistema
setpoint_temperatura = 30.0  # Temperatura desejada (°C)
setpoint_ph = 7 # pH desejado para o crescimento bacteriano 
intervalo_leitura = 10  # segundos
tempo_total = 120  # 2 minutos em segundos

# 2. Variavel com o intervalo de temperatura inicial (18 a 30 °C)

# Sorteamos a temperatura inicial de inóculo ou inicio do funcionamento do controle automático do biorreator
temperatura_atual = random.randint(15, 35)
ph_atual = random.randint(6, 8)

# Lista para armazenar o histórico
historico_biorreator = []

print(f"Temperatura Inicial Sorteada: {temperatura_atual:.2f} °C\n")

# Calculamos quantos ciclos vão rodar (120 / 10 = 12 ciclos)
total_ciclos = tempo_total // intervalo_leitura

# Loop de controle
for ciclo in range(1, total_ciclos + 1):
    # Pega data e hora atual do ciclo
    agora = datetime.now()
    data_str = agora.strftime("%Y-%m-%d")
    hora_str = agora.strftime("%H:%M:%S")

    # Adiciona um erro de variação aleatório e aceitável no sensor de temperatura ao ligar e desligar o resfriador (entre -0.5°C e +0.5°C)
    erro_sensor_temperatura = random.uniform(-0.5, 0.5)
    temperatura_com_erro = temperatura_atual + erro_sensor_temperatura

   # Ruído aleatório de leitura do eletrodo de pH (+- 0.05)
    erro_sensor_ph = random.uniform(-0.05, 0.05)
    ph_com_erro = ph_atual + erro_sensor_ph

    print(
        f"Número de ciclos: {ciclo}/{total_ciclos} | Horário: {hora_str} | Temp. Lida: {temperatura_com_erro:.2f} °C | pH Lido: {ph_com_erro:.2f}"
    )

    # Lógica de controle do Biorreator (Atuadores: Resfriador)
    if temperatura_com_erro > setpoint_temperatura:
        print("  -> Status: Temperatura alta.\nLIGANDO O RESFRIADOR")
        temperatura_atual -= random.uniform(0, 1)  # Resfria aleatóriamente em um intervalo de 1°C por ciclo
    elif temperatura_com_erro < setpoint_temperatura:
        print(
            "  -> Status: Temperatura baixa.\nDESLIGANDO RESFRIADOR"
        )
        temperatura_atual += random.uniform(0, 1)  # Aquece 1°C por ciclo
    else:
        print("  -> Status: Temperatura adequada. Sistema estabilizado.")

    # Lógica de controle do Biorreator (Atuadores: Injetores)
    if ph_com_erro > setpoint_ph:
        print("  -> Status: pH alto.\nINJETANDO 1 mL DE HCl")
        ph_atual -= random.uniform(0, 0.5)  # Abaixa aleatoriamente o pH em um intervalo de 0,5 por ciclo
    elif ph_com_erro < setpoint_ph:
        print(
            "  -> Status: pH baixo.\nINJETANDO 1 mL DE NaOH"
        )
        ph_atual += random.uniform(0, 0.5)  # Sobe o pH em 0,5 por ciclo
    else:
        print("  -> Status: pH adequado. Sistema estabilizado.")

    # Armazena as informações do ciclo em um dicionário dentro da lista
    dados_ciclo = {
        "data": data_str,
        "hora": hora_str,
        "leituras": {
            "temperatura": f"{round(temperatura_com_erro, 2)} ºC",
            "pH": round(ph_com_erro, 2)
        }
    }
    historico_biorreator.append(dados_ciclo)

    # Espera 10 segundos antes da próxima leitura
    #time.sleep(intervalo_leitura)

# Criar a variável do arquivo json que será gerado
nome_arquivo = 'registros_biorreator.json'
# Abre (ou cria) o arquivo em modo de escrita ("w") com codificação UTF-8 (Garante que caracteres com acento (como °C, horário, etc.) não fiquem corrompidos.)
if not os.path.exists(nome_arquivo):
    print("Criando arquivo JSON")
    with open(nome_arquivo, "w", encoding = "utf-8") as arquivo:
    # Escreve a lista completa no arquivo formato JSON
    # O "ensure_ascii=False" Permite salvar acentos e símbolos diretamente
    # O "indent=4" adiciona recuo ao aquivo para tornar ele mais fácil de ler
        json.dump(historico_biorreator, arquivo, indent=4, ensure_ascii=False)

    #Se quiser salvar novos dados em um arquivo pré-existente, executar esse código
#else:
#    print("Carregando dados no arquivo", nome_arquivo)
#    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
#        historico_biorreator = json.load(arquivo)

else:
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        print("Sobreescrevendo dados do arquivo", nome_arquivo)
        json.dump(historico_biorreator, arquivo, indent=4, ensure_ascii=False)
    
# Exibe a lista final com todos os dicionários salvos
print("Leitura finalizada")
for registro in historico_biorreator:
    print(registro)
