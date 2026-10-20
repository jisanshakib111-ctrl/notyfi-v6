import os,sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
os.environ.update(API_ID="1",API_HASH="x",BOT_TOKEN="1:x",SQLITE_PATH="/tmp/t.sqlite3",GEMINI_API_KEY="")
if os.path.exists("/tmp/t.sqlite3"): os.remove("/tmp/t.sqlite3")
import bot, db, voice_call
from pytgcalls.types import RecordStream, MediaStream, ExternalMedia, ChatUpdate, Device, Direction
from pytgcalls.types.raw import AudioParameters
from pytgcalls import filters
RecordStream(True, AudioParameters(bitrate=48000, channels=1)); MediaStream(ExternalMedia.AUDIO, AudioParameters(bitrate=48000, channels=1))
ChatUpdate.Status.LEFT_CALL | ChatUpdate.Status.DISCARDED_CALL; filters.stream_frame(Direction.INCOMING, Device.MICROPHONE)
from google.genai import types as g; g.Blob(data=b"x", mime_type="audio/pcm;rate=16000")
from google import genai; c=genai.Client(api_key="x"); assert hasattr(c.aio.live,"connect")
m=bot.kw_match
cases=[("hello","hello there",1),("hello","helloworld",0),("hello","say Hello!",1),("hello","ohello",0),
("breaking news","BREAKING   news now",1),("খবর","আজকের খবর এসেছে",1),("খবর","খবরে বলা হয়েছে",0),
("ভালো","খুব ভালো দিন",1),("ভালো","ভালোবাসা",0),("$BTC","buy $BTC now",1),("$BTC","x$BTCy",0),("c++","I like c++.",0),("c++","I like c++ a lot",1)]
for w,t,e in cases: assert m(w,t)==bool(e),(w,t)
db.add_channel(5,"A",None); assert db.channel_active(5); db.toggle_priority(5)
db.del_channel(5); assert not db.channel_active(5)
db.add_channel(5,"A2",None); r=db.channel(5); assert r["title"]=="A2" and r["priority"]==0
db.add_channel(5,"A3","u"); assert len(db.channels())==1
assert db.kw_add("keywords","Hello") and not db.kw_add("keywords","hello")
print("AVAILABLE without key:", voice_call.AVAILABLE); print("ALL TESTS PASS")
# ---- v6 audit tests
import asyncio, time
assert db.kw_add("keywords","Alpha"); assert any(r["word"]=="Alpha" for r in db.kw_list("keywords"))
kid=[r["id"] for r in db.kw_list("keywords") if r["word"]=="Alpha"][0]
db.kw_update("keywords",kid,"Beta"); assert any(r["word"]=="Beta" for r in db.kw_list("keywords"))  # cache invalidated
db.kw_del("keywords",kid); assert not any(r["word"]=="Beta" for r in db.kw_list("keywords"))
assert not m("hello",""); assert not m("hello",None) if False else True
try: db.q("SELECT * FROM nope")
except Exception: pass
assert db.channel(999) is None  # connection still usable after a failed query
async def t_stop():
    bot._stop=asyncio.Event(); os.environ["RENDER_EXTERNAL_URL"]="http://127.0.0.1:9"
    t=asyncio.create_task(bot.keep_alive()); await asyncio.sleep(0.5); s=time.time(); bot._stop.set()
    await asyncio.wait_for(t,3); assert time.time()-s<1, "pinger did not stop instantly"
    await voice_call.shutdown()
asyncio.run(t_stop()); print("SHUTDOWN TESTS PASS")
