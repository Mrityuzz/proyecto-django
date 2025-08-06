import datetime
from urllib import request
from django.shortcuts import redirect, render
from .models import Alumnos, ComentarioContacto
from .forms import ComentarioContactoForm
from django.shortcuts import get_object_or_404
from .models import Archivos
from .forms import FormArchivos
from django.contrib import messages

# Create your views here.

def registros(request):
    alumnos=Alumnos.objects.all()
    return render(request, "registros/principal.html", {'alumnos': alumnos})
#Indicamos el lugar donde se renderizará el resultado deesta vista

def registrar(request):
    if request.method == 'POST':
        form = ComentarioContactoForm(request.POST)
        if form.is_valid(): #Si los datos recibidos son correctos
            form.save() #inserta
            
            return redirect('Comentarios')        
    form = ComentarioContactoForm()
#Si algo sale mal se reenvian al formulario los datos ingresados
    return render(request,'registros/contacto.html',{'form': form})


def contacto(request):
    form = ComentarioContactoForm()
    return render(request,"registros/contacto.html", {'form': form})
#Indicamos el lugar donde se renderizará el resultado de esta vista


def comentarios(request):
    coments=ComentarioContacto.objects.all()
    return render(request, "registros/comentario.html", {'comentarios':coments})


def eliminarComentarioContacto(request, id):
    comentario = get_object_or_404(ComentarioContacto, id=id)
    if request.method == 'POST':
        comentario.delete()
        return redirect('Comentarios') 
    return render(request, 'registros/confirmarEliminacion.html', {'object': comentario})

def consultar1(request):
    alumnos=Alumnos.objects.filter(carrera="TI")
    return render(request,"registros/consultas.html", {'alumnos' :alumnos})

def consultar2(request):
    alumnos=Alumnos.objects.filter(carrera="TI").filter(turno="Matutino")
    return render(request,"registros/consultas.html", {'alumnos' :alumnos})

def consultar3(request):
    alumnos=Alumnos.objects.all().only("matricula", "nombre", "carrera", "turno", "imagen")
    return render(request,"registros/consultas.html", {'alumnos' :alumnos})

def consultar4(request):
    alumnos=Alumnos.objects.filter(turno__contains="Vesp")
    return render(request,"registros/consultas.html", {'alumnos' :alumnos})

def consultar5(request):
    alumnos=Alumnos.objects.filter(nombre__in=["Juan","Ana"])
    return render(request,"registros/consultas.html", {'alumnos' :alumnos})

def consultar6(request):
    fechaInicio = datetime.date(2025, 7, 9)
    fechaFin = datetime.date(2025, 7, 20)
    alumnos=Alumnos.objects.filter(created__range=(fechaInicio,fechaFin))
    return render(request,"registros/consultas.html", {'alumnos' :alumnos})

def consultar7(request):
    alumnos=Alumnos.objects.filter(comentario__coment__contains='No inscrito')
    return render(request,"registros/consultas.html", {'alumnos' :alumnos})

def consultar8(request):
    fecha_inicio = datetime.date(2025, 7, 8)
    fecha_fin = datetime.date(2025, 7, 9)
    comentarios = ComentarioContacto.objects.filter(created__range=(fecha_inicio, fecha_fin))
    return render(request, "registros/comentarios.html", {'comentarios': comentarios})

def consultar9(request):
    comentarios = ComentarioContacto.objects.filter(mensaje__contains="si")
    return render(request, "registros/comentarios.html", {'comentarios': comentarios})

def consultar10(request):
    comentarios = ComentarioContacto.objects.filter(usuario__exact="Gera")
    return render(request, "registros/comentarios.html", {'comentarios': comentarios})


def consultar11(request):
    lista_mensajes = ComentarioContacto.objects.values_list('mensaje')
    for mensaje in lista_mensajes:
        print(mensaje)
    return redirect('Comentarios')

def consultar12(request):
    comentarios = ComentarioContacto.objects.filter(mensaje__startswith="Rw")
    return render(request, "registros/comentarios.html", {'comentarios': comentarios})

def consultarComentarioIndividual(request, id):
    comentario = ComentarioContacto.objects.get(id=id)
    return render(
        request,
        "registros/formEditarComentario.html",
        {'comentario': comentario}
    )



def editarComentarioContacto(request, id):
    comentario = get_object_or_404(ComentarioContacto, id=id)
    form = ComentarioContactoForm(request.POST or None, instance=comentario)

    if form.is_valid():
        form.save()
        return redirect('Comentarios')  # ← redirige a la vista que muestra la tabla

    return render(request, "registros/formEditarComentario.html", {
        'comentario': comentario
    })


def archivos(request):
    if request.method == 'POST':
        form = FormArchivos(request.POST, request.FILES)
        
        if form.is_valid():
            titulo = request.POST['titulo']
            descripcion = request.POST['descripcion']
            archivo = request.FILES['archivo']

            nuevo_archivo = Archivos(
                titulo=titulo,
                descripcion=descripcion,
                archivo=archivo
            )
            nuevo_archivo.save()

            messages.success(request, "Archivo subido correctamente.")
            return render(request, "registros/archivos.html")
        else:
            messages.error(request, "Error al procesar el formulario.")
            return render(request, "registros/archivos.html", {'form': form})
    
    else:
        form = FormArchivos()
        archivos = Archivos.objects.all()
        return render(request, "registros/archivos.html", {
            'form': form,
            'archivos': archivos
        })


def consultasSQL(request):
    alumnos = Alumnos.objects.raw(
        'SELECT id, matricula, nombre, carrera, turno, imagen FROM registros_alumnos WHERE carrera="TI" ORDER BY turno DESC'
    )
    return render(request, "registros/consultas.html", {'alumnos': alumnos})


def seguridad(request, nombre=None):
    nombre = request.GET.get('nombre')
    return render(request, "registros/seguridad.html",
                  {'nombre': nombre})