# Test Double do NeonFC-SSL

## Descrição

Este projeto é um Test Double do NeonFC-SSL, software de tomada de decisão para robôs de futebol da categoria Small Size League (SSL) da equipe Project Neon.

Seu objetivo é simular os comportamentos do NeonFC-SSL para desenvolver e testar a GUI que futuramente será utilizada junto ao software de tomada de decisão. O Test Double envia dados fictícios da partida, da bola e dos robôs e recebe as configurações definidas na interface.

Ele não substitui completamente o NeonFC-SSL e não deve ser utilizado para validar a lógica real de tomada de decisão dos robôs.

## Instalação

Esse projeto foi desenvolvido para Ubuntu e recomenda-se utilizar Python 3.12.x. O Test Double não possui dependências adicionais.

Clone o repositório e acesse sua pasta:

```bash
git clone https://github.com/Ana-Monici/Test_Double_Neon_SSL.git
cd TestDoubleNeonFC
```

## Uso com a GUI

A comunicação utiliza sockets TCP. A GUI atua como servidor em localhost:9999, enquanto o Test Double atua como cliente.

Primeiro, execute a GUI em seu repositório raiz:

```bash
python gui.py
```

Em outro terminal, execute o Test Double:

```bash
python main.py
```

A GUI deve ser iniciada primeiro, pois o Test Double ainda não possui reconexão automática. O endereço e a porta utilizados na conexão podem ser alterados no arquivo config.json.

