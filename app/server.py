from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse, FileResponse
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
import uvicorn, aiohttp, asyncio
from io import BytesIO

from fastai import *
from fastai.vision import *

from PIL import Image
from tempfile import NamedTemporaryFile

export_file_url = 'https://storage.googleapis.com/mpirprf/export.pkl'
export_file_name = 'export.pkl'

classes = ['parabrisas']
path = Path(__file__).parent

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])
app.mount('/static', StaticFiles(directory='app/static'))

def acc_camvid(input, target):
    target = target.squeeze(1)
    mask = target != 0
    return (input.argmax(dim=1)[mask]==target[mask]).float().mean()

async def download_file(url, dest):
    if dest.exists(): return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(dest, 'wb') as f: f.write(data)

async def setup_learner():
    await download_file(export_file_url, path/export_file_name)
    try:
        defaults.device = torch.device('cpu')
        learn = load_learner(path, export_file_name)
        return learn
    except RuntimeError as e:
        if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
            print(e)
            message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
            raise RuntimeError(message)
        else:
            raise

defaults.device = torch.device('cpu')

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
    data = await request.form()
    img_bytes = await (data['file'].read())
    img = open_image(BytesIO(img_bytes))
    y = learn.predict(img)[0]
    #img_tmp = NamedTemporaryFile(suffix='.jpg')
    y_tmp = NamedTemporaryFile(suffix='.png')
    #out_tmp = NamedTemporaryFile(suffix='.jpg')
    
    #img.save(img_tmp)
    y.save(y_tmp)
    
    #im1 = Image.open(img_tmp)
    #im2 = Image.open(y_tmp)
    #blended = Image.blend(im1, im2, alpha=0.5)
    #blended.save(out_tmp)
    
    response = FileResponse(y_tmp)
    await response(receive, send)

if __name__ == '__main__':
    if 'serve' in sys.argv: uvicorn.run(app=app, host='0.0.0.0', port=5042)
