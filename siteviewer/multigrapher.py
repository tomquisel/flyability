from django.http import HttpResponse
from multiprocessing import Process, Pipe

def runGrapher(f):
    parent_conn, child_conn = Pipe()
    p = Process(target=_runner, args=(f,child_conn))
    p.start()
    return parent_conn.recv()

def _runner(f, conn):
    canvas = f()
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response, transparent=True)
    conn.send(response)
