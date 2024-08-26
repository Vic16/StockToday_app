import pandas as pd
import plotly.graph_objects as go
import random
import dataframe_image as dfi
import io

######################################################################
########################      For tables      ########################
######################################################################

def color_negative_red(value):
  """
  Colors elements in a dateframe
  green if positive and red if
  negative. Does not color NaN
  values.
  """
  light_green = '#66ff66'  # Verde claro

  if value < 0:
    color = 'red'
  elif value > 0:
    color = light_green
  else:
    color = 'white'
  return 'color: %s' % color

def setTableStyles(df):
    """
    """
    # Lista de colores para el encabezado
    header_colors = ['gold','orange','#00BFFF','#87CEFA','#FF4500']
    selected_color = random.choice(header_colors)
    df = df.dropna(how='all')
    df = df.sort_values(by='Variation', ascending=False)
    df_styled = df.style.map(lambda x: 'background-color: black; color: white') \
                    .set_table_styles(
                        [{'selector': 'thead th', 'props': [('background-color',selected_color), ('color', 'black'), ('border', '1px solid white')]},
                         {'selector': 'tbody td', 'props': [('border', '1px solid white')]},
                         {'selector': 'tbody td:first-child', 'props': [('border-left', 'none')]},
                         {'selector': 'thead th:first-child', 'props': [('border-left', 'none')]},
                         {'selector': 'index', 'props': [('display', 'none')]}, # Ocultar el índice
                         {'selector': 'thead td', 'props': [('border', 'none')]},
                         {'selector': 'thead', 'props': [('border-bottom', '1px solid white')]}]
                    ) \
                    .set_properties(**{
                        'background-color': 'black', 
                        'color': 'white', 
                        'border': '1px solid white'
                    }, subset=pd.IndexSlice[:, :]) \
                    .map(color_negative_red, subset=['Variation']) \
                    .format(na_rep='MISS', precision=3)\
                    .hide(axis='index')  # Ocultar el índice

    # Mostrar el DataFrame estilizado sin el índice
    return df_styled.hide(axis='index')

def saveDFMemory(df):
    buffer = io.BytesIO()
    dfi.export(df, buffer)
    buffer.seek(0)
    return buffer

######################################################################
########################      For Fig         ########################
######################################################################


def plot_stock_close(df, close_column='Close', stock_code='AAPL'):
    """
    Crea un gráfico minimalista de la serie temporal del precio de cierre de acciones.
    
    Args:
    - df (pd.DataFrame): DataFrame que contiene los datos con la fecha en el índice.
    - close_column (str): Nombre de la columna de precios de cierre.
    - stock_code (str): Código de la acción para mostrar en el título de la izquierda.
    """
    # Verificar si el índice está en formato datetime, si no, convertirlo
    if not pd.api.types.is_datetime64_any_dtype(df.index):
        df.index = pd.to_datetime(df.index)

    colors = ['#00BFFF', '#FFD700', '#FF6347']  # Azul claro, dorado, rojo claro, tomate
    random_color = random.choice(colors)

    fig = go.Figure()
    # Añadir la serie temporal de precios de cierre
    fig.add_trace(go.Scatter(
        x=df.index, 
        y=df[close_column], 
        mode='lines', 
        name='Close', 
        line=dict(color=random_color)  # Color aleatorio para el gráfico
    ))

    # Ajustar el formato del eje X para mostrar mes/año
    fig.update_xaxes(
        tickformat='%b %Y',  # Formato de fecha: mes y año
        dtick='M3',         # Etiquetas cada 3 meses
        tickangle=45,       # Ángulo de las etiquetas del eje X
        tickfont=dict(size=8, color='white'),  # Tamaño y color de la fuente
        showgrid=True,
        gridcolor='white',  # Color de la cuadrícula
        gridwidth=0.2       # Ancho de la línea de la cuadrícula
    )

    # Ajustar el formato del eje Y
    fig.update_yaxes(
        showgrid=True,
        gridcolor='white',  # Color de la cuadrícula
        gridwidth=0.5,      # Ancho de la línea de la cuadrícula
        title_text='Close Price',  # Título del eje Y en inglés
        title_font=dict(size=10, color='white')
    )

    # Configurar el diseño de la figura
    fig.update_layout(
        plot_bgcolor='black',
        paper_bgcolor='black',
        font_color='white',
        title_x=0.05,  # Posicionar el título a la izquierda
        title_font=dict(size=12, color='white'),
        margin=dict(t=20, b=40, l=60, r=20)  # Márgenes para evitar cortar etiquetas
    )

    # Añadir anotación en el último valor de la serie
    last_date = df.index[-1]
    last_close = df[close_column].iloc[-1]
    fig.add_annotation(
        x=last_date,
        y=last_close,
        text=f"{last_close:.2f}",
        showarrow=True,
        arrowhead=1,
        font=dict(color='white'),
        bgcolor='black',  # Fondo negro para la anotación
        bordercolor='white',  # Borde blanco para la anotación
        borderwidth=1  # Ancho del borde
    )

    # Añadir título pequeño a la izquierda
    fig.add_annotation(
        x=df.index.min(),  # Posición a la izquierda del gráfico
        y=df[close_column].max(),  # Posicionar en la parte superior del gráfico
        text=f"{stock_code}",
        showarrow=False,
        font=dict(size=12, color='white'),
        bgcolor='black',  # Fondo negro para la anotación
        bordercolor='white',  # Borde blanco para la anotación
        borderwidth=1  # Ancho del borde
    )

    return fig



def saveFigMemory(fig):
    """
    Guarda el gráfico en memoria en formato PNG.
    
    Args:
    - fig (plotly.graph_objects.Figure): La figura de Plotly.
    
    Returns:
    - BytesIO: El objeto en memoria con la imagen PNG.
    """
    buffer = io.BytesIO()
    fig.write_image(buffer, format='png')
    buffer.seek(0)  # Regresar al principio del buffer
    return buffer