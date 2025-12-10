# import gradio as gr

# # Function for the main page
# def greet(name):
#     return "Hello " + name + "!"

# # Function for the second page
# def multiply(num):
#     return num * 2

# # Main application context
# with gr.Blocks() as demo:
#     # --- Main Page Content (automatically named "Home" in navbar) ---
#     gr.Markdown("## Welcome to the Home Page")
#     name = gr.Textbox(label="Enter your name")
#     output = gr.Textbox(label="Output Box")
#     greet_btn = gr.Button("Greet")
    
#     # Event listener for the main page
#     @gr.on([greet_btn.click, name.submit], inputs=name, outputs=output)
#     def greet_user(name_input):
#         return greet(name_input)

#     # --- Second Page Content ---
#     with demo.route("Multiplier", "/multiply"):
#         gr.Markdown("## This is the Multiplier Page")
#         num = gr.Number(label="Enter a number")
#         output_num = gr.Number(label="Doubled number")
#         multiply_btn = gr.Button("Multiply by 2")

#         # Event listener for the second page
#         @multiply_btn.click(inputs=num, outputs=output_num)
#         def multiply_number(number_input):
#             return multiply(number_input)

# if __name__ == "__main__":
#     demo.launch()
import preprocesse
import matrix_test


print(len(matrix_test.load_martrix('processed_data/IT_dataset.pkl')))
# print(len(matrix_test.load_martrix('processed_data/IT_과학_dataset.pkl')))
print(len(matrix_test.load_martrix('processed_data/취미_dataset.pkl')))