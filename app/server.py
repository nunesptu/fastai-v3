from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from google.cloud import storage
import uvicorn, aiohttp, asyncio
import os
import uuid
from io import BytesIO

from fastai import *
from fastai.vision import *

export_file_url = 'https://drive.google.com/uc?export=download&id=13Nxml5y0VVrn7J8GjTuxZDO1WwR2YslX'
export_file_name = 'export.pkl'

bucket_name = 'macornotbook'

classes = ['macbook', 'notmacbook']
path = Path(__file__).parent

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])
app.mount('/static', StaticFiles(directory='app/static'))

def rename_blob(blob_name, new_name):
    """Renames a blob."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    new_blob = bucket.rename_blob(blob, new_name)

    print('Blob {} has been renamed to {}'.format(
        blob.name, new_blob.name))

def upload_blob(data, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(data, content_type='image/jpg')
    print('File uploaded to {}.'.format(destination_blob_name))

async def download_file(url, dest):
    if dest.exists(): return
    async with aiohttp.ClientSession() as session:
        print('Saving model...')
        async with session.get(url) as response:
            data = await response.read()
            with open(dest, 'wb') as f: f.write(data)
            print('Done')

async def setup_learner():
    await download_file(export_file_url, path/export_file_name)
    try:
        learn = load_learner(path, export_file_name)
        return learn
    except RuntimeError as e:
        if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
            print(e)
            message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
            raise RuntimeError(message)
        else:
            raise

loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_learner())]
learn = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()

@app.route('/')
def index(request):
    html = path/'view'/'index.html'
    return HTMLResponse(html.open().read())

@app.route('/analyze', methods=['POST'])
async def analyze(request):
    uuid_str = str(uuid.uuid4())
    data = await request.form()
    img_bytes = await (data['file'].read())
    img = open_image(BytesIO(img_bytes))
    prediction = learn.predict(img)[0]
    # Save image to google cloud
    print('Saving to google cloud...')
    upload_blob(img_bytes, uuid_str)
    print('Done.')
    return JSONResponse({'result': str(prediction), 'classes': classes, 'img_id': uuid_str})

@app.route('/report', methods=['POST'])
async def report(request):
    report = await request.json()
    new_name = '%s/%s' % (report['class'], report['img_id'])

    print("Moving to %s..." % new_name)
    rename_blob(report['img_id'], new_name)
    print('Done')
    return RedirectResponse(url='/')

if __name__ == '__main__':
    if 'serve' in sys.argv:
        port = int(os.getenv('PORT', 5042))
        uvicorn.run(app=app, host='0.0.0.0', port=port)
