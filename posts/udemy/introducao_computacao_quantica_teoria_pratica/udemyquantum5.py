# Arquivo CSV de dataset: https://raw.githubusercontent.com/qiskit-community/prototype-quantum-kernel-training/main/data/dataset_graph7.csv
# pip3 install qiskit qiskit-ibm-runtime pandas numpy
from qiskit import transpile
from qiskit.circuit import Parameter, ParameterVector, QuantumCircuit
from qiskit.circuit.library import unitary_overlap
from qiskit.primitives import StatevectorSampler
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
import pandas as pd
import numpy as np

QiskitRuntimeService.save_account(token="SEU_TOKEN_IBM_AQUI")

def get_training_data():
  df = pd.read_csv("dataset_graph7.csv", sep=",", header=None)
  training_data = df.values[:20,:]
  ind = np.argsort(training_data[:,-1])
  X_train = training_data[ind][:, :-1]
  return X_train

X_train = get_training_data()
num_samples = np.shape(X_train)[0]

num_features = np.shape(X_train)[1]
num_qubits =  int(num_features / 2)
entangler_map = [[0,2], [3,4], [2,5], [1,4], [2,3], [4,6]]

fm = QuantumCircuit(num_qubits)
training_param = Parameter("0")
feature_params = ParameterVector("x", num_qubits * 2)
fm.ry(training_param, fm.qubits)

for cz in entangler_map:
  fm.cz(cz[0], cz[1])

for i in range(num_qubits):
  fm.rz(-2 * feature_params[2 * i+1], i)
  fm.rx(-2 * feature_params[2 * i], i)

x1 = 14
x2 = 19
unitary1 = fm.assign_parameters(list(X_train[x1]) + [np.pi / 2])
unitary2 = fm.assign_parameters(list(X_train[x2]) + [np.pi / 2])

overlap_circ = unitary_overlap(unitary1, unitary2)
overlap_circ.measure_all()
overlap_circ.draw(scale=0.6, style="iqp")

service = QiskitRuntimeService()
backend = service.least_busy(operational=True, simulator=False, min_num_qubits=127)
print("Backend quântico:", backend.name)

target = backend.target
pm = generate_preset_pass_manager(target=target, optimization_level=3)
job = pm.run(overlap_circ)

num_shots = 10_000
sampler = StatevectorSampler()
counts = (sampler.run([overlap_circ], shots=num_shots).result()[0].data.meas.get_int_counts())

counts.get(0, 0.0) / num_shots