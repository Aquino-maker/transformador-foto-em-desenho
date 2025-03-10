from tkinter import Tk, ttk, mainloop, Frame, Label, Scale, Button, filedialog
from PIL import ImageTk, Image, ImageEnhance
import cv2
import os

# CORES
color0 = "#000000"  # Preto
color1 = "#feffff"  # Branco
color2 = "#4fa882"  # Verde
color3 = "#38576b"  # Valor
color4 = "#e06636"  # Profit
color5 = "#038cfc"  # Azul

# Criação da janela
janela = Tk()
janela.title("Transformador de Fotos")  # Adicionando um titulo a janela.
janela.geometry('500x600')  # Definindo a altura e largura da janela
janela.configure(bg=color0)  # Dando uma cor ao fundo do programa.
janela.resizable(width=False, height=False)  # Cria um tamanho fixo para o programa.

# Definindo Váriaveis Globais
global image_original, image_converted
image_original = None
image_converted = None

# Função da opção de escolher imagem
def choose_image():
    global image_original
    path = filedialog.askopenfile()
    if path:
        image_original = Image.open(path.name)
        image_preview = image_original.resize((200, 200))
        image_preview = ImageTk.PhotoImage(image_preview)
        label_preview_original.configure(image = image_preview)
        label_preview_original.image = image_preview

# Função para converter a imagem
def convert_image(event=None):
    global image_original, image_converted

    if image_original is None:
        return
    # Ajustes do Usuário
    intensity = scale_intensity.get()
    brightness = scale_brightness.get() / 100
    contrast = scale_contrast.get() / 100

    # Conversão para desenho a lápis
    image_cv = cv2.cvtColor(cv2.imread(image_original.filename), cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(image_cv, (21,21), 0)
    sketch = cv2.divide(image_cv, blur, scale=intensity)

    # Ajustar brilho e constraste
    pil_sketch = Image.fromarray(sketch)
    enhancer_brightness = ImageEnhance.Brightness(pil_sketch)
    pil_sketch = enhancer_brightness.enhance(brightness)
    enhancer_contrast = ImageEnhance.Contrast(pil_sketch)
    pil_sketch = enhancer_contrast.enhance(contrast)

    image_converted = pil_sketch
    image_preview = image_converted.resize((200, 200))
    image_preview = ImageTk.PhotoImage(image_preview)
    label_preview_transform.configure(image=image_preview)
    label_preview_transform.image = image_preview


# Função para salvar a imagem.
def save_image():
    if image_converted:
        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files",
                                                                                                         "*.*")])
        if path:
            image_converted.save(path)



top_frame = Frame(janela, width=450, height=50, bg=color0)
top_frame.grid(row=0, column=0, padx=10, pady=5)

preview_frame = Frame(janela, width=450, height=230, bg=color0)
preview_frame.grid(row=1, column=0, padx=10, pady=1)

control_frame = Frame(janela, width=450, height=300, bg=color0)
control_frame.grid(row=2, column=0, padx=10, pady=5)

# Título
logo = Label(top_frame, text='Foto em desenho a Lápis', font=('Arial', 16, 'bold'), bg=color0,
             fg=color1)
logo.pack()

# Previews
label_preview_original = Label(preview_frame, text='Original', font=('Arial', 14, 'bold'), bg=color0,
                               fg=color1)
label_preview_original.place(x=30, y=5)

label_preview_transform = Label(preview_frame, text='Convertida', font=('Arial', 14, 'bold'), bg=color0,
                                fg=color1)
label_preview_transform.place(x=260, y=5)

# Controles
(ttk.Label(control_frame, text="Intensidade", font=('comic sans MS', 14, 'bold'), background=color0, foreground=color1)
 .place(x=160, y=5))
scale_intensity = Scale(control_frame, command=convert_image, from_=50, to=300, orient="horizontal", length=200, bg=color0, fg=color1)
scale_intensity.set(175)
scale_intensity.place(x=115, y=40)

(ttk.Label(control_frame, text="Brilho", font=('comic sans MS', 14, 'bold'), background=color0, foreground=color1)
 .place(x=185, y=87))
scale_brightness = Scale(control_frame, command=convert_image, from_=50, to=200, orient="horizontal", length=200, bg=color0, fg=color1)
scale_brightness.set(125)
scale_brightness.place(x=115, y=125)

(ttk.Label(control_frame, text="Contraste", font=('comic sans MS', 14, 'bold'), background=color0, foreground=color1)
 .place(x=165, y=170))
scale_contrast = Scale(control_frame, command=convert_image, from_=50, to=200, orient="horizontal", length=200, bg=color0, fg=color1)
scale_contrast.set(125)
scale_contrast.place(x=115, y=210)

# Botões
button_select = Button(janela, text="Escolher Imagem", command=choose_image, bg=color5, fg=color1, font=('Arial', 10), width=15)
button_select.place(x=20, y=550)

button_save = Button(janela, text="Salvar Imagem", command=save_image, bg=color4, fg=color1, font=('Arial', 10), width=15)
button_save.place(x=300, y=550)

janela.mainloop()
