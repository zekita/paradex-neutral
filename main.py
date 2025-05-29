from paradex_py import Paradex

from paradex_py.common.order import Order, OrderSide, OrderType
import os
from dotenv import load_dotenv
import time
import requests
import traceback
from decimal import Decimal, ROUND_DOWN

load_dotenv()

paradex = Paradex(
    env="prod",  # Correto: string, não enum
    l1_address=os.getenv("L1_ADDRESS"),
    l1_private_key=os.getenv("L1_PRIVATE_KEY")
)


# Configurações

DELTA_THRESHOLD = 0.0000001  # Ignora desequilíbrios pequenos
SLEEP_INTERVAL = 5  # Intervalo entre execuções (em segundos)

def infer_hedge_market(base_asset):
    try:
        all_markets = requests.get("https://api.prod.paradex.trade/v1/markets").json()["results"]
    except Exception as e:
        print(f"[!] Erro ao buscar lista de mercados: {e}")
        return None

    for m in all_markets:
        if m.get("asset_kind") == "PERP" and m.get("base_currency") == base_asset:
            return m.get("symbol")
    return None



def get_market_delta(market):
    url = f"https://api.prod.paradex.trade/v1/markets/summary?market={market}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            results = response.json().get("results", [])
            if results and "greeks" in results[0]:
                return float(results[0]["greeks"].get("delta", 0))
    except Exception as e:
        print(f"[!] Erro ao buscar gregos de {market}: {e}")
    return 0.0

def get_positions():
    try:
        res = paradex.api_client.fetch_positions()
        return res.get("results", [])
    except Exception as e:
        print(f"[!] Erro ao buscar posições: {e}")
        return []

def calculate_total_delta(positions):
    time.sleep(2)
    total_deltas = {}

    for pos in positions:
        market = pos.get("market", "")
        signed_size = float(pos.get("size", 0))
        base = market.split("-")[0]

        delta = get_market_delta(market)
        contribution = signed_size * delta
        total_deltas[base] = total_deltas.get(base, 0.0) + contribution

    # Seleciona o ativo com maior exposição (módulo do delta)
    if not total_deltas:
        return None, None

    best_base = max(total_deltas.items(), key=lambda x: abs(x[1]))[0]
    return round(total_deltas[best_base], 6), best_base


def hedge(delta, hedge_market, all_markets):
    if abs(delta) < DELTA_THRESHOLD:
        print(f"Δ {delta:.6f} → dentro da tolerância. Nenhuma ação.")
        return

    try:
        # Encontra info do mercado com base no symbol
        market_info = next((m for m in all_markets if m.get("symbol") == hedge_market), None)
        if not market_info:
            print(f"[!] Mercado '{hedge_market}' não encontrado. Ordem cancelada.")
            return

        side = OrderSide.Sell if delta > 0 else OrderSide.Buy
        raw_size = Decimal(str(abs(delta)))

        # Usa o incremento correto do par (ex: 1, 0.01, 0.001...)
        size_increment = Decimal(market_info.get("order_size_increment", "0.001"))
        size = raw_size.quantize(size_increment, rounding=ROUND_DOWN)

        if size < size_increment:
            print(f"[!] Size {size} abaixo do mínimo permitido ({size_increment}). Ordem não enviada.")
            return

        order = Order(
            market=hedge_market,
            order_type=OrderType.Market,
            order_side=side,
            size=size
        )

        print("[DEBUG] Ordem construída:")
        print(order.__dict__)
        resp = paradex.api_client.submit_order(order)
        print(f"[+] Ordem hedge enviada: {side.name} {size} no {hedge_market}")

    except Exception as e:
        print(f"[!] Erro ao enviar ordem de hedge: {e}")
        traceback.print_exc()



def main():
    print("===> Iniciando loop de hedge delta-neutro <===")
    while True:
        try:
            positions = get_positions()
            delta, base = calculate_total_delta(positions)
            if delta is None or base is None:
                print("[!] Nenhuma posição com delta relevante. Pulando...")
                continue

            hedge_market = infer_hedge_market(base)
            if hedge_market is None:
                print(f"[!] Nenhum PERP correspondente encontrado para {base}. Pulando...")
                continue

            all_markets = paradex.api_client.fetch_markets()["results"]  # pega atualizado
            print(f"Δ total: {delta:.6f}")
            hedge(delta, hedge_market, all_markets)

        except Exception as e:
            print(f"[!] Erro no loop principal: {type(e).__name__}: {e}")
            traceback.print_exc()

        time.sleep(SLEEP_INTERVAL)

if __name__ == "__main__":
    main()
