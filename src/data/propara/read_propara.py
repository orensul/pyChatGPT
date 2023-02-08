
import json
import argparse
import csv
import os
import time
import openai
from datetime import date
from openai.error import AuthenticationError

propara_train_tsv_file = 'grids.v1.train.tsv'
propara_train_json_file = 'grids.v1.train.json'
propara_dev_json_file = 'grids.v1.dev.json'
propara_test_json_file = 'grids.v1.test.json'
propara_train_para_id_title = 'grids.v1.train.para_id_title.json'
dataset_type_file = {"train": propara_train_json_file, "dev": propara_dev_json_file, "test": propara_test_json_file}

original_text_files_path = '../original_text_files/'
OPENAI_API_KEY = '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'
openai.api_key = OPENAI_API_KEY

output_csv_file = 'analogies_subjects.csv'
output_csv_file_far = 'analogies_subjects_far.csv'

examples_txt = 'GPT3_prompts_subset.txt'
examples_far_txt = 'GPT3_prompts_subset_far.txt'
examples_propara_topics_txt = 'GPT3_prompts_propara_topics.txt'
examples_csv = 'analogies_few_shot.csv'
examples_base_target_generation = 'GPT3_prompts_analogies_fields_generate_base_target.txt'

analogies_output_csv = 'GPT3_generated_analogies.csv'
far_analogies_output_csv = 'GPT3_generated_far_analogies.csv'
analogies_base_target_csv = 'analogies_subjects_base_target.csv'

far_analogies_propara_topics_output_csv = 'GPT3_analogies_propara_topics.csv'

legal_analogies_output_csv = 'GPT3_generated_legal_analogies.csv'

# domains = ['Electrical Engineering', 'Mechanical Engineering', 'Chemical Engineering','Physics', 'Biology', 'Chemistry']

domains = ['Engineering', 'Natural Sciences', 'Social Sciences']

def create_propara_files():
    paragraph_titles = get_paragraph_titles(propara_train_tsv_file)
    d = {}
    for t in paragraph_titles:
        d[t] = 1 if t not in d else d[t] + 1

    data = read_propara_paragraphs(dataset_type_file[args.dataset_type])
    para_id_title_map = {}
    for i in range(len(data)):
        para_id_title_map[data[i]["para_id"]] = paragraph_titles[i]

    # write_paragraph_id_title(para_id_title_map, propara_train_para_id_title)

    converted_data = [{} for _ in range(len(data))]
    for idx, sample in enumerate(data):
        para_id, para_prompt, texts = sample["para_id"], para_id_title_map[sample["para_id"]], sample["texts"]
        converted_data[idx]["para_id"], converted_data[idx]["para_prompt"], converted_data[idx][
            "texts"] = para_id, para_prompt, texts

    return converted_data


def create_analogy(paragraph_prompt):
    prompt = "The subject of the Source paragraph is " + '"' + paragraph_prompt + '"' + "\n" + \
             "Suggest another process that is analogous, but from a far academic field. What is the subject of the analogous process? please write only the subject of the analogous process as a question."
    print(prompt)
    target_prompt = gpt3(prompt)
    time.sleep(1)
    print(target_prompt)
    prompt = "The subject of the analogous process is " + '"' + target_prompt + '"' + "\n" + \
             "What is the field of the analogous process?" + \
             "Write " + '"' + "The academic field of the analogous process is: " + '"' + "and then the field"
    target_field = gpt3(prompt)
    time.sleep(1)
    prompt = "Explain the analogy between " + paragraph_prompt + " to the " + target_prompt + "\n"
    explain = gpt3(prompt)
    explain = explain.replace('.', '.\n')
    print(explain)
    time.sleep(1)
    target_field = target_field.split("The academic field of the analogous process is:")[-1].strip().replace('.', '')
    print(target_field)
    return target_prompt, target_field, explain



def exp1():
    converted_data = create_propara_files()

    header = ['source_id', 'source_subject', 'source_text', 'source_field', 'target_subject', 'target_field', 'explain']
    data = []
    with open(output_csv_file_far, 'r') as file:
        csvreader = csv.reader(file)
        processed_ids = set([row[0] for row in csvreader]) - set(['source_id'])

    for paragraph in converted_data[:15]:
        paragraph_text, paragraph_prompt, paragraph_id = "\n".join(paragraph["texts"]), paragraph["para_prompt"], paragraph[
            "para_id"]
        if paragraph_id in processed_ids:
            continue
        prompt = "Source paragraph:\n" + '"' + paragraph_text + '"' + "\n\n" + \
                 "Please read the Source paragraph. The subject of the Source paragraph is " + '"' + paragraph_prompt + '"' + "\n" \
                                                                                                                              "What is the academic field of the Source paragraph? " + \
                 "write " + '"' + "The academic field of the Source paragraph is:" + '"' + " and then the field"
        print(prompt)
        source_field = gpt3(prompt)
        time.sleep(1)
        source_field = source_field.split("The academic field of the Source paragraph is:")[-1].strip().replace('.', '')
        print(source_field)
        target_prompt, target_field, explain = create_analogy(paragraph_prompt)
        data.append([paragraph_id, paragraph_prompt, paragraph_text, source_field, target_prompt, target_field, explain])

    if len(data) > 0:
        with open(output_csv_file_far, 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(data)


def   process_gpt_result(result):
    target_text, after = result.split("SUBJECT:")
    target_text = target_text[:-1]
    after = after.strip()
    split = after.split("MAPPINGS:")
    target_prompt = split[0]
    target_mappings = ''
    if len(split) == 2:
        target_mappings = split[1]
    target_prompt, target_mappings = target_prompt[:-1], target_mappings[1:]
    return target_prompt, target_text, target_mappings


def clean_illegal_data():
    examples_pairs_subjects = []
    with open(examples_csv, 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            examples_pairs_subjects.append([row[0], row[2]])
    examples_pairs_subjects = examples_pairs_subjects[1:]

    header = ['source_id', 'source_subject', 'source_text', 'target_subject', 'target_text', 'target_mappings']
    data = []

    with open(analogies_output_csv, 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            source_id, source_text, target_text, target_mappings = row[0], row[2], row[4], row[5]
            source_subject, target_subject = row[1], row[3]
            if source_subject == target_subject:
                continue
            if (source_subject, target_subject) in [(row[0], row[1]) for row in examples_pairs_subjects]:
                continue
            if source_id == 'source_id':
                continue
            data.append([source_id, source_subject, source_text, target_subject, target_text, target_mappings])

    with open(legal_analogies_output_csv, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)


def gpt3_generate_target_propara_topics_analogies():
    start_paragraph_id, end_paragraph_id = 0, 20
    converted_data = create_propara_files()

    header = ['source_id', 'source_subject', 'source_domain', 'target_domain', 'target_subject', 'target_field', 'mappings']
    data = []



    with open(far_analogies_propara_topics_output_csv, 'r') as file:
        csvreader = csv.reader(file)
        processed_ids = set([row[0] for row in csvreader])

    with open(examples_propara_topics_txt) as f:
        examples_prompt = "".join(f.readlines())

    for paragraph in converted_data[start_paragraph_id:end_paragraph_id]:
        paragraph_prompt, paragraph_id = paragraph["para_prompt"], paragraph["para_id"]
        if paragraph_id in processed_ids:
            continue

        source_domain_prompt = "Write the field of the following subject: " + '"' + paragraph_prompt + '"' + " Write FIELD: and then one of the following options: "
        for target_domain in domains:
            source_domain_prompt = source_domain_prompt + " " + target_domain + " or"
        source_domain = gpt3(source_domain_prompt[:-2])
        _, source_domain = source_domain.split('FIELD:')
        source_domain = source_domain.strip()
        time.sleep(2)

        for target_domain in domains:
            examples_and_source_paragraph_prompt = examples_prompt + "\n\n" + "Inputs:" + "\n" + "SUBJECT:" + \
                                                   paragraph_prompt + "\n" + "TARGET_DOMAIN: One of the fields of " \
                                                   + target_domain + "\n" + "Outputs:\n"
            result = gpt3(examples_and_source_paragraph_prompt)
            time.sleep(2)
            target_subj, after = result.split('TARGET_FIELD:')
            before, target_subj = target_subj.split('SUBJECT:')
            target_subj = target_subj[:-1]
            target_field, after = after.split('MAPPINGS:')
            target_field = target_field[1:-1]
            mappings = after[1:]
            print(paragraph_id, paragraph_prompt, source_domain, target_domain, target_subj, target_field)
            data.append([paragraph_id, paragraph_prompt, source_domain, target_domain, target_subj, target_field, mappings])

    if len(data) > 0:
        with open(far_analogies_propara_topics_output_csv, 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(data)



def gpt3_generate_far_analogous_pairs():
    start_paragraph_id, end_paragraph_id = 0, 40
    converted_data = create_propara_files()

    header = ['source_id', 'source_subject', 'source_text', 'target_subject', 'target_domain', 'target_text', 'target_mappings']
    data = []

    with open(far_analogies_output_csv, 'r') as file:
        csvreader = csv.reader(file)
        processed_ids = set([row[0] for row in csvreader])

    with open(examples_far_txt) as f:
        examples_prompt = "".join(f.readlines())



    for paragraph in converted_data[start_paragraph_id:end_paragraph_id]:
        paragraph_text, paragraph_prompt, paragraph_id = "\n".join(paragraph["texts"]), paragraph["para_prompt"], \
                                                         paragraph[
                                                             "para_id"]
        if paragraph_id in processed_ids:
            continue

        for target_domain in domains:
            examples_and_source_paragraph_prompt = examples_prompt + "\n\n" + "Inputs:" + "\n" + "PARAGRAPH:\n" + \
                                               paragraph_text + "\n" + "SUBJECT: " + paragraph_prompt + "\n" + "TARGET_DOMAIN: " + target_domain + "\n" + "Outputs:\n" + "TARGET_PARAGRAPH:\n"
            print(examples_and_source_paragraph_prompt)
            result = gpt3(examples_and_source_paragraph_prompt)
            time.sleep(2)
            print(result)
            target_prompt, target_text, target_mappings = process_gpt_result(result)
            data.append([paragraph_id, paragraph_prompt, paragraph_text, target_prompt, target_domain, target_text, target_mappings])

    if len(data) > 0:
        with open(far_analogies_output_csv, 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(data)







def gpt3_generate_analogous_pairs():
    start_paragraph_id, end_paragraph_id = 0, 2
    converted_data = create_propara_files()

    header = ['source_id', 'source_subject', 'source_text', 'target_subject', 'target_text', 'target_mappings']
    data = []

    times_run_gpt_same_paragraph = 3

    with open(analogies_output_csv, 'r') as file:
        csvreader = csv.reader(file)
        processed_ids = set([row[0] for row in csvreader])

    with open(examples_txt) as f:
        examples_prompt = "".join(f.readlines())

    for paragraph in converted_data[start_paragraph_id:end_paragraph_id]:
        paragraph_text, paragraph_prompt, paragraph_id = "\n".join(paragraph["texts"]), paragraph["para_prompt"], \
                                                         paragraph[
                                                             "para_id"]
        examples_and_source_paragraph_prompt = examples_prompt + "\n\n" + "Inputs:" + "\n" + "PARAGRAPH:\n" + \
                                               paragraph_text + "\n" + "SUBJECT: " + paragraph_prompt + "\n" + "Outputs:\n" + "TARGET_PARAGRAPH:\n"
        print(examples_and_source_paragraph_prompt)
        if paragraph_id in processed_ids:
            continue

        for _ in range(times_run_gpt_same_paragraph):
            result = gpt3(examples_and_source_paragraph_prompt)
            time.sleep(2)
            print(result)
            target_prompt, target_text, target_mappings = process_gpt_result(result)
            data.append([paragraph_id, paragraph_prompt, paragraph_text, target_prompt, target_text, target_mappings])

    if len(data) > 0:
        with open(analogies_output_csv, 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(data)

def gpt3_generate_base_target_analogies():

    with open(analogies_base_target_csv, 'r') as file:
        csvreader = csv.reader(file)
        seen_records = set()
        for row in csvreader:
            record = row[0] + ';' + row[1] + ';' + row[2] + ';' + row[3]
            record = record.lower()
            seen_records.add(record)

    header = ['base_subject', 'base_field', 'target_subject', 'target_field', 'mappings']
    data = []
    curr_data = set()
    for _ in range(100):
        with open(examples_base_target_generation) as f:
            examples_prompt = "".join(f.readlines())
            result = gpt3(examples_prompt)
            time.sleep(2)
            print(result)
            base_field, after = result.split('BASE:')
            base_field = base_field[:-1].strip()

            base_subject, after = after.split('TARGET FIELD:')
            base_subject = base_subject[:-1].strip()

            target_field, after = after.split('TARGET:')
            target_field = target_field[:-1].strip()

            target_subject, after = after.split('MAPPINGS:')
            target_subject = target_subject[:-1].strip()

            mappings = after[1:]

            curr_record = base_subject + ';' + base_field + ';' + target_subject + ';' + target_field
            curr_record = curr_record.lower()

            if curr_record in seen_records:
                continue

            if curr_record in curr_data:
                continue

            data.append([base_subject, base_field, target_subject, target_field, mappings])
            curr_data.add(curr_record)
    if len(data) > 0:
        with open(analogies_base_target_csv, 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(data)






def main(args):
    # gpt3_generate_analogous_pairs()
    # gpt3_generate_far_analogous_pairs()
    # gpt3_generate_base_target_analogies()
    gpt3_generate_target_propara_topics_analogies()






def gpt3(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    if response:
        if response.choices and response.choices[0]:
            res = response.choices[0].text.strip()
            return res
    return None

def write_paragraph_id_title(para_id_title_map, filename):
    with open(filename, 'w') as output_file:
        json.dump(para_id_title_map, output_file)


def get_paragraph_titles(filename):
    paragraph_titles = []
    f = open(filename, "r")
    lines = f.readlines()
    for line in lines:
        if "\t\tPROMPT:" not in line:
            continue
        start = line.find("\t\tPROMPT:") + len("\t\tPROMPT:")
        end = line.find("\t-")
        paragraph_title = line[start+1:end]
        paragraph_titles.append(paragraph_title)
    return paragraph_titles


def write_original_text_files(converted_data):
    for data in converted_data:
        para_id, texts = data['para_id'], data['texts']
        output_file_path = original_text_files_path + 'propara_para_id_' + para_id + '.txt'
        output_file = open(output_file_path, 'w')
        for line in texts:
            output_file.write(line)
            output_file.write("\n")


def read_propara_paragraphs(filename):
    f = open(filename, "r")
    lines = f.readlines()
    data = [{} for _ in range(len(lines))]
    for idx, line in enumerate(lines):
        json_object = json.loads(line)

        para_id, texts, participants, states = json_object['para_id'], json_object['sentence_texts'], \
                                               json_object['participants'], json_object['states']
        data[idx]['para_id'], data[idx]['texts'], data[idx]['participants'], data[idx]['states'] = para_id, texts, \
                                                                                                   participants, states
    return data


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_type', type=str, default='train',
                        help='possible values: train / dev / test')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    main(args)