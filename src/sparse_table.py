class SparseTableRMQ:
    """
    Implementación optimizada del problema de Consulta de Mínimo en Rango (RMQ)
    mediante la estructura de datos Sparse Table (Tabla Dispersa).
    
    Aprovecha la propiedad de idempotencia del operador mínimo (min(x, x) = x)
    para resolver cualquier consulta en tiempo constante O(1) tras una
    precomputación de O(N log N).
    
    Complejidad Temporal:
        - Construcción (Precomputación): O(N log N)
        - Consulta (Query): O(1)
    Complejidad Espacial:
        - O(N log N) para almacenar la tabla dispersa
    """
    def __init__(self, arr):
        self.arr = arr
        self.n = len(arr)
        if self.n == 0:
            self.st = []
            self.k = 0
            return
            
        # K es la cantidad de columnas necesarias en la tabla dispersa.
        # Es igual al número de bits necesarios para representar N.
        # Para N, la máxima potencia de 2 es 2^(K-1) <= N, por lo que necesitamos K columnas (de 0 a K-1).
        self.k = self.n.bit_length()
        
        # Inicializar la tabla dispersa. st[i][j] almacenará el mínimo de la sección
        # del arreglo que inicia en el índice 'i' y tiene una longitud de 2^j.
        self.st = [[0] * self.k for _ in range(self.n)]
        
        # Caso base: intervalos de longitud 2^0 = 1
        for i in range(self.n):
            self.st[i][0] = arr[i]
            
        # Llenar la tabla usando la relación de recurrencia por programación dinámica
        for j in range(1, self.k):
            # Solo podemos calcular rangos que no se salgan del arreglo
            limit = self.n - (1 << j) + 1
            for i in range(limit):
                # El mínimo de un rango de tamaño 2^j es el mínimo de dos subrangos
                # de tamaño 2^(j-1) que lo componen consecutivamente.
                self.st[i][j] = min(
                    self.st[i][j - 1], 
                    self.st[i + (1 << (j - 1))][j - 1]
                )

    def query(self, L, R):
        """
        Retorna el valor mínimo en el rango [L, R] (inclusive) en tiempo constante O(1).
        
        Args:
            L (int): Índice de inicio (inclusivo)
            R (int): Índice de fin (inclusivo)
            
        Returns:
            int/float: El valor mínimo en el subarreglo arr[L...R]
        """
        if L < 0 or R >= self.n or L > R:
            raise ValueError(f"Rango de consulta inválido: [{L}, {R}] para arreglo de tamaño {self.n}")
        
        # Calcular la longitud del rango [L, R]
        length = R - L + 1
        
        # Encontrar la mayor potencia de 2 menor o igual que la longitud
        # Usamos bit_length() - 1 que equivale a floor(log2(length)) de forma exacta en O(1)
        j = length.bit_length() - 1
        
        # Combinar el mínimo de los dos bloques solapados de longitud 2^j
        # Bloque 1: Inicia en L: [L, L + 2^j - 1]
        # Bloque 2: Termina en R: [R - 2^j + 1, R]
        return min(
            self.st[L][j], 
            self.st[R - (1 << j) + 1][j]
        )
