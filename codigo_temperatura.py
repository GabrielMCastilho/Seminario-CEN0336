import random
import time
from datetime import datetime

# 1. Parâmetros fixos do sistema
SETPOINT = 24.0  # Temperatura desejada (°C)
INTERVALO_LEITURA = 10  # segundos
TEMPO_TOTAL = 120  # 2 minutos em segundos

# 2. Variavel com o intervalo de temperatura inicial (18 a 30 °C)
# Sorteamos a temperatura inicial da faixa
temperatura_atual = random.randint(18, 30)

# Lista para armazenar o histórico
historico = []

print("--- INICIANDO CONTROLE DO BIORREATOR ---")
print(f"Temperatura Inicial Sorteada: {temperatura_atual:.2f} °C\n")

# Calculamos quantos ciclos vão rodar (120 / 10 = 12 ciclos)
total_ciclos = TEMPO_TOTAL // INTERVALO_LEITURA

# Loop de controle
for ciclo in range(1, total_ciclos + 1):
    # Pega data e hora atual do ciclo
    agora = datetime.now()
    data_str = agora.strftime("%Y-%m-%d")
    hora_str = agora.strftime("%H:%M:%S")

    # Adiciona um erro aleatório no sensor (entre -0.5°C e +0.5°C)
    erro_sensor = random.uniform(-0.5, 0.5)
    temperatura_com_erro = temperatura_atual + erro_sensor

    print(
        f"Ciclo {ciclo}/{total_ciclos} | Horário: {hora_str} | Temp. Lida: {temperatura_com_erro:.2f} °C"
    )

    # Lógica de controle do Biorreator (Atuadores: Resfriador ou Aquecedor)
    if temperatura_com_erro > SETPOINT:
        print("  -> Status: Temperatura alta. LIGANDO O RESFRIADOR (Chiller)...")
        temperatura_atual -= 1.0  # Resfria 1°C por ciclo
    elif temperatura_com_erro < SETPOINT:
        print(
            "  -> Status: Temperatura baixa. LIGANDO O AQUECEDOR (Resistência)..."
        )
        temperatura_atual += 1.0  # Aquece 1°C por ciclo
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
