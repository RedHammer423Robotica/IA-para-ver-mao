<div align="center">

# 🖐️ Controle por Gestos

### Sistema de visão computacional para controle de robótica

<br>

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-Visão_Computacional-5C3EE8?style=for-the-badge\&logo=opencv\&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand_Tracking-FF6F00?style=for-the-badge)
![Serial](https://img.shields.io/badge/Serial-Bluetooth-0082FC?style=for-the-badge)

<br>

**Controle de um sistema robótico utilizando movimentos da mão detectados pela câmera.**

</div>

---

## 📌 Sobre o projeto

Este projeto utiliza a **câmera do computador** para detectar a mão do usuário e interpretar a posição dos dedos.

Através da biblioteca **MediaPipe**, o sistema identifica os pontos da mão e determina se determinados dedos estão levantados.

Após interpretar o gesto, o programa envia comandos através de uma conexão **serial/Bluetooth** para outro dispositivo responsável pelo controle do robô.

Os principais comandos enviados são:

```text
GIRAR
PARAR
```

---

## 🧠 Como funciona?

O sistema possui três etapas principais:

```text
┌─────────────────┐
│     CÂMERA      │
│                 │
│ Captura imagem  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    MEDIAPIPE    │
│                 │
│ Detecta a mão   │
│ e seus pontos   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     GESTO       │
│                 │
│ Analisa dedos   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     PYTHON      │
│                 │
│ Envia comando   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ ESP32 / ROBÔ    │
│                 │
│ GIRAR / PARAR   │
└─────────────────┘
```

---

# 📂 Arquivos

O projeto possui três programas principais:

| Arquivo     | Função                                             |
| ----------- | -------------------------------------------------- |
| `mao.py`    | Detecta a mão e controla através do dedo indicador |
| `maoCor.py` | Detecta uma cor específica + gestos da mão         |
| `verCor.py` | Ferramenta para calibrar valores HSV               |

---

# 🖐️ `mao.py`

Este é o programa básico de controle por gestos.

Ele utiliza:

* OpenCV
* MediaPipe
* Comunicação Serial
* Webcam

O programa verifica a posição do **dedo indicador**.

### Indicador levantado

```text
☝️
```

Envia:

```text
GIRAR
```

### Indicador abaixado

```text
✊
```

Envia:

```text
PARAR
```

A comunicação é realizada através da porta:

```python
ser = serial.Serial("COM4", 115200)
```

> Caso sua porta seja diferente, altere `COM4` para a porta correspondente ao dispositivo.

---

# 🎨 `maoCor.py`

Esta é uma versão mais avançada do sistema.

Além de detectar a mão, o programa verifica se existe uma **cor específica dentro da região da mão**.

O processamento acontece em duas etapas:

```text
        CÂMERA
           │
           ▼
     Detecta a mão
           │
           ▼
     Verifica a cor
           │
      ┌────┴────┐
      │         │
   Detectou   Não detectou
      │         │
      ▼         ▼
 Analisa       Ignora
  gesto
      │
      ▼
 GIRAR/PARAR
```

---

## 🎨 Detecção de cor

A cor é definida através do espaço de cores **HSV**.

No código:

```python
lower_color = np.array([40, 50, 50])
upper_color = np.array([80, 255, 255])
```

Esses valores determinam o intervalo da cor que será reconhecida.

O sistema cria uma máscara:

```python
mask = cv2.inRange(
    hsv,
    lower_color,
    upper_color
)
```

Depois verifica quantos pixels daquela cor existem na região da mão.

---

# ✌️ Gesto utilizado

O `maoCor.py` verifica dois dedos:

### Indicador

```python
indicador_levantado = (
    handLms.landmark[8].y <
    handLms.landmark[6].y
)
```

### Dedo médio

```python
meio_levantado = (
    handLms.landmark[12].y <
    handLms.landmark[10].y
)
```

Para enviar `GIRAR`, os **dois dedos precisam estar levantados**:

```python
if indicador_levantado and meio_levantado:
    ser.write(b"GIRAR\n")
```

Caso contrário:

```python
ser.write(b"PARAR\n")
```

---

# 🔍 Pontos da mão

O MediaPipe identifica diversos pontos da mão.

Os principais utilizados neste projeto são:

```text
        8  ← ponta do indicador
        │
        6  ← base do indicador

        12 ← ponta do dedo médio
        │
        10 ← base do dedo médio
```

A comparação da coordenada `Y` permite determinar se o dedo está levantado.

```text
        Ponta
          ●
          │
          │
          ●
         Base

Ponta.y < Base.y
       ↓
 Dedo levantado
```

---

# 🎛️ `verCor.py`

O arquivo `verCor.py` é uma ferramenta auxiliar para encontrar os valores HSV da cor desejada.

Ele abre uma janela com controles:

```text
L-H
L-S
L-V

U-H
U-S
U-V
```

Onde:

* `L-H` → Hue mínimo
* `L-S` → Saturation mínimo
* `L-V` → Value mínimo
* `U-H` → Hue máximo
* `U-S` → Saturation máximo
* `U-V` → Value máximo

---

## 🧪 Como calibrar uma cor

Execute:

```bash
python verCor.py
```

Ajuste as barras até que a máscara mostre apenas a cor desejada.

Quando encontrar uma configuração adequada, pressione:

```text
Q
```

O programa mostrará no terminal algo semelhante a:

```python
lower_color = np.array([40, 50, 50])
upper_color = np.array([80, 255, 255])
```

Copie esses valores para `maoCor.py`.

---

# 📦 Instalação

## 1. Verifique o Python

```bash
python --version
```

ou:

```bash
py --version
```

---

## 2. Instale as bibliotecas

Execute:

```bash
pip install opencv-python
```

```bash
pip install mediapipe
```

```bash
pip install pyserial
```

```bash
pip install numpy
```

Ou tudo de uma vez:

```bash
pip install opencv-python mediapipe pyserial numpy
```

---

# ▶️ Executando

Entre na pasta do projeto:

```bash
cd PROGRAMACAO
```

Para executar o controle básico:

```bash
python mao.py
```

Para executar o controle com identificação de cor:

```bash
python maoCor.py
```

Para calibrar a cor:

```bash
python verCor.py
```

---

# 📡 Comunicação

Os comandos são enviados pela comunicação serial:

```python
ser.write(b"GIRAR\n")
```

e:

```python
ser.write(b"PARAR\n")
```

O `b` indica que o texto está sendo enviado como **bytes**, formato utilizado pela comunicação serial.

O `\n` indica o final do comando.

### Comando enviado

```text
GIRAR\n
```

### Comando para parar

```text
PARAR\n
```

---

# ⚙️ Configuração da porta

Atualmente os programas utilizam:

```python
ser = serial.Serial("COM4", 115200)
```

Se o dispositivo estiver em outra porta, altere:

```python
"COM4"
```

Por exemplo:

```python
ser = serial.Serial("COM10", 115200)
```

A velocidade utilizada é:

```text
115200 baud
```

---

# 📷 Webcam

O projeto utiliza a câmera padrão do computador:

```python
cap = cv2.VideoCapture(0)
```

Caso possua mais de uma câmera, pode ser necessário alterar o número:

```python
cap = cv2.VideoCapture(1)
```

ou:

```python
cap = cv2.VideoCapture(2)
```

---

# 🖥️ Interface

Durante a execução, uma janela chamada:

```text
Camera
```

mostra a imagem capturada pela webcam.

O MediaPipe desenha os pontos e conexões da mão sobre a imagem.

No modo com detecção de cor, também podem aparecer mensagens como:

```text
GIRAR
```

```text
PARAR
```

ou:

```text
COR NAO DETECTADA
```

---

# 🛑 Encerrando o programa

Para fechar o sistema, pressione:

```text
Q
```

A câmera será liberada e as janelas serão fechadas.

---

# 🗂️ Estrutura

```text
PROGRAMACAO/
│
├── mao.py
│
├── maoCor.py
│
├── verCor.py
│
└── README.md
```

---

# 🔧 Tecnologias

<div align="center">

|   Tecnologia  | Utilização                             |
| :-----------: | -------------------------------------- |
|   🐍 Python   | Linguagem principal                    |
|   👁️ OpenCV  | Captura e processamento de imagens     |
| 🖐️ MediaPipe | Detecção dos pontos da mão             |
|    🎨 NumPy   | Processamento dos dados e máscaras HSV |
|  📡 PySerial  | Comunicação serial/Bluetooth           |
|   📷 Webcam   | Entrada de vídeo                       |

</div>

---

# 🚀 Possíveis melhorias

O projeto pode ser expandido para reconhecer diversos comandos:

```text
☝️  → GIRAR
✌️  → PARAR
✋  → FRENTE
👊  → TRÁS
👍  → PEGAR
👎  → SOLTAR
```

Também é possível adicionar:

* 🤖 Controle de múltiplos motores
* 📡 Comunicação Bluetooth
* 📶 Wi-Fi
* 🎯 Reconhecimento de objetos
* 🎨 Mais cores
* 🖐️ Reconhecimento de diferentes gestos
* ⚙️ Controle de velocidade
* 🔄 Controle de servos
* 📊 Interface gráfica

---

# 🧩 Projeto de Robótica

Este sistema foi desenvolvido como parte de um projeto de **robótica e automação**, utilizando visão computacional para transformar movimentos humanos em comandos para um sistema robótico.

<div align="center">

### 🖐️ + 👁️ + 🤖

**Visão computacional → Interpretação → Controle robótico**

<br>

⭐ Desenvolvido para projetos de robótica e automação.

</div>
```

Esse README já está direcionado **exatamente para os arquivos que vieram no ZIP**, em vez de descrever o projeto de forma genérica.
