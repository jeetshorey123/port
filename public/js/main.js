const links = Array.from(document.querySelectorAll('.nav-link'));
const sections = Array.from(document.querySelectorAll('.section, .hero'));
const revealItems = Array.from(document.querySelectorAll('.reveal'));
const gameButtons = Array.from(document.querySelectorAll('.launch-game'));

const activateLink = () => {
  const offset = window.scrollY + 140;
  let current = sections[0];

  for (const section of sections) {
    if (section.offsetTop <= offset) current = section;
  }

  links.forEach((link) => {
    link.classList.toggle('active', link.dataset.target === current.id);
  });
};

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) entry.target.classList.add('is-visible');
    });
  },
  { threshold: 0.18 }
);

revealItems.forEach((item) => observer.observe(item));

links.forEach((link) => {
  link.addEventListener('click', async (event) => {
    if (link.getAttribute('href') && !link.dataset.target) {
      return;
    }
    const target = document.getElementById(link.dataset.target);
    if (!target) return;
    event.preventDefault();
    // play nav sound and speak section name clearly
    playSFX('nav');
    const name = (link.dataset.target || '').replace(/-/g,' ');
    await speakText(`Opening ${name}.`, {rate:0.95, pitch:0.9});
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
});

window.addEventListener('scroll', activateLink, { passive: true });
activateLink();

/* Speech + SFX utilities */
let selectedVoice = null;
function chooseVoice(){
  const voices = window.speechSynthesis.getVoices();
  if(!voices || voices.length === 0) return null;
  // prefer en-US, then any en, then first available
  let v = voices.find(x => /en-?us/i.test(x.lang));
  if(!v) v = voices.find(x => /^en/i.test(x.lang));
  if(!v) v = voices[0];
  return v;
}

function initVoices(){
  if(!window.speechSynthesis) return;
  const vs = window.speechSynthesis.getVoices();
  if(vs && vs.length > 0){ selectedVoice = chooseVoice(); return; }
  window.speechSynthesis.onvoiceschanged = () => { selectedVoice = chooseVoice(); };
}
initVoices();

function speakText(text, opts = {}){
  return new Promise((resolve)=>{
    if(!window.speechSynthesis) return resolve();
    // preference: allow disabling voice via localStorage 'pf_pref_voice_on' = '0'
    try{ if(localStorage.getItem('pf_pref_voice_on') === '0') return resolve(); }catch(e){}
    const utter = new SpeechSynthesisUtterance(text);
    if(!selectedVoice) selectedVoice = chooseVoice();
    if(selectedVoice) utter.voice = selectedVoice;
    utter.rate = opts.rate || 0.98;
    utter.pitch = opts.pitch || 1.0;
    utter.volume = (typeof opts.volume === 'number') ? opts.volume : 1.0;
    utter.onend = ()=> resolve();
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utter);
  });
}

// small SFX using WebAudio
const AudioCtx = window.AudioContext || window.webkitAudioContext;
let audioCtx = null;
let audioAllowed = false;

function enableAudio(){
  try{
    if(!audioCtx) audioCtx = new AudioCtx();
    if(audioCtx.state === 'suspended' && audioCtx.resume) audioCtx.resume();
    audioAllowed = true;
  }catch(e){ audioAllowed = true; }
}
function playSFX(type){
  try{
    // preference: allow disabling sfx via localStorage 'pf_pref_sfx_on' = '0'
    try{ if(localStorage.getItem('pf_pref_sfx_on') === '0') return; }catch(e){}
    if(!audioCtx) audioCtx = new AudioCtx();
    const now = audioCtx.currentTime;

    if(type === 'hit' || type === 'gun'){
      // short noise burst for hit/gun
      const len = 0.26;
      const buffer = audioCtx.createBuffer(1, Math.floor(audioCtx.sampleRate * len), audioCtx.sampleRate);
      const data = buffer.getChannelData(0);
      for(let i=0;i<data.length;i++){
        const env = Math.exp(-6 * i / data.length);
        data[i] = (Math.random() * 2 - 1) * env * 0.8;
      }
      const src = audioCtx.createBufferSource(); src.buffer = buffer;
      const g = audioCtx.createGain(); g.gain.setValueAtTime(1.0, now); g.gain.exponentialRampToValueAtTime(0.001, now + len);
      src.connect(g); g.connect(audioCtx.destination); src.start(now);
    } else if(type === 'open'){
      // two-tone sweep whoosh
      const o = audioCtx.createOscillator(), o2 = audioCtx.createOscillator();
      const g = audioCtx.createGain(); g.gain.setValueAtTime(0.0001, now);
      o.type = 'sawtooth'; o.frequency.setValueAtTime(320, now); o.frequency.exponentialRampToValueAtTime(960, now + 0.28);
      o2.type = 'sine'; o2.frequency.setValueAtTime(640, now); o2.frequency.exponentialRampToValueAtTime(880, now + 0.28);
      g.gain.exponentialRampToValueAtTime(0.18, now + 0.02); g.gain.exponentialRampToValueAtTime(0.001, now + 0.36);
      o.connect(g); o2.connect(g); g.connect(audioCtx.destination); o.start(now); o2.start(now); o.stop(now + 0.36); o2.stop(now + 0.36);
    } else if(type === 'click' || type === 'nav'){
      // sharp blip
      const o = audioCtx.createOscillator(); const g = audioCtx.createGain();
      o.type = 'square'; o.frequency.setValueAtTime(type === 'nav' ? 420 : 1200, now);
      g.gain.setValueAtTime(0.0001, now); g.gain.exponentialRampToValueAtTime(0.28, now + 0.008); g.gain.exponentialRampToValueAtTime(0.001, now + 0.12);
      o.connect(g); g.connect(audioCtx.destination); o.start(now); o.stop(now + 0.12);
    }
  }catch(e){/* ignore */}
}

// Simple game gating for Skills/Education
function revealSkills() {
  const skills = document.getElementById('skills');
  if (!skills) return;
  skills.classList.add('unlocked');
  const btn = document.querySelector('.launch-game[data-target="skills"]');
  if (btn) btn.remove();
}

function revealEducation() {
  const edu = document.getElementById('education');
  if (!edu) return;
  edu.classList.add('unlocked');
  const btn = document.querySelector('.launch-game[data-target="education"]');
  if (btn) btn.remove();
}

gameButtons.forEach((b) => {
  b.addEventListener('click', (e) => {
    openGame(b.dataset.target);
  });
});

// Intercept project links to narrate Overview, Problem, Methodology briefly
document.querySelectorAll('a.detail-link[data-title]').forEach((a)=>{
  a.addEventListener('click', (e)=>{
    // allow ctrl/cmd clicks through
    if(e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    // play a short open SFX and a concise prompt; do not block navigation
    const title = a.dataset.title || '';
    playSFX('open');
    speakText(`Opening ${title}.`, {rate:0.96, pitch:0.95});
    // allow default navigation to proceed immediately
  });
});

// Intercept timeline (experience) links similarly
document.querySelectorAll('a.timeline-item.detail-link[data-company]').forEach((a)=>{
  a.addEventListener('click', (e)=>{
    if(e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    const company = a.dataset.company || '';
    const role = a.dataset.role || '';
    playSFX('open');
    speakText(`Opening ${role} at ${company}.`, {rate:0.96, pitch:0.95});
  });
});

// allow other scripts to call unlock hooks
window.revealSkills = revealSkills;
window.revealEducation = revealEducation;

/* Game engine: moving indicator across a track, click to stop */
const $ = (id) => document.getElementById(id);
let animId = null;

function speak(text){
  if (!window.speechSynthesis) return;
  try{ window.speechSynthesis.cancel(); } catch(e){}
  const u = new SpeechSynthesisUtterance(text);
  u.rate = 1; u.pitch = 1; window.speechSynthesis.speak(u);
}
function openGame(target){
  const modal = $('game-modal');
  if(!modal) return;
  // Use shooting mini-game for Skills and Education
  if(target === 'skills' || target === 'education'){
    // use green-box timing game requiring 3 successful in-zone clicks
    openGreenBoxGame(target, 3);
    return;
  }
  modal.classList.remove('hidden');
  resultEl.textContent = '';
  // difficulty params
  const config = {
    skills: {zoneWidth: 0.16, speed: 0.014},
    education: {zoneWidth: 0.11, speed: 0.019},
  }[target] || {zoneWidth: 0.15, speed: 0.015};

  const track = document.getElementById('game-track');
  const trackRect = track.getBoundingClientRect();
  const trackWidth = trackRect.width;
  const zoneEl = $('game-zone');
  const indicator = $('game-indicator');
  const resultEl = $('game-result');
  const gameClick = $('game-click');
  const gameCloseBtn = document.querySelector('.game-close');
  const zoneWidthPx = Math.max(28, Math.floor(trackWidth * config.zoneWidth));
  const zoneLeftPx = Math.floor((trackWidth - zoneWidthPx) * (0.18 + Math.random() * 0.64));
  if(zoneEl){ zoneEl.style.width = zoneWidthPx + 'px'; zoneEl.style.left = zoneLeftPx + 'px'; }

  let pos = 0;
  let dir = 1;
  const speed = config.speed; // fraction per ms approx

  function frame(t){
    pos += dir * speed * 16; // rough millis
    if(pos < 0){pos = 0; dir = 1}
    if(pos > 1){pos = 1; dir = -1}
    const x = Math.round(pos * trackWidth);
    if(indicator) indicator.style.left = x + 'px';
    animId = requestAnimationFrame(frame);
  }
  animId = requestAnimationFrame(frame);

  const stop = () => {
    cancelAnimationFrame(animId);
    if(!indicator || !resultEl) return;
    const indRect = indicator.getBoundingClientRect();
    const indX = indRect.left + indRect.width/2 - trackRect.left;
    const inZone = (indX >= zoneLeftPx && indX <= zoneLeftPx + zoneWidthPx);
    if(inZone){
      resultEl.textContent = 'Success — unlocked!';
      speak('Nice! You unlocked it.');
      if(target === 'skills') revealSkills();
      if(target === 'education') revealEducation();
      setTimeout(()=> { const m = $('game-modal'); if(m) m.classList.add('hidden'); }, 900);
    } else {
      resultEl.textContent = 'Missed — try again';
      speak('Missed, try again');
    }
  };

  if(gameClick) gameClick.onclick = stop;
  if(gameCloseBtn) gameCloseBtn.onclick = () => { cancelAnimationFrame(animId); const m = $('game-modal'); if(m) m.classList.add('hidden'); };
  speak('Get ready. Click when the bar is inside the green zone.');
}
// Avatar speech on load
function showWelcomeBubble(){
  // create a central welcome bubble, speak, then animate to avatar
  const msg = 'Hello — welcome to the game!';
  const center = document.createElement('div');
  center.className = 'center-welcome big bubble-move';
  center.textContent = msg;
  document.body.appendChild(center);
  // attempt to enable audio immediately (may be blocked by browser until gesture)
  try{ enableAudio(); }catch(e){}
  playSFX('open');
  speakText(msg, {rate:0.95, pitch:0.95});
  // If autoplay is blocked, repeat the greeting on the first user gesture anywhere.
  document.addEventListener('pointerdown', function replayWelcomeOnce(){
    try{
      enableAudio();
      speakText(msg, {rate:0.95, pitch:0.95});
    } finally {
      document.removeEventListener('pointerdown', replayWelcomeOnce);
    }
  }, { once: true });
  setTimeout(()=>{
    const avatar = document.getElementById('game-avatar');
    if(!avatar){ center.remove(); return; }
    const rect = avatar.getBoundingClientRect();
    const left = rect.left + (rect.width/2);
    const top = rect.top + (rect.height/2);
    center.style.transform = 'translate(0,0)';
    center.style.left = left + 'px';
    center.style.top = top + 'px';
    center.style.opacity = '0.0';
    setTimeout(()=>{ center.remove(); const avatarBubble = document.getElementById('avatar-bubble'); if(avatarBubble) avatarBubble.textContent = msg; }, 900);
  }, 1200);
}

/* HUD + XP system */
const HUD = (() => {
  const key = 'pf_game_xp_v1';
  function get() { return parseInt(localStorage.getItem(key) || '0', 10); }
  function set(v){ localStorage.setItem(key, String(v)); update(); }
  function add(v){ set(get() + v); }
  function levelFromXP(xp){ return Math.floor(xp / 100) + 1; }
  function update(){
    let hud = document.getElementById('game-hud');
    if(!hud) return;
    const xp = get();
    hud.querySelector('.hud-xp').textContent = xp + ' XP';
    hud.querySelector('.hud-level').textContent = 'Lvl ' + levelFromXP(xp);
    hud.querySelector('.hud-bar-inner').style.width = Math.min(100, (xp % 100)) + '%';
  }
  return {get, set, add, update};
})();

// initialize HUD DOM if missing
if(!document.getElementById('game-hud')){
  const hud = document.createElement('div'); hud.id = 'game-hud'; hud.className = 'game-hud';
  hud.innerHTML = `
    <div class="hud-left">
      <div class="hud-level">Lvl 1</div>
      <div class="hud-xp">0 XP</div>
    </div>
    <div class="hud-right">
      <div class="hud-bar"><div class="hud-bar-inner"></div></div>
      <button class="btn hud-play" id="hud-arcade">Arcade</button>
    </div>`;
  document.body.appendChild(hud);
  document.getElementById('hud-arcade').addEventListener('click', ()=> openArcade());
}
HUD.update();

// Voice & SFX preference controls (adds toggle buttons to HUD)
const PREF_VOICE = 'pf_pref_voice_on';
const PREF_SFX = 'pf_pref_sfx_on';
function voiceEnabled(){ try{ return localStorage.getItem(PREF_VOICE) !== '0'; }catch(e){ return true; } }
function sfxEnabled(){ try{ return localStorage.getItem(PREF_SFX) !== '0'; }catch(e){ return true; } }
function setVoiceEnabled(v){ try{ localStorage.setItem(PREF_VOICE, v ? '1' : '0'); }catch(e){} updateHudControls(); }
function setSfxEnabled(v){ try{ localStorage.setItem(PREF_SFX, v ? '1' : '0'); }catch(e){} updateHudControls(); }

function updateHudControls(){
  const hud = document.getElementById('game-hud'); if(!hud) return;
  let controls = hud.querySelector('.hud-controls');
  if(!controls){
    controls = document.createElement('div'); controls.className = 'hud-controls';
    const right = hud.querySelector('.hud-right'); if(right) right.appendChild(controls);
  }
  controls.innerHTML = `
    <button class="btn hud-toggle" id="hud-voice">Voice: ${voiceEnabled() ? 'On' : 'Off'}</button>
    <button class="btn hud-toggle" id="hud-sfx">SFX: ${sfxEnabled() ? 'On' : 'Off'}</button>`;
  const vbtn = document.getElementById('hud-voice'); const sbtn = document.getElementById('hud-sfx');
  if(vbtn) vbtn.onclick = ()=> setVoiceEnabled(!voiceEnabled());
  if(sbtn) sbtn.onclick = ()=> setSfxEnabled(!sfxEnabled());
}
updateHudControls();

/* Arcade mode: click moving target N times */
function openArcade(){
  const modal = $('game-modal');
  if(!modal) return;
  modal.classList.remove('hidden');
  const resultEl = $('game-result'); if(resultEl) resultEl.textContent = '';
  const track = document.getElementById('game-track');
  if(track) track.classList.add('arcade');
  // convert to target mode: place a moving target
  const indicator = $('game-indicator');
  if(indicator){ indicator.style.width = '22px'; indicator.style.height = '22px'; indicator.style.borderRadius = '50%'; indicator.style.background = 'radial-gradient(circle at 40% 30%, #fff, #ff9ea3)'; }
  let clicks = 0; const goal = 3; let pos = 0; let dir=1; const speed = 0.02;
  const trackRect = track ? track.getBoundingClientRect() : {width:400,height:40,left:0};
  function frame(){
    pos += dir * speed;
    if(pos < 0){ pos = 0; dir = 1 }
    if(pos > 1){ pos = 1; dir = -1 }
    const x = Math.round(pos * trackRect.width);
    indicator.style.left = x + 'px';
    animId = requestAnimationFrame(frame);
  }
  animId = requestAnimationFrame(frame);
  const gameClick = $('game-click');
  const gameCloseBtn = document.querySelector('.game-close');
  if(gameClick){
    gameClick.onclick = () => {
      clicks += 1;
      if(resultEl) resultEl.textContent = `Hit ${clicks}/${goal}`;
      if(clicks >= goal){ cancelAnimationFrame(animId); if(resultEl) resultEl.textContent = 'Arcade cleared!'; HUD.add(75); HUD.update(); speak('Arcade cleared'); setTimeout(()=> { const m=$('game-modal'); if(m) m.classList.add('hidden'); },900); }
    };
  }
  if(gameCloseBtn) gameCloseBtn.onclick = () => { cancelAnimationFrame(animId); const m=$('game-modal'); if(m) m.classList.add('hidden'); };
}

/* Shooting mini-game: click moving targets until goal reached */
let shootState = {intervalId: null, targets: [], hits: 0};
function openShooting(target){
  const modal = $('game-modal');
  if(!modal) return;
  modal.classList.remove('hidden');
  const resultEl = $('game-result'); if(resultEl) resultEl.textContent = '';
  const area = document.getElementById('game-area');
  if(!area) return;
  area.innerHTML = '';
  area.setAttribute('aria-hidden','false');
  const track = document.getElementById('game-track');
  track.style.display = 'none';

  const needed = target === 'skills' ? 5 : 7;
  shootState.hits = 0;
  shootState.targets = [];

  const spawnTarget = (id) => {
    const t = document.createElement('div');
    t.className = 'shoot-target';
    t.dataset.id = id;
    t.style.left = Math.random() * (area.clientWidth - 44) + 'px';
    t.style.top = Math.random() * (area.clientHeight - 44) + 'px';
    t.textContent = '✦';
    area.appendChild(t);
    // click handler
    t.addEventListener('click', (e)=>{
      e.stopPropagation();
      if(t.dataset.hit) return;
      t.dataset.hit = '1';
      t.style.transform = 'scale(0.2)';
      t.style.opacity = '0';
      shootState.hits += 1;
      resultEl.textContent = `Hits: ${shootState.hits} / ${needed}`;
      HUD.add(8);
      HUD.update();
      // play hit SFX and spawn particles at target
      playSFX('hit');
      spawnParticlesAt(t);
      if(shootState.hits >= needed){
        speak('Target practice complete');
        if(target === 'skills') revealSkills();
        if(target === 'education') revealEducation();
        cleanupShooting();
        setTimeout(()=> modal.classList.add('hidden'),800);
      }
    });
    shootState.targets.push(t);
  };

  // spawn initial targets
  for(let i=0;i<4;i++) spawnTarget(i);

  // move targets periodically
  shootState.intervalId = setInterval(()=>{
    shootState.targets.forEach((t)=>{
      if(!t || t.dataset.hit) return;
      const nx = Math.max(0, Math.min(area.clientWidth - 44, parseFloat(t.style.left) + (Math.random()-0.5)*80));
      const ny = Math.max(0, Math.min(area.clientHeight - 44, parseFloat(t.style.top) + (Math.random()-0.5)*60));
      t.style.left = nx + 'px'; t.style.top = ny + 'px';
    });
    // sometimes add a new target
    if(Math.random() > 0.7 && shootState.targets.length < 8) spawnTarget(Date.now());
  }, 700);

  // clear on close
  const gameCloseBtn = document.querySelector('.game-close');
  if(gameCloseBtn) gameCloseBtn.onclick = () => { cleanupShooting(); const m = $('game-modal'); if(m) m.classList.add('hidden'); };
}

function cleanupShooting(){
  const area = document.getElementById('game-area');
  if(area){ area.innerHTML = ''; area.setAttribute('aria-hidden','true'); }
  const track = document.getElementById('game-track');
  if(track) track.style.display = '';
  if(shootState.intervalId) clearInterval(shootState.intervalId);
  shootState = {intervalId: null, targets: [], hits: 0};
}

/* Green-box timing game: user must click when indicator is inside the green zone N times */
function openGreenBoxGame(target, goal){
  const modal = $('game-modal'); if(!modal) return;
  modal.classList.remove('hidden');
  const resultEl = $('game-result'); if(resultEl) resultEl.textContent = '';
  const track = document.getElementById('game-track'); if(!track) return;
  const zoneEl = $('game-zone'); const indicator = $('game-indicator');
  track.style.display = '';
  // prepare zone
  const trackRect = track.getBoundingClientRect(); const trackWidth = trackRect.width;
  const zoneWidthPx = Math.max(28, Math.floor(trackWidth * 0.16));
  const zoneLeftPx = Math.floor((trackWidth - zoneWidthPx) * (0.18 + Math.random() * 0.64));
  if(zoneEl){ zoneEl.style.width = zoneWidthPx + 'px'; zoneEl.style.left = zoneLeftPx + 'px'; }
  if(indicator){ indicator.style.left = '0px'; indicator.style.width = '8px'; indicator.style.height='100%'; }
  let successes = 0; let pos = 0; let dir = 1; const speed = 0.018;
  const hitDisplay = document.getElementById('hit-display'); if(hitDisplay) hitDisplay.textContent = `${successes}/${goal}`;
  function frame(){
    pos += dir * speed;
    if(pos < 0){ pos = 0; dir = 1 }
    if(pos > 1){ pos = 1; dir = -1 }
    const x = Math.round(pos * trackWidth);
    if(indicator) indicator.style.left = x + 'px';
    animId = requestAnimationFrame(frame);
  }
  animId = requestAnimationFrame(frame);
  const stop = ()=>{
    cancelAnimationFrame(animId);
    if(!indicator || !resultEl) return;
    const indRect = indicator.getBoundingClientRect();
    const indX = indRect.left + indRect.width/2 - trackRect.left;
    const inZone = (indX >= zoneLeftPx && indX <= zoneLeftPx + zoneWidthPx);
    if(inZone){
      successes += 1;
      playSFX('hit');
      resultEl.textContent = `Success ${successes} / ${goal}`;
      if(hitDisplay) hitDisplay.textContent = `${successes}/${goal}`;
      HUD.add(8); HUD.update();
      if(successes >= goal){
        speakText('Well done. You unlocked the section.');
        if(target === 'skills') revealSkills();
        if(target === 'education') revealEducation();
        setTimeout(()=>{ const m=$('game-modal'); if(m) m.classList.add('hidden'); }, 900);
        return;
      }
    } else {
      playSFX('click');
      resultEl.textContent = 'Missed — try again';
    }
    // resume animation for next attempt
    animId = requestAnimationFrame(frame);
  };
  const gameClick = $('game-click'); const gameCloseBtn = document.querySelector('.game-close');
  if(gameClick) gameClick.onclick = stop;
  if(gameCloseBtn) gameCloseBtn.onclick = ()=>{ cancelAnimationFrame(animId); const m=$('game-modal'); if(m) m.classList.add('hidden'); };
}

/* Chart tooltips & interactions */
function attachChartTooltips(){
  document.querySelectorAll('.chart-card svg').forEach((svg)=>{
    svg.addEventListener('mousemove', (e)=>{
      const pt = svg.createSVGPoint(); pt.x = e.clientX; pt.y = e.clientY; const ctm = svg.getScreenCTM().inverse(); const loc = pt.matrixTransform(ctm);
      let info = '';
      // bar charts: rectangles
      const rect = e.target.closest('rect');
      if(rect && rect.parentNode === svg){
        const h = rect.getAttribute('height');
        // find nearby text label
        let label = '';
        Array.from(svg.querySelectorAll('text')).forEach(t=>{ try{ if(Math.abs(t.getBBox().x - rect.getBBox().x) < 80) label = t.textContent }catch(e){} });
        info = label ? `${label}: ${h}` : `Value: ${h}`;
      }
      // circles
      if(e.target.tagName === 'circle'){
        const x = e.target.getAttribute('cx'); const y = e.target.getAttribute('cy');
        let label = '';
        Array.from(svg.querySelectorAll('text')).forEach(t=>{ try{ if(Math.abs(parseFloat(t.getAttribute('x')) - parseFloat(x)) < 8) label = t.textContent }catch(e){} });
        info = label ? `${label}` : `Point`;
      }
      showTooltip(e.clientX + 12, e.clientY + 12, info);
    });
    svg.addEventListener('mouseleave', ()=> hideTooltip());
  });
}
const tt = document.createElement('div'); tt.id='svg-tooltip'; tt.className='svg-tooltip'; document.body.appendChild(tt);
function showTooltip(x,y,txt){ if(!txt) { tt.style.display='none'; return } tt.style.left = x + 'px'; tt.style.top = y + 'px'; tt.textContent = txt; tt.style.display='block'; }
function hideTooltip(){ tt.style.display='none'; }
attachChartTooltips();

// unlock hook increments XP
const origRevealSkills = revealSkills;
const origRevealEducation = revealEducation;
revealSkills = function(){ origRevealSkills(); HUD.add(35); HUD.update(); speak('Skills unlocked'); };
revealEducation = function(){ origRevealEducation(); HUD.add(45); HUD.update(); speak('Education unlocked'); };

// Start Game button on hero: navigate to Projects, then open Arcade
const startBtn = document.getElementById('start-game');
if(startBtn){
  startBtn.addEventListener('click', ()=> {
    const exp = document.getElementById('experience');
    if(exp){ exp.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
    // small delay so scrolling begins, then start green-box timing game
    setTimeout(()=> { openGreenBoxGame('skills', 3); }, 520);
  });
}

function spawnParticlesAt(element){
  const area = document.getElementById('game-area'); if(!area) return;
  const rect = element.getBoundingClientRect(); const parentRect = area.getBoundingClientRect();
  const cx = rect.left + rect.width/2 - parentRect.left; const cy = rect.top + rect.height/2 - parentRect.top;
  for(let i=0;i<10;i++){
    const p = document.createElement('div'); p.className = 'particle';
    p.style.left = cx + 'px'; p.style.top = cy + 'px';
    const angle = Math.random()*Math.PI*2; const dist = 24 + Math.random()*36;
    const dx = Math.cos(angle)*dist; const dy = Math.sin(angle)*dist;
    p.style.setProperty('--dx', dx + 'px'); p.style.setProperty('--dy', dy + 'px');
    area.appendChild(p);
    p.addEventListener('animationend', ()=> p.remove());
  }
}