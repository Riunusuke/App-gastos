from firebase_config import db

#### Transacciones

# Add: Agregar una transacción
def add_transaction(tipo, monto, fecha, descripcion, cuenta_id, categoria_id):
    doc_ref = db.collection('transacciones').document()
    doc_ref.set({
        'tipo': tipo,
        'monto': monto,
        'fecha': fecha,
        'descripcion': descripcion,
        'cuenta': db.collection('cuentas').document(cuenta_id),
        'categoria': db.collection('categorias').document(categoria_id)
    })

# Get: Obtener una transacción
def get_transaction(id):
    doc_ref = db.collection('transacciones').document(id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None

# Update: Actualizar una transacción
def update_transaction(id, tipo=None, monto=None, fecha=None, descripcion=None, cuenta_id=None, categoria_id=None):
    doc_ref = db.collection('transacciones').document(id)
    data = {}
    if tipo:
        data['tipo'] = tipo
    if monto:
        data['monto'] = monto
    if fecha:
        data['fecha'] = fecha
    if descripcion:
        data['descripcion'] = descripcion
    if cuenta_id:
        data['cuenta'] = db.collection('cuentas').document(cuenta_id)
    if categoria_id:
        data['categoria'] = db.collection('categorias').document(categoria_id)
    
    doc_ref.update(data)

# Delete: Eliminar una transacción
def delete_transaction(id):
    doc_ref = db.collection('transacciones').document(id)
    doc_ref.delete()

### Cuentas

# Add: Agregar una cuenta
def add_account(nombre, tipo, descripcion=None):
    doc_ref = db.collection('cuentas').document()
    doc_ref.set({
        'nombre': nombre,
        'tipo': tipo,
        'descripcion': descripcion
    })

# Get: Obtener una cuenta
def get_account(id):
    doc_ref = db.collection('cuentas').document(id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None

def get_accounts():
    # Acceder a la colección de cuentas en Firestore
    accounts_ref = db.collection('cuentas')  # Nombre de la colección
    docs = accounts_ref.stream()  # Obtener todos los documentos de la colección

    accounts = []
    for doc in docs:
        account_data = doc.to_dict()  # Convierte el documento a un diccionario
        account_data['id'] = doc.id  # Agrega el ID del documento
        accounts.append(account_data)
    
    return accounts


# Update: Actualizar una cuenta
def update_account(id, nombre=None, tipo=None, descripcion=None):
    doc_ref = db.collection('cuentas').document(id)
    data = {}
    if nombre:
        data['nombre'] = nombre
    if tipo:
        data['tipo'] = tipo
    if descripcion:
        data['descripcion'] = descripcion
    
    doc_ref.update(data)

# Delete: Eliminar una cuenta
def delete_account(id):
    doc_ref = db.collection('cuentas').document(id)
    doc_ref.delete()

### Categorias

# Add: Agregar una categoría
def add_category(nombre, tipo, descripcion=None):
    doc_ref = db.collection('categorias').document()
    doc_ref.set({
        'nombre': nombre,
        'tipo': tipo,
        'descripcion': descripcion
    })

# Get: Obtener una categoría
def get_category(id):
    doc_ref = db.collection('categorias').document(id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None
    
def get_categories():
    # Acceder a la colección de categorías en Firestore
    categories_ref = db.collection('categorias')  # Nombre de la colección
    docs = categories_ref.stream()  # Obtener todos los documentos de la colección

    categories = []
    for doc in docs:
        category_data = doc.to_dict()  # Convierte el documento a un diccionario
        category_data['id'] = doc.id  # Agrega el ID del documento
        categories.append(category_data)
    
    return categories

# Update: Actualizar una categoría
def update_category(id, nombre=None, tipo=None, descripcion=None):
    doc_ref = db.collection('categorias').document(id)
    data = {}
    if nombre:
        data['nombre'] = nombre
    if tipo:
        data['tipo'] = tipo
    if descripcion:
        data['descripcion'] = descripcion
    
    doc_ref.update(data)

# Delete: Eliminar una categoría
def delete_category(id):
    doc_ref = db.collection('categorias').document(id)
    doc_ref.delete()
