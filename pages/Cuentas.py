import streamlit as st
import pandas as pd
from expense_manager import add_account, get_account, get_accounts, update_account, delete_account

st.set_page_config(page_title="Cuentas", page_icon="📊")

st.header("Cuentas")

st.subheader("Gestión de Cuentas")

tabla_cuentas = pd.DataFrame(get_accounts())
tabla_cuentas = tabla_cuentas[["nombre","tipo","descripcion"]]
tabla_cuentas.columns = tabla_cuentas.columns.str.capitalize()

st.dataframe(tabla_cuentas, use_container_width=True)

account_action = st.selectbox("¿Qué acción deseas realizar?", 
                                ["Agregar", "Modificar", "Eliminar"], key="cuentas_accion")

if account_action == "Agregar":
    st.write("Formulario para agregar una cuenta")
    nombre = st.text_input("Nombre de la cuenta", key="cuentas_nombre")
    tipo = st.selectbox("Tipo de cuenta", ["Bancaria", "Efectivo", "Otro"], key="cuentas_tipo")
    descripcion = st.text_area("Descripción", key="cuentas_descripcion")

    if st.button("Agregar cuenta", key="cuentas_agregar"):
        add_account(nombre, tipo, descripcion)
        st.success("Cuenta agregada con éxito!")
        st.rerun()

elif account_action == "Modificar":
    st.write("Modificar cuenta")
    # Obtener las cuentas y categorías desde Firebase para seleccionarlas
    cuentas = get_accounts()  # Asumiendo que esta función devuelve una lista de cuentas
    cuenta_seleccionada = st.selectbox("Selecciona la cuenta", [f"{cuenta['nombre']} - {cuenta['tipo']}" for cuenta in cuentas], key="transacciones_cuenta")
    # Obtener el ID de la cuenta y categoría seleccionada
    id = cuentas[[f"{cuenta['nombre']} - {cuenta['tipo']}" for cuenta in cuentas].index(cuenta_seleccionada)]['id']
   
    
    account = get_account(id)
    if account:
        #st.write("Datos actuales:", account)
        form = st.form('my_form')

        nombre = form.text_input("Nuevo nombre", value=account['nombre'], key="cuentas_nuevo_nombre")
        tipo = form.selectbox("Nuevo tipo de cuenta", ["Bancaria", "Efectivo", "Otro"], 
                            index=["Bancaria", "Efectivo", "Otro"].index(account['tipo']), key="cuentas_nuevo_tipo")
        descripcion = form.text_area("Nueva descripción", value=account['descripcion'], key="cuentas_nueva_descripcion")
        submit = form.form_submit_button("Actualizar cuenta")
        if submit:
            update_account(id, nombre, tipo, descripcion)
            st.success('Cuenta actualizada con éxito!')
            st.rerun()
            

elif account_action == "Eliminar":
    st.write("Eliminar cuenta")
    cuentas = get_accounts()  # Asumiendo que esta función devuelve una lista de cuentas
    cuenta_seleccionada = st.selectbox("Selecciona la cuenta", [f"{cuenta['nombre']} - {cuenta['tipo']}" for cuenta in cuentas], key="transacciones_cuenta")
    # Obtener el ID de la cuenta y categoría seleccionada
    id = cuentas[[f"{cuenta['nombre']} - {cuenta['tipo']}" for cuenta in cuentas].index(cuenta_seleccionada)]['id']
    if st.button("Eliminar cuenta", key="cuentas_eliminar"):
        delete_account(id)
        st.success("Cuenta eliminada con éxito!")
        st.rerun()