# pip3 install qiskit qiskit-aer numpy qiskit[visualization]
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

n_qubits = 9
qc = QuantumCircuit(n_qubits, 4)

erro_real = np.zeros(n_qubits, dtype=int)
erro_real[4] = 1 # erro no centro

if erro_real[4]:
    qc.x(4)

print("Erro real:", erro_real)

# Estabilizadores Z (paridade), onde cada mede 4:
stabilizers = [
    [0,1,3,4], # topo-esquerda
    [1,2,4,5], # topo-direita
    [3,4,6,7], # baixo-esquerda
    [4,5,7,8]  # baixo-direita
]

# Medição de paridade (XOR clássico)
def medir_sindrome(erro, stabilizers):
    syndrome = []
    for stab in stabilizers:
        parity = sum(erro[q] for q in stab) % 2
        syndrome.append(parity)
    return np.array(syndrome)

syndrome = medir_sindrome(erro_real, stabilizers)

print("Síndrome:", syndrome)
qc.draw("mpl")

# Decodificação:
lookup = &#123;
    (1,0,0,0): 0,
    (1,1,0,0): 1,
    (0,1,0,0): 2,
    (1,0,1,0): 3,
    (1,1,1,1): 4,
    (0,1,0,1): 5,
    (0,0,1,0): 6,
    (0,0,1,1): 7,
    (0,0,0,1): 8
&#125; # Mapeamento manual (d=3)

key = tuple(syndrome)
correcao = np.zeros(n_qubits, dtype=int)

if key in lookup:
    qubit_corrigir = lookup[key]
    correcao[qubit_corrigir] = 1

print("Correção:", correcao)

residual = (erro_real + correcao) % 2
print("Erro residual:", residual)

if np.sum(residual) == 0:
    print("Corrigido")
else:
    print("Falha")