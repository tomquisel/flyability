import traceback, sys
from multiprocessing import Process, Pipe
from django.http import HttpResponse

def runGrapher(f):
    parent_conn, child_conn = Pipe()
    p = Process(target=_runner, args=(f,child_conn))
    p.start()
    return parent_conn.recv()

def _runner(f, conn):
    try: 
        canvas = f()
        response = HttpResponse(content_type='image/png')
        canvas.print_png(response, transparent=True)
        conn.send(response)
    except Exception, e:
        print "### Traceback in original process:"
        traceback.print_tb(sys.exc_info()[2])
        conn.send(e)
        
