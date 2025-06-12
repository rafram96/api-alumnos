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
        response = table.get_item(
            Key={
                'tenant_id': tenant_id,
                'alumno_id': alumno_id
            }
        )
        
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'message': 'Alumno no encontrado',
                'tenant_id': tenant_id,
                'alumno_id': alumno_id
            }
        
        alumno = response['Item']
        print(f"Alumno encontrado: {alumno}")
        
        # Salida (json)
        return {
            'statusCode': 200,
            'message': 'Alumno encontrado exitosamente',
            'tenant_id': tenant_id,
            'alumno': alumno
        }
        
    except Exception as e:
        print(f"Error al buscar alumno: {str(e)}")
        return {
            'statusCode': 500,
            'message': f'Error al buscar alumno: {str(e)}'
        }
