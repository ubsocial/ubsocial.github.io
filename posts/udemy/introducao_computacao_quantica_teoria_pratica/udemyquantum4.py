# pip3 install qiskit qiskit-aer qiskit[visualization]
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

qc = QuantumCircuit(2, 2)

qc.h(0)
qc.cx(0, 1)

qc.measure([0, 1], [0, 1])

print("Quantum Circuit:")
qc.draw('mpl')

sim = AerSimulator()
job = sim.run(qc, shots=1024)
result = job.result()
counts = result.get_counts()

print("Counts:")
print(counts)

fig = plot_histogram(counts)
display(fig)