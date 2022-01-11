import fire,json

file_name = 'api_core'
api_modules_subdir = 'exp_api_modules'


def choose_api(api_config_path:str='notebooks_to_api/api_config.json'): 
    ''' Configuring the API with user input '''

    configs = json.load(open(api_config_path))
    files_allowed = configs['files_allowed']
    input_type = configs['input_type']
    bearer_token = configs['bearer_token']
    url_name = configs['url_name']
    func_name = configs['func_name']
    port_nmbr = configs['port_nmbr']
    request_type = configs['request_type']
    num_workers = configs['num_workers']

    if not isinstance(files_allowed, dict): 
        raise TypeError(f'files_allowed must be a dictionary,but given {type(files_allowed)}')
    if not isinstance(bearer_token, str): 
        raise TypeError(f'bearer token must be a string,but given {type(bearer_token)}')
    if not isinstance(url_name, str): 
        raise TypeError(f'url_name must be a string,but given {type(url_name)}')
    if not isinstance(func_name, str):
        raise TypeError(f'func_name must be a string,but given {type(func_name)}')
    if not isinstance(port_nmbr, int):
        raise TypeError(f'port_nmbr must be a integer,but given {type(port_nmbr)}')
    if not isinstance(request_type, str):
        raise TypeError(f'request_type must be a string,but given {type(request_type)}')
    if not isinstance(num_workers, int):
        raise TypeError(f'num_workers must be a integer,but given {type(num_workers)}')

    if request_type not in ['post', 'get']:
        raise ValueError(f'request_type must be either "post" or "get", but given {request_type}')

    file_input = '''
import uvicorn
from fastapi import FastAPI, File, UploadFile, Depends, Response, status
from fastapi.security import OAuth2PasswordBearer
from api_flow import main
from api_flow import load_model

app = FastAPI()

bearer_token = "'''+bearer_token+'''"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
file_types_allowed = '''+str(files_allowed)+'''


@app.on_event('startup')
async def startup_event():

    print('=======MODEL LOADING======')
    global model
    model = load_model()    # dictionary of models, model_name:model_object in case of multiple models
    print('=======MODEL LOADED======')


@app.'''+request_type+'''("/'''+url_name+'''/", status_code=200)
async def '''+func_name+'''(response:Response, file:UploadFile = File(...), token:str = Depends(oauth2_scheme)):

    if token != bearer_token:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "Unauthorized access"

    if (file.filename.split('.')[-1]) in file_types_allowed['image'] and (file.filename.split('.')[-1]) not in file_types_allowed['pdf']:
        response.status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        return "Invalid Document"
    else:
        try:
            output = main(file, model)

            if "couldNotExtract" in output.values() or "" in output.values():
                response.status_code = status.HTTP_206_PARTIAL_CONTENT

            return output

        except Exception as e:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            print(f'while running the following error occured , {e}')


if __name__ == "__main__":
    uvicorn.run("'''+file_name+''':app", host="0.0.0.0", port='''+str(port_nmbr)+''', log_level="info", workers = '''+str(num_workers)+''')
    
'''

    if input_type == 'file':
        with open(f'{api_modules_subdir}/{file_name}.py', 'w') as f: 
            f.write(file_input)


if __name__ == '__main__': fire.Fire(choose_api)