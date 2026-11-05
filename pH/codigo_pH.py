import random
import time
from datetime import datetime

# 1. Parâmetros fixos do sistema
SETPOINT_PH = 7.0  # pH ótimo neutro para bactérias
INTERVALO_LEITURA = 10  # segundos
TEMPO_TOTAL = 120  # 2 minutos (12 ciclos)

# 2. Variavel com o intervalo de pH inicial (faixa ampla de 5.5 a 8.5)
# Sorteamos um pH inicial realista
ph_atual = round(random.uniform(5.5, 8.5), 2)

# Lista para armazenar o histórico
historico_ph = []

print("--- INICIANDO CONTROLE DE pH DO BIORREATOR ---")
print(f"pH Inicial Sorteado: {ph_atual:.2f} (Setpoint Ótimo: {SETPOINT_PH})\n")

total_ciclos = TEMPO_TOTAL // INTERVALO_LEITURA

# Loop de controle
for ciclo in range(1, total_ciclos + 1):
    agora = datetime.now()
    data_str = agora.strftime("%Y-%m-%d")
    hora_str = agora.strftime("%H:%M:%S")

    # Ruído aleatório de leitura do eletrodo de pH (+- 0.05)
    erro_sensor = random.uniform(-0.05, 0.05)
    ph_com_erro = ph_atual + erro_sensor

    print(
        f"Ciclo {ciclo}/{total_ciclos} | Horário: {hora_str} | pH Lido: {ph_com_erro:.2f}"
    )

    # Lógica de controle do Biorreator (Atuadores: Bombas Peristálticas)
    if ph_com_erro < SETPOINT_PH - 0.1:
        print("  -> Status: Meio ácido. BOMBA DE BASE LIGADA (Injetando NaOH)...")
        ph_atual += 0.2  # Adiciona base para elevar o pH
    elif ph_com_erro > SETPOINT_PH + 0.1:
        print(
            "  -> Status: Meio alcalino. BOMBA DE ÁCIDO LIGADA (Injetando HCl)..."
        )
        ph_atual -= 0.2  # Adiciona ácido para reduzir o pH
    else:
        print("  -> Status: pH na faixa ótima. Bombas desligadas.")

    # Armazena as informações do ciclo
    dados_ciclo = {
        "data": data_str,
        "hora": hora_str,
        "ph": round(ph_com_erro, 2),
    }
    historico_ph.append(dados_ciclo)

    print("-" * 50)
    time.sleep(INTERVALO_LEITURA)

# Exibe a lista final com todos os dicionários salvos
print("\n--- HISTÓRICO FINAL DE pH ARMAZENADO ---")
for registro in historico_ph:
    print(registro)
