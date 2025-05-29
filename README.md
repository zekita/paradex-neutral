# paradex-neutral
It automatically rebalances your positions to a delta neutral. The scope is to exposure to perpetual options points while getting no directional risk by auto neutralizing it  with equivalent in perpetual futures positions 


# 🤖 Bot de Hedge Delta-Neutro - Paradex

Bot automatizado para hedging delta-neutro em derivativos na plataforma Paradex.

## ⚡ Funcionalidades

- 📊 Monitora posições em tempo real
- 🎯 Calcula delta total do portfólio  
- ⚖️ Executa hedge automático quando necessário
- 🔄 Loop contínuo com intervalo configurável
- 📈 Identifica automaticamente mercado PERP para hedge

## 🛠️ Configuração

### 1. Instalar Dependências

```bash
pip install paradex-py python-dotenv requests
```

### 2. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
L1_ADDRESS=sua_carteira_ethereum_aqui
L1_PRIVATE_KEY=sua_chave_privada_aqui
```

### 3. Configurações do Bot

Edite as configurações no `main.py`:

```python
DELTA_THRESHOLD = 0.0000001  # Tolerância para desequilíbrio
SLEEP_INTERVAL = 5          # Intervalo entre execuções (segundos)
```

## 🚀 Execução

```bash
python main.py
```

## ⚠️ **AVISOS IMPORTANTES DE SEGURANÇA**

### 🔒 **NUNCA FAÇA:**
- ❌ **Não compartilhe seu arquivo `.env`**
- ❌ **Não commite chaves privadas no git**
- ❌ **Não deixe credenciais hardcoded no código**

### ✅ **SEMPRE FAÇA:**
- ✅ Use variáveis de ambiente para dados sensíveis
- ✅ Teste primeiro no ambiente TESTNET
- ✅ Use `.gitignore` para proteger o `.env`
- ✅ Monitore suas posições e ordens

## 🧪 Testnet

Para testar, altere a configuração:

```python
env="testnet"  # em vez de "prod"
```

## 📖 Documentação

- [Paradex Python SDK](https://tradeparadex.github.io/paradex-py/)
- [Paradex API](https://docs.paradex.trade/api-reference/)

## ⚖️ Disclaimer

**Este bot executa ordens reais de trading com dinheiro real.**

- Use por sua conta e risco
- Teste extensivamente no testnet primeiro
- Monitore constantemente durante operação
- O autor não se responsabiliza por perdas

## 📝 Licença

MIT License - Use como quiser, mas sem garantias.

---

**🚨 LEMBRE-SE: Trading automatizado envolve riscos financeiros significativos.** 
