import streamlit as st
from expense_manager import add_transaction, get_transaction, update_transaction, delete_transaction
from expense_manager import add_account, get_account, get_accounts, update_account, delete_account
from expense_manager import add_category, get_category, get_categories, update_category, delete_category
from datetime import date

# Título de la aplicación
st.title("App de Gastos Personales")

# Crear pestañas
tab1, tab2, tab3 = st.tabs(["Transacciones", "Cuentas", "Categorías"])

# Funciones para Transacciones
with tab1:
    st.subheader("Gestión de Transacciones")

    # Submenú dentro de la pestaña
    transaction_action = st.selectbox("¿Qué acción deseas realizar?", 
                                      ["Agregar", "Ver", "Actualizar", "Eliminar"], key="transacciones_accion")

    if transaction_action == "Agregar":
        st.write("Formulario para agregar una transacción")
        tipo = st.selectbox("Tipo de transacción", ["Gasto", "Ingreso"], key="transacciones_tipo")
        monto = st.number_input("Monto", min_value=0.01, key="transacciones_monto")
        fecha = st.date_input("Fecha de la transacción", key="transacciones_fecha").strftime('%Y-%m-%d')
        descripcion = st.text_area("Descripción", key="transacciones_descripcion")
        
        # Obtener las cuentas y categorías desde Firebase para seleccionarlas
        cuentas = get_accounts()  # Asumiendo que esta función devuelve una lista de cuentas
        categorias = get_categories()  # Asumiendo que esta función devuelve una lista de categorías
        
        cuenta_seleccionada = st.selectbox("Selecciona la cuenta", [cuenta['nombre'] for cuenta in cuentas], key="transacciones_cuenta")
        categoria_seleccionada = st.selectbox("Selecciona la categoría", [categoria['nombre'] for categoria in categorias], key="transacciones_categoria")
        
        # Obtener el ID de la cuenta y categoría seleccionada
        cuenta_id = cuentas[[cuenta['nombre'] for cuenta in cuentas].index(cuenta_seleccionada)]['id']
        categoria_id = categorias[[categoria['nombre'] for categoria in categorias].index(categoria_seleccionada)]['id']

        if st.button("Agregar transacción", key="transacciones_agregar"):
            add_transaction(tipo, monto, fecha, descripcion, cuenta_id, categoria_id)
            st.success("Transacción agregada con éxito!")

    elif transaction_action == "Ver":
        st.write("Ver transacción por ID")
        id = st.text_input("ID de la transacción", key="transacciones_ver_id")
        if st.button("Obtener transacción", key="transacciones_ver"):
            transaction = get_transaction(id)
            if transaction:
                st.write(transaction)
            else:
                st.error("Transacción no encontrada.")

    elif transaction_action == "Actualizar":
        st.write("Actualizar transacción")
        id = st.text_input("ID de la transacción", key="transacciones_actualizar_id")
        if st.button("Cargar datos de transacción", key="transacciones_cargar"):
            transaction = get_transaction(id)
            if transaction:
                st.write("Datos actuales:", transaction)
                tipo = st.selectbox("Nuevo tipo de transacción", ["Gasto", "Ingreso"], 
                                    index=["Gasto", "Ingreso"].index(transaction['tipo']), key="transacciones_nuevo_tipo")
                monto = st.number_input("Nuevo monto", value=transaction['monto'], key="transacciones_nuevo_monto")
                fecha = st.date_input("Nueva fecha", value=transaction['fecha'].to_date(), key="transacciones_nueva_fecha")
                descripcion = st.text_area("Nueva descripción", value=transaction['descripcion'], key="transacciones_nueva_descripcion")
                cuenta_id = st.text_input("Nuevo ID de la cuenta", value=transaction['cuenta'].id, key="transacciones_nuevo_cuenta")
                categoria_id = st.text_input("Nuevo ID de la categoría", value=transaction['categoria'].id, key="transacciones_nueva_categoria")

                if st.button("Actualizar transacción", key="transacciones_actualizar"):
                    update_transaction(id, tipo, monto, fecha, descripcion, cuenta_id, categoria_id)
                    st.success("Transacción actualizada con éxito!")

    elif transaction_action == "Eliminar":
        st.write("Eliminar transacción")
        id = st.text_input("ID de la transacción", key="transacciones_eliminar_id")
        if st.button("Eliminar transacción", key="transacciones_eliminar"):
            delete_transaction(id)
            st.success("Transacción eliminada con éxito!")

# Funciones para Cuentas
with tab2:
    st.subheader("Gestión de Cuentas")

    account_action = st.selectbox("¿Qué acción deseas realizar?", 
                                  ["Agregar", "Ver", "Actualizar", "Eliminar"], key="cuentas_accion")

    if account_action == "Agregar":
        st.write("Formulario para agregar una cuenta")
        nombre = st.text_input("Nombre de la cuenta", key="cuentas_nombre")
        tipo = st.selectbox("Tipo de cuenta", ["Bancaria", "Efectivo", "Otro"], key="cuentas_tipo")
        descripcion = st.text_area("Descripción", key="cuentas_descripcion")

        if st.button("Agregar cuenta", key="cuentas_agregar"):
            add_account(nombre, tipo, descripcion)
            st.success("Cuenta agregada con éxito!")

    elif account_action == "Ver":
        st.write("Ver cuenta por ID")
        id = st.text_input("ID de la cuenta", key="cuentas_ver_id")
        if st.button("Obtener cuenta", key="cuentas_ver"):
            account = get_account(id)
            if account:
                st.write(account)
            else:
                st.error("Cuenta no encontrada.")

    elif account_action == "Actualizar":
        st.write("Actualizar cuenta")
        id = st.text_input("ID de la cuenta", key="cuentas_actualizar_id")
        if st.button("Cargar datos de cuenta", key="cuentas_cargar"):
            account = get_account(id)
            if account:
                st.write("Datos actuales:", account)
                nombre = st.text_input("Nuevo nombre", value=account['nombre'], key="cuentas_nuevo_nombre")
                tipo = st.selectbox("Nuevo tipo de cuenta", ["Bancaria", "Efectivo", "Otro"], 
                                    index=["Bancaria", "Efectivo", "Otro"].index(account['tipo']), key="cuentas_nuevo_tipo")
                descripcion = st.text_area("Nueva descripción", value=account['descripcion'], key="cuentas_nueva_descripcion")

                if st.button("Actualizar cuenta", key="cuentas_actualizar"):
                    update_account(id, nombre, tipo, descripcion)
                    st.success("Cuenta actualizada con éxito!")

    elif account_action == "Eliminar":
        st.write("Eliminar cuenta")
        id = st.text_input("ID de la cuenta", key="cuentas_eliminar_id")
        if st.button("Eliminar cuenta", key="cuentas_eliminar"):
            delete_account(id)
            st.success("Cuenta eliminada con éxito!")

# Funciones para Categorías
with tab3:
    st.subheader("Gestión de Categorías")

    category_action = st.selectbox("¿Qué acción deseas realizar?", 
                                   ["Agregar", "Ver", "Actualizar", "Eliminar"], key="categorias_accion")

    if category_action == "Agregar":
        st.write("Formulario para agregar una categoría")
        nombre = st.text_input("Nombre de la categoría", key="categorias_nombre")
        tipo = st.selectbox("Tipo de categoría", ["Gasto", "Ingreso"], key="categorias_tipo")
        descripcion = st.text_area("Descripción", key="categorias_descripcion")

        if st.button("Agregar categoría", key="categorias_agregar"):
            add_category(nombre, tipo, descripcion)
            st.success("Categoría agregada con éxito!")

    elif category_action == "Ver":
        st.write("Ver categoría por ID")
        id = st.text_input("ID de la categoría", key="categorias_ver_id")
        if st.button("Obtener categoría", key="categorias_ver"):
            category = get_category(id)
            if category:
                st.write(category)
            else:
                st.error("Categoría no encontrada.")

    elif category_action == "Actualizar":
        st.write("Actualizar categoría")
        id = st.text_input("ID de la categoría", key="categorias_actualizar_id")
        if st.button("Cargar datos de categoría", key="categorias_cargar"):
            category = get_category(id)
            if category:
                st.write("Datos actuales:", category)
                nombre = st.text_input("Nuevo nombre", value=category['nombre'], key="categorias_nuevo_nombre")
                tipo = st.selectbox("Nuevo tipo de categoría", ["Gasto", "Ingreso"], 
                                    index=["Gasto", "Ingreso"].index(category['tipo']), key="categorias_nuevo_tipo")
                descripcion = st.text_area("Nueva descripción", value=category['descripcion'], key="categorias_nueva_descripcion")

                if st.button("Actualizar categoría", key="categorias_actualizar"):
                    update_category(id, nombre, tipo, descripcion)
                    st.success("Categoría actualizada con éxito!")

    elif category_action == "Eliminar":
        st.write("Eliminar categoría")
        id = st.text_input("ID de la categoría", key="categorias_eliminar_id")
        if st.button("Eliminar categoría", key="categorias_eliminar"):
            delete_category(id)
            st.success("Categoría eliminada con éxito!")
