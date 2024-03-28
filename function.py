import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json

def stop_start_instances(request):

    request = request.get_data()
    decoded_str = request.decode('utf-8')
    corrected_str = decoded_str.replace('action', '"action"').replace('start', '"start"').replace('stop', '"stop"')
    request_json = json.loads(corrected_str)
    action = request_json['action']

    print(request)

    project_id = 'terraform-projeto'  # Substitua pelo seu Project ID
    zone = 'us-central1-a'  # Substitua pela zona das suas instâncias, se necessário

    # Inicializa o cliente Compute Engine
    compute_client = build('compute', 'v1')

    # Lista todas as instâncias do Compute Engine
    instances = compute_client.instances().list(project=project_id, zone=zone).execute()

    # Verifica se é hora de parar ou iniciar as instâncias
    if action == 'stop':
        for instance in instances.get('items', []):
            # Verificar se a instância tem a tag especificada
            tags = instance.get('labels', {})
            if tags.get('turbot_stop_start') == 'true':
                request = compute_client.instances().stop(project=project_id, zone=zone, instance=instance['name'])
                response = request.execute()
                print(f"Pausando a instância: {instance['name']}")
            else:
                print(f"A instância {instance['name']} não tem a tag 'turbot_stop_start = true'.")

                
    elif action == 'start':
        for instance in instances.get('items', []):
            # Verificar se a instância tem a tag especificada
            tags = instance.get('labels', {})
            if tags.get('turbot_stop_start') == 'true':
                request = compute_client.instances().start(project=project_id, zone=zone, instance=instance['name'])
                response = request.execute()
                print(f"Iniciando a instância: {instance['name']}")
            else:
                print(f"A instância {instance['name']} não tem a tag 'turbot_stop_start = true'.")
    
    return "sucesso", 200