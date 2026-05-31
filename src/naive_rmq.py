class NaiveRMQ:
    """
    Implementación ingenua para el problema de Consulta de Mínimo en Rango (RMQ).
    Resuelve cada consulta recorriendo el rango linealmente.
    
    Complejidad Temporal:
        - Construcción: O(1)
        - Consulta: O(N) en el peor caso (donde N es el tamaño del arreglo)
    Complejidad Espacial:
        - O(1) memoria auxiliar (solo almacena la referencia al arreglo)
    """
    def __init__(self, arr):
        self.arr = arr

    def query(self, L, R):
        """
        Retorna el valor mínimo en el rango [L, R] (inclusive).
        
        Args:
            L (int): Índice de inicio (inclusivo)
            R (int): Índice de fin (inclusivo)
            
        Returns:
            int/float: El valor mínimo en el subarreglo arr[L...R]
        """
        if L < 0 or R >= len(self.arr) or L > R:
            raise ValueError(f"Rango de consulta inválido: [{L}, {R}] para arreglo de tamaño {len(self.arr)}")
        
        min_val = self.arr[L]
        for i in range(L + 1, R + 1):
            if self.arr[i] < min_val:
                min_val = self.arr[i]
        return min_val
