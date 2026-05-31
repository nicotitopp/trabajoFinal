import time
import random
import sys
from naive_rmq import NaiveRMQ
from sparse_table import SparseTableRMQ

def run_correctness_tests(num_tests=50, max_size=1000):
    """
    Verifica que la implementación de SparseTableRMQ retorne exactamente
    los mismos resultados que la versión NaiveRMQ.
    """
    print("=" * 60)
    print("INICIANDO PRUEBAS DE CORRECCIÓN (CORRECTNESS TESTS)")
    print("=" * 60)
    
    passed = True
    for test_idx in range(1, num_tests + 1):
        # Generar arreglo aleatorio
        size = random.randint(10, max_size)
        arr = [random.randint(-100000, 100000) for _ in range(size)]
        
        # Inicializar ambos solucionadores
        naive_solver = NaiveRMQ(arr)
        st_solver = SparseTableRMQ(arr)
        
        # Hacer varias consultas aleatorias
        num_queries = random.randint(10, 200)
        for _ in range(num_queries):
            L = random.randint(0, size - 1)
            R = random.randint(L, size - 1)
            
            val_naive = naive_solver.query(L, R)
            val_st = st_solver.query(L, R)
            
            if val_naive != val_st:
                print(f"[FALLO] Prueba {test_idx}: Rango [{L}, {R}] en arreglo de tamaño {size}.")
                print(f"        Esperado (Naive): {val_naive}, Obtenido (Sparse Table): {val_st}")
                passed = False
                break
        
        if not passed:
            break
            
    if passed:
        print(f"[OK] Se completaron {num_tests} pruebas de corrección aleatorias de forma exitosa.")
    else:
        print("[ERROR] Falló alguna prueba de corrección.")
        sys.exit(1)
    print("=" * 60 + "\n")


def benchmark():
    """
    Ejecuta el benchmark comparativo de rendimiento entre Naive RMQ y Sparse Table RMQ.
    Utiliza proyección para Naive en conjuntos de datos muy grandes para evitar congelamientos.
    """
    print("=" * 60)
    print("INICIANDO BENCHMARK DE RENDIMIENTO (BENCHMARKING)")
    print("=" * 60)
    
    # Configuración de los escenarios de prueba: (N, Q)
    # N: Tamaño del arreglo, Q: Número de consultas
    scenarios = [
        (100, 1000),
        (1000, 5000),
        (5000, 10000),
        (10000, 20000),
        (50000, 50000),
        (100000, 100000),
        (500000, 1000000)
    ]
    
    # Encabezado de la tabla de resultados
    results = []
    
    for N, Q in scenarios:
        print(f"Ejecutando escenario: N = {N:,}, Q = {Q:,} ...")
        
        # Generar datos aleatorios
        arr = [random.randint(-1000000, 1000000) for _ in range(N)]
        
        # Generar consultas aleatorias predeterminadas
        queries = []
        for _ in range(Q):
            L = random.randint(0, N - 1)
            R = random.randint(L, N - 1)
            queries.append((L, R))
            
        # --- 1. EVALUAR SPARSE TABLE ---
        # Tiempo de construcción
        t0 = time.perf_counter()
        st_solver = SparseTableRMQ(arr)
        t_build_st = time.perf_counter() - t0
        
        # Tiempo de consultas
        t0 = time.perf_counter()
        for L, R in queries:
            st_solver.query(L, R)
        t_query_st = time.perf_counter() - t0
        
        t_total_st = t_build_st + t_query_st
        
        # --- 2. EVALUAR NAIVE ---
        # Tiempo de construcción (instantáneo)
        t0 = time.perf_counter()
        naive_solver = NaiveRMQ(arr)
        t_build_naive = time.perf_counter() - t0
        
        # Para evitar que el benchmark tarde horas, si Q * N es muy grande,
        # estimamos el tiempo de Naive corriendo una muestra de 200 consultas.
        use_projection = (N * Q) > 10**8
        
        if use_projection:
            # Tomar muestra de consultas
            sample_size = min(200, Q)
            sample_queries = queries[:sample_size]
            
            t0 = time.perf_counter()
            for L, R in sample_queries:
                naive_solver.query(L, R)
            t_sample = time.perf_counter() - t0
            
            # Proyectar
            t_query_naive = (t_sample / sample_size) * Q
            is_projected = True
        else:
            t0 = time.perf_counter()
            for L, R in queries:
                naive_solver.query(L, R)
            t_query_naive = time.perf_counter() - t0
            is_projected = False
            
        t_total_naive = t_build_naive + t_query_naive
        
        # Calcular mejora de rendimiento (Speedup)
        # Solo en la fase de consulta y en el tiempo total
        query_speedup = t_query_naive / t_query_st
        total_speedup = t_total_naive / t_total_st
        
        results.append({
            'N': N,
            'Q': Q,
            'build_naive': t_build_naive,
            'query_naive': t_query_naive,
            'total_naive': t_total_naive,
            'build_st': t_build_st,
            'query_st': t_query_st,
            'total_st': t_total_st,
            'query_speedup': query_speedup,
            'total_speedup': total_speedup,
            'projected': is_projected
        })
        
    # Imprimir resultados en formato de tabla Markdown
    print("\n### RESULTADOS DEL BENCHMARK COMPARATIVO")
    print("\n| Arreglo (N) | Consultas (Q) | T. Construcción Naive (s) | T. Consultas Naive (s) | T. Total Naive (s) | T. Prec. Sparse Table (s) | T. Consultas ST (s) | T. Total ST (s) | Speedup Consulta | Speedup Total |")
    print("|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    
    for r in results:
        naive_query_str = f"{r['query_naive']:.6f}" + ("*" if r['projected'] else "")
        naive_total_str = f"{r['total_naive']:.6f}" + ("*" if r['projected'] else "")
        
        print(f"| {r['N']:,} | {r['Q']:,} | {r['build_naive']:.6f} | {naive_query_str} | {naive_total_str} | {r['build_st']:.6f} | {r['query_st']:.6f} | {r['total_st']:.6f} | {r['query_speedup']:.1f}x | {r['total_speedup']:.1f}x |")
        
    print("\n*Nota: Los valores con un asterisco (*) son estimaciones proyectadas basadas en una muestra de consultas para evitar la congelación del script debido a la lentitud del algoritmo ingenuo.*")
    print("\n" + "=" * 60)
    print("BENCHMARK FINALIZADO")
    print("=" * 60)

if __name__ == "__main__":
    run_correctness_tests()
    benchmark()
