import docker
import subprocess
import time

client = docker.from_env()

def buildDockerfileImage(image_name:str, client=client):
    try:
        client.images.get(image_name)
        print(f"La imagen '{image_name}' ya existe.")
    except docker.errors.ImageNotFound:
        print(f"La imagen '{image_name}' no existe. Construyendo la imagen...")
        # Construir la imagen
        image, logs = client.images.build(path=".", tag=image_name)
        for log in logs:
            print(log.get('stream', ''))
            
def removeContainer(containerName:str, client=client):
    try:
        container = client.containers.get(containerName)
        # Detener el contenedor (opcional, si está en ejecución)
        container.stop()
        # Eliminar el contenedor
        container.remove()
    except Exception as e:
        print(f'ERROR. o se ha podido borrar el contenedor:\n  {e}')
        
def runContainer(imageName:str, containerName:str, client=client):
    container = client.containers.run(
        imageName,  # Imagen del contenedor
        detach=True,  # Ejecuta el contenedor en segundo plano
        ports={'8834/tcp': 8834},  # Mapea el puerto 80 del contenedor al puerto 8080 del host
        name = containerName
    )
    while container.status != 'running':
        container.reload()
        time.sleep(1)
    return container

def runComposeUp(ymlFilePath:str=".",  build:bool=False, client=client):
    """
    Executes the services defined in a Docker Compose file.
    Args:
        ymlFilePath (str): Full path to the Docker Compose file.
        build (bool, optional): if it is True, the images are built before starting the containers. Defaults to False.
    """

    command = ["docker", "compose", "-f", ymlFilePath, "up", "-d"]
    if build:
        command.append("--build")
    try:
        output = subprocess.run(command, check=True, capture_output=True)
        print(f"Servicios iniciados desde {ymlFilePath}")
        print(output.stdout.decode('utf-8'))
    except Exception as e:
        print(f"Error al iniciar los servicios: {str(e)}")