from fastapi import FastAPI 
import uvicorn
import json
from pydantic import BaseModel

app=FastAPI()

@app.get("/test")
def welcam():
    return { "msg": "hi from test"}


@app.get("/test/{name}")
def get_name(name):
    with open("names.text","a")as t:
        t.write(f"{name} \n")

    return { "msg": name}


class TodoBase(BaseModel):
    text :str
    offset: int
    mode: str 


@app.post("/caesar")
def caesar(data:TodoBase):
    text=data.text
    tx=""
    i=data.offset
    if data.mode=="encrypt":
        for ch in text:
            if ord(ch)+i<=122:
                tx+=chr(ord(ch)+i)
            else:
                tx+=chr(((ord(ch)+i)%122)+97)

    elif data.mode=="decrypt":
        for ch in text:
            if ord(ch)-i>=97:
                tx+=chr(ord(ch)-i)
            else:
                tx+=chr((97+26)-i)
    return tx
    

@app.get("/fence/encrypt")
def cipher_endpoints(text):
    tex=""
    for ch in text:
        if ch==" ":
            continue
        tex+=ch
    x=""
    y=""
    for ch in range(len(tex)):
        if ch%2==0:
            x+=tex[ch]
        else:
            y+=tex[ch]
    return x+y


class Text(BaseModel):
    text :str
 

@app.post("/fence/decrypt")
def fence_decrypt(text:Text):
    ch=text.text
    s,char=0,len(ch)//2
    d=""
    if len(ch)%2==0:
        for i in range(len(ch)):
            if i%2==0:
                d+=ch[s]
                s+=1
            else:
                d+=ch[char]
                char+=1
        return d
    else:
        s,char=0,(len(ch)//2)+1
        for i in range(len(ch)):
            if i%2==0:
                d+=ch[s]
                s+=1
            else:
                d+=ch[char]
                char+=1
        return d


    
if __name__ == "__main__":
    print(" מתחיל את שרת Todo API...")
    print(" תיעוד זמין בכתובת: http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="127.0.0.1", port=8000)