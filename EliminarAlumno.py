import boto3  # import Boto3
from boto3.dynamodb.conditions import Key  # import Boto3 conditions

def lambda_handler(event, context):
    # Entrada (json)
    print(event)
    body = event['body']
    tenant_id = body['tenant_id']
    alumno_id = body['alumno_id']
    
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')
    
    try:
        # Primero verificar si el alumno existe
        response = table.get_item(
            Key={
                'tenant_id': tenant_id,
                'alumno_id': alumno_id
            }
        )
        
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'message': 'Alumno no encontrado'
            }
        
        # Eliminar el alumno
        table.delete_item(
            Key={
                'tenant_id': tenant_id,
                'alumno_id': alumno_id
            }
        )
        
        print(f"Alumno eliminado: tenant_id={tenant_id}, alumno_id={alumno_id}")
        
        # Salida (json)
        return {
            'statusCode': 200,
            'message': 'Alumno eliminado exitosamente',
            'tenant_id': tenant_id,
            'alumno_id': alumno_id
        }
        
    except Exception as e:
        print(f"Error al eliminar alumno: {str(e)}")
        return {
            'statusCode': 500,
            'message': f'Error al eliminar alumno: {str(e)}'
        }
