# Trabajo Final: Optimización de Consultas de Mínimo en Rango (RMQ) con Sparse Table

Este repositorio contiene el trabajo final desarrollado para la materia de Algoritmos y Estructuras de Datos. El objetivo principal es investigar, implementar y demostrar cómo mediante ingenio matemático y precomputación se puede optimizar drásticamente la complejidad temporal de un problema (de lineal a constante) para permitir una escalabilidad masiva.

El problema seleccionado es **Range Minimum Query (RMQ)**.

## Estructura del Repositorio

El proyecto se organiza de la siguiente manera:

*   `src/`: Directorio con el código fuente en Python.
    *   [`naive_rmq.py`](src/naive_rmq.py): Implementación del algoritmo ingenuo de costo lineal $O(N)$ por consulta.
    *   [`sparse_table.py`](src/sparse_table.py): Implementación del algoritmo optimizado usando *Sparse Table* que resuelve consultas en tiempo constante $O(1)$.
    *   [`benchmark.py`](src/benchmark.py): Script de validación de corrección y medición de rendimiento comparativo.
*   `doc/`: Directorio con la investigación teórica.
    *   [`documento.tex`](doc/documento.tex): Documento académico formal escrito en LaTeX.
*   `README.md`: Este archivo con instrucciones de uso.

---

## Cómo Ejecutar el Benchmark

Para ejecutar las pruebas de corrección automática y la medición de rendimiento de ambos algoritmos, debes tener instalado **Python 3** en tu sistema.

1.  Abre una terminal o consola de comandos en la carpeta raíz del proyecto.
2.  Ejecuta el script de pruebas con el siguiente comando:
    ```bash
    python src/benchmark.py
    ```

El script realizará:
1.  **50 Pruebas de Corrección**: Genera arreglos y rangos de consulta aleatorios para comparar el resultado de `SparseTableRMQ` contra `NaiveRMQ`. El benchmark continuará solo si ambos arrojan exactamente el mismo resultado.
2.  **Benchmark de Escenarios**: Ejecuta la medición de tiempos para diferentes valores de tamaño de arreglo ($N$) y cantidad de consultas ($Q$), desde $N=100, Q=1000$ hasta $N=500,000, Q=1,000,000$.

---

## Resumen de Resultados

Los tiempos de consulta y construcción obtenidos en las ejecuciones de prueba son:

| Arreglo (N) | Consultas (Q) | T. Construcción Naive (s) | T. Consultas Naive (s) | T. Prec. Sparse Table (s) | T. Consultas ST (s) | Speedup Consulta | Speedup Total |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 100 | 1,000 | 0.000001 | 0.000710 | 0.000084 | 0.000239 | 3.0x | 2.2x |
| 1,000 | 5,000 | 0.000002 | 0.028931 | 0.001370 | 0.001299 | 22.3x | 10.8x |
| 5,000 | 10,000 | 0.000005 | 0.278195 | 0.008548 | 0.002953 | 94.2x | 24.2x |
| 10,000 | 20,000 | 0.000022 | 1.096940* | 0.018902 | 0.006228 | 176.1x | 43.7x |
| 50,000 | 50,000 | 0.000050 | 13.075675* | 0.118743 | 0.023038 | 567.6x | 92.2x |
| 100,000 | 100,000 | 0.000175 | 56.849350* | 0.281506 | 0.064673 | 879.0x | 164.2x |
| 500,000 | 1,000,000 | 0.000411 | 3104.669500* | 1.902360 | 0.829445 | **3743.1x** | **1136.5x** |

*\*Nota: Los tiempos con asterisco son proyecciones estadísticas estimadas debido a la inviabilidad temporal de ejecutar el algoritmo de fuerza bruta en arreglos de gran tamaño en un tiempo razonable.*

### Conclusión Clave
Para un millón de consultas sobre medio millón de elementos, el algoritmo lineal tardaría aproximadamente **51 minutos** en completarse en Python, mientras que la solución con **Sparse Table** resuelve todas las operaciones en **menos de 3 segundos** (incluyendo el tiempo de precomputación). Esto representa una ganancia de rendimiento en consultas de más de **3,700 veces**.

---

## Compilación del Documento LaTeX

El archivo `doc/documento.tex` contiene la investigación formal redactada bajo el formato estándar de artículos técnicos en español. Puedes compilar este archivo a formato PDF en cualquier entorno local de LaTeX (como TeX Live, MiKTeX con `pdflatex`) u Overleaf.

Comando estándar de compilación:
```bash
pdflatex doc/documento.tex
```

## Control de Versiones

El desarrollo de este trabajo se encuentra registrado y estructurado bajo la rama:
*   `dev-nico`

Repositorio remoto oficial: [https://github.com/nicotitopp/trabajoFinal.git](https://github.com/nicotitopp/trabajoFinal.git)
