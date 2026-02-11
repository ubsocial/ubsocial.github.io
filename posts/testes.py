# pip3 install qiskit qiskit-ibm-runtime qiskit-aer matplotlib qiskit[visualization]
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel
from qiskit.primitives import BackendSamplerV2
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from IPython.display import display
import matplotlib.pyplot as plt
import numpy as np
QiskitRuntimeService.save_account(token="SEU_TOKEN_AQUI")


# ========================================================================
rng = np.random.default_rng()
bit_num = 20
qc = QuantumCircuit(bit_num, bit_num)
 
# QKD step 1: Random bits and bases for Alice
abits = np.round(rng.random(bit_num))
abase = np.round(rng.random(bit_num))
 



# Alice's state preparation. Check that this creates states according to table 1
for n in range(bit_num):
    if abits[n] == 0:
        if abase[n] == 1:
            qc.h(n)
    if abits[n] == 1:
        if abase[n] == 0:
            qc.x(n)
        if abase[n] == 1:
            qc.x(n)
            qc.h(n)
qc.barrier()
 




# QKD step 2: Random bases for Bob
bbase = np.round(rng.random(bit_num))

for m in range(bit_num):
    if bbase[m] == 1:
        qc.h(m)
    qc.measure(m, m)



print("Alice's bits are ", abits)
print("Alice's bases are ", abase)
print("Bob's bases are ", bbase)
display(qc.draw("mpl"))




service = QiskitRuntimeService()
backend = service.least_busy(operational=True, simulator=False, min_num_qubits = 127)
print(backend.name)

 
 
noise_model = NoiseModel.from_backend(backend)
backend_sim = AerSimulator(noise_model=noise_model)
sampler_sim = BackendSamplerV2(backend=backend_sim)


target = backend.target
pm = generate_preset_pass_manager(target=target, optimization_level=3)
qc_isa = pm.run(qc)



# This required 5 s to run on a Heron r2 processor on 10-28-24
sampler = Sampler(mode=backend)
job = sampler.run([qc_isa], shots=1)
# job = sampler_sim.run([qc], shots = 1)
counts = job.result()[0].data.c.get_counts()
countsint = job.result()[0].data.c.get_int_counts()





# Get an array of bits 
keys = counts.keys()
key = list(keys)[0]
bmeas = list(key)
bmeas_ints = []
for n in range(bit_num):
    bmeas_ints.append(int(bmeas[n]))
 
bbits = bmeas_ints[::-1]
print(bbits)






# QKD step 3: Public discussion of bases
agoodbits = []
bgoodbits = []
match_count = 0
for n in range(bit_num):
    # Check whether bases matched.
    if abase[n] == bbase[n]:
        agoodbits.append(int(abits[n]))
        bgoodbits.append(bbits[n])
        # If bits match when bases matched, increase count of matching bits
        if int(abits[n]) == bbits[n]:
            match_count += 1
 
print(agoodbits)
print(bgoodbits)
print("fidelity = ", match_count / len(agoodbits))
print("loss = ", 1 - match_count / len(agoodbits))