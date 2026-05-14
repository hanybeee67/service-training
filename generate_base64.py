import base64
from gtts import gTTS

texts = {
    "kr1": "안녕하세요, 에베레스트입니다. 몇 분이십니까?",
    "kr2": "이 테이블로 모시겠습니다.",
    "kr3": "이 태블릿으로 주문 부탁드립니다."
}

base64_strings = {}

for key, text in texts.items():
    tts = gTTS(text=text, lang='ko', slow=False)
    filename = f"{key}.mp3"
    tts.save(filename)
    
    with open(filename, "rb") as f:
        encoded = base64.b64encode(f.read()).decode('utf-8')
        base64_strings[key] = f"data:audio/mp3;base64,{encoded}"

# Now update the files
kr_audio_code = "var KR_AUDIO = {\n"
for key, b64 in base64_strings.items():
    kr_audio_code += f'    {key}: "{b64}",\n'
kr_audio_code += "  };\n"

new_tts_code = """  var KR_TEXTS = {
    kr1: "안녕하세요, 에베레스트입니다. 몇 분이십니까?",
    kr2: "이 테이블로 모시겠습니다.",
    kr3: "이 태블릿으로 주문 부탁드립니다."
  };

""" + kr_audio_code + """

  var _audio = null;

  function _resetBtns() {
    document.querySelectorAll(".kr-speak-btn").forEach(function(b){
      b.classList.remove("playing");
    });
  }

  function speakKorean(key, btn) {
    if (_audio) { try{ _audio.pause(); _audio.currentTime=0; }catch(e){} _audio = null; }
    _resetBtns();
    btn.classList.add("playing");

    var src = KR_AUDIO[key];
    if (!src) { btn.classList.remove("playing"); return; }
    
    var a = new Audio(src);
    _audio = a;
    a.onended = function() { btn.classList.remove("playing"); _audio = null; };
    a.onerror = function() { btn.classList.remove("playing"); _audio = null; };
    a.play().catch(function() { btn.classList.remove("playing"); _audio = null; });
  }"""

def update_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    start_idx = content.find('var KR_TEXTS = {')
    end_idx = content.find('</script>', start_idx)
    
    if start_idx != -1 and end_idx != -1:
        new_content = content[:start_idx] + new_tts_code + '\n' + content[end_idx:]
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Updated {filename}')
    else:
        print(f'Could not find TTS block in {filename}')

update_file('c:\\service-training\\everest_mobile_eng_v2.html')
update_file('c:\\service-training\\everest_mobile_nep_v1.html')
update_file('c:\\service-training\\index.html')
