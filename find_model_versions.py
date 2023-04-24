# Author: Viet Dac Lai
import openai
import pprint
import env_setter
import os

env_setter.setup_keys()

openai.organization =  os.environ["OPENAI_ORGANIZATION_ID"] 
openai.api_key = os.environ["OPENAI_API_KEY"] 


def list_all_models():
    model_list = openai.Model.list()['data']
    model_ids = [x['id'] for x in model_list]
    model_ids.sort()
    pprint.pprint(model_ids)

if __name__ == '__main__':
    list_all_models()