import boto3  # import Boto3
import json
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
    
    # Construir expresiones de actualización dinámicamente
    update_expression = "SET "
    expression_attribute_names = {}
    expression_attribute_values = {}
      # Campos que se pueden actualizar (excluyendo las claves primarias)
    updatable_fields = ['nombre', 'sexo', 'fecha_nac', 'celular', 'direccion', 'distrito', 'provincia', 'departamento', 'pais']
    
    updates = []
    
    # Manejar campos directos
    for field in updatable_fields:
        if field in body:
            placeholder = f"#{field}"
            value_placeholder = f":{field}"
            updates.append(f"{placeholder} = {value_placeholder}")
            expression_attribute_names[placeholder] = field
            expression_attribute_values[value_placeholder] = body[field]
    
    # Manejar objeto domicilio si existe
    if 'domicilio' in body:
        domicilio = body['domicilio']
        domicilio_fields = {
            'direccion': 'direcc',
            'distrito': 'distrito', 
            'provincia': 'provincia',
            'departamento': 'departamento',
            'pais': 'pais'
        }
        
        for db_field, json_field in domicilio_fields.items():
            if json_field in domicilio:
                placeholder = f"#{db_field}"
                value_placeholder = f":{db_field}"
                updates.append(f"{placeholder} = {value_placeholder}")
                expression_attribute_names[placeholder] = db_field
                expression_attribute_values[value_placeholder] = domicilio[json_field]
    
    # Agregar fecha de modificación
    if updates:
        from datetime import datetime
        updates.append("#fecha_modificacion = :fecha_modificacion")
        expression_attribute_names["#fecha_modificacion"] = "fecha_modificacion"
        expression_attribute_values[":fecha_modificacion"] = datetime.now().isoformat()
    
    if not updates:
        return {
            'statusCode': 400,
            'message': 'No hay campos para actualizar'
        }
    
    update_expression += ", ".join(updates)
    
    try:
        response = table.update_item(
            Key={
                'tenant_id': tenant_id,
                'alumno_id': alumno_id
            },
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues='ALL_NEW'
        )
        
        updated_alumno = response['Attributes']
        print(f"Alumno actualizado: {updated_alumno}")
        
        # Salida (json)
        return {
            'statusCode': 200,
            'message': 'Alumno modificado exitosamente',
            'alumno': updated_alumno
        }
        
    except Exception as e:
        print(f"Error al modificar alumno: {str(e)}")
        return {
            'statusCode': 500,
            'message': f'Error al modificar alumno: {str(e)}'
        }
