import random
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
    temperatura_com_erro = temperatura_atual + erro_sensor

    print(
        f"Ciclo {ciclo}/{total_ciclos} | Horário: {hora_str} | Temp. Lida: {temperatura_com_erro:.2f} °C"
    )

    # Lógica de controle do Biorreator (Atuadores: Resfriador)
    if temperatura_com_erro > SETPOINT:
        print("  -> Status: Temperatura alta.\nLIGANDO O RESFRIADOR")
        temperatura_atual -= random.uniform(-1, 1)  # Resfria aleatóriamente em um intervalo de 1°C por ciclo
    elif temperatura_com_erro < SETPOINT:
        print(
            "  -> Status: Temperatura baixa. DESLIGANDO RESFRIADOR"
        )
        temperatura_atual += random.uniform(-1, 1)  # Aquece 1°C por ciclo
    else:
        print("  -> Status: Temperatura no setpoint. Sistema estabilizado.")

    # Armazena as informações do ciclo em um dicionário dentro da lista
    dados_ciclo = {
        "data": data_str,
        "hora": hora_str,
        "temperatura": round(temperatura_com_erro, 2),
    }
    historico.append(dados_ciclo)

    print("-" * 50)

    # Espera 10 segundos antes da próxima leitura
    time.sleep(INTERVALO_LEITURA)

# Exibe a lista final com todos os dicionários salvos
print("\n--- HISTÓRICO FINAL ARMAZENADO ---")
for registro in historico:
    print(registro)
