from pyChatGPT import ChatGPT
import os

class Paragraph:
    def __init__(self, filename, prompt):
        self.filename = filename
        self.prompt = prompt

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

session_token = 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..wV3CPM-gYZL0nvkF.xsUE9jz48jELoIVTlRQI8P5H8dx24cCzkD0fNfH9HiuBeYsLJCscQWQ-klAfdql2f13N49nm0xgMpHvkahY6L132ocsu1kLjBVHF6M2I2bnMqd8AVqmW95Y88HHUKSLiGBYpPvozRWWmUhDiF7kYdsU9hp95qTf1x1KK8tNsRRBzna5ZC-tPNZ8msS9La84lFBn66MeVbUG44ZAO-NMNKRuK97e4tyPg0hhOWR22v6GX170-OQP9u9SJV8G1SU8aa8oo5w7Ida5T8xNUEDUMXEqMYw1XmMLjZYTgct4CLZ1hqGTr1ejg0j1bHgmwnew2a_0iURjmLm9QlJY8WP5Trt5nkLVzqNEVXeiZ2cVxH3-BKEDeQHNkUhNK7wx_jJ-RDcqLvzcNgaQS7_evy87WpmEJ1ORBj_ZC3bAy3QXNQn9H7c5N-bVywKmaJLadVNWFvWpRxw-Mp54BDrz-CRqajNu8TAtMQ4-H-aqUeA32Kwv1gYDX2pi46PyRTgZ8vfDp6Hw_qKnLDEm3xqgez3-zSjVqDN4MvGhd8d3hW0x4upojUxbiCacRnNhDxtl0QKVCf2n6L27TjfvtUqP-Or3nYXXdZVD37gvbXm5zWDphszY2HH21X9cAezMuT6jNLVquRFIt7pOMMfjO4IoZjG6Lc7XsOFcaYprCWHs93PGTpQnwY13FPiPUhHIAoiHuGqiIuP8CJZoKV7LFnbsUnIh1WFEQOWjdxT4kJ4gcIjGB4ZowRdOp6vJV8hsHUBgVaNOB9je4Q9kgsPiSJaqUeFmJLi2C5leZEuBoKLf5sD7Lc9W7LqIdiej3ikcq4OQXh6kEb1D4nUQBqYYL4PdhyzPZK4RCJf9_NRYhx-F8UupHC29BnwmRxeiSvGxoNMSxAO01w6KOkNAZaiktpLVcu8C0AtuDhRxXb5R5-cl4H0cx11q6Fg8oQbbH-m6oXi2MbzfeP63oWsevSr0oZIAlDKv-u2SueIstNzsUvaamizwY77qDhzg6XFAX4NopXVojWfGLtldzPtDTWHnppVbFdybucT5lQGPXNxEm3cgePn5lsWq_L36dDrm1CDRNWEKnhygMHJqOSou6FL-NdurOhiHCn2gMFL7BSsxjj8jTo2YV8vkpirzkdHVWLErbViyPrA8HP0WEWoegvtCjvf-YT_A23Mf8O8pO4XDKWbyci80nJ8l06Eb1OUnw0vspxGFuh7LpmxHOG8JZhRCNPjRBer8JGW0OwoPr7_RZ7QpNJZQ1NtL8_JaZd6aAI6dQsreHii2Ks6W6JrVEfyAp4Iz7jyVjRV4WxeqDOWzdyKp8lKipUMe5fhjnk9xv8YTfCyq3Y2qUaYz1ae-JtTd4IY0QbYNpFrESdGpr6avvOUCr-8-jbLxyROJjfxd4wAbZR9B_IeWsicJPqCvPsOSp9mxlQKtJgkh5DQGYd-BgNBORNJ8YFqPk0Dh0LzOG2wHDCcvEuBGhFebLvp9U42ihzXV7zdpCTZPCyPCSI124LCJ-RkxSQYcAeskjvMiqUQXHpIkeybGY_p7ip0BPzFHKdfu5VUyUyW_oth2AWpF1SwlmYB8Lw-ePBWMEO8LrUrkUDumULcnVf-SUeJzNN1jM2t8Q3be_L8WBuuEUUv_m__eTf-AFq88mdkn2NoZYIWR1aEs6LlHfBRCM3ACP2pcNemDZaaF67UOQ0IarOv5WsZ7FGsRVPqjfi_PrBFe2s3aaAlaIQuf679nJjCMExTW7SzK9YvxvRQpPhq7d-CGPoCztmrFXAX2T356IKj54S_k3d8P_eZuB7E-yrhAJiE7AQ528qesnpqnolFnDv0uorg3VT_P7qwG7EVmSLk4xXgt1OERNt50nX2SYK5LdZIR6bMVuC_rAGSrBmQKmlP8NrOhE9DQmqBQsYIFnCommonxSudDR8S4h1wTo8IAYaSSVuAj5SIz9TRFf7HwWEyvd163f_gZdSGjylrho-_50JZuFTsbS3pA9z7zgzFwcrpE0BDeGKdOBihRyFfgZI3nWHMZcJA_6koN51laeEot4ltgDABeuQ_t0mZ_PTONMM78HLqXx55OVc670QEMJlACntLdb0P0w_oFr4qhyW8Wxr7_CDjMb_GRYV9f-f5CSdON4Nx-dOK2a3OWU8aMjjj2-pvetCz_UU7N-Q7Xo8u3ye4lcq0yKl6UDaLIbSCpKdF36yfdOw0zIC9PiTwVH6mOKzLa4NuK-GI4i-hO56l-qKXF7c0QaIKtynDBj7BLTk26aZM9aCbU9F-rO0ahJpS-_dqBmANwnyjCsyYfyKpqtnSqYsWGELeKhTCxPfLY999K2DP8VzYAwocE246ZqWYqqqsiT2SOW97reTMQIBgleojaM9GE.YcRnMzYsbUgatfXcX8kGWw'

text_files_folder = '../data/coref_text_files'




example_paragraph_pairs = ( (Paragraph("animal_cell.txt", "animal cell"), Paragraph("factory.txt", "how a factory works")),
                            (Paragraph("electrical_circuit.txt", "electrical circuit"), Paragraph("water_pump.txt", "water pump"))
                            )

def read_file(filename):
    input_file = open(filename, 'r')
    text = ''
    for line in input_file:
        text += line
    return text


def get_inputs_from_examples():
    inputs = []
    for pair in example_paragraph_pairs:
        p1_prompt, p1_filename = pair[0].prompt, pair[0].filename
        p2_prompt, p2_filename = pair[1].prompt, pair[1].filename

        p1_path, p2_path = get_text_file_path(p1_filename), get_text_file_path(p2_filename)
        p1_text, p2_text = read_file(p1_path), read_file(p2_path)

        input = create_input(p1_text, p2_text, p1_prompt, p2_prompt)
        inputs.append(input)
    return inputs


def run_examples(chat):
    inputs = get_inputs_from_examples()
    clear_screen()
    for input in inputs:
        print(input)
        prompt = input
        if prompt.lower() == 'reset':
            chat.reset_conversation()
            clear_screen()
            continue
        if prompt.lower() == 'quit':
            break
        print('\nChatGPT: ', end='')
        response = chat.send_message(prompt)
        print(response['message'], end='')




def create_input(base_text, target_text, base_prompt, target_prompt):
    input = ''
    input = 'Source paragraph:\n'
    input += base_text + '\n'
    input += 'Target paragraph:\n'
    input += target_text + '\n'
    input += 'The Source paragraph is about ' + base_prompt + '.\n'
    input += 'The Target paragraph is about ' + target_prompt + '.\n'
    input += 'Note that the two paragraphs are analogous.'
    return input

def get_text_file_path(text_file_name):
    return text_files_folder + '/' + text_file_name



def init_chatGPT():
    while True:
        chat = ChatGPT(session_token, "")
        break
    return chat

if __name__ == '__main__':
    chat = init_chatGPT()
    run_examples(chat)



