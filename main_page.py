import gradio as gr
import matrix_test 
from kiwipiepy import Kiwi
import time

kiwi = Kiwi()

Matrix = matrix_test.load_martrix('processed_data/IT_dataset.pkl')
Matrix_n1 = matrix_test.load_martrix('processed_data_n=1/IT_과학_dataset.pkl')

komoran = matrix_test.komoran
compos_hangle_ver2 = matrix_test.compos_hangle_ver2

def generate_sentence(seed_text: str, max_steps: int, T: float, time_step: float) -> str:
    """
    seed_text: 사용자가 입력한 시작 문장
    max_steps: 생성할 단어(토큰) 개수
    """
    seed_text = seed_text.strip()
    if not seed_text:
        return "시작 문장을 입력해 주세요."

    # 형태소 분석 + compos_hangle_ver2 적용
    try:
        sentence = compos_hangle_ver2(komoran.pos(seed_text))
    except Exception as e:
        return f"형태소 분석 중 오류 발생: {e}"

    for _ in range(max_steps):
        if len(sentence) < 3:
            next_word = matrix_test.select_word(Matrix_n1, (sentence[-1], ), T) 
        else:
            try:
                next_word = matrix_test.select_word(Matrix, (sentence[-3], sentence[-2], sentence[-1]), T)
            except:
                next_word = matrix_test.select_word(Matrix_n1, (sentence[-1], ), T) 

        time.sleep(time_step)

        sentence.append(next_word)
        rlt = kiwi.space("".join(sentence))
        yield rlt

    # compos_hangle_ver2가 반환하는 단위에 따라 join 방식 조절
    # 지금은 그냥 글자/음절 단위라고 보고 붙여서 출력
    

with gr.Blocks() as demo:
    gr.Markdown("# 한국어 마르코프체인 기반 문장 생성기")
    gr.Markdown("시작 문장을 입력하면 학습된 전이 행렬을 이용해 이어지는 문장을 생성합니다.")

    with gr.Row():
        with gr.Column():
            seed_box = gr.Textbox(
                label="시작 문장",
                lines=2,
                placeholder="예: 애플이 지난 13일",
            )
            step_slider = gr.Slider(
                minimum=1,
                maximum=200,
                value=50,
                step=1,
                label="생성할 토큰(단어) 개수",
            )
            T_value_slider = gr.Slider(
                minimum=0.01,
                maximum=1,
                value=0.35,
                step=0.01,
                label="온도(Temperature) 값 조정",
            )
            time_step = gr.Slider(
                minimum=0.1,
                maximum=10,
                value=0.2,
                step=0.1,
                label="단어 출력시간 조정",
            )
            generate_button = gr.Button("문장 생성하기")

        with gr.Column():
            output_box = gr.Textbox(
                label="생성된 문장",
                lines=10,
            )

    generate_button.click(
        fn=generate_sentence,
        inputs=[seed_box, step_slider, T_value_slider, time_step],
        outputs=output_box,
    )


if __name__ == "__main__":
    demo.launch()
