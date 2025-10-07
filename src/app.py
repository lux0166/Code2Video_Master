import gradio as gr
import traceback
from agent import generate_video_from_code, find_scene_class

# --- Wrapper for Gradio UI ---

def gradio_video_generator(manim_code):
    """
    A wrapper function for the Gradio interface to handle video generation
    and error feedback.
    """
    try:
        if not find_scene_class(manim_code):
            raise ValueError("Lỗi: Không tìm thấy lớp Manim Scene trong mã. Hãy chắc chắn rằng bạn có một lớp kế thừa từ 'Scene', ví dụ: 'class MyScene(Scene):'")

        print("Bắt đầu tạo video...")
        video_path = generate_video_from_code(manim_code)
        print(f"Video đã được tạo thành công: {video_path}")

        # Return the path to the generated video
        return f"Thành công! Video đã được lưu tại: {video_path}"

    except Exception as e:
        print(f"Đã xảy ra lỗi trong quá trình tạo video: {e}")
        traceback.print_exc()
        raise gr.Error(f"Đã xảy ra lỗi: {str(e)}")


# --- Gradio Interface Definition ---

with gr.Blocks(theme=gr.themes.Soft(), title="Code2Video") as demo:
    gr.Markdown("# Code2Video: Tạo video từ mã Manim")
    gr.Markdown("Dán mã Python sử dụng thư viện Manim của bạn vào ô bên dưới và nhấn 'Tạo Video'.")

    with gr.Row():
        manim_code_input = gr.Code(
            label="Mã Manim",
            language="python",
            lines=20,
            value="""from manim import *

class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        square.flip(RIGHT)
        square.rotate(-3 * TAU / 8)
        self.play(Create(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))
"""
        )

    with gr.Row():
        generate_button = gr.Button("Tạo Video", variant="primary")

    with gr.Row():
        # Use a Textbox to display the output path instead of a Video component
        output_path_textbox = gr.Textbox(label="Đường dẫn video kết quả", interactive=False)

    # Connect the button to the function
    generate_button.click(
        fn=gradio_video_generator,
        inputs=manim_code_input,
        outputs=output_path_textbox
    )

if __name__ == "__main__":
    # Launch the Gradio app
    # share=True creates a public link, which is required in this environment
    demo.launch(share=True)