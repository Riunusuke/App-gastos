import streamlit as st
import pyrebase

from expense_manager import add_transaction, get_transaction, update_transaction, delete_transaction
from expense_manager import add_account, get_account, get_accounts, update_account, delete_account
from expense_manager import add_category, get_category, get_categories, update_category, delete_category
from datetime import date


st.set_page_config(
    page_title="App Gastos",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="collapsed"
    )

# Agrega este CSS personalizado
st.markdown("""
<style>
@keyframes bounce {
    0%, 20%, 50%, 80%, 100% {
        transform: translateY(0);
    }
    40% {
        transform: translateY(-30px);
    }
    60% {
        transform: translateY(-15px);
    }
}

.bouncing-emoji {
    display: inline-block;
    animation: bounce 2s infinite;
}
h1 {
    text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Título de la aplicación con emojis animados
st.markdown("<h1><span class='bouncing-emoji'>💸</span> App de Gastos Personales <span class='bouncing-emoji'>💸</span></h1>", unsafe_allow_html=True)

firebase = pyrebase.initialize_app( st.secrets["firebaseConfig"])
pb_auth = firebase.auth()
db = firebase.database()

if 'user_info' not in st.session_state:
    st.session_state.user_info = None

def main():
    if st.session_state.user_info:
        user_info = st.session_state.user_info
        if user_info['role'] == 'admin':
            with st.sidebar:
                st.markdown(f"### 🏠 Bienvenido, {user_info['name']}!")
                st.markdown(f"Rol: **{user_info['role']}**")
                #st.button("Cerrar sesión", on_click=lambda: st.session_state.update({"user_info": None}))
                tabs = st.tabs(["Crear usuario", "Gestionar usuarios"])
                with tabs[0]:
                    create_user_form()
                with tabs[1]:
                    manage_users_module()    
        app()
    else:
        st.markdown("")
        form = st.form("login_form")
        form.markdown("<h2 style='text-align: center'>Autenticación</h2>", unsafe_allow_html=True)
        email = form.text_input("Correo")
        password = form.text_input("Contraseña", type="password")
        col1, col2 = form.columns([8, 2])
        
        if col2.form_submit_button("Iniciar Sesión"):
            with st.spinner("Procesando..."):
                try:
                    # Autenticar usuario
                    user = pb_auth.sign_in_with_email_and_password(email, password)
                    user_id = user['localId']
                    
                    # Obtener información adicional de la base de datos
                    user_info = db.child("users").child(user_id).get().val()
                    if user_info:
                        if user_info["habilitado"]:
                            st.session_state.user_info = user_info
                            st.toast(f"✅ ¡Inicio de sesión exitoso, {user_info['name']}! 🎉")
                            st.rerun()  # Recargar para mostrar la información
                        else:
                            st.error("❌ El usuario se encuentra inhabilitado.")
                    else:
                        st.error("No se encontró información del usuario.")
                except Exception as e:
                    error_message = str(e)
                    if "INVALID_PASSWORD" in error_message:
                        st.toast("❌ Contraseña incorrecta. 🔒")
                    elif "EMAIL_NOT_FOUND" in error_message:
                        st.toast("❌ Correo no registrado. 📧")
                    else:
                        st.toast("⚠️ Error inesperado. Intenta nuevamente. ❓")
                        st.write(e)


def register_user(email, password, name, role):
    try:
        user = pb_auth.create_user_with_email_and_password(email, password)
        user_id = user['localId']
        # Guardar información adicional en la base de datos
        db.child("users").child(user_id).set({"name": name, "role": role, "email": email, "habilitado": True})
        st.success(f"✅ Usuario {name} creado exitosamente con rol {role}!")
    except Exception as e:
        st.error(f"❌ Error al crear el usuario: {e}")


def create_user_form():
    """Función para mostrar el formulario de creación de usuario."""
    st.markdown("## Crear usuario")
    with st.form("create_user_form"):
        new_email = st.text_input("Correo del nuevo usuario")
        new_password = st.text_input("Contraseña", type="password")
        new_name = st.text_input("Nombre")
        new_role = st.selectbox("Rol", ["admin", "Director", "Coordinador", "Analista"])
        submitted = st.form_submit_button("Crear Usuario")

        if submitted:
            if new_email and new_password and new_name and new_role:
                register_user(new_email, new_password, new_name, new_role)
            else:
                st.error("❌ Todos los campos son obligatorios.")

def manage_users_module():
    """Módulo para gestionar usuarios (cambiar rol y contraseña)."""
    st.markdown("## Gestión de usuarios")
    users = db.child("users").get().val()

    if not users:
        st.warning("No hay usuarios registrados.")
        return

    user_list = [{"id": user_id, **info} for user_id, info in users.items()]
    selected_user = st.selectbox(
        "Selecciona un usuario",
        options=user_list,
        format_func=lambda user: f"{user['name']} ({user['email']})"
    )

    if selected_user:
        st.markdown(f"### Editar usuario: **{selected_user['name']}**")
        formulario_mod_usuario = st.form("form_editar_usuario")
        habilitado = formulario_mod_usuario.checkbox("Habilitado", value=selected_user['habilitado'])
        new_role = formulario_mod_usuario.selectbox(
            "Nuevo rol",
            options=["admin", "Director", "Coordinador", "Analista"],
            index=["admin", "Director", "Coordinador", "Analista"].index(selected_user['role'])
        )
        new_password = formulario_mod_usuario.text_input("Nueva contraseña (opcional)", type="password")

        if formulario_mod_usuario.form_submit_button("Guardar cambios"):
            try:
                # Actualizar rol en la base de datos
                db.child("users").child(selected_user["id"]).update({"role": new_role, 'habilitado': habilitado})

                # Actualizar contraseña si se proporciona una nueva
                if new_password:
                    pb_auth.update_user(selected_user["id"], password=new_password)

                st.success(f"✅ Usuario {selected_user['name']} actualizado correctamente.")
            except Exception as e:
                st.error(f"❌ Error al actualizar el usuario: {e}")


def app():
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
            monto = st.number_input("Monto", min_value=1, key="transacciones_monto")
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


if __name__ == "__main__":
    main()
    
