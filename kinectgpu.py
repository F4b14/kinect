import pyopencl as cl
import numpy as np

# Configurar el contexto y la cola de comandos
platform = cl.get_platforms()[0]
device = platform.get_devices()[0]
context = cl.Context([device])
queue = cl.CommandQueue(context)

# Crear matrices de entrada y salida
a = np.array([1, 2, 3, 4], dtype=np.int32)
b = np.array([5, 6, 7, 8], dtype=np.int32)
c = np.empty_like(a)

# Crear buffers de memoria en la GPU
a_buf = cl.Buffer(context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=a)
b_buf = cl.Buffer(context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=b)
c_buf = cl.Buffer(context, cl.mem_flags.WRITE_ONLY, c.nbytes)

# Escribir el kernel de OpenCL
kernel_code = """
__kernel void add(__global const int* a, __global const int* b, __global int* c) {
    int gid = get_global_id(0);
    c[gid] = a[gid] + b[gid];
}
"""
program = cl.Program(context, kernel_code).build()

# Ejecutar el kernel
program.add(queue, a.shape, None, a_buf, b_buf, c_buf)

# Leer el resultado de vuelta a la CPU
cl.enqueue_copy(queue, c, c_buf).wait()

print("Resultado:", c)
