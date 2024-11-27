import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eig


def calculate_equilibrium_point(A, B=None):
    if B is None:
        return np.zeros(A.shape[0])
    try:
        return np.linalg.solve(-A, B)
    except np.linalg.LinAlgError:
        return np.dot(np.linalg.pinv(-A), B)


def classify_system(eigenvalues, tol=1e-10):
    real_parts = np.real(eigenvalues)
    imag_parts = np.imag(eigenvalues)

    # Tratar partes reales e imaginarias muy pequeñas como cero
    real_parts[np.abs(real_parts) < tol] = 0
    imag_parts[np.abs(imag_parts) < tol] = 0

    if np.all(imag_parts != 0):  # Valores propios complejos
        if np.all(real_parts == 0):
            return "Centro (valores propios puramente imaginarios)"
        elif np.all(real_parts < 0):
            return "Foco Estable (valores propios complejos con parte real negativa)"
        elif np.all(real_parts > 0):
            return "Foco Inestable (valores propios complejos con parte real positiva)"
    else:  # Valores propios reales
        if np.all(real_parts > 0):
            return "Nodo Inestable (valores propios reales positivos)"
        elif np.all(real_parts < 0):
            return "Nodo Estable (valores propios reales negativos)"
        elif np.any(real_parts > 0) and np.any(real_parts < 0):
            return "Punto Silla (valores propios reales de signos opuestos)"
        elif np.all(real_parts == 0):
            return "Nodo Degenerado (valores propios reales repetidos)"

    return "Caso no clasificado"


def format_complex(complex_number, decimals=2, tolerance=1e-10):
    real = 0 if abs(complex_number.real) < tolerance else round(complex_number.real, decimals)
    imaginary = 0 if abs(complex_number.imag) < tolerance else round(complex_number.imag, decimals)
    if imaginary == 0:
        return f"{real}"
    elif real == 0:
        return f"{imaginary}i"
    elif imaginary > 0:
        return f"{real}+{imaginary}i"
    else:
        return f"{real}{imaginary}i"


def scale_eigenvector(vector):
    norm = np.linalg.norm(vector)
    if norm != 0:
        return vector / norm
    else:
        return vector


def print_general_equation(eigenvalues, eigenvectors, tol=1e-10, decimals=2):
    print("\nEcuación general combinada del sistema:")
    if np.all(np.iscomplex(eigenvalues)) and not np.all(np.imag(eigenvalues) == 0):
        # Suponiendo que hay dos valores propios complejos conjugados
        lambda_real = np.real(eigenvalues[0])
        lambda_imag = np.imag(eigenvalues[0])
        vector = eigenvectors[:, 0]
        c1, c2 = 'C1', 'C2'
        x_eq = (f"({format_complex(vector[0].real)} * {c1} - {format_complex(vector[0].imag)} * {c2}) * "
                f"cos({round(lambda_imag, decimals)}t) - "
                f"({format_complex(vector[0].imag)} * {c1} + {format_complex(vector[0].real)} * {c2}) * "
                f"sin({round(lambda_imag, decimals)}t)")
        y_eq = (f"({format_complex(vector[1].real)} * {c1} - {format_complex(vector[1].imag)} * {c2}) * "
                f"cos({round(lambda_imag, decimals)}t) - "
                f"({format_complex(vector[1].imag)} * {c1} + {format_complex(vector[1].real)} * {c2}) * "
                f"sin({round(lambda_imag, decimals)}t)")
        print(f"x(t) = {x_eq}")
        print(f"y(t) = {y_eq}")
    else:
        # Manejo para valores propios reales
        x_eq_terms = []
        y_eq_terms = []
        for i, eigenvalue in enumerate(eigenvalues):
            vector = eigenvectors[:, i].real
            coef = f"C{i + 1}"
            term_x = f"{coef} * {round(vector[0], decimals)} * e^({round(eigenvalue.real, decimals)}t)"
            term_y = f"{coef} * {round(vector[1], decimals)} * e^({round(eigenvalue.real, decimals)}t)"
            x_eq_terms.append(term_x)
            y_eq_terms.append(term_y)
        x_eq = " + ".join(x_eq_terms)
        y_eq = " + ".join(y_eq_terms)
        print(f"x(t) = {x_eq}")
        print(f"y(t) = {y_eq}")


def plot_extended_vectors(ax, equilibrium_point, V1, V2, axis_limit):
    equilibrium_point = np.array(equilibrium_point)
    t = np.linspace(-axis_limit, axis_limit, 100)
    V1_real = V1.real
    V1_imag = V1.imag
    V1_real_line = equilibrium_point[:, None] + V1_real[:, None] * t
    V1_imag_line = equilibrium_point[:, None] + V1_imag[:, None] * t
    ax.plot(V1_real_line[0], V1_real_line[1], 'r-',
            label=f"V1 real {format_complex(V1_real[0])}, {format_complex(V1_real[1])}")
    ax.plot(V1_imag_line[0], V1_imag_line[1], 'r--',
            label=f"V1 imag {format_complex(V1_imag[0])}, {format_complex(V1_imag[1])}")
    V2_real = V2.real
    V2_imag = V2.imag
    V2_real_line = equilibrium_point[:, None] + V2_real[:, None] * t
    V2_imag_line = equilibrium_point[:, None] + V2_imag[:, None] * t
    ax.plot(V2_real_line[0], V2_real_line[1], 'g-',
            label=f"V2 real {format_complex(V2_real[0])}, {format_complex(V2_real[1])}")
    ax.plot(V2_imag_line[0], V2_imag_line[1], 'g--',
            label=f"V2 imag {format_complex(V2_imag[0])}, {format_complex(V2_imag[1])}")


def plot_phase_portrait(A, V1, V2, equilibrium_point, B=None):
    eigenvalues, _ = eig(A)
    max_eigenvalue = max(np.abs(eigenvalues.real))
    axis_limit = max(3, max_eigenvalue * 2)  # Aumentar el rango para mejor visualización
    x_vals = np.linspace(-axis_limit, axis_limit, 20) + equilibrium_point[0]
    y_vals = np.linspace(-axis_limit, axis_limit, 20) + equilibrium_point[1]
    X, Y = np.meshgrid(x_vals, y_vals)
    # Ajustar el campo de direcciones
    U = A[0, 0] * (X - equilibrium_point[0]) + A[0, 1] * (Y - equilibrium_point[1])
    V_dir = A[1, 0] * (X - equilibrium_point[0]) + A[1, 1] * (Y - equilibrium_point[1])
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.streamplot(X, Y, U, V_dir, color='b', density=1.5, linewidth=0.8)
    plot_extended_vectors(ax, equilibrium_point, V1, V2, axis_limit)

    ax.set_title("Diagrama de Fase del Sistema Lineal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()
    ax.set_xlim(equilibrium_point[0] - axis_limit, equilibrium_point[0] + axis_limit)
    ax.set_ylim(equilibrium_point[1] - axis_limit, equilibrium_point[1] + axis_limit)
    plt.grid()
    plt.show()


def validate_inputs(A, B):
    if A.shape[0] != A.shape[1]:
        raise ValueError("La matriz A debe ser cuadrada.")
    if B is not None and B.shape[0] != A.shape[0]:
        raise ValueError("El vector B debe tener la misma cantidad de filas que A.")


def display_eigen_info(eigenvalues, eigenvectors):
    print("Valores propios:")
    for i, eigenvalue in enumerate(eigenvalues):
        print(f"\nλ{i + 1} = {format_complex(eigenvalue)}")
        vector = eigenvectors[:, i]
        scaled_vector = scale_eigenvector(vector)
        formatted_vector = [format_complex(component) for component in scaled_vector]
        print(f"Vector propio V{i + 1}: {formatted_vector}")


def process_system(A, B=None):
    validate_inputs(A, B)
    equilibrium_point = calculate_equilibrium_point(A, B)
    eigenvalues, eigenvectors = eig(A)
    V1 = scale_eigenvector(eigenvectors[:, 0])
    V2 = scale_eigenvector(eigenvectors[:, 1])
    display_eigen_info(eigenvalues, eigenvectors)
    system_type = classify_system(eigenvalues)
    print("\nTipo de sistema:", system_type)
    print("Punto de equilibrio:", equilibrium_point)
    print_general_equation(eigenvalues, eigenvectors)
    plot_phase_portrait(A, V1, V2, equilibrium_point, B)


def bifurcation_analysis_linear(mu_range, A_func, B_func=None):
    classifications = []
    for mu in mu_range:
        A = A_func(mu)
        B = B_func(mu) if B_func is not None else None
        eigenvalues, _ = eig(A)
        classification = classify_system(eigenvalues)
        classifications.append(classification)
    return classifications


def plot_bifurcation_linear(mu_range, classifications, title="Clasificación del Sistema Lineal según μ"):
    unique_classes = sorted(list(set(classifications)), key=classifications.index)
    colors = plt.cm.get_cmap('tab10', len(unique_classes))
    color_map = {cls: colors(i) for i, cls in enumerate(unique_classes)}

    plt.figure(figsize=(10, 6))
    for mu, cls in zip(mu_range, classifications):
        plt.plot(mu, unique_classes.index(cls), 'o', color=color_map[cls], markersize=4)

    plt.yticks(ticks=range(len(unique_classes)), labels=unique_classes)
    plt.xlabel("μ")
    plt.ylabel("Clasificación del Sistema")
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def main():
    realizar_analisis = input(
        "¿Deseas analizar un sistema para un valor específico de μ o realizar un análisis de bifurcación? (escribe 'especifico' o 'bifurcacion'): ").strip().lower()

    if realizar_analisis == 'especifico':
        try:
            mu = float(input("Ingresa el valor de μ: "))
        except ValueError:
            print("Entrada inválida para μ.")
            return

        def A_func(mu):
            # Define aquí cómo A depende de μ
            return np.array([[mu, -2],
                             [2, 2]])

        def B_func(mu):
            # Si B también depende de μ, define aquí. Si no, retorna un valor fijo o None
            return None  # Por ejemplo, B no depende de μ

        A = A_func(mu)
        B = B_func(mu)
        print(f"\nAnalizando el sistema para μ = {mu}:")
        process_system(A, B)

    elif realizar_analisis == 'bifurcacion':
        def A_func(mu):
            return np.array([[mu, -2],
                             [2, 2]])

        def B_func(mu):
            return None  # Por ejemplo, B no depende de μ

        try:
            mu_min = float(input("Ingresa el valor mínimo de μ: "))
            mu_max = float(input("Ingresa el valor máximo de μ: "))
            num_mu = int(input("Ingresa la cantidad de valores de μ a analizar: "))
            if num_mu <= 0:
                raise ValueError("La cantidad de valores de μ debe ser un entero positivo.")
        except ValueError as e:
            print(f"Entrada inválida: {e}")
            return

        mu_range = np.linspace(mu_min, mu_max, num_mu)

        print("\nRealizando análisis de bifurcación...")
        classifications = bifurcation_analysis_linear(mu_range, A_func, B_func)

        plot_bifurcation_linear(mu_range, classifications, title="Clasificación del Sistema Lineal según μ")
    else:
        print("Entrada inválida. Por favor, escribe 'especifico' o 'bifurcacion'.")


if __name__ == "__main__":
    main()
