import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eig

# Definir la matriz A
A = np.array([[0.1, 0.4],
              [0.4, -0.1]])

# Definir el vector B (si no existe dejar None)
B = None
# B = np.array([-5, -7])
# B = None

# Calcular el punto de equilibrio
def calculate_equilibrium_point(A, B=None):
    if B is None:
        return np.array([0, 0])
    return np.dot(np.linalg.pinv(A), -B)

equilibrium_point = calculate_equilibrium_point(A, B)

# Calcular valores propios y vectores propios
eigenvalues, eigenvectors = eig(A)

def simplify_vector(vector):
    vector = np.round(vector, decimals=5)
    absolute_vector = np.abs(vector)
    if np.any(absolute_vector > 1e-5):  # Simplificar solo si hay valores significativos
        min_nonzero = absolute_vector[absolute_vector > 1e-5].min()
        vector = (vector / min_nonzero).astype(int)
        if vector[0] < 0:  # Normalizar el signo para que el primer componente sea positivo
            vector = -vector
    return vector

# Mostrar valores propios y simplificar los vectores propios
print("Valores propios (solo parte real):")
for i, eigenvalue in enumerate(eigenvalues):
    print(f"\nλ{i + 1} = {eigenvalue.real}")

    # Obtener y simplificar el vector propio
    vector = eigenvectors[:, i].real
    vector = simplify_vector(vector)
    print(f"Vector propio simplificado V{i + 1}: {vector}")

# Asignar los vectores propios simplificados a V1 y V2
V1 = simplify_vector(eigenvectors[:, 0].real)
V2 = simplify_vector(eigenvectors[:, 1].real)

# Determinar el tipo de sistema
def classify_system(eigenvalues):
    real_parts = np.real(eigenvalues)
    if np.all(real_parts > 0):
        return "Nodo Inestable (valores propios reales y positivos)"
    elif np.all(real_parts < 0):
        return "Nodo Estable (valores propios reales y negativos)"
    elif np.any(real_parts > 0) and np.any(real_parts < 0):
        return "Punto Silla (valores propios reales de signos opuestos)"
    elif np.all(real_parts == 0):
        return "Centro (valores propios puramente imaginarios)"
    elif np.all(real_parts < 0):
        return "Foco Estable (valores propios complejos con parte real negativa)"
    elif np.all(real_parts > 0):
        return "Foco Inestable (valores propios complejos con parte real positiva)"
    else:
        return "Caso Indeterminado"

system_type = classify_system(eigenvalues)
print("\nTipo de sistema:", system_type)
print("Punto de equilibrio:", equilibrium_point)

# Función para graficar las trayectorias
def plot_phase_portrait(A, V1, V2, equilibrium_point, B=None):
    eigenvalues, _ = eig(A)
    max_eigenvalue = max(np.abs(eigenvalues.real))
    axis_limit = max(3, max_eigenvalue * 1.5)  # Aumentar el rango para mejor visualización
    x_vals = np.linspace(-axis_limit, axis_limit, 20) + equilibrium_point[0]
    y_vals = np.linspace(-axis_limit, axis_limit, 20) + equilibrium_point[1]
    X, Y = np.meshgrid(x_vals, y_vals)
    # Ajustar el campo de direcciones según si B está definido o no
    U = A[0, 0] * (X - equilibrium_point[0]) + A[0, 1] * (Y - equilibrium_point[1]) + (B[0] if B is not None else 0)
    V = A[1, 0] * (X - equilibrium_point[0]) + A[1, 1] * (Y - equilibrium_point[1]) + (B[1] if B is not None else 0)

    fig, ax = plt.subplots()
    ax.streamplot(X, Y, U, V, color='b', density=1.2, linewidth=0.8)

    # Graficar los vectores propios desde el punto de equilibrio
    ax.quiver(equilibrium_point[0], equilibrium_point[1], V1[0], V1[1], angles='xy', scale_units='xy', scale=1, color='r', label=f"V1 {V1}")
    ax.quiver(equilibrium_point[0], equilibrium_point[1], V2[0], V2[1], angles='xy', scale_units='xy', scale=1, color='g', label=f"V2 {V2}")

    ax.set_title("Diagrama de Fase con Vectores Propios Simplificados y Punto de Equilibrio")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()
    ax.set_xlim(equilibrium_point[0] - axis_limit, equilibrium_point[0] + axis_limit)
    ax.set_ylim(equilibrium_point[1] - axis_limit, equilibrium_point[1] + axis_limit)
    plt.grid()
    plt.show()

# Graficar el diagrama de fase
plot_phase_portrait(A, V1, V2, equilibrium_point, B)
