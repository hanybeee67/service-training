import re

# Read index.html to extract KR_AUDIO
with open('c:\\service-training\\index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

kr_audio_match = re.search(r'(var KR_AUDIO = \{.*?\n\s*\};)', index_content, re.DOTALL)
if not kr_audio_match:
    print('KR_AUDIO not found')
    exit(1)

kr_audio_code = kr_audio_match.group(1)

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

# Function to update mobile files
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
