from pyChatGPT import ChatGPT
import os
import openai

from openai.error import AuthenticationError

class Paragraph:
    def __init__(self, filename, prompt):
        self.filename = filename
        self.prompt = prompt

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

session_token = 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..kiINyIQJTMr8lKUO.HMqEUfgVDTgvNWMLpsnJCpd6ideNnpJSwX1IDgLzd_801OctgURL5jkDx4XuXhuZnfXRX8Fuyher-L116IcYGoM7scLaBmv6ui0y1FWfGvCQ6qdMtpZjhMb5DzzoMsIUOkX-jY_4_Wy6Qwl8u_BMGdzEpv8GCL34CqSN3tJDxk5X5hagMzYu8c5zeFXjCq1TdRSWdWeI4embxh_AetQ5ieok15UGFaLZ0UX0HdBN4Xj9OIeygTvbZJESK-T_R15VvqyNFhCLn260ytREBtBtTBZ5wgaBtcVIEQ4JrUkGoXS1Gd3nLSfPK7zdD4dOZtNz_LRWxHYzXlXMAf5cWMBvrNpvHqMEfLJBCFmXhEGivoHuyxYoji0KJrwt74wt-Y7AKN5GuLhT5WiedRKd43IEbBiJ-eKEmVjy0hK-Cd04r-JJcrG_-k47-EMiQg_xVK2baHt-OSjrPVdrvi7L93RTsMOlbIzGu_Mb-iS0Zkr2mLrIaIagpctTXEFM20nAHxPofZNA1ql5E2JbvO9x78AaW-UXwxiTuuvh5R5P53nnh7VH7mM8KK1JNqh0XiDHnntDmWp6eAQyd7pImPfIel9euN5I3MJR9kCp6cYKKTnBRbIgcduLt713sW8vxIV5wABAULG_ujUsaLioCoBsI6Me4CefGOff0Hzp5Nu56VJCmp9kiEo36gwB0jDWJpySTusNWTZfuj7gmJ0W96QP938OJG1wtYQka5Mn5Bded9WspVHJl4nHvQy5GQsX0lMs4a7ON4u1xUy9yKCaSVn1wVU8Va7qLnQnhF50h2TGwgPRkN782CDxdCpcX5Zjus1cViqXJZZ_wjR3j9IDT9EvOpdsOcFyidO4wBSAEMvfWPD3DofKszFaf8R_CUucJO6kKUAfqiVgJKOCmNAYoLTGqn-v9Jq114wlQYWOffWo5hqM6fz6IG6LxBEURuRciGugjXnxXOVdkB8jVPkjdHHj_FIgOFpkJuFAL8kFlY05gTQ1Gtim5TAAPDWv_IH8cMKdPm25CZhc-BKw6W5nafdZR1qL5FVik4dUr5YUdX3JGkTV3t0sEEb-6WcWaEJIAtx_rsfEjBDu-WxOQCt-yjw5dCU3fOQPnk6Z1NhGhZ0aGqpzU8K2WFbzX3WjEmwXezYwLg5tY3b9m4JtaJujgKJix891w7ejD6XKlv5pifwlv8_WOD4n5eSNu4PsWuhVEU9F4_bCmHhIby6p73b9E9MtPJ3MevKxgUJT7uH92t70re1P8mAXy3hkGo2eGJoKRkNocPbFX8nCspZewXq-Q_QmvVkc29V1B9J0EWac43y2QS2KO55xJpkXIh4Asxr6O9dMGa3xtMv8HxKg7Oa6L7zuAplQD5lcNB3nEPvspWAoclTrpDnXS2RThmBtBqCIo5vZEBIYqvflFIvKQZgE2LS4yiaMc66Gv5ixkmmZR0qhQOz9fBA58tQ4hRPPer6UUkgel3_56n9FtO55kwtcOesWgMR7ooH2MH503pGJpBlIRJGSRm38L-BgEK9HYwl-O3jMOakMyHBd5EU9qxQve6YPFsRfbNdcCiwA7hQTkoCPyDSC9y9uL50DQBQ7dYuzgOeUaxl1DZOEfrLy11Z_EVOkYEgEKaPDl3O5GZWc4eRV7T0reQKk-LDNgrhhSZjaML7PkCvYB0_Z8qXsZYfRmzlRT5mgikXbq3J5qLm-sysydKBKvit4S4YRbw_DukGQBX4pnYUr_gXKeyARYW4efFBJloo8TKL-FabtuEwW8dQpBPinxBIWrgK8b-U5_euZ-Kyo9lQs7yTcl02VMPW4j_qu9rIZdGybt305HR58bjC1Q2ke2A-i2R-i9Sk-zGuK23Ax8h3AVnN0gest-OR7ploe44_S49MsK2HHYe9MbgLRoSONTCRTS4J6w3__iJ2aj5SamIAEhwspAozNZgoIEEK2RR_MwzdM9SzkysOGZPG_HGubNlRGMPMt0oRlfqNIJ5IUDt6zH7i8LrjIe_BdMohATNEztpsamVhywsoufGTsm5ZsFkIqZ99L7NUSy-Hm4fCAoyiIbi5IrbpN4cZGuAw-0yhAxrbALRSMidAosWcXuhcJ-AUjOmo2Su5de3sTUIFAZEcopDW-9ZlLMVczviMn-K6GSGIU-7Ykijijb5P8nhvxBsrpjJZEOKwEcQ5T55Ae1aK9LSGND781ICPUT8o637rIRuS5YH2Ir2xscjLxQPoUZUL760dpGz4UF1lRzLdbh1qZ_fNhYJCFau5AbEswSeis65jlSuHAWnhN-cT9qBUzZLaquf-FYmmHrn7jdSlY4UQ9cnywZbrGBEiWYozXv4FLyV1qL7DwFoh5eNWZUHUIfG_3x_uG00Pdhx338VA.DE5qs5HUqDSBvjEv7lejlA'
text_files_folder = '../data/original_text_files'


OPENAI_API_KEY = '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'



example_paragraph_pairs = ((Paragraph("electrical_circuit.txt", "electrical circuit"), Paragraph("water_pump.txt", "water pump")),
                           (Paragraph("animal_cell.txt", "animal_cell"), Paragraph("factory.txt", "how the factory works")))

paragraphs = [Paragraph("propara_para_id_519.txt", "life cycle of the fish")]

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

        input = create_input_example(p1_text, p2_text, p1_prompt, p2_prompt)
        inputs.append(input)
    return inputs

def get_inputs():
    inputs = []
    for paragraph in paragraphs:
        p_prompt, p_filename = paragraph.prompt, paragraph.filename
        p_path = get_text_file_path(p_filename)
        p_text = read_file(p_path)
        input = create_input(p_text, p_prompt)
        inputs.append(input)
        inputs.append('what is the mapping between entities in the analogous paragraphs?')
    return inputs

def find_analogies(chat):
    inputs = get_inputs()
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

    return chat



def run_examples(chat):
    inputs = get_inputs_from_examples()

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

    return chat


def create_input(base_text, base_prompt):
    input = 'Source paragraph:\n'
    input += base_text + '\n'
    input += 'The Source paragraph is about ' + base_prompt + '.\n'
    input += 'Please write a Target paragraph that is analogous to the Source paragraph, no need to explain the analogy.'
    return input

def create_input_example(base_text, target_text, base_prompt, target_prompt):
    input = 'Source paragraph:\n'
    input += base_text + '\n'
    input += 'Target paragraph:\n'
    input += target_text + '\n'
    input += 'The Source paragraph is about ' + base_prompt + '.\n'
    input += 'The Target paragraph is about ' + target_prompt + '.\n'
    input += 'The two paragraphs are analogous.\n'
    input += 'The mapping between entities in the two paragraphs:\n'
    input += 'battery : pump\n'
    input += 'electrical voltage : pressure\n'
    input += 'electrons : water\n'
    input += 'copper wire : pipe\n'
    input += 'resistor : clams'
    return input

def get_text_file_path(text_file_name):
    return text_files_folder + '/' + text_file_name



def init_chatGPT():
    while True:
        chat = ChatGPT(session_token, "")
        break
    return chat

def gpt3():
    openai.api_key = OPENAI_API_KEY


    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="",
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    if response:
        if response.choices and response.choices[0]:
            a = response.choices[0].text
            print(1)
    print(1)




if __name__ == '__main__':

    # gpt3()
    # chat = init_chatGPT()
    # chat = run_examples(chat)
    # find_analogies(chat)



