# ------------------ NOTEBOOK BÁSICO ------------------
!pip3 install qiskit-braket-provider

import qiskit_braket_provider
from qiskit import QuantumCircuit
from qiskit_braket_provider import BraketLocalBackend, AWSBraketProvider
from qiskit.visualization import plot_histogram

circuit = QuantumCircuit(3)
circuit.h(0) # Apply H-gate to the first qubit

# Apply a CNOT to each qubit:
for qubit in range(1, 3):
    circuit.cx(0, qubit)

circuit.draw('mpl')


local_simulator = BraketLocalBackend()
task = local_simulator.run(circuit, shots=1000)
plot_histogram(task.result().get_counts())




provider = AWSBraketProvider()

# devices
ionq_device = provider.get_backend("IonQ Device")
rigetti_device = provider.get_backend("Aspen-M-1")
oqc_device = provider.get_backend("Lucy")


ionq_task = ionq_device.run(circuit, shots=100)
ionq_arn = ionq_task.job_id()

ionq_retrieved = ionq_device.retrieve_job(job_id=ionq_arn)
ionq_retrieved.status()

plot_histogram(retrieved_job.result().get_counts())



rigetti_task = rigetti_device.run(circuit, shots=100)
rigetti_retrieved = rigetti_device.retrieve_job(job_id=rigetti_task.job_id()) # retrieve task by ID

plot_histogram(rigetti_retrieved.result().get_counts())



oqc_task = oqc_device.run(circuit, shots=100)
oqc_retrieved = oqc_device.retrieve_job(job_id=oqc_task.job_id()) # retrieve task by ID

plot_histogram(oqc_retrieved.result().get_counts())




# ----------- COMPUTAÇÃO HÍBRIDA -----------
